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

## Détection
Comparer `clusterMaxZoom` de la source au zoom du seuil de la règle (voir
[denominateur-d-echelle-en-zoom-tuiles-512](denominateur-d-echelle-en-zoom-tuiles-512.md)).
Au zoom du seuil, `queryRenderedFeatures({ layers: [pointLayer] })` doit renvoyer des
entités ; une liste vide avec des bulles à l'écran signe le piège.

## Geste
- Fixer `clusterMaxZoom` strictement sous le zoom du seuil, ou ne pas regrouper cette couche.
- Preuve d'effet : capture au zoom du seuil avec points et étiquettes visibles.

## Versions concernées
MapLibre GL JS 5 (vécu) ; options de source documentées.

## Source
- https://maplibre.org/maplibre-style-spec/sources/#clustermaxzoom (« Defaults to one zoom less
  than maxzoom »)
- vécu 2026-09-17 (MapLibre GL JS 5, aérodromes regroupés jusqu'à z6).

## Statut
prouvé
