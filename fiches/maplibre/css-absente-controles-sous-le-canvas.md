# Sans `maplibre-gl.css`, popups et contrôles tombent sous la carte

## Symptôme
Le popup d'un clic apparaît en bas de page, sous le canvas, ou hors de l'écran ; l'échelle,
l'attribution et les boutons de zoom ont disparu (ils sont sous la carte). La page qui
devait tenir à l'écran défile : `document.documentElement.scrollHeight > innerHeight`,
`window.scrollY > 0`.

## Cause
Le positionnement des éléments d'interface de MapLibre (`.maplibregl-popup`,
`.maplibregl-ctrl-*`, coins `.maplibregl-ctrl-top-right`…) est entièrement porté par la
feuille `maplibre-gl.css`. Sans elle, ces éléments restent dans le flux normal du DOM et
s'empilent après le canvas.

## Détection
```js
getComputedStyle(document.querySelector('.maplibregl-popup')).position
// 'absolute' avec la feuille, 'static' sans
```
et chercher l'import dans le projet : `grep -rn "maplibre-gl.css"`.

## Geste
Importer la feuille une fois, dans le bundle global, avant tout composant de carte :
- Vite / React : `import 'maplibre-gl/dist/maplibre-gl.css';`
- Angular : ajouter `node_modules/maplibre-gl/dist/maplibre-gl.css` à `styles` dans
  `angular.json`.

Preuve d'effet : `position` vaut `absolute`, la page ne défile plus.

## Versions concernées
MapLibre GL JS 5.24 (vécu) ; exigence toujours écrite dans la doc de MapLibre GL JS 6.

## Source
- https://maplibre.org/maplibre-gl-js/docs/ (section « MapLibre CSS » : « Without the CSS, elements
  like Popups and Markers won't work. » ; les contrôles : vécu)
- vécu 2026-05-22 (MapLibre GL JS 5.24, popup et contrôles d'échelle et d'attribution).

## Statut
prouvé
