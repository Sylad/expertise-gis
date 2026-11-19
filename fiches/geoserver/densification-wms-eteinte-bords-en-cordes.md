# Densification du WMS éteinte : bords de polygones en cordes en Lambert ou polaire, parfois en double

## Symptôme
En EPSG:3034 (Lambert conique) ou EPSG:3995 (polaire), un bord de polygone qui suit un
parallèle est dessiné en segment droit (corde) au lieu d'une courbe ; deux polygones voisins
d'une couche PostGIS tracent deux traits différents pour la même frontière. Mesuré : 18 à
26 px d'écart moyen au parallèle à 45° N, à 0,79 km/px.

## Cause
Le rendu reprojette les seuls sommets ; la densification automatique du WMS est éteinte par
défaut (`WMS.java:218-221`, `ENABLE_ADVANCED_PROJECTION_DENSIFICATION = false`, clé
`advancedProjectionDensification`). Pour les traits en double : la simplification à la volée
du magasin retire les sommets alignés en EPSG:4326, pas les mêmes pour chaque polygone.
Preuve (notes) : même GetMap avec
`FORMAT_OPTIONS=advancedProjectionHandlingDensification:true` → écart 0 px.

## Détection
GetMap de la zone en EPSG:3034, sans puis avec
`FORMAT_OPTIONS=advancedProjectionHandlingDensification:true` : images différentes = piège.
Une fois le geste fait, l'image sans paramètre est égale à l'image avec, et l'écart au
parallèle calculé est < 2 px. Comparer sur les mêmes réplicas chauds : un réplica
fraîchement démarré est plus lent (compilation JIT).

## Geste
- Activer la densification dans le WMS **global** : case « Enable automatic densification
  of geometries » de la page WMS (doc `webadmin.md:118`), qui écrit l'entrée
  `advancedProjectionDensification=true` dans la metadata du service. Aucun réglage par
  couche ; un WMS d'espace de travail n'est lu que par `/geoserver/<ws>/wms`.
- Coût mesuré (réplicas chauds, médiane de 15) : fond de 800 px en 3995 +0,13 à +0,19 s,
  en 3034 +0,03 s ; première tuile GWC aux niveaux 2–3 environ deux fois plus longue.
- La densification ne règle pas les fentes venues des données découpées :
  [st-subdivide-fentes-blanches-apres-reprojection](../postgis/st-subdivide-fentes-blanches-apres-reprojection.md).

Le format option n'est pas dans la page des paramètres vendeur du WMS (`vendor.md` ne cite
que `advancedProjectionHandling` et `mapWrapping`) : seulement `webadmin.md:120` et le code.

## Versions concernées
GeoServer 3.0.2 / GeoTools 35.2 (vécu et mesuré, rapporté par les notes de dépannage reçues
le 2026-11-19 ; code et doc relus ici le 2026-11-19 au tag `3.0.2`).

## Source
- https://github.com/geoserver/geoserver/blob/3.0.2/src/wms-core/src/main/java/org/geoserver/wms/WMS.java#L218-L221
- https://github.com/geoserver/geoserver/blob/3.0.2/doc/en/user/services/wms/webadmin.md?plain=1#L118-L120
- https://github.com/geoserver/geoserver/blob/3.0.2/doc/en/user/services/wms/vendor.md
- Notes de dépannage d'un autre compte, cas « G6 », reçues le 2026-11-19.

## Statut
prouvé
