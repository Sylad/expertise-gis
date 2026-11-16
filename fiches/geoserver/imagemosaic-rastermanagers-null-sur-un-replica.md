# Harvest en 500 « rasterManagers is null » sur un seul réplica

## Symptôme
Un `harvest` ImageMosaic échoue par intermittence :
`HTTP 500 Cannot invoke "java.util.Map.get(Object)" because "this.rasterManagers" is null` —
environ une fois sur N, N étant le nombre de réplicas.

## Cause
Le lecteur ImageMosaic de cette mosaïque est mort (libéré ou jamais rouvert) sur **un**
réplica ; le Service répartit les appels, donc seul ce réplica échoue. Cause vue derrière : le
lecteur n'obtient pas de connexion à son index PostGIS (voir
[limite-de-connexions-du-role-geoserver](limite-de-connexions-du-role-geoserver.md)), ou
rechargements en boucle (voir [grappe-hazelcast-sync-reload](grappe-hazelcast-sync-reload.md)).

## Détection
`kubectl logs <pod> | grep -c rasterManagers` sur chaque réplica : un seul en a.

## Geste
`POST /geoserver/rest/reset` sur **ce** réplica (`kubectl port-forward pod/<pod> …`, pas
`svc/` qui épingle un pod quelconque), puis relancer l'ingestion. Ne pas redémarrer les autres
réplicas.

## Versions concernées
GeoServer 3.0.1, 3 réplicas (vécu).

## Source
vécu 2026-09-21 (GeoServer 3.0.1, deux cycles d'ingestion en échec).

## Statut
prouvé
