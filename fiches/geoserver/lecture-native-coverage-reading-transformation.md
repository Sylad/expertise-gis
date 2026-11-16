# Transformation raster : elle reçoit une couverture déjà suréchantillonnée

## Symptôme
Une transformation qui lisse ou interpole un raster à maille grossière (0,25°) produit des
blocs : elle travaille sur une couverture que le pipeline a déjà rééchantillonnée à la
résolution d'affichage (au plus proche voisin) ; grands rendus en OOM.

## Cause
Le pipeline de `RenderingTransformation` lit la source à la résolution de sortie avant
d'appeler la transformation. Une fonction qui implémente le marqueur
`org.geotools.coverage.grid.io.CoverageReadingTransformation` reçoit à la place le lecteur et
ses paramètres (`ReaderAndParams`) et lit elle-même, à la résolution native
(`RenderingTransformationHelper`).

## Détection
Taille de la `GridCoverage2D` reçue (journal) : égale à la taille de l'image demandée ⇒
suréchantillonnée.

## Geste
- Classe qui étend `FunctionImpl` et implémente `CoverageReadingTransformation`, déclarée par
  `META-INF/services/org.geotools.api.filter.expression.Function`.
- Nom de fonction sans `:` (sinon `Unable to find function`).
- Les paramètres reçus ne contiennent pas `READ_GRIDGEOMETRY2D` : lire la couverture entière
  (borné pour une couverture compacte) faute d'emprise cible.
- Mesuré : 0,9 s et ~50 Mo au lieu d'un OOM à 6 Go sur un rendu 2560×1271.

## Versions concernées
GeoServer 2.28 / GeoTools 34 (vécu) ; 3.x non vérifié.

## Source
- Code source : `RenderingTransformationHelper`, `FootprintsTransformation` du module imagemosaic (https://github.com/geotools/geotools).
- vécu en mai 2026, date exacte non consignée (GeoServer 2.28, rendu 2560×1271).

## Statut
à reprouver — établi sur 2.28.
