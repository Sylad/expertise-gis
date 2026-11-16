# jdbcconfig : le fichier .properties du data dir l'emporte sur les variables d'environnement

## Symptôme
Après déplacement d'un data dir (nouvel hôte, nouvelle base), GeoServer se connecte toujours
à l'ancienne base (ancien nom d'hôte) malgré les variables d'environnement `GEOSERVER_JDBCCONFIG_*`
injectées ; ou, sur un volume neuf, il démarre en mode fichiers avec `localhost`.

## Cause
Les modules lisent d'abord `jdbcconfig/jdbcconfig.properties` et `jdbcstore/jdbcstore.properties`
du data dir ; les variables ne servent que si le fichier est absent. Sur un volume neuf, l'image
écrit un fichier par défaut (`enabled=false`, `localhost`).

## Détection
`cat $GEOSERVER_DATA_DIR/jdbcconfig/jdbcconfig.properties` : hôte, base et `enabled`.

## Geste
Réécrire **entièrement** ces fichiers à chaque démarrage depuis la configuration déclarée
(conteneur d'initialisation ou script d'amorçage), plutôt que de compter sur les variables.
Avant le premier démarrage, créer le schéma cible (sinon `no schema has been selected`).

## Versions concernées
GeoServer 2.28 (vécu) ; 3.x non vérifié.

## Source
vécu 2026-05-14 (GeoServer 2.28.3, déplacement d'un data dir de Docker vers Kubernetes) ; vécu 2026-05-15 (volume neuf).

## Statut
à reprouver — établi sur 2.28.
