# Étiquettes absentes ou posées sur leur point au bord des métatuiles WMTS (gutter à 0)

## Symptôme
En WMTS servi par GeoWebCache (EPSG:900913, PNG), certains noms de villes manquent, ou sont
décalés jusqu'à 20 px vers l'ouest et posés sur leur point, toujours le long des colonnes ou
rangées multiples de 4 (bord d'une métatuile 4×4). La même emprise en GetMap WMS non tuilé
montre tous les noms, chacun à l'est de son point.

## Cause
La couche tuilée a `<gutter>0</gutter>` et des métatuiles 4×4. GeoTools ne peint pas une
étiquette qui dépasse l'image rendue (`LabelCacheImpl.java:1419-1422`, sauf `partials` ; doc
`labeling.md`, option `partials`) : elle est déplacée dans la limite du `maxDisplacement` du
style (20 px, angles E puis W dans le cas vécu ; recherche : `LabelCacheImpl.java:1289-1305`)
ou abandonnée, le point restant dessiné. Au bord de la métatuile, il n'y a pas de marge pour
la placer. Preuve (notes) : métatuiles voisines élargies de 100 px puis rognées → noms
présents, raccord sans couture.

## Détection
Mosaïque de tuiles WMTS de part et d'autre d'une colonne multiple de 4, comparée à une GetMap
WMS de la même emprise : mêmes noms, chacun à l'est de son point, sinon piège. Ce n'est pas
un reste de vieilles tuiles. Attention : hors bord, un nom déplacé par conflit avec un autre
est aussi posé sur son point (déplacement E, W borné à 20 px) : ne compter que les écarts
alignés sur les bords de métatuile.

En WMTS, `STYLE` doit être qualifié par l'espace de travail (`ws:style` → 200, `style` → 400),
alors que le WMS accepte les deux.

## Geste
Gutter de la couche tuilée ≥ la plus longue étiquette (≈ 100 px), puis troncature du cache
de la couche. `partials` seul couperait les noms au bord. Preuve d'effet : la comparaison de
la détection ne montre plus aucun écart.

## Versions concernées
GeoServer 3.0.2 / GeoTools 35.2 avec GeoWebCache intégré (vécu et mesuré, rapporté par les
notes de dépannage reçues le 2026-11-19 ; code relu ici le 2026-11-19 au tag GeoTools `35.2`).

## Source
- https://github.com/geotools/geotools/blob/35.2/modules/library/render/src/main/java/org/geotools/renderer/label/LabelCacheImpl.java#L1419-L1422
- https://github.com/geotools/geotools/blob/35.2/modules/library/render/src/main/java/org/geotools/renderer/label/LabelCacheImpl.java#L1289-L1305
- https://github.com/geoserver/geoserver/blob/3.0.2/doc/en/user/styling/sld/reference/labeling.md (`partials`,
  `maxDisplacement`)
- https://github.com/geoserver/geoserver/blob/3.0.2/doc/en/user/geowebcache/webadmin/defaults.md
  (métatuiles et gutter par défaut des couches tuilées)
- Notes de dépannage d'un autre compte, cas « G7 », reçues le 2026-11-19.

## Statut
prouvé
