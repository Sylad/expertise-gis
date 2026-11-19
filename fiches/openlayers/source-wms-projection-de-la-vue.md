# Source WMS hors EPSG:3857 : `projection` dit qui reprojette, la grille vient de la vue, un CRS nord d'abord veut `+axis=neu` en WMS 1.3.0

## Symptôme
La vue n'est pas en EPSG:3857 (EPSG:4326, LAEA EPSG:3035, polaire…) et un raster WMS est faux :
- tuiles posées au mauvais endroit (patchwork de rectangles) sur une `TileWMS` qui a reçu
  un `tileGrid` construit pour une autre projection, sans option `projection` ;
- image cisaillée ou décalée par rapport au trait de côte (vécu en EPSG:3035, WMS 1.3.0) :
  la cause de ce cas n'a pas été isolée, voir « Cause » ;
- image décalée ou vide en Lambert conique Europe (EPSG:3034, WMS 1.3.0) : symptôme évité
  d'avance par `+axis=neu` (notes de dépannage reçues le 2026-11-19, cas « O3 »).

En EPSG:3857 tout est juste, d'où un piège qui n'apparaît qu'au changement de projection.

## Cause
Lue dans le code d'OpenLayers 10.11.0 et mesurée (script Node, voir « Détection ») :
- **Projection égale à la vue ou absente : aucune reprojection côté client.** `ImageWMS`
  (`source/Image.js:225-237`) et `TileWMS` (`source/TileImage.js:236-250`) demandent alors
  l'image au serveur directement dans la projection de la vue (`CRS=` code de la vue). Régler
  `projection` sur la projection de la vue revient à l'omettre : pas de double reprojection.
- **Projection différente de la vue** (au sens de `equivalent`, `proj.js:487-497`) : le
  serveur rend dans la projection de la source et OpenLayers reprojette l'image dans le
  navigateur (`ReprojImage`, `ReprojTile` : `source/Image.js:251`, `source/TileImage.js:253-270`).
- **Grille de tuiles par défaut : celle de la vue.** Sans `tileGrid`, la grille est créée pour
  la projection demandée (`source/TileImage.js:173-184` → `tilegrid.js:24-31`), sur l'emprise
  de cette projection, ou une emprise globale centrée sur 0,0 si elle n'en a pas
  (`tilegrid.js:167-183`). Elle n'est jamais EPSG:3857 par défaut.
- **Un `tileGrid` fourni sans `projection` sert pour toute vue** (`source/TileImage.js:175`) :
  une grille EPSG:3857 posée sur une vue EPSG:3035 donne des BBOX en mètres Mercator étiquetées
  `CRS=EPSG:3035`, donc des tuiles rendues ailleurs : c'est le patchwork.
- **Ordre des axes.** En WMS 1.3.0, OpenLayers n'inverse la BBOX que si l'orientation des
  axes de la projection commence par `ne` (`source/wms.js:44-58`). Une projection
  enregistrée par proj4 sans `+axis=neu` est `enu` (défaut documenté de `Projection`) ; la
  chaîne proj4 d'epsg.io ne donne pas l'ordre des axes. Or EPSG:3035 et EPSG:3034 sont nord
  d'abord dans le registre EPSG (système de coordonnées 4500 : northing, easting), et
  EPSG:3995 est est d'abord (rien à ajouter). **Côté GeoServer** (3.0.2, relu ici le
  2026-11-19), `WMS.toInternalSRS` réécrit en 1.3.0 le code `EPSG:xxxx` en URN OGC
  (`urn:ogc:def:crs:EPSG::3034`), qui suit l'ordre du registre : la BBOX est lue nord
  d'abord (`WMS.java:981-997`). Une BBOX est d'abord est donc lue à l'envers. proj4 n'inverse
  les axes que sur demande (`enforceAxis`), ce qu'OpenLayers ne fait jamais : la carte se
  dessine toujours est d'abord, `+axis=neu` ne sert qu'à écrire la BBOX 1.3.0 nord d'abord.
  Que ce soit la cause du cisaillement vécu en EPSG:3035 reste non démontré (cas non
  rejoué).

