# Rafales de tuiles sur une couche à rendu lourd : 502 en cascade

## Symptôme
Au déplacement ou au zoom, le client lance des dizaines de tuiles en parallèle sur une couche
à transformation coûteuse (interpolation, isolignes, carte de chaleur) ; le serveur sature,
le proxy répond 502/504, **d'autres** couches disparaissent aussi.

## Cause
Sans limite, toutes les requêtes entrent dans le pool de threads de Tomcat et se disputent le
CPU ; les plus lentes dépassent le délai du proxy, et la file bloque aussi les couches légères.

## Détection
Pendant une rafale : temps de réponse d'une couche légère qui explose ; threads `http-nio`
occupés (`jcmd 1 Thread.print`).

## Geste
Extension officielle **control-flow** : `controlflow.properties` dans le data dir, par exemple
```properties
ows.global=16
ows.wms.getmap=6
ows.wfs.getfeature=4
ows.wps.execute=2
user=8
timeout=30
```
(limites **par réplica** ; une requête qui attend plus de `timeout` s reçoit un refus propre au
lieu d'un 502). Au démarrage, une ligne `Loaded control-flow rule: …` par règle. Calibrer sur
le CPU et la mesure ; alléger aussi le rendu lui-même (voir
[../sld/idw-sur-grille-dense](../sld/idw-sur-grille-dense.md)).

## Versions concernées
GeoServer 2.28 (vécu) ; extension documentée sur les versions courantes.

## Source
- https://docs.geoserver.org/latest/en/user/extensions/controlflow/index.html
- vécu 2026-05-12 (GeoServer 2.28, 3 réplicas sur processeur quatre cœurs).

## Statut
prouvé
