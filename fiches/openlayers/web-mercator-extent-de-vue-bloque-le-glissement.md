# Web Mercator : la carte glisse à peine de côté et le centre reste bloqué au dézoom (`extent` de la vue)

## Symptôme
Vue en EPSG:3857 au zoom 2 (monde de 2048 px) dans une fenêtre de 1440 px : la carte ne
glisse que de ±300 px de côté ; plus dézoomé, le centre ne bouge plus du tout. Rien n'est
dessiné au-delà de ±180°.

## Cause
- La `View` a reçu `extent` = le carré Mercator. La contrainte de centre maintient alors le
  centre dans `[extent + largeur de vue / 2, extent − largeur de vue / 2]`
  (`src/ol/centerconstraint.js:34-55`) ; quand la vue est plus large que l'emprise
  (min > max), le centre est épinglé au milieu (`:45-48`).
- Sans `extent`, une projection globale reçoit par défaut `[-Infinity, sud, +Infinity, nord]`
  (`src/ol/View.js:2037-2042`, sauf `multiWorld: true`) : libre en X, tenue en Y.
- `wrapX: false` sur une source tuilée rogne l'étendue rendue à la grille
  (`src/ol/renderer/canvas/TileLayer.js:94-101`) : rien au-delà de ±180°.

Points vérifiés dans le code : la `View` ne normalise jamais son centre ;
`map.getPixelFromCoordinate(c, {wrapX: true})` ramène au monde le plus proche du centre
(`src/ol/Map.js:1096-1105`), `map.getCoordinateFromPixel(p, {wrapX: true})` au monde
principal (`:940-950`). Avec `wrapX: true`, les colonnes hors grille sont rabattues avant
l'URL (`src/ol/source/Tile.js:257-268`, `src/ol/tilegrid.js:39-52`), mais chaque copie du
monde est une tuile distincte (`src/ol/source/TileImage.js:287-297`) : une requête par copie.
`showFullExtent` sans `extent` s'applique à l'étendue de la projection (`View.js:2088-2091`).

## Détection
Playwright, fenêtre 1440 × 900, vue EPSG:3857 au zoom 2 : glisser de 400 px → la carte doit
bouger de 400 px. Les tuiles demandées à l'antiméridien doivent avoir leurs colonnes dans
[0, 2^z). Dans le code : `new View({ … extent: … })` avec l'emprise de EPSG:3857 = piège.

## Geste
- `View` sans `extent` en EPSG:3857 ; `wrapX: true` sur les sources ; `{wrapX: true}` dans
  les conversions pixel ↔ coordonnée (sinon une coordonnée cliquée sur une copie du monde
  sort de ±180°).
- `multiWorld: true` enlèverait aussi la tenue en latitude et le plafond de dézoom : à éviter
  ici.
- `view.fit(monde, {size})` ajuste le monde à la plus petite dimension de la fenêtre
  (`View.js:1163-1167`, résolution = max des deux axes), pas à la largeur.
- Preuve d'effet : la mesure Playwright de la détection.

## Versions concernées
OpenLayers 10.11.0 (code relu et mesure Playwright, rapportés par les notes de dépannage
reçues le 2026-11-19 ; code relu ici le 2026-11-19 au tag `v10.11.0`, lignes à ±1 de celles
des notes).

## Source
- https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/centerconstraint.js#L34-L55
- https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/View.js#L2037-L2042
- https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/renderer/canvas/TileLayer.js#L94-L101
- https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/Map.js#L1096-L1105
- https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/source/Tile.js#L257-L268
- https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/source/TileImage.js#L287-L297
- Notes de dépannage d'un autre compte, cas « O4 », reçues le 2026-11-19.

## Statut
prouvé
