"""Contrôle de ecrans-carte/ (L4) : les 13 invariants, les règles d'interface sourcées,
et les gabarits de tests légende = rendu, qui doivent eux-mêmes marcher.

Lancer : python3 -m unittest discover -s tests -v
"""

import importlib
import io
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
ECRANS = RACINE / "ecrans-carte"
GABARITS = ECRANS / "gabarits"

sys.path.insert(0, str(GABARITS))
lr = importlib.import_module("legende_rendu")

CHAMPS_INVARIANT = ("**Symptôme**", "**Cause**", "**Contrôle**")


def invariants():
    """{numéro: texte} des sections « ## n. … » de invariants.md."""
    texte = (ECRANS / "invariants.md").read_text(encoding="utf-8")
    morceaux = re.split(r"^## (\d+)\. ", texte, flags=re.M)
    return {int(morceaux[i]): morceaux[i + 1] for i in range(1, len(morceaux), 2)}


class TestDocuments(unittest.TestCase):
    def test_treize_invariants_dans_l_ordre(self):
        self.assertEqual(list(invariants()), list(range(1, 14)))

    def test_chaque_invariant_a_symptome_cause_controle(self):
        for n, texte in invariants().items():
            with self.subTest(invariant=n):
                for champ in CHAMPS_INVARIANT:
                    self.assertIn(champ, texte)

    def test_regles_d_interface_sourcees(self):
        texte = (ECRANS / "interface.md").read_text(encoding="utf-8")
        sections = re.split(r"^## ", texte, flags=re.M)[1:]
        regles = [s for s in sections if re.match(r"\d+\. ", s)]
        self.assertEqual(len(regles), 6, "six familles de règles numérotées")
        for s in regles:
            with self.subTest(section=s.splitlines()[0]):
                self.assertRegex(s, r"(?s)Sources? : .*https://", "règle sans source liée")

    def test_seuils_d_interface(self):
        """Les seuils qui servent aux contrôles : un changement doit être voulu."""
        texte = (ECRANS / "interface.md").read_text(encoding="utf-8")
        for motif in [r"< 600 px", r"≥ 840 px", r"\*\*24 px minimum\*\* \(WCAG 2\.5\.8",
                      r"4,5:1", r"3:1", r"640 px", r"`100dvh`", r"320, 390, 600, 840 et 1280",
                      r"844 × 390", r"interligne 1,5", r"lettres 0,12", r"mots 0,16"]:
            with self.subTest(motif=motif):
                self.assertRegex(texte, motif)

    def test_liens_internes(self):
        for doc in sorted(ECRANS.rglob("*.md")):
            texte = doc.read_text(encoding="utf-8")
            for lien in re.findall(r"\]\(([^)#\s:]+)\)", texte):
                with self.subTest(doc=str(doc.relative_to(RACINE)), lien=lien):
                    self.assertTrue((doc.parent / lien).resolve().exists(), "lien mort")

    def test_gabarits_presentes(self):
        presentation = (GABARITS / "README.md").read_text(encoding="utf-8")
        for f in sorted(GABARITS.iterdir()):
            if f.suffix in (".py", ".mjs") and f.name != "gabarits.test.mjs":
                with self.subTest(gabarit=f.name):
                    self.assertIn(f"]({f.name})", presentation)

    def test_index_et_readme_renvoient_ici(self):
        for doc in (RACINE / "README.md", RACINE / "fiches" / "README.md"):
            with self.subTest(doc=doc.name):
                self.assertTrue("ecrans-carte/" in doc.read_text(encoding="utf-8"),
                                "aucun renvoi vers ecrans-carte/")


STEP = ["step", ["get", "v"], "#000", 10, "#FF0000", 20, "rgb(0, 255, 0)"]
SLD = """<StyledLayerDescriptor xmlns="http://www.opengis.net/sld">
  <ColorMap type="intervals">
    <ColorMapEntry color="#000000" quantity="10" opacity="0"/>
    <ColorMapEntry quantity="20" color="#FF0000" label="20"/>
  </ColorMap></StyledLayerDescriptor>"""


