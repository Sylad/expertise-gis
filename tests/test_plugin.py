"""Contrôle du plugin Claude Code d'expertise-gis (L5).

- les manifestes (.claude-plugin/plugin.json, marketplace.json) sont cohérents ;
- le skill fiches-gis a son en-tête et cite son script ;
- chaque domaine de fiches du dépôt est connu du script, et inversement ;
- « chercher » retrouve la bonne fiche pour des symptômes connus ;
- « references » écrit le bloc sous la forme unique de cadence (L760) :
  references: { dir?, run: [{ mots, docs }] }, docs = fichiers locaux sans numéro de version ;
  lu par le vrai code de cadence run (aiguiller) et de cadence ref (referencesDir), sans
  message de migration ni refus.

Lancer : python3 -m unittest discover -s tests -v
"""

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
MANIFESTES = RACINE / ".claude-plugin"
SKILL = RACINE / "skills" / "fiches-gis"
SCRIPT = SKILL / "scripts" / "fiches.py"


def charger_script():
    spec = importlib.util.spec_from_file_location("fiches_gis", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


F = charger_script()


def bloc_references(texte):
    """Lecture minimale du bloc produit, sans PyYAML : {"dir"?: ..., "run": [{"mots", "docs"}]}.

    Forme unique de cadence (L760) : references: { dir, run: [{ mots, docs }] }. Chaque valeur
    est écrite en JSON (texte ou liste en flux), donc lisible par json.loads ; les commentaires
    (« # … ») sont ignorés, comme le ferait un lecteur YAML."""
    lignes = [l for l in texte.splitlines() if not l.lstrip().startswith("#")]
    assert "references:" in lignes, texte
    bloc, entrees = {}, None
    for ligne in lignes[lignes.index("references:") + 1:]:
        m = re.match(r"^  (\w+):(?: (.+))?$", ligne)
        if m:
            cle, valeur = m.groups()
            assert cle not in bloc, f"clé en double : {cle}"
            if cle == "run":
                assert valeur is None, ligne
                bloc["run"] = entrees = []
            else:
                bloc[cle] = json.loads(valeur)
            continue
        m = re.match(r"^    - (\w+): (.+)$", ligne)
        if m:
            assert entrees is not None, f"entrée hors de run: {ligne!r}"
            entrees.append({m.group(1): json.loads(m.group(2))})
            continue
        m = re.match(r"^      (\w+): (.+)$", ligne)
        assert m and entrees, f"ligne inattendue : {ligne!r}"
        entrees[-1][m.group(1)] = json.loads(m.group(2))
    return bloc


def entrees_references(texte):
    """Les entrées de references.run : [{"mots": [...], "docs": [...]}]."""
    return bloc_references(texte)["run"]


def schema_cadence(entrees):
    """Le schéma que lit `cadence run` (aiguiller) : une liste de { mots: [...], docs: [...] }."""
    return isinstance(entrees, list) and all(
        isinstance(e, dict) and isinstance(e.get("mots"), list) and isinstance(e.get("docs"), list)
        for e in entrees)


def depot_cadence():
    """La copie de cadence à essayer (lue, jamais modifiée) : CADENCE_RACINE, sinon la copie en
    service (~/.local/share/cadence/service, celle que lance la commande cadence), sinon un
    voisin nommé cadence. Le dist/ d'un dépôt voisin peut être plus ancien que ses sources."""
    service = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share") / "cadence/service"
    candidats = [os.environ.get("CADENCE_RACINE", ""), str(service)] + [
        str(d / "cadence") for d in (RACINE.parent, RACINE.parent.parent)]
    for c in candidats:
        if c and all((Path(c) / f).exists() for f in ("v2/dist/run/aiguillage.js", "dist/ref/store.js")):
            return Path(c)
    return None


class TestManifestes(unittest.TestCase):
    def setUp(self):
        self.plugin = json.loads((MANIFESTES / "plugin.json").read_text(encoding="utf-8"))
        self.marche = json.loads((MANIFESTES / "marketplace.json").read_text(encoding="utf-8"))

    def test_plugin(self):
        self.assertEqual(self.plugin["name"], "expertise-gis")
        self.assertRegex(self.plugin["version"], r"^\d+\.\d+\.\d+$")
        self.assertTrue(self.plugin["description"])

    def test_marketplace_sert_ce_depot(self):
        self.assertTrue(self.marche["name"])
        self.assertTrue(self.marche["owner"]["name"])
        (entree,) = self.marche["plugins"]
        self.assertEqual(entree["name"], self.plugin["name"])
        self.assertEqual(entree["source"], "./")
        self.assertEqual(entree["version"], self.plugin["version"],
                         "versions du plugin et de la marketplace différentes")

    def test_readme_dit_comment_installer(self):
        readme = (RACINE / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"/plugin marketplace add {F.DEPOT_GITHUB}",
                      readme)
        self.assertIn("/plugin install expertise-gis@expertise-gis", readme)


class TestSkill(unittest.TestCase):
    def test_en_tete(self):
        texte = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", texte, re.S)
        self.assertTrue(m, "en-tête YAML absent")
        champs = dict(re.findall(r"^(\w+): (.+)$", m.group(1), re.M))
        self.assertEqual(champs.get("name"), SKILL.name)
        self.assertGreater(len(champs.get("description", "")), 80)
        self.assertLessEqual(len(champs["description"]), 1024)

    def test_skill_cite_les_commandes_du_script(self):
        texte = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for commande in ("scripts/fiches.py\" chercher", "scripts/fiches.py\" references",
                         "scripts/fiches.py\" domaines"):
            self.assertIn(commande, texte)

    def test_chemins_cites_existent(self):
        texte = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for chemin in re.findall(r"`((?:fiches|ecrans-carte|docs)/[^`]+)`", texte):
            self.assertTrue((RACINE / chemin).exists(), chemin)


class TestDomaines(unittest.TestCase):
    def test_chaque_dossier_de_fiches_est_un_domaine(self):
        dossiers = {p.relative_to(RACINE).as_posix()
                    for p in (RACINE / "fiches").iterdir() if p.is_dir()}
        connus = {d for d, *_ in F.DOMAINES.values()}
        self.assertEqual(sorted(dossiers - connus), [],
                         "dossier de fiches sans entrée dans DOMAINES (fiches.py)")
        for nom, (dossier, quand, mots_cles) in F.DOMAINES.items():
            self.assertTrue(mots_cles, nom)
            self.assertTrue((RACINE / dossier).is_dir(), nom)
            self.assertTrue(quand, nom)

    def test_compte_des_fiches(self):
        total = sum(F.compter(RACINE, d) for d, *_ in F.DOMAINES.values()
                    if d.startswith("fiches/"))
        attendu = sum(1 for p in (RACINE / "fiches").rglob("*.md") if p.name != "README.md")
        self.assertEqual(total, attendu)


class TestChercher(unittest.TestCase):
    CAS = {
        ("image", "cannot", "be", "decoded"): "fiches/geoserver/erreur-wms-http-200-en-xml.md",
        ("GetCapabilities", "lentes", "cascade"):
            "fiches/geoserver/capabilities-lentes-amont-cascade-en-panne.md",
        ("Interpolation", "bicubique", "sans", "effet"):
            "fiches/geoserver/interpolations-au-pluriel.md",
        ("projection", "globe", "ignorée"):
            "fiches/maplibre/projection-globe-ignoree-au-constructeur.md",
    }

    def test_symptomes_connus(self):
        for mots, attendu in self.CAS.items():
            with self.subTest(mots=mots):
                trouvees = [f["relatif"] for f in F.chercher(RACINE, list(mots))]
                self.assertIn(attendu, trouvees[:3], trouvees)

    def test_accents_ignores(self):
        avec = [f["relatif"] for f in F.chercher(RACINE, ["hémisphère"])]
        sans = [f["relatif"] for f in F.chercher(RACINE, ["hemisphere"])]
        self.assertTrue(avec)
        self.assertEqual(avec, sans)

    def test_rien_trouve(self):
        self.assertEqual(F.chercher(RACINE, ["zzzqqqxxx"]), [])
        sortie = subprocess.run([sys.executable, str(SCRIPT), "chercher", "zzzqqqxxx"],
                                capture_output=True, text=True)
        self.assertEqual(sortie.returncode, 1)
        self.assertIn("fiches/README.md", sortie.stdout)

    def test_statut_lu_dans_la_fiche(self):
        for f in F.fiches(RACINE):
            statut = F.section(f["chemin"].read_text(encoding="utf-8"), "Statut")
            self.assertTrue(statut.startswith(f["statut"]), f["relatif"])


class TestReferences(unittest.TestCase):
    """Le bloc est celui que lit cadence (scripts/references.mjs, forme unique de L760) :
    references: { dir?, run: [{ mots, docs }] }, chaque doc un fichier présent sur la machine.
    Cadence écarte sans erreur un doc absent ou une URL : le test l'interdit."""

    def bloc(self, *args, **kw):
        kw.setdefault("racine_docs", RACINE)
        return F.references(RACINE, *args, **kw)

    def test_schema_de_cadence(self):
        entrees = entrees_references(self.bloc())
        self.assertTrue(schema_cadence(entrees), entrees)
        self.assertEqual(len(entrees), len(F.DOMAINES))
        for e in entrees:
            self.assertEqual(set(e), {"mots", "docs"}, e)
            self.assertTrue(e["mots"] and all(isinstance(m, str) and m for m in e["mots"]), e)
            self.assertTrue(e["docs"], e)

    def test_forme_unique_objet_dir_run(self):
        """Plus de liste directement sous references: (ancienne forme de cadence run, L760)."""
        texte = self.bloc()
        self.assertNotRegex(texte, r"(?m)^  - ", "liste directement sous references: (ancienne forme)")
        bloc = bloc_references(texte)
        self.assertEqual(set(bloc), {"run"}, "sans --dir, seule la clé run est écrite")
        self.assertTrue(set(bloc) <= {"dir", "run"})

    def test_dir_ecrit_si_demande(self):
        bloc = bloc_references(self.bloc(dir_ref="~/kb/references"))
        self.assertEqual(bloc["dir"], "~/kb/references")
        self.assertEqual(len(bloc["run"]), len(F.DOMAINES))
        for vide in ("", "   "):
            with self.assertRaises(ValueError):
                self.bloc(dir_ref=vide)
        sortie = subprocess.run([sys.executable, str(SCRIPT), "references", "--domaines", "sld",
                                 "--racine", str(RACINE), "--dir", "~/kb/references"],
                                capture_output=True, text=True, check=True).stdout
        self.assertEqual(bloc_references(sortie)["dir"], "~/kb/references")

    def test_docs_sont_des_fichiers_locaux_existants(self):
        for e in entrees_references(self.bloc()):
            for doc in e["docs"]:
                self.assertNotRegex(doc, r"^[a-z]+://", doc)
                chemin = Path(os.path.expanduser(doc))
                self.assertTrue(chemin.is_absolute() and chemin.is_file(), doc)

    def test_front_seulement_en_expression(self):
        """« front » / « fronts » seuls attrapent « front-end » (cadence coupe au tiret) : expressions seulement."""
        for nom, (_, _, mots) in F.DOMAINES.items():
            for m in mots:
                with self.subTest(domaine=nom, mot=m):
                    self.assertNotIn(F.normaliser(m), ("front", "fronts", "front-end", "frontend"))

    def test_mots_reperent_le_domaine(self):
        """Mots comparés comme cadence : sans accents ni casse, en mot entier."""
        par_nom = dict(zip(F.DOMAINES, entrees_references(self.bloc())))
        for nom, demande in [("geoserver", "Le GetCapabilities de GeoServer est lent"),
                             ("postgis", "migration PostGIS cassée"),
                             ("sld", "le SLD est ignoré"),
                             ("openlayers", "décalage OpenLayers en 4326"),
                             ("maplibre", "globe MapLibre vide"),
                             ("symbologie", "barbules à l'envers sur la SIGWX"),
                             ("ecrans-carte", "la légende ne suit pas la carte")]:
            texte = F.normaliser(demande)
            self.assertTrue(any(re.search(rf"(^|[^\w]){re.escape(F.normaliser(m))}($|[^\w])", texte)
                                for m in par_nom[nom]["mots"]), (nom, demande))

    def test_defaut_clone_de_la_place_de_marche_sans_version(self):
        """Par défaut (copie installée), les docs visent le clone de la place de marché :
        ~/.claude/plugins/marketplaces/expertise-gis/…, sans numéro de version."""
        with tempfile.TemporaryDirectory() as tmp:
            accueil = Path(tmp)
            cache = accueil / ".claude/plugins/cache/expertise-gis/expertise-gis/0.1.0"
            place = accueil / ".claude/plugins/marketplaces/expertise-gis"
            for copie in (cache, place):
                shutil.copytree(RACINE, copie, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            env = {k: v for k, v in os.environ.items() if k != "EXPERTISE_GIS_RACINE"}
            env["HOME"] = str(accueil)
            for option in ([], ["--local"]):
                sortie = subprocess.run(
                    [sys.executable, "-I", str(cache / "skills/fiches-gis/scripts/fiches.py"),
                     "references", *option], capture_output=True, text=True, env=env, check=True)
                self.assertEqual(sortie.stderr, "", option)
                self.assertNotIn("0.1.0", sortie.stdout)
                self.assertNotIn("/cache/", sortie.stdout)
                for e in entrees_references(sortie.stdout):
                    for doc in e["docs"]:
                        self.assertTrue(doc.startswith("~/.claude/plugins/marketplaces/expertise-gis/"), doc)
                        self.assertTrue((accueil / doc[2:]).is_file(), doc)

    def test_racine_stable(self):
        accueil = Path("/h")
        self.assertEqual(
            F.racine_stable(Path("/h/.claude/plugins/cache/expertise-gis/expertise-gis/0.1.0")),
            Path("/h/.claude/plugins/marketplaces/expertise-gis"))
        # Une configuration ailleurs (CLAUDE_CONFIG_DIR) garde la même disposition.
        self.assertEqual(F.racine_stable(Path("/c/plugins/cache/m/p/1.2.3")),
                         Path("/c/plugins/marketplaces/m"))
        # Un clone ordinaire reste tel quel.
        self.assertEqual(F.racine_stable(Path("/src/expertise-gis")), Path("/src/expertise-gis"))
        self.assertEqual(F.raccourcir(Path("/h/a/b"), accueil), "~/a/b")
        self.assertEqual(F.raccourcir(Path("/x/a"), accueil), "/x/a")

    def test_doc_absent_signale(self):
        with tempfile.TemporaryDirectory() as tmp:
            sortie = subprocess.run([sys.executable, str(SCRIPT), "references", "--racine", tmp],
                                    capture_output=True, text=True)
        self.assertEqual(sortie.returncode, 3)
        self.assertIn("absent", sortie.stderr)
        self.assertTrue(schema_cadence(entrees_references(sortie.stdout)))

    def test_selection_et_domaine_inconnu(self):
        entrees = entrees_references(self.bloc(["sld", "maplibre"]))
        self.assertEqual([e["mots"] for e in entrees],
                         [F.DOMAINES["sld"][2], F.DOMAINES["maplibre"][2]])
        with self.assertRaises(ValueError):
            F.references(RACINE, ["inconnu"])
        sortie = subprocess.run([sys.executable, str(SCRIPT), "references",
                                 "--domaines", "inconnu"], capture_output=True, text=True)
        self.assertEqual(sortie.returncode, 2)
        self.assertIn("inconnu", sortie.stderr)

    def test_yaml_valide_si_pyyaml(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML absent : la lecture minimale ci-dessus suffit")
        for kw in ({}, {"dir_ref": "~/kb/references"}):
            donnees = yaml.safe_load(self.bloc(**kw))
            self.assertTrue(schema_cadence(donnees["references"]["run"]))
            self.assertEqual(donnees["references"], bloc_references(self.bloc(**kw)))

    def test_ligne_de_commande(self):
        sortie = subprocess.run([sys.executable, str(SCRIPT), "references", "--domaines",
                                 "postgis", "--racine", str(RACINE)],
                                capture_output=True, text=True, check=True).stdout
        self.assertEqual(sortie, self.bloc(["postgis"]))


@unittest.skipUnless(shutil.which("node"), "Node absent")
class TestLuParCadence(unittest.TestCase):
    """Le bloc lu par le vrai code de cadence : cadence run (v2/dist/run/aiguillage.js,
    referencesDuDepot et aiguiller) et cadence ref (dist/ref/store.js, referencesDir), qui
    passent tous deux par scripts/references.mjs. Aucun message de migration, aucun refus."""

    def setUp(self):
        self.cadence = depot_cadence()
        if not self.cadence:
            self.skipTest("dépôt cadence introuvable (CADENCE_RACINE)")

    def aiguiller(self, bloc, demande):
        with tempfile.TemporaryDirectory() as projet:
            (Path(projet) / "cadence.yaml").write_text(bloc, encoding="utf-8")
            module = (self.cadence / "v2/dist/run/aiguillage.js").as_uri()
            code = (f"import({json.dumps(module)}).then(m => process.stdout.write(JSON.stringify("
                    f"m.aiguiller({json.dumps(demande)}, {json.dumps(projet)}, []))))")
            sortie = subprocess.run(["node", "-e", code], capture_output=True, text=True, cwd=projet)
        self.assertEqual(sortie.returncode, 0, sortie.stderr)
        return json.loads(sortie.stdout)

    def node(self, bloc, code):
        """Écrit bloc dans un cadence.yaml jetable et lance code (ESM) ; renvoie le JSON écrit."""
        with tempfile.TemporaryDirectory() as tmp:
            projet = Path(tmp) / "projet"
            projet.mkdir()
            (projet / "cadence.yaml").write_text(bloc, encoding="utf-8")
            env = dict(os.environ, HOME=tmp, XDG_DATA_HOME=str(Path(tmp) / "xdg"))
            sortie = subprocess.run(["node", "--input-type=module", "-e", code, str(projet), tmp],
                                    capture_output=True, text=True, cwd=projet, env=env)
        self.assertEqual(sortie.returncode, 0, sortie.stderr)
        return json.loads(sortie.stdout), tmp

    def lu_par_run(self, bloc):
        module = (self.cadence / "v2/dist/run/aiguillage.js").as_uri()
        code = (f"const m = await import({json.dumps(module)});"
                "process.stdout.write(JSON.stringify(m.referencesDuDepot(process.argv[1])));")
        return self.node(bloc, code)[0]

    def lu_par_ref(self, bloc):
        module = (self.cadence / "dist/ref/store.js").as_uri()
        code = (f"const m = await import({json.dumps(module)});"
                "const avis = [];"
                "const projet = process.argv[1];"
                "const dir = m.referencesDir(projet, projet + '/cadence.yaml', process.env, a => avis.push(a));"
                "process.stdout.write(JSON.stringify({ dir, avis }));")
        return self.node(bloc, code)

    def test_cadence_run_lit_le_bloc_sans_migration(self):
        for kw in ({}, {"dir_ref": "~/kb/references"}):
            with self.subTest(**kw):
                lu = self.lu_par_run(F.references(RACINE, racine_docs=RACINE, **kw))
                self.assertNotIn("migration", lu, lu)
                self.assertEqual(len(lu["run"]), len(F.DOMAINES))
                self.assertEqual([e["mots"] for e in lu["run"]], [m for *_, m in F.DOMAINES.values()])

    def test_cadence_ref_lit_le_bloc_sans_migration(self):
        lu, accueil = self.lu_par_ref(F.references(RACINE, racine_docs=RACINE))
        self.assertEqual(lu["avis"], [])
        self.assertEqual(lu["dir"], str(Path(accueil) / "xdg/cadence/references"))
        lu, accueil = self.lu_par_ref(F.references(RACINE, racine_docs=RACINE, dir_ref="~/kb/references"))
        self.assertEqual(lu["avis"], [])
        self.assertEqual(lu["dir"], str(Path(accueil) / "kb/references"))

    def test_ancienne_forme_temoin_de_migration(self):
        """Témoin : la liste directe sous references: (forme de la 0.1.x) déclenche le message de migration."""
        ancien = "references:\n  - mots: [\"sld\"]\n    docs: [\"x.md\"]\n"
        self.assertIn("migration", self.lu_par_run(ancien))
        self.assertTrue(self.lu_par_ref(ancien)[0]["avis"])

    def test_bloc_lu_et_docs_retenus(self):
        bloc = F.references(RACINE, racine_docs=RACINE)
        r = self.aiguiller(bloc, "Le GetCapabilities de GeoServer est lent et la légende est fausse")
        self.assertEqual(r["mode"], "complet", r)
        self.assertNotIn("aucun document présent", r["raison"])
        self.assertIn(F.raccourcir(RACINE / "fiches/README.md"), r["pieces"])
        self.assertIn(F.raccourcir(RACINE / "ecrans-carte/invariants.md"), r["pieces"])
        self.assertEqual(len(r["pieces"]), len(set(r["pieces"])))

    def test_demande_sans_mot_reste_legere(self):
        r = self.aiguiller(F.references(RACINE, racine_docs=RACINE), "corriger une faute dans le README")
        self.assertEqual(r["mode"], "leger", r)

    def test_demande_frontend_ne_declenche_pas_la_symbologie(self):
        """Revue L5 passe 2 : « front » seul faisait passer toute demande de frontend en mode complet."""
        bloc = F.references(RACINE, racine_docs=RACINE)
        for demande in ("corrige le frontend du login", "corrige le front-end du login",
                        "le front end plante au démarrage", "refais le front de la page profil",
                        "les fronts des deux applis divergent"):
            with self.subTest(demande=demande):
                r = self.aiguiller(bloc, demande)
                self.assertEqual(r["mode"], "leger", r)

    def test_expressions_de_fronts_declenchent_la_symbologie(self):
        bloc = F.references(RACINE, racine_docs=RACINE)
        for demande in ("le front froid est dessiné à l'envers", "les fronts chauds n'ont pas de demi-cercles",
                        "front occlus mal orienté", "cold front symbols are reversed"):
            with self.subTest(demande=demande):
                r = self.aiguiller(bloc, demande)
                self.assertEqual(r["mode"], "complet", r)
                self.assertIn(F.raccourcir(RACINE / "fiches/README.md"), r["pieces"])

    def test_ancien_format_refuse_par_cadence(self):
        """Témoin : le format de la 0.1.0 (nom/url/dossier/lire_quand) faisait planter cadence."""
        with tempfile.TemporaryDirectory() as projet:
            (Path(projet) / "cadence.yaml").write_text(
                "references:\n  - nom: x\n    url: https://exemple/x.md\n", encoding="utf-8")
            module = (self.cadence / "v2/dist/run/aiguillage.js").as_uri()
            code = f"import({json.dumps(module)}).then(m => m.aiguiller('x', {json.dumps(projet)}, []))"
            sortie = subprocess.run(["node", "-e", code], capture_output=True, text=True)
        self.assertNotEqual(sortie.returncode, 0)
        self.assertIn("mots", sortie.stderr)


if __name__ == "__main__":
    unittest.main()
