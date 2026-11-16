# Désactiver la grappe Hazelcast par enabled=false fait tomber l'application

## Symptôme
Après avoir voulu couper la grappe (`enabled=false`), GeoServer ne démarre plus :
`IllegalStateException: Hazelcast Clustering has not been enabled` à l'initialisation du
contexte ; ou démarrage interminable (« cluster not initialized ») parce que la découverte
Kubernetes reste active sans droit de lister les pods.

## Cause
Les jars du module (`gs-hz-cluster-*`, `hazelcast-*`) sont toujours dans `WEB-INF/lib` ;
cette version du module lève une exception si elle est présente sans grappe active. La
configuration persistée (`cluster/cluster.properties`, `hazelcast.xml`) dans le volume survit
au retrait d'un montage ; si le fichier est absent, le module en recrée un avec `enabled=true`.

## Détection
`ls WEB-INF/lib | grep -i hazelcast` ; `cat $GEOSERVER_DATA_DIR/cluster/cluster.properties`.

## Geste
Pour désactiver le module : **retirer ses jars** au démarrage (script d'amorçage, idempotent)
et laisser le fichier avec `enabled=false` (ne pas le supprimer). Pour le réactiver : remettre
les jars et les droits de découverte.

## Versions concernées
GeoServer 2.28 (vécu) ; 3.x non vérifié.

## Source
vécu 2026-08-15 (GeoServer 2.28, Kubernetes, démarrage de 42 min au-delà de la sonde).

## Statut
à reprouver — établi sur 2.28.
