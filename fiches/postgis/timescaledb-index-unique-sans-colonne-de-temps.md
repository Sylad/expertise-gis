# Hypertable TimescaleDB : clé unique refusée sans la colonne de temps

## Symptôme
`CREATE TABLE … PRIMARY KEY (station_id)` puis `create_hypertable(…, 'ts')` (ou l'ajout de la
contrainte après coup) échoue : `cannot create a unique index without the column "ts"
(used in partitioning)`.

## Cause
Une hypertable est partitionnée par le temps : tout index unique (clé primaire comprise) doit
contenir la ou les colonnes de partitionnement, faute de quoi l'unicité ne peut pas être
garantie entre morceaux.

## Détection
Le message d'erreur ci-dessus à la création.

## Geste
Clé composite qui inclut le temps, par exemple `PRIMARY KEY (ts, station_id)`. Si la table est
publiée directement dans GeoServer, les colonnes de cette clé ne sont exposées qu'avec
`Expose primary keys` (voir
[../geoserver/postgis-cle-primaire-non-exposee](../geoserver/postgis-cle-primaire-non-exposee.md)).

## Versions concernées
TimescaleDB 2.x (documenté).

## Source
https://docs.timescale.com/use-timescale/latest/hypertables/hypertables-and-unique-indexes/

## Statut
prouvé
