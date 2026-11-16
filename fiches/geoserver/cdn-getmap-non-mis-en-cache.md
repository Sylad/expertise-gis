# Tuiles WMS jamais mises en cache par le CDN (DYNAMIC)

## Symptôme
Derrière Cloudflare, chaque tuile GetMap remonte à l'origine : en-tête
`cf-cache-status: DYNAMIC`, alors que GeoServer envoie un `Cache-Control: max-age`.

## Cause
Par défaut Cloudflare ne met pas en cache une URL sans extension de fichier statique et
avec chaîne de requête (cas de tout `…/wms?SERVICE=WMS&REQUEST=GetMap…`) : il faut une
règle de cache explicite.

## Détection
```bash
curl -s -D - -o /dev/null '<url de tuile>' | grep -iE 'cf-cache-status|age|cache-control'
```
Deux appels : `DYNAMIC` = pas de cache ; `MISS` puis `HIT` avec `age` qui monte = cache actif.

## Geste
- Règle de cache (Caching → Cache Rules) ciblant seulement les GetMap : chemin finissant par
  `/wms` et requête contenant `GetMap` (pas les capabilities, pas l'authentification, pas REST).
- Éligible au cache ; TTL d'arête « utiliser Cache-Control si présent, sinon ne pas mettre en
  cache » (évite de figer une réponse sans en-tête).
- Clé de cache par défaut (chaîne de requête complète) : chaque `TIME`, `BBOX`, `LAYERS`
  est une entrée distincte.
- Risque : une erreur WMS arrive en HTTP 200 (voir
  [erreur-wms-http-200-en-xml](erreur-wms-http-200-en-xml.md)) et peut être cachée ;
  purger le cache si une tuile fausse persiste. Voir aussi
  [cdn-rejoue-en-tete-gwc](cdn-rejoue-en-tete-gwc.md).

## Versions concernées
Indépendant de la version GeoServer ; interface Cloudflare de juin 2026.

## Source
- vécu 2026-06-17 (GeoServer 2.28 derrière un tunnel Cloudflare ; `DYNAMIC` avant, `MISS` puis `HIT` après la règle).
- https://developers.cloudflare.com/cache/how-to/cache-rules/

## Statut
prouvé
