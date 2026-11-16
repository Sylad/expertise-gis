# Capture de la carte (`toDataURL`, image figée) vide ou noire

## Symptôme
`map.getCanvas().toDataURL()` (export PNG, impression, vignette figée d'une carte) renvoie
une image transparente ou noire, alors que la carte est bien affichée à l'écran.

## Cause
Par défaut un contexte WebGL n'est pas conservé après affichage
(`preserveDrawingBuffer: false`) : en dehors de l'image en cours de rendu, le tampon lu est
vide. Depuis MapLibre GL JS 5.0, l'option ne se passe plus à la racine de `MapOptions` mais
dans `canvasContextAttributes` ; l'ancienne forme est ignorée.

## Détection
Lire la valeur effective : `map.getCanvas().getContext('webgl2').getContextAttributes()
.preserveDrawingBuffer` (`false` = piège), et compter les pixels non transparents de l'image
exportée.

## Geste
```js
new maplibregl.Map({ …, canvasContextAttributes: { preserveDrawingBuffer: true } });
```
- Coût : un peu de mémoire et de cadence ; la réserver aux cartes qu'on exporte.
- Alternative sans le drapeau : capturer dans le gestionnaire `render` (même image que le
  rendu en cours), ou après `map.once('idle')` en forçant `map.triggerRepaint()`.
- Preuve d'effet : l'image exportée a des pixels non transparents.

## Versions concernées
MapLibre GL JS 5 (vécu, `canvasContextAttributes`) ; changement de 5.0 (CHANGELOG), même
forme documentée en MapLibre GL JS 6.

## Source
- https://raw.githubusercontent.com/maplibre/maplibre-gl-js/refs/heads/main/CHANGELOG.md (5.0.0 :
  « must now be defined inside the `canvasContextAttributes` object on `MapOptions` »)
- https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/MapOptions/
- vécu 2026-06-17 (MapLibre GL JS 5, cartes figées en image dans un tableau de bord).

## Statut
prouvé
