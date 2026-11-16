# `projection` passé au constructeur de la carte : la carte reste en Mercator

## Symptôme
`new maplibregl.Map({ …, projection: { type: 'globe' } })` affiche une carte plate, sans
erreur ni avertissement.

## Cause
`MapOptions` n'a pas d'option `projection` : la clé est ignorée. La projection est une
propriété **du style** (racine `projection`) ou se règle par `map.setProjection(…)`.

## Détection
`map.getProjection()` après `load` : pas de globe = l'option a été ignorée. Et la liste des
options de `MapOptions` dans la doc de la version utilisée.

## Geste
- Mettre la projection dans le style (`style.projection`), ou appeler
  `map.setProjection({ type: 'globe' })` dans le gestionnaire `load` (vécu en 5.24).
- En MapLibre GL JS 6, la spécification de style documente `mercator`,
  `vertical-perspective` et le préréglage `globe` (passage de l'une à l'autre selon le
  zoom) ; écrire la forme documentée de la version utilisée.
- Preuve d'effet : globe visible à faible zoom, `getProjection()` le confirme.

## Versions concernées
MapLibre GL JS 5.24 (vécu) ; absence de `projection` dans `MapOptions` relue dans la doc de
MapLibre GL JS 6.

## Source
- https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/MapOptions/
- https://maplibre.org/maplibre-style-spec/root/#projection
- https://maplibre.org/maplibre-gl-js/docs/API/classes/Map/ (`setProjection`)
- vécu 2026-05-20 (MapLibre GL JS 5.24).

## Statut
prouvé
