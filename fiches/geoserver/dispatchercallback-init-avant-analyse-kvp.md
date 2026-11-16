# DispatcherCallback.init : service et requête encore nuls

## Symptôme
Un `DispatcherCallback` maison qui filtre sur le service (`"WMS".equals(request.getService())`)
dans `init()` ne fait jamais rien : la condition est toujours fausse.

## Cause
`init(Request)` est appelé en tout premier, **avant** l'analyse des paramètres KVP :
`getService()` et `getRequest()` sont `null`. L'ordre : `init` → `serviceDispatched` →
`operationDispatched` (KVP analysés) → `operationExecuted` → `finished`.

## Détection
Journal inconditionnel dans `init()` : `service=null request=null`.

## Geste
Lire les paramètres dans `operationDispatched(Request, Operation)` (`getRawKvp()` rempli) ;
réserver `init()` à des remises à zéro défensives (par exemple vider un `ThreadLocal`), et
`finished()` au nettoyage.

## Versions concernées
GeoServer 2.28 (vécu) ; 3.x non vérifié.

## Source
- vécu 2026-05-26 (GeoServer 2.28, 4 h de diagnostic).
- Code source : `org.geoserver.ows.Dispatcher`, `org.geoserver.ows.DispatcherCallback` (https://github.com/geoserver/geoserver).

## Statut
à reprouver — établi sur 2.28.
