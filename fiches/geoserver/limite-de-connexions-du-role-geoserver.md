# « too many connections for role » : pools multipliés par les réplicas

## Symptôme
Échecs intermittents qui changent d'une exécution à l'autre : une sonde WMS qui tombe sur une
couche **différente** à chaque passage, des rendus en 500
`FATAL: too many connections for role "<role>"`, des `harvest` ImageMosaic en
`rasterManagers is null`.

## Cause
Chaque magasin a son pool par réplica : magasins vecteur (`max connections`, 10 par défaut) et
**chaque** mosaïque à index PostGIS (son propre pool). Le besoin total = somme des pools × nombre
de réplicas ; il dépasse vite une limite `CONNECTION LIMIT` posée « large ». Des lecteurs
ImageMosaic recréés sans libération (re-`PUT` des magasins) gardent chacun leur pool : les
connexions montent avec le nombre de redéploiements.

## Détection
```sql
SELECT rolconnlimit FROM pg_roles WHERE rolname = '<role>';           -- valeur réelle, pas celle du dépôt
SELECT state, count(*) FROM pg_stat_activity WHERE usename = '<role>' GROUP BY state;
```
Plafond trop bas ou fuite ? Fuite = connexions `idle in transaction` ou qui ne redescendent
jamais ; pool normal = décrue mesurée (éviction après ~5 min par défaut).

## Geste
- Borner d'abord les pools à la source (`max connections` des magasins, paramètres de pool du
  `datastore.properties` des mosaïques), puis fixer la limite du rôle ≈ 3 × le pic mesuré, en
  restant sous `max_connections` de la base (sinon la panne passe à toute la base).
- Après une série de redéploiements, `POST /rest/reset` sur chaque réplica libère les lecteurs.
- Une erreur qui change de couche à chaque passage signe une contention, pas une couche cassée.

## Versions concernées
GeoServer 3.0.1, 3 réplicas, PostgreSQL (vécu).

## Source
vécu 2026-09-18, 2026-09-24 et 2026-09-25 (GeoServer 3.0.1, ~35 mosaïques à index PostGIS ; pic mesuré 105 puis 173).

## Statut
prouvé
