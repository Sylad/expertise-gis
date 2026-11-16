# GeoTIFF multibande planaire : trois bandes verticales répétées

## Symptôme
Une mosaïque de GeoTIFF à 3 bandes rend l'image compressée en largeur et répétée trois fois
(bandes verticales), à certaines validités seulement ; une sonde « image non vide » est verte.

## Cause
Les granules fautifs sont écrits en **interleave par bande** (`PlanarConfiguration=2`),
souvent hérité sans le voir d'un profil copié (rasterio : `src.profile` d'un fichier 1 bande
porte `interleave='band'`). Le lecteur de GeoServer 3.0.1 les a lus comme entrelacés par pixel.

## Détection
`gdalinfo <granule>.tif | grep INTERLEAVE` → `BAND` = fautif, `PIXEL` = bon. Regarder une
validité **ancienne**, pas seulement la dernière.

## Geste
Tout écrivain multibande fixe `interleave='pixel'` explicitement (rasterio, GDAL
`-co INTERLEAVE=PIXEL`) ; réécrire les granules existants ; purger les tuiles en cache.

## Versions concernées
GeoServer 3.0.1 (lecteur ImageN) (vécu).

## Source
vécu 2026-09-10 (GeoServer 3.0.1 ; ~200 granules réécrits).

## Statut
prouvé
