# Le regroupement (`cluster`) masque une règle d'échelle : le point et sa lettre n'apparaissent jamais

## Symptôme
La norme ou le style de référence demande, à partir d'une échelle, un point avec son
étiquette ; sur la carte, on ne voit que des bulles numérotées jusqu'au zoom où la règle
ne s'applique plus. Aucune erreur : la règle est juste, mais invisible.

## Cause
Une source GeoJSON `cluster: true` regroupe les points jusqu'à `clusterMaxZoom` inclus ;
par défaut, un niveau sous le `maxzoom` de la source (18 par défaut), donc presque partout.
Si cette plage couvre celle où la règle demande le point isolé, la couche qui dessine le
point (filtrée sur `!['has', 'point_count']`) n'a jamais rien à dessiner.

Deux arrondis, lus dans le code de MapLibre GL JS 5.24 et 6.18 :
- `clusterMaxZoom` est arrondi à l'entier le plus proche (`Math.round`, avec un avertissement
  « Integer expected for option 'clusterMaxZoom' ») dans `source/geojson_source.ts` ;
- une source GeoJSON est découpée en tuiles de zoom entier, et la carte au zoom fractionnaire Z
  affiche les tuiles de `floor(Z)` (`coveringZoomLevel`, `Math.floor` pour toute source sans
  `roundZoom`, dans `geo/projection/covering_tiles.ts`). Pour un seuil à z 5,80, les tuiles
  z5 restent affichées jusqu'à z 6 : `clusterMaxZoom: 5` regroupe encore entre 5,80 et 6.

## Détection
Comparer `clusterMaxZoom` de la source au zoom du seuil de la règle (voir
[denominateur-d-echelle-en-zoom-tuiles-512](denominateur-d-echelle-en-zoom-tuiles-512.md)).
Au zoom du seuil, `queryRenderedFeatures({ layers: [pointLayer] })` doit renvoyer des
entités ; une liste vide avec des bulles à l'écran signe le piège.

## Geste
- Fixer `clusterMaxZoom` à un entier ≤ `floor(seuil) − 1` (seuil 5,80 → 4), ou ne pas regrouper
  cette couche. « Strictement sous le seuil » ne suffit pas pour un seuil fractionnaire.
- Preuve d'effet : capture au zoom du seuil avec points et étiquettes visibles.

## Versions concernées
MapLibre GL JS 5 (vécu) ; arrondis relus dans le code de MapLibre GL JS 5.24 et 6.18.

## Source
- https://maplibre.org/maplibre-style-spec/sources/#clustermaxzoom (« Defaults to one zoom less
  than maxzoom »)
- https://github.com/maplibre/maplibre-gl-js/blob/v5.24.0/src/source/geojson_source.ts
  (`_getClusterMaxZoom` : `Math.round(clusterMaxZoom)`)
- https://github.com/maplibre/maplibre-gl-js/blob/v5.24.0/src/geo/projection/covering_tiles.ts
  (`coveringZoomLevel` : `Math.floor` sans `roundZoom`)
- vécu 2026-09-17 (MapLibre GL JS 5, aérodromes regroupés jusqu'à z6).

## Statut
prouvé
