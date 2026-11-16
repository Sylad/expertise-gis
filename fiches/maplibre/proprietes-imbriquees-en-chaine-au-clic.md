# Au clic, les propriétés imbriquées d'une entité GeoJSON arrivent en chaîne JSON

## Symptôme
La fiche au clic plante sur une propriété tableau ou objet de l'entité :
`TypeError: x.map is not a function`, ou affiche `[{"a":1}]` littéralement. Les tests
passent (ils lisent l'entité d'origine) ; seule la vraie carte casse. Les propriétés à
`null` ont en plus disparu.

## Cause
Les entités renvoyées par `queryRenderedFeatures` et les événements de clic ne sont pas les
objets GeoJSON fournis : elles sont relues depuis les tuiles vecteur que MapLibre fabrique à
partir de la source GeoJSON. Ce format ne stocke que des valeurs simples : un objet ou un
tableau y est écrit en chaîne JSON, un `null` n'est pas écrit. Mécanisme observé ; le code
d'encodage (`writeProperties` de vt-pbf) n'a pas été relu.

## Détection
Dans le gestionnaire de clic : `typeof e.features[0].properties.maPropriete` vaut
`'string'` pour une propriété qui est un tableau dans la donnée d'origine.

## Geste
- Ne lire depuis l'entité cliquée que l'identifiant (`promoteId` ou `id`) et retrouver
  l'objet d'origine dans les données de l'application ;
- ou, à défaut, `JSON.parse` défensif des propriétés de type chaîne attendues structurées,
  et une valeur par défaut pour les clés absentes (anciens `null`).
- Un test de bout en bout qui clique réellement sur la carte, pas seulement un test de la
  fonction de fiche.

## Versions concernées
MapLibre GL JS 5 (vécu) ; MapLibre GL JS 6 non vérifié.

## Source
- vécu 2026-10-14 (MapLibre GL JS 5, source GeoJSON, fiche au clic en production).
- https://maplibre.org/maplibre-gl-js/docs/API/classes/Map/ (`queryRenderedFeatures`)

## Statut
à reprouver : mécanisme d'encodage non relu dans le code, version 6 non vérifiée