class TestGabaritPython(unittest.TestCase):
    def test_normaliser_couleur(self):
        self.assertEqual(lr.normaliser_couleur("#ABC"), "#aabbcc")
        self.assertEqual(lr.normaliser_couleur("rgba(255,0,0,0.5)"), "#ff000080")
        self.assertEqual(lr.normaliser_couleur("0xFF0000"), "#ff0000")
        self.assertEqual(lr.normaliser_couleur("#ff0000ff"), "#ff0000")
        with self.assertRaises(ValueError):
            lr.normaliser_couleur("rouge")

    def test_entrees_maplibre(self):
        self.assertEqual(lr.entrees_depuis_maplibre(STEP),
                         [(None, "#000000"), (10, "#ff0000"), (20, "#00ff00")])
        self.assertEqual(lr.entrees_depuis_maplibre(
            ["interpolate", ["linear"], ["get", "v"], 0, "#fff", 5, "#000"]),
            [(0, "#ffffff"), (5, "#000000")])
        self.assertEqual(lr.entrees_depuis_maplibre(
            ["match", ["get", "k"], ["a", "b"], "#f00", "c", "#0f0", "#00f"]),
            [("a", "#ff0000"), ("b", "#ff0000"), ("c", "#00ff00"), ("*", "#0000ff")])
        with self.assertRaises(ValueError):
            lr.entrees_depuis_maplibre(["case", True, "#000", "#fff"])

    def test_entrees_sld(self):
        self.assertEqual(lr.entrees_depuis_sld(SLD), [(10.0, "#00000000"), (20.0, "#ff0000")])
        with self.assertRaises(ValueError):
            lr.entrees_depuis_sld("<ColorMap/>")

    def test_entrees_sld_commentees_ignorees(self):
        """Même résultat que le gabarit JS (gabarits.test.mjs) sur le même texte."""
        commente = ('<ColorMap><!-- <ColorMapEntry color="#fff" quantity="5"/> -->'
                    '<ColorMapEntry color="#000" quantity="10"/></ColorMap>')
        self.assertEqual(lr.entrees_depuis_sld(commente), [(10.0, "#000000")])

    def test_entree_sld_sans_quantity_refusee(self):
        with self.assertRaisesRegex(ValueError, "quantity"):
            lr.entrees_depuis_sld('<ColorMap><ColorMapEntry color="#000"/></ColorMap>')

    def test_ecarts_legende(self):
        attendu = lr.entrees_depuis_maplibre(STEP)
        self.assertEqual(lr.ecarts_legende(attendu, [(None, "#000"), (10, "#f00"), (20, "#0f0")]), [])
        ecarts = lr.ecarts_legende(attendu, [(None, "#000"), (15, "#f00"), (20, "#00f")])
        self.assertEqual(len(ecarts), 2)
        self.assertIn("seuil 15", ecarts[0])
        self.assertIn("2 entrées dans la légende, 3", lr.ecarts_legende(attendu, attendu[1:])[0])

    def test_conversion_d_unite(self):
        kelvin = [(None, "#000000"), (273.15, "#ff0000")]
        self.assertEqual(lr.ecarts_legende(lr.convertir_seuils(kelvin, lambda k: k - 273.15),
                                           [(None, "#000000"), (0, "#ff0000")]), [])

    def test_classe_et_arrondi(self):
        self.assertEqual(lr.classe(9.99, [10, 20]), 0)
        self.assertEqual(lr.classe(10, [10, 20]), 1)
        valeurs = lr.valeurs_autour_des_seuils([25], 1)
        afficher = lambda v: round(v, 1)  # noqa: E731
        fautes = lr.classes_changees_par_arrondi(valeurs, [25], afficher)
        self.assertTrue(any(v < 25 and aff == 25 for v, aff, _, _ in fautes),
                        "24,96 affiché « 25,0 » dans la couleur de « < 25 » doit être vu")
        self.assertEqual(lr.classes_changees_par_arrondi(
            valeurs, [25], afficher, lambda v: lr.classe(afficher(v), [25])), [])


class TestModelePython(unittest.TestCase):
    """Le modèle à copier saute à vide, passe rempli juste, échoue rempli faux."""

    def _lancer(self, legende, expression=("step", ["get", "t"], "#00f", 273.15, "#f00")):
        modele = importlib.reload(importlib.import_module("modele_test_legende"))
        modele.OPTIONS = list(legende)
        conversions = {"K": (lambda k: k, "K"), "°C": (lambda k: k - 273.15, "°C")}
        modele.expression_couleur_du_rendu = lambda o: list(expression)
        modele.legende_affichee = lambda o: legende[o]
        modele.conversion_vers_l_unite_affichee = lambda o: conversions[o]
        modele.unite_affichee_par_la_legende = lambda o: o
        modele.afficher = lambda v: round(v, 1)
        modele.classer = lambda v, s: lr.classe(round(v, 1), s)
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(modele.TestLegendeEgaleRendu)
        return unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)

    def test_vide_saute(self):
        modele = importlib.reload(importlib.import_module("modele_test_legende"))
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(modele.TestLegendeEgaleRendu)
        resultat = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
        self.assertEqual(len(resultat.skipped), resultat.testsRun)

    def test_rempli_juste_passe(self):
        juste = {"K": [(None, "#0000ff"), (273.15, "#ff0000")],
                 "°C": [(None, "#0000ff"), (0, "#ff0000")]}
        resultat = self._lancer(juste)
        self.assertTrue(resultat.wasSuccessful())
        self.assertEqual(resultat.skipped, [])

    def test_rempli_faux_echoue(self):
        faux = {"K": [(None, "#0000ff"), (273.15, "#ff0000")],
                "°C": [(None, "#0000ff"), (273.15, "#ff0000")]}  # seuil resté en K
        resultat = self._lancer(faux)
        self.assertEqual(resultat.errors, [], "le modèle doit échouer sur l'écart, pas planter")
        self.assertEqual(len(resultat.failures), 1)
        self.assertIn("seuil 273.15 dans la légende, 0.0 dans le rendu", resultat.failures[0][1])

    def test_arrondi_saute_sans_seuil_numerique(self):
        """Légende catégorielle (`match`) : le test d'arrondi est sauté, pas vert à vide."""
        match = ["match", ["get", "k"], "a", "#f00", "#00f"]
        resultat = self._lancer({"K": [("a", "#ff0000"), ("*", "#0000ff")]}, match)
        self.assertTrue(resultat.wasSuccessful())
        sautes = [str(t) for t, _ in resultat.skipped]
        self.assertEqual(len(sautes), 1, sautes)
        self.assertIn("arrondi", sautes[0])


