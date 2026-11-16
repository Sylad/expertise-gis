# Animation WMS par `setTiles` : rafales d'erreurs de décodage sur les instants sans donnée

## Symptôme
Pendant une animation d'une couche WMS temporelle (URL changée à chaque pas par
`RasterTileSource.setTiles([url])`), la console se remplit de
`InvalidStateError: The source image could not be decoded` et `map.on('error')` compte des
centaines d'erreurs ; la couche clignote ou reste vide sur certains pas. Une couche à pas
journalier passe sans erreur au même rythme.

## Cause
Le pas de l'animation (par exemple horaire) tombe sur des instants que la couche ne publie
pas (prévision toutes les 6 h, vagues toutes les 3 h). Le serveur répond alors une exception
XML en HTTP 200 au lieu d'une image (voir
[erreur-wms-http-200-en-xml](../geoserver/erreur-wms-http-200-en-xml.md)) et MapLibre échoue
à la décoder. Mesuré : 18 instants sur 24 sans donnée pour une couche à 6 h, 0 erreur pour
une couche journalière. Observé en plus, non démontré : des
`TypeError: Cannot read properties of undefined (reading 'bind')` internes au rendu raster
quand une source est invalidée avant que la texture précédente soit liée (course, non fatale).

## Détection
Compter `map.on('error')` pendant un cycle d'animation, couche par couche ; pour un pas en
erreur, rejouer l'URL avec `curl -w "%{content_type}"` : `text/xml` = instant absent.
Comparer les instants demandés à la liste des validités de la couche (dimension `time` des
capabilities).

## Geste
- Animer sur les **validités publiées** de la couche (aimanter chaque pas à la validité
  disponible la plus proche, une couche « maître du temps »), jamais à cadence libre.
- Avec plusieurs couches de pas différents, chacune prend sa propre validité la plus proche.
- `{bbox-epsg-3857}` dans l'URL des tuiles laisse MapLibre calculer l'emprise de chaque
  tuile ; il marche aussi en projection globe.
- Preuve d'effet : 0 erreur au même rythme d'animation.

## Versions concernées
MapLibre GL JS 5.24 (vécu, 168 pas à 8 images/s, GeoServer derrière).

## Source
- https://maplibre.org/maplibre-gl-js/docs/API/classes/RasterTileSource/ (`setTiles`)
- https://maplibre.org/maplibre-style-spec/sources/ (gabarit `{bbox-epsg-3857}` : « for WMS requests »)
- vécu 2026-05-22 (MapLibre GL JS 5.24, couche de prévision à 6 h et couche journalière).

## Statut
prouvé
