# Polygones découpés par `ST_Subdivide` : fentes blanches une fois reprojetés en conique ou polaire

## Symptôme
Fond vectoriel (océan et terres de type Natural Earth `ne_10m_ocean` / `ne_10m_land`) servi
en WMS : traînées ou coins blancs entre océan et terre en EPSG:3034 (Lambert conique Europe)
ou EPSG:3995 (stéréographique polaire arctique) ; la même emprise en EPSG:4326 est propre.

## Cause
Les données, pas le serveur cartographique. Les polygones ont été découpés par
`ST_Subdivide(geom, 256)` pour accélérer le tuilage : chaque morceau reçoit des bords droits
communs avec ses voisins, qui n'ont que leurs extrémités pour sommets. Reprojetés sommet
par sommet, ces bords deviennent des cordes différentes de chaque côté, d'où une fente entre
deux morceaux (constat des notes). Explication probable, non démontrée : un même bord n'est
pas décrit par les mêmes sommets des deux côtés (un voisin redécoupé y a un sommet de plus).

Le serveur rend fidèlement les polygones qu'on lui donne : la densification à la volée du WMS
([densification-wms-eteinte-bords-en-cordes](../geoserver/densification-wms-eteinte-bords-en-cordes.md))
ne règle pas ces fentes, et, allumée, elle n'en crée pas non plus.

## Détection
- Refaire le GetMap hors de l'application, en EPSG:3034 et EPSG:3995, puis en EPSG:4326 :
  compter les pixels blancs isolés entre la couleur de l'océan et celle des terres, et
  « regarder l'image » (les notes demandent les deux). Des
  pixels en 3034 / 3995 et aucun en 4326 = piège (pour écarter le client, voir
  [fentes-en-projection-conique-chercher-cote-serveur](../openlayers/fentes-en-projection-conique-chercher-cote-serveur.md)).
- Contre-épreuve (déduction, non jouée par les notes) : la même requête sur la table non
  découpée ne montre aucune fente.

## Geste
Densifier les morceaux après la découpe (`ST_Segmentize` sur le résultat de
`ST_Subdivide`), ou découper autrement. Unité de la longueur maximale (déduction, absente
des notes) : en degrés sur une `geometry` en EPSG:4326, en mètres via `::geography`.
Preuve d'effet attendue : le même comptage de pixels blancs tombe à zéro en 3034 et 3995
(les notes donnent le geste, pas la mesure après correction).

## Versions concernées
GeoServer 3.0.2 / GeoTools 35.2 (vécu, rapporté par les notes de dépannage reçues le
2026-11-19) ; version de PostGIS non donnée par les notes. Le mécanisme (sommets seuls
reprojetés) ne dépend pas de la version.

## Source
- Notes de dépannage d'un autre compte, cas « G1 », reçues le 2026-11-19 (vécu : fentes
  mesurées en 3034 et 3995, image propre en 4326).
- https://postgis.net/docs/ST_Subdivide.html
- https://postgis.net/docs/ST_Segmentize.html

## Statut
prouvé
