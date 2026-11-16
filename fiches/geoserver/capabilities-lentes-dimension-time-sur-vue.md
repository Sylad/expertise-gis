# Capabilities lentes : la dimension TIME est calculée sur une vue coûteuse

## Symptôme
GetCapabilities en 8–22 s, appels REST en dépassement de délai ; CPU de GeoServer au repos,
aucun verrou côté base.

## Cause
Pour une couche vecteur temporelle, GeoServer calcule la dimension TIME par
`SELECT max(<col_temps>)` puis `SELECT distinct(<col_temps>)` sur la table ou la vue publiée.
Sur une vue en `DISTINCT ON (…) ORDER BY …` d'une grosse table (2,2 M lignes), chaque appel
trie toute la vue ; avec `work_mem` de 4 Mo le tri part sur disque
(`Sort Method: external merge Disk`), ~10 s à froid, et c'est payé à chaque capabilities.

## Détection
- Thread dump pendant la requête (`jcmd 1 Thread.print`) : thread `http-nio` dans
  `DimensionHelper`.
- Échantillonner `pg_stat_activity` (rôle de GeoServer, `state='active'`) toutes les 0,5 s :
  les `max`/`distinct` sur la vue.
- `EXPLAIN (ANALYZE, BUFFERS)` de la requête : `external merge Disk`.

## Geste
- Durable : dédoublonner à l'ingestion, stocker la colonne de temps et l'indexer, publier une
  vue plate (sans `DISTINCT ON`).
- Atténuation : `ALTER ROLE <role_geoserver> SET work_mem = '64MB'` (mesuré 10 s → 2,3 s) ;
  ne vaut que pour les nouvelles connexions du pool.

## Versions concernées
GeoServer 3.0.1 avec PostgreSQL/PostGIS (vécu).

## Source
vécu 2026-09-22 (GeoServer 3.0.1, vue d'observations de 2,2 M lignes sur 7 jours).

## Statut
prouvé
