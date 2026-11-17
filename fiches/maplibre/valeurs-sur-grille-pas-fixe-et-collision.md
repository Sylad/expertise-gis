# Valeurs sur grille (barbules, chiffres) : éclaircir par un pas multiple de la maille, puis par collision

## Symptôme
Une grille de modèle (0,25°, par exemple) tracée en barbules ou en chiffres :
- toutes les valeurs tracées : le champ devient une bouillie illisible ;
- éclaircie par ré-échantillonnage (WCS `scale`, rendu à une résolution plus grossière) : les
  valeurs affichées sont **interpolées**, à des positions qui ne sont pas des points de grille,
  alors que la légende ou le cartouche dit « valeur lue au point de grille » ;
- éclaircie « une cellule sur n » : les points retenus changent quand l'emprise change ;
- une barbule tracée sans sa température (ou l'inverse) sur un tracé qui les apparie.

## Cause
- Ré-échantillonner moyenne ou interpole : la valeur montrée n'existe pas dans la source.
- Un pas en **indices** (une cellule sur n depuis le bord de l'extrait) dépend de l'origine
  de l'extrait : deux emprises différentes ne retiennent pas les mêmes cellules.
- Une bande à `NaN` en un point, gardée « à moitié », donne un symbole incomplet.
- Côté client, sans collision, une barbule (bien plus grande qu'une flèche) recouvre ses
  voisines à tout zoom.

## Détection
- Test unitaire sur une grille synthétique : chaque point retenu a `lon` et `lat` multiples du
  pas (à `maille/4` près) et sa valeur est **égale** à celle de la cellule source ; un point
  dont une bande vaut `NaN` est absent.
- Même calcul sur deux emprises qui se recouvrent : les points de la zone commune sont identiques.
- Résultat vide alors que la grille est pleine : les centres de cellules ne tombent pas sur les
  multiples du pas (grille enregistrée aux coins des pixels, ou pas non multiple de la maille).

## Geste
- Lire la grille native (WCS 2.0.1 `GetCoverage` en `text/plain`, `subset` répété par axe), puis
  ne retenir que les cellules **existantes** dont le centre tombe sur un multiple du pas, ancré
  au monde (`|v/pas − round(v/pas)|·pas < maille/4`) — jamais d'interpolation. Pas = multiple
  exact de la maille (0,25° → 2,5° ou 5°).
- Écarter un point dès qu'une bande vaut `NaN` ; apparier deux grilles (vent, température) par
  position et écarter le point orphelin.
- Lier le pas à l'échelle de sortie (sur une carte imprimée : 5° en A4, 2,5° en A3) et l'écrire
  dans la légende : « valeurs lues au point de grille 0,25°, pas 5°, aucune interpolation ».
- Côté client (MapLibre), barbules : `icon-allow-overlap: false`, `icon-ignore-placement: false`,
  `icon-padding: 6` — la collision retire les symboles qui se recouvrent et la densité suit le
  zoom ; flèches courtes : chevauchement permis (`allow-overlap: true`). Un symbole composé de
  plusieurs couches demande une décision commune :
  [modele-de-station-desencombrement-atomique](modele-de-station-desencombrement-atomique.md).

## Versions concernées
WCS 2.0.1 sur GeoServer 3.0.1 (code relu, test unitaire du sous-échantillonnage, 2026-09-17) ;
MapLibre GL JS 5.24 (vécu, 2026-09 : grille de barbules illisible sans collision).

## Source
- vécu 2026-09-17 (grille de modèle global 0,25°, niveaux isobares, WCS 2.0.1 `text/plain` de
  GeoServer 3.0.1, tracé vent + température imprimé à pas 2,5° et 5° ; test : pas 0,5° sur une
  grille synthétique, point à `NaN` écarté).
- https://docs.geoserver.org/latest/en/user/services/wcs/reference.html
- https://maplibre.org/maplibre-style-spec/layers/#icon-allow-overlap

## Statut
prouvé
