# ImageMosaic de GeoTIFF lue par le lecteur NetCDF : image uniforme

## Symptôme
Le coverage existe, les granules sont indexés, l'emprise et le temps sont bons, le GetMap
répond 200 en PNG… mais l'image est d'une seule couleur (~1,5 Ko pour 256×256 au lieu de
5–50 Ko). Une sonde « 200 + image/png + taille > 1 Ko » la voit verte.

## Cause
Sans `SuggestedSPI` explicite dans `indexer.properties`, le lecteur est choisi en devinant à
partir de `sample_image.dat` ; constaté : `SuggestedSPI=…NetCDFImageReaderSpi` écrit dans le
`<store>.properties` généré, qui lit les GeoTIFF en NaN/0.

## Détection
- `grep SuggestedSPI <dossier mosaïque>/<store>.properties`.
- Contenu de l'image : nombre de couleurs distinctes (une seule entrée de palette utilisée).

## Geste
Dans `indexer.properties` de chaque mosaïque GeoTIFF :
```properties
SuggestedFormat=org.geotools.gce.geotiff.GeoTiffFormat
SuggestedSPI=it.geosolutions.imageioimpl.plugins.tiff.TIFFImageReaderSpi
```
Pour une mosaïque déjà créée : corriger `<store>.properties`, puis
`POST /rest/workspaces/<ws>/coveragestores/<s>/reset`. Une sonde de rendu compte les couleurs,
pas seulement les octets.

## Versions concernées
GeoServer 2.28 avec le module NetCDF installé (vécu) ; 3.x non vérifié.

## Source
vécu 2026-06-15 (GeoServer 2.28, 6 mosaïques GeoTIFF après recréation du data dir).

## Statut
à reprouver — établi sur 2.28.
