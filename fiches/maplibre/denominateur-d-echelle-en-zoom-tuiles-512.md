# Seuil d'échelle d'un SLD porté en zoom MapLibre : un niveau d'écart avec 156 543 m/px

## Symptôme
Une règle d'échelle reprise d'un SLD (`MinScaleDenominator`/`MaxScaleDenominator`) bascule
dans MapLibre un niveau de zoom trop tôt ou trop tard : l'étiquette ou le symbole apparaît
à 1:2 500 000 au lieu de 1:5 000 000. Le seuil « calculé » ne correspond pas à ce qu'on voit.

## Cause
Les niveaux de zoom de MapLibre sont définis sur des tuiles de **512 px** (taille de tuile
par défaut, `tileSize: 512`) : à z0 la
résolution à l'équateur vaut 40 075 016,686 / 512 = **78 271,517 m/px**. La valeur classique
156 543,03 m/px correspond à des tuiles de 256 px et décale le résultat d'un niveau entier.
Deuxième source d'écart : une expression `['zoom']` ne dépend pas de la latitude, alors que
l'échelle au sol si (facteur cos φ, ±0,5 niveau entre l'équateur et 60° N).

## Détection
Formule, avec le pixel normalisé OGC de 0,28 mm et une latitude de référence φ :
```
zoom = log2( 78271.517 × cos φ / (D × 0.00028) )
```
Exemple D = 5 000 000 : z 5,80 à l'équateur, 5,30 à 45° N, 4,80 à 60° N (avec 156 543 :
6,80 / 6,30 / 5,80, un niveau de trop). Puis le **voir** basculer : capture de part et d'autre
du seuil, sur un objet isolé, en comptant les pixels non-fond (un comptage global est noyé
par le nombre d'entités).

## Geste
- Une seule fonction de conversion, importée partout (carte, légende, widgets), avec la
  latitude de référence écrite en commentaire ; jamais une constante recopiée.
- Annoncer un seuil seulement après l'avoir vu basculer dans un navigateur.

## Versions concernées
MapLibre GL JS 5 (vécu, seuil vu basculer dans un navigateur) ; MapLibre GL JS 6 non
vérifié (`tileSize` par défaut toujours 512 dans la spécification de style 6.x).

## Source
- https://maplibre.org/maplibre-style-spec/sources/ (`tileSize` : « Defaults to 512 »)
- https://www.ogc.org/standards/wms/ (WMS 1.3.0 et SLD 1.0 : pixel de rendu normalisé de 0,28 mm)
- vécu 2026-09-17 (MapLibre GL JS 5, deux couches vecteur alignées sur leur SLD).

## Statut
prouvé
