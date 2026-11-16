# `import Map from 'ol/Map'` masque le `Map` de JavaScript

## Symptôme
Dans un module qui importe la carte OpenLayers, un cache écrit `new Map()` crée… une carte
OpenLayers (sans cible) ou échoue : `cache.get is not a function`, méthodes inattendues,
erreurs de typage TypeScript sur `get`/`set`.

## Cause
Le nom importé `Map` masque le constructeur global `Map` dans toute la portée du module.

## Détection
`console.log(new Map() instanceof globalThis.Map)` dans le module : `false` signe le masquage.

## Geste
- Importer la carte sous un autre nom : `import OlMap from 'ol/Map';`
- ou, pour le cache, appeler explicitement `new globalThis.Map()`.

## Versions concernées
OpenLayers 10 (vécu) ; règle de portée du langage, toutes versions.

## Source
- https://openlayers.org/en/latest/apidoc/module-ol_Map-Map.html (export par défaut `Map`)
- vécu 2026-05 (OpenLayers 10, cache de styles d'une couche regroupée).

## Statut
prouvé
