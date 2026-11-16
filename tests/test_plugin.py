"""Contrôle du plugin Claude Code d'expertise-gis (L5).

- les manifestes (.claude-plugin/plugin.json, marketplace.json) sont cohérents ;
- le skill fiches-gis a son en-tête et cite son script ;
- chaque domaine de fiches du dépôt est connu du script, et inversement ;
- « chercher » retrouve la bonne fiche pour des symptômes connus ;
- « references » écrit le bloc que lit cadence (liste de { mots, docs }, docs = fichiers
  locaux sans numéro de version), validé par la vraie fonction aiguiller de cadence.

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


def entrees_references(texte):
    """Lecture minimale du bloc produit, sans PyYAML : [{"mots": [...], "docs": [...]}].

    Chaque valeur est une liste en flux écrite en JSON, donc lisible par json.loads ;
    les commentaires (« # … ») sont ignorés, comme le ferait un lecteur YAML."""
    lignes = [l for l in texte.splitlines() if not l.lstrip().startswith("#")]
    assert "references:" in lignes, texte
    entrees = []
    for ligne in lignes[lignes.index("references:") + 1:]:
        m = re.match(r"^  - (\w+): (.+)$", ligne)
        if m:
            entrees.append({m.group(1): json.loads(m.group(2))})
            continue
        m = re.match(r"^    (\w+): (.+)$", ligne)
        assert m and entrees, f"ligne inattendue : {ligne!r}"
        entrees[-1][m.group(1)] = json.loads(m.group(2))
    return entrees


def schema_cadence(entrees):
    """Le schéma que lit `cadence run` (aiguiller) : une liste de { mots: [...], docs: [...] }."""
    return isinstance(entrees, list) and all(
        isinstance(e, dict) and isinstance(e.get("mots"), list) and isinstance(e.get("docs"), list)
        for e in entrees)


def depot_cadence():
    """Le dépôt de cadence (lu, jamais modifié) : CADENCE_RACINE, sinon un voisin nommé cadence."""
    candidats = [os.environ.get("CADENCE_RACINE", "")] + [
        str(d / "cadence") for d in (RACINE.parent, RACINE.parent.parent)]
    for c in candidats:
        if c and (Path(c) / "v2" / "dist" / "run" / "aiguillage.js").exists():
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
    """Le bloc est celui que lit cadence (v2/src/run/aiguillage.ts, aiguiller) :
    une liste de { mots, docs }, chaque doc un fichier présent sur la machine.
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
        donnees = yaml.safe_load(self.bloc())
        self.assertTrue(schema_cadence(donnees["references"]))
        self.assertEqual(donnees["references"], entrees_references(self.bloc()))

    def test_ligne_de_commande(self):
        sortie = subprocess.run([sys.executable, str(SCRIPT), "references", "--domaines",
                                 "postgis", "--racine", str(RACINE)],
                                capture_output=True, text=True, check=True).stdout
        self.assertEqual(sortie, self.bloc(["postgis"]))


@unittest.skipUnless(shutil.which("node"), "Node absent")
class TestLuParCadence(unittest.TestCase):
    """Le bloc passé à la vraie fonction aiguiller de cadence (v2/dist/run/aiguillage.js)."""

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
