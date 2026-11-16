# Grappe Hazelcast en sync_method=reload : chaque réplica se recharge en boucle

## Symptôme
Capabilities qui alternent entre lentes et très lentes, magasins en cascade recréés, journal
plein de `dispose()`, lecteurs ImageMosaic perdus (`rasterManagers is null`), pools de
connexions recréés — sans action humaine.

## Cause
Avec le module de grappe Hazelcast et `sync_method=reload` dans `cluster.properties`, tout
`CatalogModifyEvent` reçu provoque un `reload()` **complet** du nœud. Or un `harvest`
ImageMosaic par REST fait un `catalog.save(store)` : avec des ingestions toutes les quelques
minutes, chaque réplica recharge tout son catalogue toutes les 45–80 s.

## Détection
Corréler les horodatages des `harvest` (journal des ingesteurs) et des rechargements
(journal GeoServer) ; lire `sync_method` dans `cluster/cluster.properties`.

## Geste
`sync_method=event` (applique l'événement reçu et ne libère que le magasin touché), puis
redémarrage roulant. Effet de ce changement non encore mesuré au moment de la note.

## Versions concernées
GeoServer 3.0.1, module `gs-hz-cluster` (vécu).

## Source
- vécu 2026-09-22 (GeoServer 3.0.1, 3 réplicas ; corrélation mesurée sur 6 min).
- Code source : `ReloadHzSynchronizer`, `EventHzSynchronizer` du module de grappe Hazelcast (https://github.com/geoserver/geoserver, modules communautaires).

## Statut
à reprouver — cause mesurée, remède non encore mesuré.
