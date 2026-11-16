# Projection non intégrée (EPSG:3035, polaire…) utilisée sans être enregistrée

## Symptôme
Une vue ou une source déclarée en `EPSG:3035` (ou toute projection hors EPSG:4326 / EPSG:3857)
ne s'affiche pas : erreur à la création de la `View` (projection `null`, propriétés de
`null` illisibles), ou carte vide sans message quand la projection n'est qu'une source.

## Cause
OpenLayers ne connaît d'origine que EPSG:4326 et EPSG:3857 (et leurs alias). Pour toute
autre projection, `get('EPSG:3035')` renvoie `null` tant qu'elle n'a pas été définie,
par exemple via proj4.

## Détection
```js
import { get } from 'ol/proj';
get('EPSG:3035');  // null = non enregistrée ; un objet Projection = prête
```

## Geste
Enregistrer une fois au démarrage, **avant** de créer la vue ou les sources :
```js
import proj4 from 'proj4';
import { register } from 'ol/proj/proj4';
proj4.defs('EPSG:3035',
  '+proj=laea +lat_0=52 +lon_0=10 +x_0=4321000 +y_0=3210000 +ellps=GRS80 +units=m +no_defs');
register(proj4);
```
Preuve d'effet : `get('EPSG:3035')` renvoie un objet. Les rasters servis dans une autre
projection sont ensuite reprojetés : voir
[source-wms-projection-de-la-vue](source-wms-projection-de-la-vue.md).

## Versions concernées
OpenLayers 10 (vécu) ; `get` et `ol/proj/proj4` documentés en OpenLayers 10.11.

## Source
- https://openlayers.org/en/latest/apidoc/module-ol_proj.html (`get` : « Projection object, or null
  if not in list »)
- https://openlayers.org/en/latest/apidoc/module-ol_proj_proj4.html (`register`)
- vécu 2026-05-14 (OpenLayers 10, vue LAEA EPSG:3035).

## Statut
prouvé
