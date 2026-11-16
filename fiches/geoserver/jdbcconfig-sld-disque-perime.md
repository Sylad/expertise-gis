# Style mis à jour par REST mais rendu avec l'ancienne version

## Symptôme
Après `PUT …/styles/<s>`, la relecture REST renvoie la nouvelle version, mais le rendu
utilise toujours l'ancienne (par exemple une transformation retirée qui continue d'échouer).

## Cause
Constaté avec un catalogue jdbcconfig sur 3 réplicas : la copie du fichier `.sld` dans le
data dir de chaque réplica restait à l'ancienne version, et c'est elle qui était lue au rendu.
Mécanisme exact non démontré (cache de style par réplica, ressources non partagées).

## Détection
Comparer, réplica par réplica, le fichier du data dir et `GET …/styles/<s>.sld?raw=true` ;
et rendre un GetMap **sur chaque réplica** (adresse du pod), pas à travers le Service.

## Geste
Partager les ressources (jdbcstore, voir
[jdbcstore-fichiers-servis-depuis-la-base](jdbcstore-fichiers-servis-depuis-la-base.md)), puis
réinitialiser chaque réplica (`POST /rest/reset` par adresse de pod) après la publication.
Vérifier l'effet par un GetMap par réplica.

## Versions concernées
GeoServer 2.28.3 avec jdbcconfig (vécu) ; 3.x non vérifié.

## Source
vécu 2026-05-12 (GeoServer 2.28.3, 3 réplicas, catalogue jdbcconfig).

## Statut
à reprouver — mécanisme non démontré, établi sur 2.28.
