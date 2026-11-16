"""Gabarit « légende = rendu » (invariants 1 et 2 de ecrans-carte/invariants.md).

Copier ce fichier dans le dépôt d'un projet (aucune dépendance hors bibliothèque standard),
puis écrire un test par couche qui, POUR CHAQUE OPTION du réglage (style, unité, langue…) :

    attendu = entrees_depuis_maplibre(style_de_la_couche(option))   # ou entrees_depuis_sld
    attendu = convertir_seuils(attendu, conversion(option))          # unité de l'utilisateur
    self.assertEqual(ecarts_legende(attendu, legende_affichee(option)), [])

Le modèle de test complet est dans modele_test_legende.py.

Conventions :
- Une entrée est (seuil, couleur) ; le seuil est None pour la classe « en dessous du premier
  seuil » d'une expression `step`, et la valeur catégorielle pour une expression `match`
  (« * » pour la couleur par défaut).
- Une valeur égale à un seuil appartient à la classe qui commence à ce seuil (sémantique de
  `step` de MapLibre et des ColorMap `type="intervals"` du SLD).
- Les couleurs sont comparées normalisées en « #rrggbb » (ou « #rrggbbaa » si l'opacité
  n'est pas 1).
"""

from bisect import bisect_right
import math
import re
import xml.etree.ElementTree as ET

INTERPOLATIONS = ("interpolate", "interpolate-hcl", "interpolate-lab")


def normaliser_couleur(couleur, opacite=None):
    """'#ABC', '#aabbcc', 'rgb(1,2,3)', 'rgba(1,2,3,0.5)' → '#rrggbb' ou '#rrggbbaa'."""
    c = str(couleur).strip().lower()
    alpha = 1.0
    m = re.fullmatch(r"rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)", c)
    if m:
        r, g, b = (round(float(x)) for x in m.group(1, 2, 3))
        if m.group(4) is not None:
            alpha = float(m.group(4))
    else:
        if c.startswith("0x"):  # notation SLD 0xRRGGBB
            c = "#" + c[2:]
        if not re.fullmatch(r"#(?:[0-9a-f]{3}|[0-9a-f]{6}|[0-9a-f]{8})", c):
            raise ValueError(f"couleur non reconnue : {couleur!r}")
        h = c[1:]
        if len(h) == 3:
            h = "".join(x * 2 for x in h)
        if len(h) == 8:
            alpha = int(h[6:], 16) / 255
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    if opacite is not None:
        alpha *= float(opacite)
    hexa = f"#{r:02x}{g:02x}{b:02x}"
    return hexa if math.isclose(alpha, 1.0) else hexa + f"{round(alpha * 255):02x}"


def entrees_depuis_maplibre(expression):
    """Entrées (seuil, couleur) d'une expression de couleur MapLibre : step, interpolate
    (linéaire, hcl, lab) ou match. Une couleur constante donne une seule entrée (None, c)."""
    if isinstance(expression, str):
        return [(None, normaliser_couleur(expression))]
    op = expression[0]
    if op == "step":
        sortie = [(None, normaliser_couleur(expression[2]))]
        reste = expression[3:]
        return sortie + [(reste[i], normaliser_couleur(reste[i + 1]))
                         for i in range(0, len(reste), 2)]
    if op in INTERPOLATIONS:
        reste = expression[3:]
        return [(reste[i], normaliser_couleur(reste[i + 1])) for i in range(0, len(reste), 2)]
    if op == "match":
        reste, defaut = expression[2:-1], expression[-1]
        sortie = []
        for i in range(0, len(reste), 2):
            valeurs = reste[i] if isinstance(reste[i], list) else [reste[i]]
            sortie += [(v, normaliser_couleur(reste[i + 1])) for v in valeurs]
        return sortie + [("*", normaliser_couleur(defaut))]
    raise ValueError(f"expression de couleur non prise en charge : {op!r}")


def entrees_depuis_sld(texte_sld):
    """Entrées (quantité, couleur) des ColorMapEntry d'un SLD ou d'un SE, dans l'ordre.
    Une entrée d'opacité 0 est gardée (elle dessine « rien » et la légende doit le dire)."""
    racine = ET.fromstring(texte_sld)
    sortie = []
    for e in racine.iter():
        if e.tag.rsplit("}", 1)[-1] == "ColorMapEntry":
            if e.get("quantity") is None:
                raise ValueError(f"ColorMapEntry sans quantity : {ET.tostring(e, 'unicode')}")
            sortie.append((float(e.get("quantity")),
                           normaliser_couleur(e.get("color", "#000000"), e.get("opacity"))))
    if not sortie:
        raise ValueError("aucun ColorMapEntry dans le style")
    return sortie


def convertir_seuils(entrees, conversion):
    """Applique la conversion d'unité aux seuils numériques (pas à None ni aux catégories)."""
    return [(conversion(s) if isinstance(s, (int, float)) and not isinstance(s, bool) else s, c)
            for s, c in entrees]


def ecarts_legende(attendu, legende, tolerance=1e-6):
    """Liste des écarts entre les entrées attendues (source du rendu) et celles de la
    légende affichée ; vide quand la légende correspond au rendu."""
    ecarts = []
    if len(attendu) != len(legende):
        ecarts.append(f"{len(legende)} entrées dans la légende, {len(attendu)} dans le rendu")
    for i, ((sa, ca), (sl, cl)) in enumerate(zip(attendu, legende)):
        numeriques = all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in (sa, sl))
        if numeriques:
            egal = math.isclose(sa, sl, rel_tol=tolerance, abs_tol=tolerance)
        else:
            egal = sa == sl
        if not egal:
            ecarts.append(f"entrée {i} : seuil {sl!r} dans la légende, {sa!r} dans le rendu")
        if normaliser_couleur(cl) != normaliser_couleur(ca):
            ecarts.append(f"entrée {i} : couleur {cl} dans la légende, {ca} dans le rendu")
    return ecarts


def classe(valeur, seuils):
    """Indice de la classe d'une valeur : 0 sous le premier seuil, i à partir du seuil i-1."""
    return bisect_right(sorted(seuils), valeur)


def valeurs_autour_des_seuils(seuils, decimales):
    """Valeurs de contrôle : juste sous et juste sur chaque seuil, à la moitié du pas
    d'affichage près — là où un arrondi peut faire changer une valeur de classe."""
    pas = 10 ** -decimales
    sortie = []
    for s in seuils:
        sortie += [s - pas / 2, s - pas / 10, s, s + pas / 10, s + pas / 2]
    return sortie


def classes_changees_par_arrondi(valeurs, seuils, afficher, classer=None):
    """Valeurs dont la couleur ne correspond pas à la valeur AFFICHÉE (invariant 2).

    `afficher(v)` rend le nombre que l'utilisateur lit (celui du formatage du projet, par
    exemple `lambda v: round(v, 1)`) ; `classer(v)` rend l'indice de classe qui choisit la
    couleur (par défaut : la valeur brute). Rend une liste de (valeur, affichée, classe de la
    couleur, classe de la valeur affichée) ; vide quand aucune valeur ne s'affiche « 25,0 »
    dans la couleur de « < 25 ». Remèdes : classer sur la valeur affichée
    (`classer=lambda v: classe(afficher(v), seuils)`), ou afficher assez de décimales.
    """
    classer = classer or (lambda v: classe(v, seuils))
    sortie = []
    for v in valeurs:
        affichee = afficher(v)
        cc, ca = classer(v), classe(affichee, seuils)
        if cc != ca:
            sortie.append((v, affichee, cc, ca))
    return sortie
