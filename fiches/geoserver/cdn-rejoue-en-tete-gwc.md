# Un CDN rejoue l'en-tête GeoWebCache : faux « MISS » permanent

## Symptôme
Un test de cache conclut que GeoWebCache ne sert jamais depuis son cache : la même tuile
demandée deux fois répond `geowebcache-cache-result: MISS`, alors que l'origine fonctionne.

## Cause
Le CDN a mis en cache la **première** réponse de l'origine, en-têtes compris (un MISS à froid
légitime), et la rejoue telle quelle : `cf-cache-status: HIT` mais
`geowebcache-cache-result: MISS` figé.

## Détection
- `cf-cache-status: HIT` (ou équivalent) ⇒ l'en-tête GWC est périmé, non concluant.
- Contourner le CDN : interroger l'origine directement (port-forward, IP du pod), ou ajouter
  un paramètre inconnu de la tuile (`&_bust=<n>`) : il change la clé du CDN sans changer la
  clé de tuile GWC **si** ce paramètre n'est pas déclaré dans les `parameterFilters` de la
  couche. Attendu : MISS puis HIT à l'origine.

## Geste
Tout test d'efficacité GWC se fait à l'origine, ou avec un paramètre de contournement non
filtré ; ne jamais conclure sur un en-tête GWC lu à travers un CDN qui répond HIT.

## Versions concernées
GeoServer 3.0.1 / GWC 2.0.1 (vécu) ; indépendant de la version.

## Source
vécu 2026-09-08 (GeoServer 3.0.1, 3 réplicas, cache de tuiles S3 partagé, Cloudflare devant).

## Statut
prouvé
