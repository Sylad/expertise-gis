"""Contrôle du plugin Claude Code d'expertise-gis (L5).

- les manifestes (.claude-plugin/plugin.json, marketplace.json) sont cohérents ;
- le skill fiches-gis a son en-tête et cite son script ;
- chaque domaine de fiches du dépôt est connu du script, et inversement ;
- « chercher » retrouve la bonne fiche pour des symptômes connus ;
- « references » écrit un bloc YAML dont chaque adresse vise un fichier du dépôt.

Lancer : python3 -m unittest discover -s tests -v
"""

import importlib.util
import json
import re
import subprocess
import sys
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
    """Lecture minimale du bloc produit : [{cle: valeur}] (sans PyYAML)."""
    lignes = texte.splitlines()
    assert "references:" in lignes, texte
    entrees = []
    for ligne in lignes[lignes.index("references:") + 1:]:
        m = re.match(r"^  - (\w+): (.+)$", ligne)
        if m:
            entrees.append({m.group(1): m.group(2)})
            continue
        m = re.match(r"^    (\w+): (.+)$", ligne)
        assert m and entrees, f"ligne inattendue : {ligne!r}"
        entrees[-1][m.group(1)] = m.group(2)
    return entrees


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
        self.assertIn(f"/plugin marketplace add {F.DEPOT_PUBLIC.split('github.com/')[1].split('/blob')[0]}",
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
        connus = {d for d, _ in F.DOMAINES.values()}
        self.assertEqual(sorted(dossiers - connus), [],
                         "dossier de fiches sans entrée dans DOMAINES (fiches.py)")
        for nom, (dossier, quand) in F.DOMAINES.items():
            self.assertTrue((RACINE / dossier).is_dir(), nom)
            self.assertTrue(quand, nom)

    def test_compte_des_fiches(self):
        total = sum(F.compter(RACINE, d) for d, _ in F.DOMAINES.values()
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
    def test_tous_les_domaines_par_defaut(self):
        entrees = entrees_references(F.references(RACINE))
        self.assertEqual([e["nom"] for e in entrees],
                         [f"expertise-gis/{n}" for n in F.DOMAINES])

    def test_adresses_publiques_visent_le_depot(self):
        for e in entrees_references(F.references(RACINE)):
            for cle in ("url", "dossier"):
                self.assertTrue(e[cle].startswith(F.DEPOT_PUBLIC + "/"), e[cle])
                relatif = e[cle][len(F.DEPOT_PUBLIC) + 1:]
                self.assertTrue((RACINE / relatif).exists(), relatif)
            self.assertRegex(e["lire_quand"], r'^".+\((\d+ fiches|règles et gabarits)\)"$')

    def test_local_donne_des_chemins_existants(self):
        for e in entrees_references(F.references(RACINE, local=True)):
            self.assertNotIn("url", e)
            for cle in ("chemin", "dossier"):
                self.assertTrue(Path(e[cle]).is_absolute() and Path(e[cle]).exists(), e[cle])

    def test_selection_et_domaine_inconnu(self):
        entrees = entrees_references(F.references(RACINE, ["sld", "maplibre"]))
        self.assertEqual([e["nom"] for e in entrees],
                         ["expertise-gis/sld", "expertise-gis/maplibre"])
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
        donnees = yaml.safe_load(F.references(RACINE))
        self.assertEqual(len(donnees["references"]), len(F.DOMAINES))
        self.assertEqual(set(donnees["references"][0]), {"nom", "url", "dossier", "lire_quand"})

    def test_ligne_de_commande(self):
        sortie = subprocess.run([sys.executable, str(SCRIPT), "references",
                                 "--domaines", "postgis"], capture_output=True, text=True,
                                check=True).stdout
        self.assertEqual(sortie, F.references(RACINE, ["postgis"]))


if __name__ == "__main__":
    unittest.main()
