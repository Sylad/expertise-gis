# ALTER SEQUENCE … OWNER refusé : tout le bloc DO est annulé en silence

## Symptôme
Un script qui change le propriétaire de tous les objets d'un schéma dans un bloc `DO`
semble passer, mais rien de ce qu'il faisait ensuite n'est appliqué (`search_path`,
propriétaires) ; l'erreur se perd si le job efface son pod.

## Cause
`ALTER SEQUENCE … OWNER TO` est refusé pour une séquence **liée** à une colonne
(`serial`/`identity`) : elle suit sa table (`cannot change owner of sequence … is linked to table`).
L'erreur fait échouer le bloc `DO` et annule toute sa transaction.

## Détection
Lister les séquences liées :
```sql
SELECT c.relname FROM pg_class c JOIN pg_depend d ON d.objid = c.oid
WHERE c.relkind = 'S' AND d.refobjsubid > 0 AND d.deptype IN ('a','i');
```

## Geste
Exclure ces séquences de la boucle (changer le propriétaire de la table suffit) ;
`ON_ERROR_STOP` et un contrôle d'effet après le script (propriétaires, `search_path` lus en base).

## Versions concernées
PostgreSQL 18 (vécu) ; comportement documenté.

## Source
- https://www.postgresql.org/docs/current/sql-altersequence.html
- vécu 2026-09-18 (PostgreSQL 18, création d'un rôle dédié à GeoServer).

## Statut
prouvé
