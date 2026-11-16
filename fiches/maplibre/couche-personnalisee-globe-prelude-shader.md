# Couche WebGL personnalisée en globe : rien ne s'affiche (prélude de shader, `args` incomplets)

## Symptôme
Une couche `custom` qui marche en Mercator ne dessine rien en projection globe, ou plus rien
du tout après l'ajout du prélude de projection de MapLibre ; parfois une erreur de
compilation `'PI' : redefinition` qui passe inaperçue, la couche étant simplement absente.

## Cause
Pour suivre la projection courante (globe ou Mercator), le shader de la couche doit être
compilé avec le prélude que MapLibre fournit à `render` (`args.shaderData` :
`vertexShaderPrelude`, `define`, `variantName`) et recevoir à chaque image les uniformes
de `args.defaultProjectionData` (`mainMatrix`, `fallbackMatrix`, `tileMercatorCoords`,
`clippingPlane`, `projectionTransition`), puis projeter par `projectTile()`. Trois façons
de casser :
- ne passer que la matrice à la fonction de dessin au lieu de tout `args` ;
- redéclarer une constante déjà définie par le prélude (`PI`) : échec de compilation ;
- ne pas recompiler quand `variantName` change (passage globe ↔ Mercator).
Le prélude est en GLSL ES 3.00 : la couche doit être écrite pour WebGL2.

## Détection
Après `gl.compileShader`, lire `gl.getShaderInfoLog(shader)` et lever une erreur si
`COMPILE_STATUS` est faux ; journaliser `args.shaderData.variantName` à chaque `render` et
basculer de projection pour vérifier qu'il change et que le programme est recompilé.

## Geste
- Passer `args` entier à la fonction de dessin ; mettre les programmes en cache par
  `variantName`.
- Préfixer le shader par `#version 300 es`, le prélude, puis le code de la couche, sans
  redéfinir `PI` ni les autres noms du prélude.
- Préférer la `custom layer` native à une surcouche tierce quand on veut le globe.

## Versions concernées
MapLibre GL JS 5.24 (vécu) ; MapLibre GL JS 6 non vérifié.

## Source
- https://maplibre.org/maplibre-gl-js/docs/API/interfaces/CustomLayerInterface/
- vécu 2026-05-20 (MapLibre GL JS 5.24, WebGL2, globe et Mercator).

## Statut
prouvé