## Détection
Dans l'onglet réseau, lire `CRS`, `BBOX` et `VERSION` des GetMap :
- `CRS` = code de la vue : pas de reprojection client ; `CRS` différent : reprojection client.
- BBOX dont les nombres ne sont pas dans l'emprise de `CRS` (mètres Mercator sous
  `CRS=EPSG:3035`) : grille d'une autre projection, cas du patchwork.
- En `VERSION=1.3.0` avec un CRS nord d'abord (EPSG:3035, EPSG:4326) : la BBOX doit commencer
  par le nord. Mesure (OpenLayers 10.11.0, `TileWMS`, tuile 3/4/2, vue EPSG:3035 sur son emprise) :

| Source | `CRS` envoyé | Reprojection client | BBOX envoyée |
|---|---|---|---|
| sans `projection` | EPSG:3035 | non | `4557642.82,4834113.8,…` (est d'abord) |
| `projection: 'EPSG:3035'` | EPSG:3035 | non | identique |
| `projection: 'EPSG:3857'` | EPSG:3857 | oui | `0,5009377.09,…` |
| `tileGrid` 3857, sans `projection` | EPSG:3035 | non | `0,5009377.09,…` (mètres Mercator) |
| proj4 avec `+axis=neu` | EPSG:3035 | non | `4834113.8,4557642.82,…` (nord d'abord) |

Puis poser un trait de côte vecteur par-dessus et basculer la vue entre 3857 et la projection
cible : l'écart doit rester nul.

## Geste
- Laisser `projection` absente (ou égale à la vue) quand le serveur sait rendre dans la
  projection de la vue : rendu serveur, pas de reprojection client.
- La fixer sur une projection que le serveur sert (par exemple `'EPSG:3857'`) seulement si le
  serveur ne sert pas celle de la vue : OpenLayers reprojette alors côté client
  (plus de calcul, bords à vérifier).
- Ne passer un `tileGrid` à `TileWMS` qu'avec la `projection` dans laquelle il est défini.
- En WMS 1.3.0 avec un CRS nord d'abord (EPSG:3035, EPSG:3034), ajouter `+axis=neu` à la
  définition proj4 et l'enregistrer (`register(proj4)`) avant toute recherche de la
  projection (ou demander en WMS 1.1.1, ordre est-nord) ; preuve d'effet : la BBOX envoyée commence par le
  nord et le trait de côte se superpose.
- La projection de la vue doit être connue d'OpenLayers : voir
  [projection-personnalisee-non-enregistree](projection-personnalisee-non-enregistree.md).

## Versions concernées
OpenLayers 10.11.0 (code relu et mesure scriptée le 2026-11-16, tableau ci-dessus) ;
OpenLayers 10.6 (cisaillement observé en EPSG:3035, cause non isolée) ; OpenLayers 10.11.0
avec proj4 2.22.0 et `+axis=neu` en EPSG:3034 (vécu, image d'une zone connue regardée,
rapporté par les notes de dépannage reçues le 2026-11-19). GeoServer 3.0.2 : lecture nord
d'abord de la BBOX 1.3.0 relue dans le code (`WMS.toInternalSRS`) ; autres serveurs WMS non
vérifiés.

## Source
- https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/source/Image.js#L225-L237
- https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/source/TileImage.js#L173-L184
- https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/source/TileImage.js#L236-L270
- https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/tilegrid.js#L24-L31
- https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/source/wms.js#L44-L58
- https://openlayers.org/en/latest/apidoc/module-ol_proj_Projection-Projection.html
  (`axisOrientation` : « defaults to 'enu' »)
- https://epsg.io/3035 (axes : northing (Y), puis easting (X))
- https://epsg.io/3034 (système de coordonnées 4500 : northing, easting)
- https://github.com/geoserver/geoserver/blob/3.0.2/src/wms-core/src/main/java/org/geoserver/wms/WMS.java#L981-L997
- Notes de dépannage d'un autre compte, cas « O3 », reçues le 2026-11-19 (fusionné ici :
  même piège que cette fiche).
- vécu 2026-05-14 (OpenLayers 10, vue LAEA EPSG:3035, GetMap servis en EPSG:3857 avec
  reprojection client : rendu juste).

## Statut
à reprouver : le mécanisme est prouvé des deux côtés (OpenLayers par le code et la mesure,
GeoServer 3.0.2 par le code), mais le cisaillement vécu en EPSG:3035 n'a pas été rejoué avec
et sans `+axis=neu` pour en établir la cause.
