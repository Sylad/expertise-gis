# Étiquette de zone posée hors de la forme : centroïde au lieu du pôle d'inaccessibilité

## Symptôme
L'étiquette d'une zone en croissant, en U ou très découpée tombe hors de la zone, sur la
zone voisine ; d'une géométrie multiple (zone en plusieurs morceaux), une seule partie est
étiquetée.

## Cause
L'étiquette est posée sur un point calculé à part (centroïde, centre de l'emprise), qui
peut sortir d'une forme non convexe. MapLibre sait faire mieux tout seul : une couche
`symbol` en `symbol-placement: point` sur un **polygone** place l'étiquette au pôle
d'inaccessibilité, toujours dans la forme, et une par polygone d'un multipolygone.

## Détection
Pour chaque point d'étiquette, tester son inclusion dans sa zone (`turf.booleanPointInPolygon`) :
un `false` signe le piège. Compter les étiquettes rendues
(`queryRenderedFeatures({ layers: [labelLayer] })`) face au nombre de parties.

## Geste
- Donner le polygone lui-même à la couche `symbol` (`symbol-placement: 'point'`), pas une
  source de centroïdes.
- Étiqueter le champ que le style de référence étiquette (souvent l'indicatif normalisé),
  pas le champ « évident ».

## Versions concernées
MapLibre GL JS 5 (vécu) ; code de la branche principale (MapLibre GL JS 6) relu.

## Source
- https://github.com/maplibre/maplibre-gl-js/blob/main/src/symbol/symbol_layout.ts
  (`addFeature` : pour un `Polygon`, `classifyRings` puis `findPoleOfInaccessibility` par polygone)
- vécu 2026-09-17 (MapLibre GL JS 5, zones aériennes en croissant).

## Statut
prouvé
