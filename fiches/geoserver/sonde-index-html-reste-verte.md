# Sonde de vie sur /geoserver/index.html : verte alors que GeoServer est figé

## Symptôme
Un pod GeoServer ne répond plus aux requêtes OWS ni à l'interface, mais reste `Running` et
prêt, 0 redémarrage. Juste après un déploiement, des GetMap échouent en 500 alors que tous les
pods sont « Ready ».

## Cause
`/geoserver/index.html` est une page statique servie par Tomcat : elle répond 200 même quand
le dispatcher de GeoServer est bloqué ou que le catalogue n'a pas fini de converger.
(Pour mémoire : `/geoserver/` et `/geoserver/web` répondent 302, `/geoserver/web/index.html` 404.)

## Détection
Depuis un autre pod, avec un délai : `curl --max-time 10` sur GetCapabilities du pod suspect.

## Geste
- Sondes de démarrage, vie et disponibilité sur une requête qui traverse GeoServer, par
  exemple `GET /geoserver/<ws>/ows?service=WMS&version=1.3.0&request=GetCapabilities` (léger,
  sans authentification).
- Budget de la sonde de démarrage large (premier démarrage avec catalogue en base : minutes).
- Tout client automatique (amorçage, préchauffage) porte `--connect-timeout` et `--max-time` :
  un `curl` sans délai sur un pod figé bloque indéfiniment le job.
- Après un déploiement, attendre quelques minutes après le dernier pod prêt avant de conclure
  à une régression ; relancer avant de conclure.

## Versions concernées
GeoServer 2.28 et 3.0.1 (vécu).

## Source
vécu 2026-09-09 et 2026-09-10 (GeoServer 3.0.1, 3 réplicas) ; vécu 2026-05-14 (GeoServer 2.28.3, tableau des chemins).

## Statut
prouvé
