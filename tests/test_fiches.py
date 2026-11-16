"""Contrôle des fiches d'expertise-gis.

Vérifie, pour chaque fiche de fiches/<domaine>/<slug>.md :
- le format de docs/format-fiche.md (titre, sept sections dans l'ordre, aucune vide) ;
- un statut valide (« prouvé » ou « à reprouver ») ;
- une source exploitable (lien, ou « vécu » daté AAAA-MM-JJ) ;
- l'absence de tout terme privé dans les fichiers suivis par git ;
- sa présence dans l'index fiches/README.md, dont aucun lien n'est mort.

Lancer : python3 -m unittest discover -s tests -v

Termes interdits : aucun n'est écrit dans un fichier suivi par git. La liste
vient du fichier .termes-prives à la racine (une expression par ligne, « # »
pour un commentaire, ignoré par git) et/ou de la variable d'environnement
EXPERTISE_GIS_TERMES_PRIVES (séparés par des virgules). Sans liste, le test
échoue et dit quoi faire : jamais de contrôle vide. Il parcourt tous les
fichiers suivis par git (git ls-files).
"""

import os
import re
import subprocess
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
FICHES = RACINE / "fiches"
DOCS = RACINE / "docs"
INDEX = FICHES / "README.md"

SECTIONS = [
    "Symptôme",
    "Cause",
    "Détection",
    "Geste",
    "Versions concernées",
    "Source",
    "Statut",
]
STATUTS = ("prouvé", "à reprouver")

SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
DATE = re.compile(r"\b20\d\d-\d\d-\d\d\b")


def termes_prives(racine=RACINE, env=None):
    """Liste des termes privés : fichier .termes-prives puis variable d'env."""
    env = os.environ if env is None else env
    termes = [t.strip() for t in env.get("EXPERTISE_GIS_TERMES_PRIVES", "").split(",")
              if t.strip()]
    fichier = Path(racine) / ".termes-prives"
    if fichier.exists():
        for ligne in fichier.read_text(encoding="utf-8").splitlines():
            ligne = ligne.strip()
            if ligne and not ligne.startswith("#"):
                termes.append(ligne)
    return termes


MESSAGE_SANS_LISTE = (
    "aucune liste de termes privés : créer le fichier .termes-prives à la "
    "racine (une expression par ligne, ignoré par git) ou définir "
    "EXPERTISE_GIS_TERMES_PRIVES=\"terme1,terme2\" avant de lancer les tests"
)


def fichiers_suivis():
    """Tous les fichiers suivis par git (sauf ceux supprimés du disque)."""
    sortie = subprocess.run(["git", "ls-files", "-z"], cwd=RACINE, check=True,
                            capture_output=True).stdout.decode("utf-8")
    return [c for c in sortie.split("\0") if c and (RACINE / c).is_file()]


def fiches():
    return sorted(p for p in FICHES.rglob("*.md") if p != INDEX)


def sections(texte):
    """Découpe une fiche en {titre de section: contenu}, dans l'ordre."""
    resultat = {}
    ordre = []
    courant = None
    for ligne in texte.splitlines():
        m = re.match(r"^## (.+?)\s*$", ligne)
        if m:
            courant = m.group(1)
            ordre.append(courant)
            resultat[courant] = []
        elif courant is not None:
            resultat[courant].append(ligne)
    return ordre, {k: "\n".join(v).strip() for k, v in resultat.items()}


# Bibliothèques côté client : motif d'une version citée, et majeure minimale pour
# « prouvé ». Une version ne compte que suivie de « (vécu » ou de « (code relu et
# mesure » : « non vérifié », « documenté » ou « relu » seuls ne prouvent rien.
SUFFIXE_VECU = r"(?:\.\d+)*\s*\((?:vécu|code relu et mesure)"
MOTIFS_CLIENT = {
    "openlayers": (re.compile(r"OpenLayers\s+v?(\d+)" + SUFFIXE_VECU), 10),
    "maplibre": (re.compile(r"MapLibre(?:\s+GL\s+JS)?\s+v?(\d+)" + SUFFIXE_VECU), 5),
}


def versions_vecues(texte, motif):
    """Majeures des versions citées avec « (vécu » ou « (code relu et mesure »."""
    return [int(m) for m in motif.findall(texte)]


