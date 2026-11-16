# Colonne PostgreSQL JSONB servie en chaîne par le WFS GeoJSON

## Symptôme
Dans une réponse WFS `outputFormat=application/json`, une propriété issue d'une colonne
`jsonb` est une chaîne (`"{\"a\":1}"`) et non un objet ; un gabarit qui lit `props.x.a` est vide.

## Cause
Le type `jsonb` est exposé comme `String` par le magasin PostGIS ; l'encodeur GeoJSON
l'écrit donc comme une chaîne.

## Détection
`curl … outputFormat=application/json | jq '.features[0].properties.<col> | type'` → `"string"`.

## Geste
Analyser côté client (`JSON.parse` sous `try`) toute colonne `jsonb` publiée ; ou exposer
les champs utiles comme colonnes dans une vue.

## Versions concernées
GeoServer 2.28 (vécu) ; 3.x non vérifié.

## Source
vécu consigné le 2026-05-11 (GeoServer 2.28, magasin PostGIS).

## Statut
à reprouver — établi sur 2.28.