@unittest.skipUnless(shutil.which("node"), "node absent : gabarits JS non testés")
class TestGabaritsJs(unittest.TestCase):
    def test_gabarits_js(self):
        r = subprocess.run(["node", "--test", "gabarits.test.mjs"], cwd=GABARITS,
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr[-2000:])

    def test_modele_js_saute_a_vide(self):
        r = subprocess.run(["node", "--test", "modele-legende.test.mjs"], cwd=GABARITS,
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr[-2000:])
        self.assertRegex(r.stdout, r"# skipped 3")


@unittest.skipUnless(shutil.which("node"), "node absent : modèle JS non testé")
class TestModeleJsRempli(unittest.TestCase):
    """Le modèle JS, rempli dans une copie temporaire : juste → vert, faux → rouge,
    légende catégorielle → arrondi sauté. Garde la condition `rempli` honnête."""

    REMPLI = {
        "const OPTIONS = [];": "const OPTIONS = ['K', '°C'];",
        "const expressionCouleurDuRendu = (option) => NON_REMPLI;":
            "const expressionCouleurDuRendu = (option) => EXPRESSION;",
        "const legendeAffichee = (option) => NON_REMPLI;":
            "const legendeAffichee = (option) => LEGENDES[option];",
        "const conversionVersUniteAffichee = (option) => NON_REMPLI;":
            "const conversionVersUniteAffichee = (option) => (option === 'K'"
            " ? { conversion: (k) => k, unite: 'K' }"
            " : { conversion: (k) => k - 273.15, unite: '°C' });",
        "const uniteAfficheeParLaLegende = (option) => NON_REMPLI;":
            "const uniteAfficheeParLaLegende = (option) => option;",
        "const classer = null;": "const classer = (v, s) => classe(afficher(v), s);",
    }

    def _lancer(self, legendes, expression):
        texte = (GABARITS / "modele-legende.test.mjs").read_text(encoding="utf-8")
        for avant, apres in self.REMPLI.items():
            self.assertIn(avant, texte, "le modèle JS a changé : mettre ce test à jour")
            texte = texte.replace(avant, apres)
        texte += f"\nconst EXPRESSION = {expression};\nconst LEGENDES = {legendes};\n"
        with tempfile.TemporaryDirectory() as d:
            shutil.copy(GABARITS / "legende-rendu.mjs", d)
            Path(d, "modele-legende.test.mjs").write_text(texte, encoding="utf-8")
            return subprocess.run(["node", "--test", "modele-legende.test.mjs"], cwd=d,
                                  capture_output=True, text=True)

    STEP_K = "['step', ['get', 't'], '#00f', 273.15, '#f00']"

    def test_rempli_juste_passe(self):
        r = self._lancer("{ K: [[null, '#0000ff'], [273.15, '#ff0000']],"
                         " '°C': [[null, '#0000ff'], [0, '#ff0000']] }", self.STEP_K)
        self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr[-2000:])
        self.assertRegex(r.stdout, r"# pass 6")
        self.assertRegex(r.stdout, r"# skipped 0")

    def test_rempli_faux_echoue(self):
        r = self._lancer("{ K: [[null, '#0000ff'], [273.15, '#ff0000']],"
                         " '°C': [[null, '#0000ff'], [273.15, '#ff0000']] }", self.STEP_K)
        self.assertNotEqual(r.returncode, 0)
        self.assertRegex(r.stdout, r"# fail 1")
        self.assertIn("seuil 273.15 dans la légende, 0 dans le rendu", r.stdout)

    def test_arrondi_saute_sans_seuil_numerique(self):
        r = self._lancer("{ K: [['a', '#ff0000'], ['*', '#0000ff']],"
                         " '°C': [['a', '#ff0000'], ['*', '#0000ff']] }",
                         "['match', ['get', 'k'], 'a', '#f00', '#00f']")
        self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr[-2000:])
        self.assertRegex(r.stdout, r"# skipped 2")


if __name__ == "__main__":
    unittest.main()
