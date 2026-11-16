# VendorOption « interpolation » du SLD : les classes de couleur restent en escalier

## Symptôme
Un raster sur grille régulière stylé par `ColorMap` garde des bords de cellules et des
transitions de couleur en marches, malgré `<VendorOption name="interpolation">BICUBIC</VendorOption>`
dans le `RasterSymbolizer`.

## Cause
Constaté : l'option du SLD n'a joué que sur le rééchantillonnage géométrique (reprojection
4326 → 3857) ; la `ColorMap` s'applique ensuite pixel par pixel sur les valeurs brutes.
L'interpolation de la couche (`defaultWMSInterpolationMethod`) ou le paramètre de requête
`INTERPOLATIONS` interpolent les valeurs **avant** la `ColorMap`.

## Détection
Même GetMap rendu (a) avec la seule VendorOption, (b) avec `INTERPOLATIONS=bicubic` :
compter les couleurs distinctes ou comparer visuellement une frontière de classe.

## Geste
- Raster sur grille dense (modèle, analyse) : SLD réduit à `RasterSymbolizer` + `ColorMap`,
  interpolation par `INTERPOLATIONS=bicubic` dans la requête (voir
  [interpolations-au-pluriel](interpolations-au-pluriel.md)) ou par la couche.
- Ne pas employer une interpolation de données éparses (IDW) sur une grille déjà dense :
  voir [../sld/idw-sur-grille-dense](../sld/idw-sur-grille-dense.md).

## Versions concernées
GeoServer 2.28.3 (vécu) ; 3.x non vérifié.

## Source
vécu 2026-05-15 (GeoServer 2.28.3, grille 0,25°, rendu 2560×1271 en EPSG:3857).

## Statut
à reprouver — mécanisme déduit d'une comparaison visuelle sur 2.28.
