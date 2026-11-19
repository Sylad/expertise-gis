# Raster Float32 au style par défaut « raster » : contraste différent sur chaque tuile

## Symptôme
Une mosaïque de COG Float32 mono-bande (NaN = nodata), servie avec le style par défaut
`raster` (un `RasterSymbolizer` avec `<Opacity>` seul), montre une marche de luminosité entre
tuiles WMS voisines : chaque tuile 256×256 va de 1 à 255, et la colonne de bord commune de
deux tuiles voisines diffère en moyenne de 19 niveaux de gris, contre 1,4 entre les colonnes
centrales d'une seule GetMap 512×256 couvrant les deux.

## Cause
Sans `ColorMap` ni `ContrastEnhancement`, `RasterSymbolizerHelper` convertit toute image qui
n'est pas en octets (Float, Double, Int, Short, et UShort sans palette) par
`ImageWorker.rescaleToBytes()` (`RasterSymbolizerHelper.java:114-133`). Celui-ci prend les
extrema **de l'image de la requête** (`ImageWorker.java:1358`, `getExtremas()` :1019) et étire
[min, max] sur [1, 255] quand le nodata est remappé (`:1366-1383`). Le rendu ne lit que
l'emprise demandée (`GridCoverageRenderer.java:697-718`) : les bornes sont celles de chaque
tuile. `<Normalize/>` seul fait pareil (algorithme par défaut, extrema de l'image :
`ContrastEnhancementType.java:272-281`). Les plages (Range) des dimensions de la couverture
saisies dans l'interface d'administration ne sont lues nulle part par ce rendu.

## Détection
Deux GetMap voisines 256×256 et une GetMap 512×256 couvrant les deux, même style : écart
moyen entre les colonnes de bord des deux tuiles > 5 niveaux quand celui entre les deux
colonnes centrales de la grande image est < 2 → étirement par tuile. Ni le cache de tuiles,
ni le client, ni la lecture COG n'y sont pour quelque chose : la GetMap directe suffit.

## Geste
Fixer les bornes dans un SLD par produit :
- `ColorMap type="ramp"` (le NaN reste transparent : `ColorMapNode.java:153-189`) ;
- ou `<ContrastEnhancement><Normalize>` avec les VendorOptions
  `algorithm=StretchToMinimumMaximum`, `minValue`, `maxValue`
  (`ContrastEnhancementType.java:359` et suivantes, doc `rastersymbolizer.md:342-369`).
  Les VendorOptions acceptent `env()` : un style générique avec
  `&env=minValue:…;maxValue:…` par couche est possible.

Aucun réglage global ne fixe les bornes. Preuve d'effet : la même mesure donne un écart de
bord du même ordre que l'écart central. L'ordre des éléments du symboliseur compte :
[ordre-des-elements-rastersymbolizer](../sld/ordre-des-elements-rastersymbolizer.md).

## Versions concernées
GeoServer 3.0.2 / GeoTools 35.2 (vécu et mesuré, rapporté par les notes de dépannage reçues
le 2026-11-19 ; code relu ici le 2026-11-19 au tag GeoTools `35.2`, lignes à ±2 de celles des
notes).

## Source
- https://github.com/geotools/geotools/blob/35.2/modules/library/render/src/main/java/org/geotools/renderer/lite/gridcoverage2d/RasterSymbolizerHelper.java#L114-L133
- https://github.com/geotools/geotools/blob/35.2/modules/library/coverage/src/main/java/org/geotools/image/ImageWorker.java#L1358-L1385
- https://github.com/geotools/geotools/blob/35.2/modules/library/render/src/main/java/org/geotools/renderer/lite/gridcoverage2d/ContrastEnhancementType.java#L272-L281
- https://github.com/geotools/geotools/blob/35.2/modules/library/render/src/main/java/org/geotools/renderer/lite/gridcoverage2d/GridCoverageRenderer.java#L697-L718
- https://github.com/geoserver/geoserver/blob/3.0.2/doc/en/user/styling/sld/reference/rastersymbolizer.md?plain=1#L342-L369
- Notes de dépannage d'un autre compte, cas « G5 », reçues le 2026-11-19.

## Statut
prouvé
