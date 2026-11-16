# search_path : un schéma sans droit USAGE est sauté en silence, tables créées dans public

## Symptôme
Un outil (GeoServer jdbcconfig/jdbcstore, migration) configuré pour le schéma `<s>` crée ou
lit ses tables dans `public` ; on croit avoir un catalogue isolé et on en partage un autre.
Aucune erreur.

## Cause
PostgreSQL ignore sans erreur, dans `search_path`, tout schéma inexistant **ou sur lequel le
rôle n'a pas `USAGE`**. Cas typique : schéma créé par un script d'initialisation exécuté en
superutilisateur (propriétaire `postgres`), utilisé ensuite par un rôle applicatif sans droit.
Une URL JDBC `currentSchema=<s>,public` retombe aussi sur `public`.

## Détection
```sql
SELECT has_schema_privilege('<role>', '<s>', 'USAGE');      -- f = piège
SELECT nspname, pg_get_userbyid(nspowner) FROM pg_namespace WHERE nspname = '<s>';
```
Simuler la résolution du client : `PGOPTIONS='-c search_path=<s>' psql -U <role> -c 'SELECT current_schemas(false)'`.

## Geste
`ALTER SCHEMA <s> OWNER TO <role>` (ou `GRANT USAGE, CREATE ON SCHEMA <s> TO <role>`) dans le
script d'initialisation ; `currentSchema=<s>` **sans** `,public` quand on veut l'isolement.

## Versions concernées
PostgreSQL 16 (vécu) ; comportement documenté sur toutes les versions courantes.

## Source
- https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-SEARCH-PATH
- vécu 2026-09-08 (PostgreSQL 16, catalogue GeoServer trouvé dans `public`).

## Statut
prouvé
