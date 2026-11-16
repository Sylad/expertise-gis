# Image officielle 3.x : conf/context.xml ignoré, ressource JNDI introuvable

## Symptôme
Au démarrage : `javax.naming.NameNotFoundException: Name [<nom>] is not bound`, puis les modules
(jdbcconfig, jdbcstore…) se replient sur leur URL par défaut
(`jdbc:postgresql://localhost:5432/…`).

## Cause
Le `server.xml` de l'image déclare le contexte de l'application avec
`<Context override="true" docBase="geoserver" …>` : le `conf/context.xml` global est ignoré,
et une `<Resource>` qu'on y ajoute n'existe pas.

## Détection
`grep -n 'override="true"' /opt/config/server.xml` dans le conteneur ; la ressource n'apparaît
pas dans ce `<Context>`.

## Geste
Fournir un `server.xml` complet dans `/opt/config_overrides/server.xml` (copie du modèle de
l'image + les `<Resource>` voulues). Le script de démarrage l'installe en passant **tout le
fichier** par `envsubst` : n'y mettre que des `${VAR}` qui sont des variables d'environnement
exportées. Les modules jdbcconfig/jdbcstore acceptent `jndiName=java:comp/env/jdbc/<nom>` dans
leurs `.properties` ; un magasin PostGIS, `jndiReferenceName=java:comp/env/jdbc/<nom>`.
Le pilote PostgreSQL est déjà dans `$CATALINA_HOME/lib`.

## Versions concernées
Image `docker.osgeo.org/geoserver:3.0.1` (Tomcat 11, JDK 21) (vécu).

## Source
vécu 2026-09-01 (construction d'une image dérivée de `docker.osgeo.org/geoserver:3.0.1`).

## Statut
prouvé
