# Interpolation IDW sur une grille déjà dense : rendus de 10 à 20 s

## Symptôme
Une couche raster sur grille régulière (modèle, analyse) stylée avec une transformation
d'interpolation IDW (facteur 8) met 10–21 s à rendre à froid en plein écran, sature le
serveur et fait tomber les autres couches en dépassement de délai. Un style « raster +
isolignes » qui refait l'interpolation deux fois aggrave le tout (2 transformations par requête).

## Cause
IDW est fait pour des données **éparses** (stations, bouées) ; sur une grille dense, il
recalcule chaque pixel suréchantillonné par moyenne pondérée de voisins. Le style combiné
rend aussi le raster une seconde fois.

## Détection
`curl -w %{time_total}` du GetMap avec le style à IDW contre le même GetMap en
`RasterSymbolizer` + `ColorMap` simple.

## Geste
- Grille dense : `RasterSymbolizer` + `ColorMap`, interpolation bicubique par la requête
  (`INTERPOLATIONS=bicubic`) — mesuré 0,5–1 s.
- Isolignes dans un style séparé « contours seuls » avec `ras:Contour` (`simplify`, `smooth`,
  intervalle par `env`), sur une couche cliente à part au-dessus du raster, même
  `INTERPOLATIONS` — mesuré 6,6 s → 0,3–1,1 s.
- IDW réservé aux points épars, facteur 2–3 au plus, ou raster précalculé (`gdal_grid`).

## Versions concernées
GeoServer 2.28.3 (vécu) ; 3.x non vérifié.

## Source
- vécu 2026-05-15 et 2026-05-17 (GeoServer 2.28.3, grille 0,25°, rendus 1280×640 et 2560×1271).
- https://docs.geoserver.org/latest/en/user/styling/sld/extensions/rendering-transform.html

## Statut
à reprouver — mesures sur 2.28 avec une implémentation IDW maison.
