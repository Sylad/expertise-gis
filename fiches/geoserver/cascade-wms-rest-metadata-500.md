# REST : modifier les métadonnées d'une couche en cascade répond 500

## Symptôme
`PUT /rest/workspaces/<ws>/wmsstores/<store>/wmslayers/<couche>` avec des `metadata`
(par exemple une `dimensionInfo` de temps) répond HTTP 500 :
`java.lang.UnsupportedOperationException` — `class: org.geoserver.catalog.impl.WMSLayerInfoImpl`,
`converter-type: …XStreamPersister$WMSLayerInfoConverter`. En XML comme en JSON.

## Cause
Le convertisseur XStream de `WMSLayerInfo` ne gère pas cette mise à jour. Une écriture SQL
directe du blob dans le catalogue en base n'est pas lue non plus (aucun effet, en silence).

## Détection
Le corps de la réponse 500 cite `WMSLayerInfoConverter`.

## Geste
- Créer la couche en cascade par un `POST` minimal (`name`, `nativeName`, `title`, `enabled`,
  `advertised`), sans `metadata`.
- Pour une configuration plus riche : interface web (non reproductible) ou module Java au
  démarrage (`catalog.save(...)`).
- Ne pas écrire dans les blobs du catalogue en base.

## Versions concernées
GeoServer 2.28.3 (vécu) ; 3.x non vérifié.

## Source
vécu 2026-06-15 (GeoServer 2.28.3) ; vécu 2026-05-24 (écriture SQL du blob sans effet).

## Statut
à reprouver — établi sur 2.28.
