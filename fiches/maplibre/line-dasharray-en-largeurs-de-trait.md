# `line-dasharray` compte en largeurs de trait : un tireté de SLD paraît continu

## Symptôme
Un tireté repris tel quel d'un SLD (`stroke-dasharray` `6 3` en pixels) est rendu par
MapLibre avec des tirets et des blancs mal proportionnés ; sur un trait fin, il paraît
continu de loin, sur un trait épais il s'allonge démesurément.

## Cause
Dans le style MapLibre, `line-dasharray` est exprimé en **multiples de la largeur du trait**
(`line-width`), pas en pixels. Le SLD, lui, donne des longueurs en pixels.

## Détection
Rendre le même segment avec `line-width` 1, puis 4 : la longueur des tirets à l'écran est
multipliée par 4. Mesurer la période des tirets sur une capture (pixels) et la comparer à
la somme des valeurs du SLD.

## Geste
Diviser le motif du SLD par la largeur du trait :
```js
const w = 0.55;                       // largeur du SLD, en px
paint: { 'line-width': w, 'line-dasharray': [6 / w, 3 / w] }
```
Si la largeur varie avec le zoom, le motif en pixels varie avec elle ; le recalculer pour la
largeur de référence de la norme. Preuve d'effet : même période mesurée qu'au rendu du SLD.

## Versions concernées
MapLibre GL JS 5 (vécu) ; définition de la spécification de style.

## Source
- https://maplibre.org/maplibre-style-spec/layers/#line-dasharray (« Units in line widths »)
- vécu 2026-09-17 (MapLibre GL JS 5, contour tireté repris d'un SLD à 0,55 px).

## Statut
prouvé
