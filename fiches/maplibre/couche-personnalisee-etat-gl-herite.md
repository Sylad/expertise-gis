# Couche WebGL personnalisée : état GL hérité de MapLibre (fondu jamais effacé, effacement partiel)

## Symptôme
Une couche `custom` (particules, traînées par fondu dans des textures en ping-pong) dessine,
la cadence est bonne, mais :
- les anciennes positions ne s'effacent jamais (« le point d'origine reste allumé ») ;
- un effacement ne nettoie qu'un coin de la texture (par exemple 25 × 25 px) ;
- ou c'est la carte elle-même qui se dessine mal après la couche.

Une mesure de cadence est verte : seul le regard voit le défaut.

## Cause
La doc de `CustomLayerInterface` le dit : à l'entrée de `render`, le mélange est actif avec
`gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA)`, et la couche ne peut rien supposer d'autre
de l'état GL. Un « fondu » qui doit **remplacer** le contenu d'une texture s'ajoute alors à
l'ancien et ne descend jamais. De même, un `gl.clear()` appelé après une passe qui a réduit
`gl.viewport` à la taille d'une petite texture n'efface que cette zone. Inversement, un état
modifié par la couche et non restauré casse le rendu de MapLibre.

## Détection
- En début de `render`, journaliser `gl.isEnabled(gl.BLEND)`, `gl.getParameter(gl.VIEWPORT)`,
  `gl.isEnabled(gl.SCISSOR_TEST)`.
- Lire les pixels d'une texture de traînées (`gl.readPixels` sur son framebuffer) sur
  plusieurs images : avec le fondu juste, une zone sans particule tend vers 0.
- Toujours une capture **regardée**, et sur plusieurs secondes : un défaut temporel ne se
  voit pas sur une image.

## Geste
- Poser explicitement tout l'état dont chaque passe a besoin : `gl.disable(gl.BLEND)` avant
  la passe de fondu, réactivé seulement pour la composition finale ;
  `gl.viewport(0, 0, gl.canvas.width, gl.canvas.height)` et `gl.disable(gl.SCISSOR_TEST)`
  avant tout effacement plein écran.
- Sauver puis restaurer ce que la couche modifie (BLEND, DEPTH_TEST, STENCIL_TEST, viewport,
  framebuffer, programme courant) avant de rendre la main : la doc ne l'exige pas en toutes
  lettres, mais sans restauration la carte s'est dessinée faux (vécu).
- Preuve d'effet : la même lecture de pixels tend vers 0 hors des particules.

## Versions concernées
MapLibre GL JS 5.24 (vécu, projections globe et Mercator) ; état d'entrée de `render`
documenté pour MapLibre GL JS 6.

## Source
- https://maplibre.org/maplibre-gl-js/docs/API/interfaces/CustomLayerInterface/
- vécu 2026-05-20 (MapLibre GL JS 5.24, WebGL2, couche de particules en ping-pong).

## Statut
prouvé
