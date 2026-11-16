# ImageMosaic à index shapefile : l'heure des granules est perdue

## Symptôme
Une mosaïque temporelle à pas infra-journalier (granules toutes les 5 min, toutes les heures)
n'annonce qu'**une** validité par jour, à `00:00` ; les rendus successifs écrasent les heures.
Invisible tant que tous les granules sont à `T000000Z`.

## Cause
L'index par défaut est un shapefile : la colonne temps y est un champ DBF de type `D`
(date seule, 8 octets). L'heure est tronquée, quel que soit le `timeregex.properties`, sauf
avec l'option JVM `-Dorg.geotools.shapefile.datetime=true`.

## Détection
```bash
curl -s -u "$AUTH" "$GS/rest/workspaces/<ws>/coveragestores/<s>/coverages/<c>/index/granules.json" | jq '.features[].properties.time' | sort -u
```
Toutes les valeurs à `T00:00:00` alors que les noms de fichiers portent des heures ⇒ piège.
Le `.dbf` de l'index montre `time` de type `D`.

## Geste
Index en base : un `datastore.properties` (PostGIS) dans le dossier de la mosaïque **avant**
la création du magasin ; pour une mosaïque existante, supprimer le magasin à index shapefile et
le recréer. Faire la bascule avant tout passage à un pas horaire.

## Versions concernées
GeoServer 3.0.1 (vécu) ; documenté pour le module shapefile de GeoTools.

## Source
- vécu 2026-09-10 (GeoServer 3.0.1 : 35 granules radar → 1 validité 00:00).
- https://docs.geotools.org/latest/userguide/library/data/shape.html (dates et option `org.geotools.shapefile.datetime`).

## Statut
prouvé
