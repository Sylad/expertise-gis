# Couche WMS en cascade : le paramètre TIME n'est pas transmis à l'amont

## Symptôme
Une animation sur une couche en cascade (WMS distant republié) montre la même image à
chaque instant : notre GetMap renvoie le même PNG (même md5) pour des `TIME` différents,
alors que le serveur amont, interrogé directement, renvoie des images distinctes.

## Cause
Le lecteur de cascade de GeoTools (`gt-wms` : `WMSCoverageReader`,
`WebMapServer.issueRequest()`) ne propage pas `TIME` dans la requête amont ; aucune
configuration du catalogue (dimension sur la couche) n'y remédie.

## Détection
```bash
for t in 2026-01-01T08:00:00Z 2026-01-01T10:00:00Z; do
  curl -s "$AMONT?...&LAYERS=<amont>&TIME=$t" | md5sum      # md5 distincts
  curl -s "$GS/<ws>/wms?...&LAYERS=<ws>:<cascade>&TIME=$t" | md5sum   # md5 identiques = piège
done
```

## Geste
- Sans code : ne pas proposer l'animation sur la couche en cascade (dernier instant seulement,
  sans `TIME`), ou interroger l'amont directement côté client.
- Avec code : seule voie trouvée, un module Java qui intercepte le client HTTP de la cascade
  (le cache `ResourcePool.wmsCache` remplacé par réflexion par une table qui enveloppe le client
  de chaque `WebMapServer` inséré) et réécrit l'URL amont avec le `TIME` lu dans
  `operationDispatched` (voir
  [dispatchercallback-init-service-et-requete-nuls](dispatchercallback-init-service-et-requete-nuls.md)).
  Fragile : dépend d'un champ privé.

## Versions concernées
GeoServer 2.28 (vécu) ; GeoServer 3.0.1 non vérifié sans module correctif.

## Source
- vécu 2026-05-24 (GeoServer 2.28, 5 couches en cascade : 4 instants → 1 seul md5 côté cascade).
- Code source : module `gt-wms` (https://github.com/geotools/geotools).

## Statut
à reprouver — établi sur 2.28.
