# Image Docker officielle : EXTRA_JAVA_OPTS ramène le tas à 1 Go

## Symptôme
GeoServer tombe en `OutOfMemoryError` sur des requêtes ordinaires (WFS de quelques milliers
d'entités, rendu avec transformation) alors que `JAVA_OPTS=-Xmx6g` est posé ; le vidage de
tas fait ~1,1 Go au lieu de ~6 Go ; redémarrages à répétition.

## Cause
L'image `docker.osgeo.org/geoserver` définit `EXTRA_JAVA_OPTS=-Xms256m -Xmx1g` et l'ajoute à
`CATALINA_OPTS`. Tomcat lance `java $JAVA_OPTS $CATALINA_OPTS …` : le **dernier** `-Xmx` de la
ligne de commande l'emporte, donc 1 Go.

## Détection
```bash
cat /proc/1/cmdline | tr '\0' ' ' | grep -oE 'Xm[sx][0-9]+[gm]'
```
Plusieurs `-Xmx` ⇒ piège présent ; il n'en faut qu'un, à la valeur voulue.

## Geste
Fixer `EXTRA_JAVA_OPTS` avec la même taille de tas que `JAVA_OPTS` (ou y mettre toute la
config mémoire), puis relire la ligne de commande du processus. Dimensionner la limite
mémoire du conteneur : voir [jvm-limite-memoire-conteneur](jvm-limite-memoire-conteneur.md).

## Versions concernées
Image `docker.osgeo.org/geoserver` 2.28.x (vécu) ; image 3.x non vérifiée.

## Source
vécu 2026-05-15 (image officielle 2.28.x sous Kubernetes, 5 redémarrages en 2 h).

## Statut
à reprouver — établi sur l'image 2.28.