class TestFiches(unittest.TestCase):
    def test_il_y_a_des_fiches(self):
        self.assertTrue(fiches(), "aucune fiche dans fiches/")

    def test_emplacement_et_nom(self):
        for f in fiches():
            with self.subTest(fiche=str(f.relative_to(RACINE))):
                self.assertEqual(f.parent.parent, FICHES,
                                 "une fiche vit dans fiches/<domaine>/")
                self.assertRegex(f.name, SLUG, "slug en kebab-case minuscule")

    def test_format(self):
        for f in fiches():
            with self.subTest(fiche=str(f.relative_to(RACINE))):
                texte = f.read_text(encoding="utf-8")
                premiere = texte.lstrip().splitlines()[0]
                self.assertTrue(premiere.startswith("# ") and len(premiere) > 4,
                                "la fiche commence par « # Titre »")
                ordre, contenu = sections(texte)
                self.assertEqual(ordre, SECTIONS,
                                 "sections attendues, dans cet ordre : "
                                 + ", ".join(SECTIONS))
                for s in SECTIONS:
                    self.assertTrue(contenu.get(s), f"section « {s} » vide")

    def test_statut(self):
        for f in fiches():
            with self.subTest(fiche=str(f.relative_to(RACINE))):
                _, contenu = sections(f.read_text(encoding="utf-8"))
                statut = contenu.get("Statut", "").splitlines()[0:1]
                self.assertTrue(statut and statut[0].startswith(STATUTS),
                                "statut : « prouvé » ou « à reprouver »")

    def test_source_exploitable(self):
        for f in fiches():
            with self.subTest(fiche=str(f.relative_to(RACINE))):
                _, contenu = sections(f.read_text(encoding="utf-8"))
                source = contenu.get("Source", "")
                lien = "http://" in source or "https://" in source
                vecu = "vécu" in source.lower() and DATE.search(source)
                self.assertTrue(lien or vecu,
                                "source : un lien (doc, ticket, code) "
                                "ou « vécu » daté AAAA-MM-JJ")

    def test_prouve_a_un_lien_ou_la_version_courante(self):
        """Garde-fou partiel : « prouvé » sans lien ni version 3.x = établi
        seulement sur une version ancienne, donc « à reprouver »."""
        for f in fiches():
            with self.subTest(fiche=str(f.relative_to(RACINE))):
                _, contenu = sections(f.read_text(encoding="utf-8"))
                if not contenu.get("Statut", "").startswith("prouvé"):
                    continue
                source = contenu.get("Source", "")
                lien = "http://" in source or "https://" in source
                courante = re.search(r"\b3\.\d", contenu.get("Versions concernées", ""))
                self.assertTrue(lien or courante,
                                "« prouvé » exige un lien en Source ou une version 3.x "
                                "en Versions concernées ; sinon « à reprouver »")

    def test_domaines_client(self):
        """L2 : les bibliothèques de carte côté client ont leurs fiches."""
        for domaine in ("openlayers", "maplibre"):
            with self.subTest(domaine=domaine):
                self.assertTrue(list((FICHES / domaine).glob("*.md")),
                                f"aucune fiche dans fiches/{domaine}/")

    def test_prouve_client_sur_version_courante(self):
        """Un fait établi seulement sur OpenLayers < 10 ou MapLibre < 5 est « à
        reprouver » : une fiche client « prouvé » cite au moins une version
        courante vécue (ou mesurée), pas seulement « non vérifié » ou « documenté »."""
        for domaine, (motif, minimum) in MOTIFS_CLIENT.items():
            for f in sorted((FICHES / domaine).glob("*.md")):
                with self.subTest(fiche=str(f.relative_to(RACINE))):
                    _, contenu = sections(f.read_text(encoding="utf-8"))
                    if not contenu.get("Statut", "").startswith("prouvé"):
                        continue
                    vecues = versions_vecues(contenu.get("Versions concernées", ""), motif)
                    self.assertTrue(any(v >= minimum for v in vecues),
                                    f"« prouvé » exige une version ≥ {minimum} vécue "
                                    "(« (vécu » ou « (code relu et mesure ») en Versions "
                                    "concernées ; sinon « à reprouver »")

    def test_versions_vecues_seules(self):
        """Une version citée « non vérifié », « relu » ou « documenté » ne compte
        pas : seules comptent celles suivies de « (vécu » ou « (code relu et mesure »."""
        ol, ml = MOTIFS_CLIENT["openlayers"][0], MOTIFS_CLIENT["maplibre"][0]
        self.assertEqual(versions_vecues(
            "MapLibre GL JS 4 (vécu) ; MapLibre GL JS 6 non vérifié", ml), [4])
        self.assertEqual(versions_vecues(
            "MapLibre GL JS 5.24 (vécu, globe) ; MapLibre 6 documenté", ml), [5])
        self.assertEqual(versions_vecues(
            "OpenLayers 9 (vécu) ; OpenLayers 10.11 relu", ol), [9])
        self.assertEqual(versions_vecues(
            "OpenLayers 10.11.0 (code relu et mesure scriptée le 2026-11-16)", ol), [10])

    def test_statut_de_l_index_egal_a_la_fiche(self):
        index = INDEX.read_text(encoding="utf-8")
        for icone, lien in re.findall(r"^- (✅|🔁) .*\]\(([^)#\s]+\.md)\)", index, re.M):
            with self.subTest(lien=lien):
                _, contenu = sections((FICHES / lien).read_text(encoding="utf-8"))
                attendu = "✅" if contenu.get("Statut", "").startswith("prouvé") else "🔁"
                self.assertEqual(icone, attendu, "icône de l'index ≠ statut de la fiche")

    def test_aucun_terme_interdit(self):
        termes = termes_prives()
        self.assertTrue(termes, MESSAGE_SANS_LISTE)
        for chemin in fichiers_suivis():
            texte = (RACINE / chemin).read_bytes().decode("utf-8", "replace").lower()
            for terme in termes:
                with self.subTest(fichier=chemin, terme=terme):
                    self.assertFalse(terme.lower() in texte,
                                     f"terme privé présent dans {chemin}")

    def test_liste_des_termes_prives(self):
        import tempfile
        with tempfile.TemporaryDirectory() as vide:
            self.assertEqual(termes_prives(vide, {}), [],
                             "sans fichier ni variable : liste vide, donc échec")
            Path(vide, ".termes-prives").write_text(
                "# commentaire\n\n  Terme Un \nterme-deux\n", encoding="utf-8")
            self.assertEqual(
                termes_prives(vide, {"EXPERTISE_GIS_TERMES_PRIVES": "a, b,"}),
                ["a", "b", "Terme Un", "terme-deux"])

    def test_termes_prives_ignores_par_git(self):
        sortie = subprocess.run(["git", "check-ignore", "-q", ".termes-prives"],
                                cwd=RACINE)
        self.assertEqual(sortie.returncode, 0, ".termes-prives doit être dans .gitignore")
        self.assertNotIn(".termes-prives", fichiers_suivis())

    def test_index_complet_sans_lien_mort(self):
        self.assertTrue(INDEX.exists(), "fiches/README.md manquant")
        index = INDEX.read_text(encoding="utf-8")
        liens = set(re.findall(r"\]\(([^)#\s]+\.md)\)", index))
        for lien in liens:
            with self.subTest(lien=lien):
                self.assertTrue((FICHES / lien).exists(), "lien mort")
        for f in fiches():
            with self.subTest(fiche=str(f.relative_to(RACINE))):
                self.assertIn(str(f.relative_to(FICHES)), liens,
                              "fiche absente de l'index")

    def test_liens_internes_des_fiches(self):
        for f in fiches():
            texte = f.read_text(encoding="utf-8")
            for lien in re.findall(r"\]\(([^)#\s:]+\.md)\)", texte):
                with self.subTest(fiche=str(f.relative_to(RACINE)), lien=lien):
                    self.assertTrue((f.parent / lien).resolve().exists(), "lien mort")

    def test_format_documente(self):
        doc = DOCS / "format-fiche.md"
        self.assertTrue(doc.exists(), "docs/format-fiche.md manquant")
        texte = doc.read_text(encoding="utf-8")
        for s in SECTIONS:
            with self.subTest(section=s):
                self.assertIn(f"## {s}", texte)


if __name__ == "__main__":
    unittest.main()
