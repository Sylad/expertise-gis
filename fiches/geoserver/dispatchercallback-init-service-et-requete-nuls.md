# DispatcherCallback.init : service et requête encore nuls

## Symptôme
Un `DispatcherCallback` maison qui filtre sur le service (`"WMS".equals(request.getService())`)
dans `init()` ne fait jamais rien : la condition est toujours fausse.

## Cause
Quand `init(Request)` est appelé, les KVP bruts sont déjà analysés (`getKvp()` et
`getRawKvp()` remplis, d'après `Dispatcher` en 3.0.1), mais le service et la requête n'en sont
pas encore extraits : `getService()` et `getRequest()` sont `null`. Ils ne sont remplis que
dans l'étape de résolution du service, juste avant `serviceDispatched`. L'ordre : `init` →
`serviceDispatched` → `operationDispatched` → `operationExecuted` → `finished`.

## Détection
Journal inconditionnel dans `init()` : `service=null request=null`, alors que
`request.getKvp().get("SERVICE")` est rempli.

## Geste
Lire le service et l'opération dans `operationDispatched(Request, Operation)` ; dans `init()`,
lire au besoin `request.getKvp().get("SERVICE")` plutôt que `getService()` ;
réserver `init()` à des remises à zéro défensives (par exemple vider un `ThreadLocal`), et
`finished()` au nettoyage.

## Versions concernées
GeoServer 2.28 (vécu) ; ordre d'appel relu dans le code de 3.0.1, symptôme non rejoué en 3.x.

## Source
- vécu 2026-05-26 (GeoServer 2.28, 4 h de diagnostic).
- Code source : `org.geoserver.ows.Dispatcher`, `org.geoserver.ows.DispatcherCallback` (https://github.com/geoserver/geoserver).

## Statut
à reprouver — établi sur 2.28.
