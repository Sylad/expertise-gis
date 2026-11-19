# Fentes blanches dans le fond de carte en Lambert ou polaire : chercher d'abord côté serveur

## Symptôme
Vue OpenLayers en EPSG:3034 (Lambert conique) ou EPSG:3995 (polaire) : fentes ou coins blancs
dans le fond de carte WMS, entre océan et terre. En EPSG:4326 ou EPSG:3857, rien.

## Cause
Quand la source demande l'image au WMS dans le CRS de la vue (`ImageWMS` non tuilé sans
`projection`, ou `projection` égale à la vue : `CRS=` code de la vue), le navigateur ne
reprojette aucun pixel : il affiche l'image telle que le serveur l'a rendue. Le défaut est
donc dans l'image servie, par exemple des polygones découpés sans densification
([st-subdivide-fentes-blanches-apres-reprojection](../postgis/st-subdivide-fentes-blanches-apres-reprojection.md)).
Le mécanisme (projection égale ou absente = aucune reprojection client) est relu dans le
code : [source-wms-projection-de-la-vue](source-wms-projection-de-la-vue.md).

À l'inverse, une source WMTS sur une grille EPSG:900913 posée sur une vue 3034 est, elle,
reprojetée dans le navigateur (`ol/reproj`) : là, le client peut être en cause. Même chose
pour une source XYZ (déduction, les notes ne parlent que de WMTS).

## Détection
Dans l'onglet réseau, relever le GetMap (vérifier `CRS=` = code de la vue), puis le refaire
hors de l'application (`curl … -o image.png`) et regarder l'image : si elle a les fentes, ce
n'est pas le client.

## Geste
Corriger côté serveur ou côté données (fiche ci-dessus) ; ne rien changer au client. Preuve
d'effet : le GetMap rejoué hors de l'application est propre, et la carte aussi.

## Versions concernées
OpenLayers 10.11.0 (vécu, `ImageWMS` en vue 3034 et 3995, rapporté par les notes de
dépannage reçues le 2026-11-19), proj4 2.22.0.

## Source
- Notes de dépannage d'un autre compte, cas « O1 », reçues le 2026-11-19.
- https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/source/Image.js#L225-L237

## Statut
prouvé
