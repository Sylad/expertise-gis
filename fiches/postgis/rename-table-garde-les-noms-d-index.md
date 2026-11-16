# Table renommée : ses index, sa clé et sa séquence gardent leur nom

## Symptôme
Après `ALTER TABLE <t> RENAME TO <t>_old`, recréer `<t>` échoue :
`relation "<t>_pkey" already exists` (ou l'index spatial `spatial_<t>_the_geom`, la séquence
`<t>_fid_seq`).

## Cause
`ALTER TABLE … RENAME` ne renomme que la table ; index, contraintes et séquences gardent leur
nom, et ces noms partagent l'espace de noms des relations du schéma.

## Détection
```sql
SELECT indexname FROM pg_indexes WHERE schemaname = '<s>' AND indexname LIKE '%<t>%';
SELECT sequence_name FROM information_schema.sequences WHERE sequence_schema = '<s>';
```

## Geste
Renommer aussi index, contrainte de clé et séquence (`ALTER INDEX … RENAME`,
`ALTER TABLE … RENAME CONSTRAINT`, `ALTER SEQUENCE … RENAME`), ou supprimer la table quand
c'est permis. Lister ces noms avant toute relance d'une création d'index de mosaïque.

## Versions concernées
PostgreSQL 18 / PostGIS (vécu) ; comportement documenté.

## Source
- https://www.postgresql.org/docs/current/sql-altertable.html
- vécu 2026-09-23 (index PostGIS d'une ImageMosaic GeoServer recréé).

## Statut
prouvé
