"""Modèle de test « légende = rendu » à copier dans un projet (unittest ou pytest).

Remplir les quatre fonctions marquées À REMPLIR, une classe de test par couche. Tant
qu'elles ne sont pas remplies, les tests sont sautés (jamais verts à vide).

Invariant 1 : pour chaque option du réglage, la légende affichée = la source du rendu.
Invariant 2 : l'unité de la légende est celle de la préférence, et aucune valeur ne
s'affiche dans la couleur d'une autre classe que celle qu'on lit.
"""

import unittest

from legende_rendu import (classe, classes_changees_par_arrondi, convertir_seuils,
                           ecarts_legende, entrees_depuis_maplibre, valeurs_autour_des_seuils)

# À REMPLIR : toutes les valeurs du réglage qui changent le rendu ou la légende
# (styles, unités, langues des lettres, niveaux, modèles…). Une liste vide saute le test.
OPTIONS = []


def expression_couleur_du_rendu(option):
    """À REMPLIR : l'expression de couleur que la carte utilise vraiment pour `option`
    (lue dans le style produit par le code, pas recopiée), ou le texte du SLD servi
    (utiliser alors entrees_depuis_sld)."""
    raise unittest.SkipTest("expression_couleur_du_rendu non remplie")


def legende_affichee(option):
    """À REMPLIR : les entrées (seuil, couleur) que la légende affiche pour `option`, lues
    dans le modèle de la légende ou dans son DOM rendu, dans l'unité affichée."""
    raise unittest.SkipTest("legende_affichee non remplie")


def conversion_vers_l_unite_affichee(option):
    """À REMPLIR : fonction seuil de la donnée → seuil dans l'unité de la préférence, et
    libellé de cette unité. Exemple : (lambda k: k - 273.15, "°C")."""
    raise unittest.SkipTest("conversion_vers_l_unite_affichee non remplie")


def unite_affichee_par_la_legende(option):
    """À REMPLIR : le libellé d'unité que la légende affiche pour `option`."""
    raise unittest.SkipTest("unite_affichee_par_la_legende non remplie")


# À REMPLIR : le formatage des valeurs du projet (carte, fiche au clic), et la fonction
# qui choisit la couleur d'une valeur. Par défaut : une décimale, couleur sur la valeur brute.
def afficher(valeur):
    return round(valeur, 1)


DECIMALES_AFFICHEES = 1
classer = None  # None = classe de la valeur brute ; sinon fonction (valeur, seuils) -> indice


class TestLegendeEgaleRendu(unittest.TestCase):
    def setUp(self):
        if not OPTIONS:
            self.skipTest("OPTIONS vide : lister les options du réglage")

    def test_legende_suit_le_rendu_pour_chaque_option(self):
        for option in OPTIONS:
            with self.subTest(option=option):
                conversion, _ = conversion_vers_l_unite_affichee(option)
                attendu = convertir_seuils(
                    entrees_depuis_maplibre(expression_couleur_du_rendu(option)), conversion)
                self.assertEqual(ecarts_legende(attendu, legende_affichee(option)), [])

    def test_unite_de_la_preference(self):
        for option in OPTIONS:
            with self.subTest(option=option):
                _, unite = conversion_vers_l_unite_affichee(option)
                self.assertEqual(unite_affichee_par_la_legende(option), unite)

    def test_arrondi_ne_change_pas_la_classe(self):
        for option in OPTIONS:
            with self.subTest(option=option):
                seuils = [s for s, _ in legende_affichee(option)
                          if isinstance(s, (int, float)) and not isinstance(s, bool)]
                if not seuils:
                    self.skipTest("aucun seuil numérique (légende catégorielle) : arrondi sans objet")
                valeurs = valeurs_autour_des_seuils(seuils, DECIMALES_AFFICHEES)
                fautes = classes_changees_par_arrondi(
                    valeurs, seuils, afficher,
                    (lambda v, s=seuils: classer(v, s)) if classer
                    else (lambda v, s=seuils: classe(v, s)))
                self.assertEqual(fautes, [], "valeur affichée dans la couleur d'une autre classe")


if __name__ == "__main__":
    unittest.main()
