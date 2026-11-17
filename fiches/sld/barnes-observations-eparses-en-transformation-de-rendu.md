# Champ interpolé d'observations éparses : Barnes en transformation de rendu, pas IDW

## Symptôme
On veut un champ continu (raster coloré, isolignes) à partir de points d'observation
(stations, bouées) stockés en vecteur, et l'un de ces pièges apparaît :
- `idw:IDW` refuse la couche : son paramètre `data` attend une `GridCoverage2D`, pas des points ;
- le champ « invente » des valeurs au large ou dans les trous du réseau ;
- une isoligne « falaise » longe la frontière des zones sans donnée ;
- le bord de la carte est faux (les stations juste hors de la vue ne comptent pas) ;
- la portée réglée en km ne correspond pas à ce qu'on voit ;
- l'enchaînement `ras:Contour(data = vec:BarnesSurface(…))` échoue avec
  « Parameter data is missing but has min multiplicity > 0 ».

## Cause
- `idw:IDW` densifie un raster existant ; l'interpolation de **points** fournie par GeoTools
  est l'analyse objective de Barnes, `vec:BarnesSurface` (`BarnesSurfaceProcess`).
- Sans `maxObservationDistance`, chaque cellule reçoit une valeur, même à 1 000 km de toute
  station. Avec un `noDataValue` numérique (−999…), le contour suit le saut de valeur à la
  frontière ; `NaN` est transparent et ne produit aucune isoligne.
- La requête vecteur est limitée à l'emprise de la vue, sauf `queryBuffer` (appliqué par
  `invertQuery`).
- `scale`, `maxObservationDistance` et `queryBuffer` sont en **unités du CRS source** (degrés
  pour une table en EPSG:4326), convertis par 111 320 m/° vers le CRS de sortie. Rendu en
  EPSG:3857, une distance en mètres Mercator vaut `cos φ` mètres vrais : la portée vraie est
  réduite d'environ 0,64 à 50° N.
- L'enchaînement de deux processus : voir
  [transformations-imbriquees-sans-injection](transformations-imbriquees-sans-injection.md).
- Une transformation ne filtre pas ses entrées : elle reçoit toutes les entités de la requête
  (les valeurs `NULL` de l'attribut sont ignorées par Barnes, mais une ligne jugée invalide par
  un drapeau de qualité est prise).

## Détection
- Capabilities WPS : `vec:BarnesSurface` présent (module `wps` installé).
- Une station isolée : au-delà de `maxObservationDistance`, les pixels sont transparents
  (canal alpha à 0) et aucune isoligne ne coupe la zone — test unitaire : aucune ligne
  produite n'intersecte l'emprise d'un quart vide.
- `curl -w %{time_total}` du GetMap avec le style Barnes contre le même GetMap en étiquettes
  simples (`TextSymbolizer`) : l'écart est le coût de la surface, pas de la base.

## Geste
Style raster (paramètres via `env`, distances saisies en km puis divisées par 111,32 pour une
source en degrés) :
```xml
<ogc:Function name="vec:BarnesSurface">
  <ogc:Function name="parameter"><ogc:Literal>data</ogc:Literal></ogc:Function>
  <ogc:Function name="parameter"><ogc:Literal>valueAttr</ogc:Literal>
    <ogc:Function name="env"><ogc:Literal>param</ogc:Literal><ogc:Literal>temp</ogc:Literal></ogc:Function></ogc:Function>
  <!-- scale = radius km / 111.32 ; convergence 0.3 ; passes 2 ; minObservations 2 -->
  <!-- maxObservationDistance = queryBuffer = maxDist km / 111.32 ; noDataValue NaN -->
  <!-- pixelsPerCell 4 ; outputBBOX / outputWidth / outputHeight = env wms_bbox / wms_width / wms_height -->
</ogc:Function>
```
- `valueAttr` accepte une expression : un seul style générique sert tous les paramètres
  (`env('param')`), plutôt qu'un style par paramètre.
- Dimensionnement : longueur d'échelle = 2 à 4 fois l'espacement médian au plus proche voisin
  (mesuré : 46 km pour un réseau aéronautique européen, 32 km pour un réseau synoptique) — de
  80 km (précipitations, visibilité) à 200 km (pression) ; portée maximale ≈ 2,5 × l'échelle ;
  `queryBuffer` = portée maximale ; avertir l'utilisateur sous ~10 stations renseignées dans la vue.
- Filtrer en amont, par `CQL_FILTER` côté client : `<param> IS NOT NULL AND <drapeau qualité>`.
- Isolignes du **même** champ : un processus unique qui appelle `BarnesSurfaceProcess.execute`
  puis `ContourProcess.process` et délègue `invertQuery(queryBuffer, …)` à Barnes.
- Ne calculer que sur des créneaux complets : un créneau en cours de réception ne porte qu'une
  partie du réseau (mesuré : 323 stations au lieu d'environ 700).

## Versions concernées
GeoServer 3.0.1 / GeoTools 35.1 (vécu, 2026-09-12 et 2026-09-13) ; 2.x non vérifié.

## Source
- vécu 2026-09-12 (GeoServer 3.0.1, GeoTools 35.1, points en table PostGIS EPSG:4326 rendus en
  EPSG:3857 ; processus Barnes + contours écrit en Java 21, tests JUnit : champ linéaire,
  `NULL` ignorés, rien au-delà de la portée, intervalle obligatoire).
- Mesures du 2026-09-13, GetMap Europe 1024 × 660, cache de tuiles contourné : environ 300
  stations → étiquettes 115 ms, raster Barnes 493 ms, isolignes Barnes 477 ms ; environ 120
  stations → 66 / 183 / 174 ms. Requête SQL du créneau : 1,5 ms d'exécution.
- Code source : `org.geotools.process.vector.BarnesSurfaceProcess` et
  `org.geotools.process.raster.ContourProcess` — https://github.com/geotools/geotools
- https://docs.geoserver.org/latest/en/user/styling/sld/extensions/rendering-transform.html

## Statut
prouvé
