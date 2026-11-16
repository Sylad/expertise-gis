# Mosaïque élargie : l'emprise déclarée et la grille GWC restent les anciennes

## Symptôme
Après avoir élargi la zone couverte par les granules, le WMS rend bien la nouvelle zone,
mais les capabilities gardent l'ancienne emprise et, hors de l'ancienne fenêtre, les tuiles
ne sont jamais mises en cache : à chaque appel `geowebcache-cache-result: MISS`,
`geowebcache-miss-reason: Coverage […], index […]`.

## Cause
L'emprise déclarée d'un coverage ImageMosaic est fixée à sa création ; un `harvest` ne la
modifie pas. Le sous-ensemble de grille de la couche tuilée est calculé depuis cette emprise.
`?recalculate=nativebbox,latlonbbox` est sans effet sur une mosaïque à index PostGIS (même
après `reset` du magasin).

## Détection
Comparer `EX_GeographicBoundingBox` des capabilities à `ST_Extent` de l'index ; tuile hors de
l'ancienne fenêtre demandée deux fois : MISS/MISS avec `miss-reason` = piège.

## Geste
`PUT …/coveragestores/<s>/coverages/<c>.xml` avec `<nativeBoundingBox>` et
`<latLonBoundingBox>` explicites (union de l'emprise déclarée et de `ST_Extent` de l'index) ;
retirer les `extent` figés de la couche tuilée ; vérifier par `GET /gwc/rest/layers/<ws>:<c>.xml`
et par la même tuile : MISS puis HIT. Automatiser à l'étape d'ingestion quand l'index dépasse
l'emprise déclarée.

## Versions concernées
GeoServer 3.0.1 / GWC 2.0.1, index PostGIS (vécu).

## Source
vécu 2026-09-17 (GeoServer 3.0.1 ; 29 mosaïques corrigées, MISS → HIT vérifié sur 3 couches).

## Statut
prouvé
