# RasterSymbolizer : un élément hors de l'ordre du schéma est sans effet

## Symptôme
Un `ChannelSelection` (ou un `ContrastEnhancement`) présent dans le SLD n'a aucun effet au
rendu ; aucune erreur à la publication.

## Cause
Le schéma SLD 1.0 impose l'ordre des enfants de `RasterSymbolizer` : `Geometry`, `Opacity`,
`ChannelSelection`, `OverlapBehavior`, `ColorMap`, `ContrastEnhancement`, `ShadedRelief`,
`ImageOutline`. Constaté : un élément hors de cet ordre a été ignoré sans message.

## Détection
Valider le SLD contre le schéma (`xmllint --schema StyledLayerDescriptor.xsd`) ; comparer un
GetMap avec et sans l'élément.

## Geste
Respecter l'ordre du schéma ; valider les SLD contre le XSD avant publication. Vérifier
l'effet par un rendu, et relire le style stocké avec `?raw=true` (voir
[../geoserver/rest-get-style-sans-raw-reencode](../geoserver/rest-get-style-sans-raw-reencode.md)).

## Versions concernées
SLD 1.0 ; GeoServer 3.0.1 (vécu).

## Source
- http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd
- vécu 2026-09-10 (GeoServer 3.0.1).

## Statut
à reprouver — l'ignorance silencieuse par GeoServer est notée sans mesure isolée.
