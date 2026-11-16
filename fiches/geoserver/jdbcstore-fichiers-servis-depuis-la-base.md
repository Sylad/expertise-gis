# jdbcstore : modifier un fichier du data dir n'a aucun effet

## Symptôme
On corrige un fichier du data dir (`gwc/geowebcache.xml`, un SLD, un gabarit) dans le volume ;
GeoServer continue de se comporter comme avant, même après redémarrage.

## Cause
Le module **jdbcstore** sert le contenu des ressources (fichiers du data dir hors `ignoreDirs`)
depuis la base (table des ressources). Le fichier du volume n'est pas lu.

## Détection
Comparer le fichier du volume et la ressource servie :
`GET /rest/resource/<chemin>` (contenu servi) contre `cat $GEOSERVER_DATA_DIR/<chemin>`.

## Geste
Écrire par l'API de ressources (`PUT /rest/resource/<chemin>`) ou, dans un module Java, par
`catalog.getResourceLoader().get(path).out()` : le contenu est alors partagé par tous les
réplicas. Mettre dans `ignoreDirs` ce qui doit rester local et lisible sur disque (par exemple
`cluster`, voir [grappe-hazelcast-config-et-jdbcstore](grappe-hazelcast-config-et-jdbcstore.md)).

## Versions concernées
GeoServer 2.28.3 et 3.0.1 (vécu).

## Source
vécu 2026-05-14 (GeoServer 2.28.3) ; vécu 2026-09-01 (GeoServer 3.0.1, écriture par le chargeur de ressources).

## Statut
prouvé
