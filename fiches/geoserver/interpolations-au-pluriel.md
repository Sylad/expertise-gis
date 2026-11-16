# Paramètre WMS INTERPOLATION (singulier) ignoré en silence

## Symptôme
Un raster continu (température, vent, vagues) reste pixelisé alors que la requête porte
`INTERPOLATION=bicubic`. Aucune erreur, aucun avertissement, ni côté client ni dans le journal.

## Cause
Le paramètre fournisseur de GeoServer s'appelle **`INTERPOLATIONS`** (pluriel, une valeur par
couche de `LAYERS`, séparées par des virgules) : `nearest neighbor`, `bilinear`, `bicubic`.
Un paramètre inconnu est ignoré.

## Détection
Deux GetMap identiques, l'un avec `INTERPOLATIONS=bicubic`, l'autre sans : les images
doivent différer (`md5sum`). Si la variante « singulier » donne le même md5 que « sans »,
le paramètre est ignoré.

## Geste
- Passer `INTERPOLATIONS: 'bicubic'` dans les paramètres de la source WMS du client
  (OpenLayers `ImageWMS`/`TileWMS`).
- Avantage par rapport au réglage `defaultWMSInterpolationMethod` de la couche : il survit à
  une recréation du store ou de la couche dans le catalogue.
- Garder la même interpolation sur une couche d'isolignes superposée au raster, pour que les
  contours tombent sur les couleurs.

## Versions concernées
GeoServer 2.28.3 (vécu) ; paramètre documenté sur les versions courantes.

## Source
- https://docs.geoserver.org/latest/en/user/services/wms/vendor.html#interpolations
- vécu 2026-05-17 (GeoServer 2.28.3 : singulier sans effet, pluriel corrige).

## Statut
prouvé
