# Entités vecteur mal placées dès que la vue n'est pas en EPSG:3857

## Symptôme
En EPSG:3857 les points, flèches ou polygones sont à leur place ; en EPSG:4326, Lambert ou
polaire, ils sont décalés, écrasés vers l'origine ou hors de la carte. Aucune erreur en
console. Même chose pour un dessin maison (canvas de particules, marqueurs calculés à la
main) qui suit la vue.

## Cause
Deux options qui supposent Web Mercator si on les fige :
- `new GeoJSON({ featureProjection: 'EPSG:3857' })` : les géométries sont transformées vers
  3857, puis interprétées dans le repère de la vue courante ;
- `fromLonLat([lon, lat])` sans second argument projette en EPSG:3857 par défaut.

## Détection
`map.getView().getProjection().getCode()` puis, pour une entité dont on connaît la position,
`feature.getGeometry().getCoordinates()` : les coordonnées doivent être dans les unités de la
vue (degrés en 4326, mètres de la projection sinon). Des mètres Mercator dans une vue en
degrés signent le piège.

## Geste
```ts
const proj = map.getView().getProjection();
new GeoJSON().readFeatures(fc, { dataProjection: 'EPSG:4326', featureProjection: proj });
fromLonLat([lon, lat], proj);
```
- Lire la projection au moment de la lecture (pas une constante figée à la construction) et
  relire les entités quand la vue change de projection.
- Un dessin maison recalcule ses pixels via `map.getPixelFromCoordinate(fromLonLat(c, proj))`.

## Versions concernées
OpenLayers 10 (vécu) ; options documentées, toutes versions.

## Source
- https://openlayers.org/en/latest/apidoc/module-ol_format_GeoJSON-GeoJSON.html
- https://openlayers.org/en/latest/apidoc/module-ol_proj.html (`fromLonLat` : « The default is Web
  Mercator, i.e. 'EPSG:3857' »)
- vécu 2026-05-14 (OpenLayers 10, vue LAEA EPSG:3035, flèches de vent décalées).

## Statut
prouvé
