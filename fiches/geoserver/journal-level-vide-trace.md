# Niveau de journal vide : flot de TRACE et GeoServer ralenti

## Symptôme
Des dizaines de milliers de lignes `TRACE`/`DEBUG` (par exemple `jdbcconfig.internal`) par
pod et par quelques minutes ; requêtes plus lentes.

## Cause
La configuration de journalisation du catalogue a un `level` vide (par exemple après
migration du catalogue, ou un `PUT /rest/logging` sans `<level>`) : le profil le plus bavard
s'applique.

## Détection
```bash
curl -s -u "$AUTH" "$GS/rest/logging.xml"     # <level> absent ou vide
```

## Geste
`PUT /rest/logging` avec `<logging><level>PRODUCTION_LOGGING.xml</level>…</logging>` **sur
chaque réplica** (adresse du pod, ou `kubectl port-forward pod/<pod>`, pas le Service) :
l'événement de catalogue ne reconfigure pas la journalisation des autres nœuds. Vérifier
`/rest/logging` après toute migration de catalogue.

## Versions concernées
GeoServer 3.0.1, 3 réplicas en grappe (vécu).

## Source
vécu 2026-09-22 (GeoServer 3.0.1, jdbcconfig, ~30 000 lignes TRACE par pod en 5 min).

## Statut
prouvé
