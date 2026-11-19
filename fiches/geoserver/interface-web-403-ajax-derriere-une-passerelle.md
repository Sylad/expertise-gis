# Interface web derrière une passerelle : 403 sur chaque action Ajax (protection CSRF de Wicket)

## Symptôme
La page Couches de l'interface web s'affiche, mais chaque action Ajax (page 2 du tableau,
repli d'un espace de travail) répond `403 (Forbidden)`. Journal d'accès :
`GET /geoserver/web/wicket/bookmarkable/…LayerPage?2-1.0-table-navigatorBottom-…  403`.
Le même chemin par `http://localhost` (redirection de port) fonctionne. Le 403 tombe sur
chaque réplica.

## Cause
La protection CSRF de Wicket, posée par GeoServer : `ResourceIsolationRequestCycleListener`
avec `FetchMetadataResourceIsolationPolicy` puis `OriginResourceIsolationPolicy`
(`GeoServerApplication.java:312-321`).
1. Chrome n'envoie les en-têtes `Sec-Fetch-*` qu'aux origines « potentially trustworthy »
   (https ou localhost). Sur une adresse IP en http, ils manquent et la politique Fetch
   Metadata rend `UNKNOWN` (`FetchMetadataResourceIsolationPolicy.java:95-99`).
2. La politique Origin compare alors l'`Origin` / le `Referer` à `request.getRequestURL()`
   vue par Tomcat. Si la passerelle envoie `Host` = l'adresse de l'amont et que la
   `RemoteIpValve` n'a ni `hostHeader` ni `portHeader`, l'URL vue est celle du Service
   interne : `DISALLOWED`, et l'action par défaut est `ABORT` avec le code 403
   (`ResourceIsolationRequestCycleListener.java:134-146`).

Preuve par `curl` (notes) : Ajax GET sans en-tête → 403 ; `Referer` = URL interne → 200 ;
`Sec-Fetch-Site: same-origin` seul → 200.

## Détection
À travers la passerelle, avec le cookie de session :
`curl -s -o /dev/null -w '%{http_code}\n' -b 'JSESSIONID=<id>' -H 'Wicket-Ajax: true' -H 'Referer: <origine de la passerelle>/geoserver/web/' '<origine de la passerelle>/geoserver/web/?0-1.0-…'`
sans aucun en-tête `Sec-Fetch-*` : `403` = piège ; après le geste, `200`.

## Geste
- Court terme : `-DGEOSERVER_CSRF_WHITELIST=<hôtes de la passerelle>`, hôte seul, sans
  schéma ni port (comparé au nom d'hôte de l'origine, sous-domaines compris :
  `OriginResourceIsolationPolicy.java:264-278`).
- Durable : `RemoteIpValve` avec `hostHeader="X-Forwarded-Host"` (et `portHeader`), ou une
  passerelle qui conserve `Host` : Tomcat voit alors l'URL publique.
- Contournement : `http://localhost` par redirection de port, ou
  `chrome://flags/#unsafely-treat-insecure-origin-as-secure` pour l'adresse de la passerelle.
- Ce qui n'y est pour rien : Hazelcast, les sessions et l'affinité (403 sur chaque réplica).
  Les messages « Applying inline style » de `jquery.parseXML` viennent de la CSP stricte à
  nonces de 3.0.2 (`GeoServerApplication.java:109,268-269`) et ne cassent rien ;
  `-Dorg.geoserver.web.csp.strict=false` les passe en simple rapport.

Cette fiche prouve les pistes notées « non appliquées » au point 7 de
[montee-2-28-3-a-3-0-2](montee-2-28-3-a-3-0-2.md).

## Versions concernées
GeoServer 3.0.2 / Wicket 10.11.0 (vécu, rapporté par les notes de dépannage reçues le
2026-11-19, preuve par `curl` ; code relu ici le 2026-11-19 aux tags `3.0.2` et
`rel/wicket-10.11.0`, lignes à ±1 de celles des notes). Chrome (comportement des
`Sec-Fetch-*`) ; autres navigateurs non vérifiés.

## Source
- https://github.com/geoserver/geoserver/blob/3.0.2/src/web/core/src/main/java/org/geoserver/web/GeoServerApplication.java#L312-L321
- https://github.com/apache/wicket/blob/rel/wicket-10.11.0/wicket-core/src/main/java/org/apache/wicket/protocol/http/FetchMetadataResourceIsolationPolicy.java#L95-L99
- https://github.com/apache/wicket/blob/rel/wicket-10.11.0/wicket-core/src/main/java/org/apache/wicket/protocol/http/ResourceIsolationRequestCycleListener.java#L134-L146
- https://github.com/apache/wicket/blob/rel/wicket-10.11.0/wicket-core/src/main/java/org/apache/wicket/protocol/http/OriginResourceIsolationPolicy.java#L264-L278
- https://developer.mozilla.org/en-US/docs/Glossary/Fetch_metadata_request_header
- Notes de dépannage d'un autre compte, cas « G4 », reçues le 2026-11-19.

## Statut
prouvé
