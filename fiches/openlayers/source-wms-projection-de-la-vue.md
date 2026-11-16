# Source WMS hors EPSG:3857 : `projection` dit qui reprojette, la grille vient de la vue, l'ordre des axes reste à vérifier

## Symptôme
La vue n'est pas en EPSG:3857 (EPSG:4326, LAEA EPSG:3035, polaire…) et un raster WMS est faux :
- tuiles posées au mauvais endroit (patchwork de rectangles) sur une `TileWMS` qui a reçu
  un `tileGrid` construit pour une autre projection, sans option `projection` ;
- image cisaillée ou décalée par rapport au trait de côte (vécu en EPSG:3035, WMS 1.3.0) :
  la cause de ce cas n'a pas été isolée, voir « Cause ».

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
- **Ordre des axes (hypothèse pour le cisaillement vécu, non mesurée côté serveur).** En
  WMS 1.3.0, OpenLayers n'inverse la BBOX que si l'orientation des axes de la projection
  commence par `ne` (`source/wms.js:44-58`). Une projection enregistrée par proj4 sans
  `+axis=neu` est `enu` (défaut documenté de `Projection`) ; or EPSG:3035 est
  nord d'abord dans le registre EPSG, et WMS 1.3.0 suit l'ordre des axes du CRS. Un serveur
  qui applique cet ordre lit alors la BBOX à l'envers. Que ce soit la cause du cisaillement
  vécu n'est pas démontré.

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
- En WMS 1.3.0 avec un CRS nord d'abord, enregistrer la projection avec `+axis=neu` (ou
  demander en WMS 1.1.1, ordre est-nord) ; preuve d'effet : la BBOX envoyée commence par le
  nord et le trait de côte se superpose.
- La projection de la vue doit être connue d'OpenLayers : voir
  [projection-personnalisee-non-enregistree](projection-personnalisee-non-enregistree.md).

## Versions concernées
OpenLayers 10.11.0 (code relu et mesure scriptée le 2026-11-16, tableau ci-dessus) ;
OpenLayers 10.6 (cisaillement observé en EPSG:3035, cause non isolée). Comportement du
serveur WMS face à une BBOX est d'abord sous un CRS nord d'abord : non vérifié.

## Source
- https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/source/Image.js#L225-L237
- https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/source/TileImage.js#L173-L184
- https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/source/TileImage.js#L236-L270
- https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/tilegrid.js#L24-L31
- https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/source/wms.js#L44-L58
- https://openlayers.org/en/latest/apidoc/module-ol_proj_Projection-Projection.html
  (`axisOrientation` : « defaults to 'enu' »)
- https://epsg.io/3035 (axes : northing (Y), puis easting (X))
- vécu 2026-05-14 (OpenLayers 10, vue LAEA EPSG:3035, GetMap servis en EPSG:3857 avec
  reprojection client : rendu juste).

## Statut
à reprouver : le mécanisme d'OpenLayers est prouvé par le code et la mesure, mais la cause
du cisaillement vécu (ordre des axes ?) n'est pas démontrée côté serveur.
