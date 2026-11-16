# Source WMS dont `projection` suit la vue : image en parallélogramme ou tuiles mal posées

## Symptôme
La vue n'est pas en EPSG:3857 (EPSG:4326, LAEA EPSG:3035, polaire…) et un raster WMS est faux :
- `projection` de la source réglée sur la projection de la vue : l'image est cisaillée,
  en parallélogramme, décalée par rapport au trait de côte ;
- `TileWMS` sans `projection` : chaque tuile est juste, mais posée au mauvais endroit
  (patchwork de rectangles) ;
- `ImageWMS` sans `projection` : image rendue, alignement approximatif.

En EPSG:3857 tout est juste, d'où un piège qui n'apparaît qu'au changement de projection.

## Cause
L'option `projection` d'une source est la projection **des données de la source** (celle
dans laquelle on demande au serveur de rendre), pas celle de la vue. Quand elle diffère de
la vue, OpenLayers reprojette l'image côté client, automatiquement. La régler sur la vue
fait reprojeter deux fois (serveur puis client) ; l'omettre sur `TileWMS` laisse la grille
de tuiles par défaut (EPSG:3857) interprétée dans le repère de la vue.

## Détection
Dans l'onglet réseau, lire le `CRS`/`SRS` et la `BBOX` des GetMap envoyés : ils doivent être
dans la projection déclarée sur la source (par exemple `CRS=EPSG:3857` avec une emprise en
mètres Mercator) quelle que soit la vue. Poser un trait de côte vecteur par-dessus et
basculer la vue entre 3857 et la projection cible : l'écart doit rester nul.

## Geste
```ts
new ImageWMS({
  url, params: { LAYERS: '…', TRANSPARENT: true },
  serverType: 'geoserver',
  projection: 'EPSG:3857', // projection SERVEUR, stable ; pas view.getProjection()
});
```
- Pour une vue en projection libre, préférer `ImageWMS` (une image, reprojetée) à
  `TileWMS` (qui demande une grille de tuiles propre à chaque projection) ; on perd le cache
  de tuiles côté serveur.
- La projection de la vue doit être connue d'OpenLayers : voir
  [projection-personnalisee-non-enregistree](projection-personnalisee-non-enregistree.md).

## Versions concernées
OpenLayers 10.6 (vécu, vues EPSG:3035 et EPSG:4326) ; comportement documenté.

## Source
- https://openlayers.org/en/latest/apidoc/module-ol_source_ImageWMS-ImageWMS.html (`projection` :
  « projection of the source »)
- https://openlayers.org/en/latest/examples/wms-image-custom-proj.html
- vécu 2026-05-14 (OpenLayers 10, GetMap servis par GeoServer en EPSG:3857, vue LAEA EPSG:3035).

## Statut
prouvé
