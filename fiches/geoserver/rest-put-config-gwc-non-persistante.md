# Configuration GWC posée par REST perdue au redémarrage

## Symptôme
Un magasin de tuiles (BlobStore S3) ou les réglages d'une couche tuilée (`blobStoreId`,
`parameterFilters`) posés par REST fonctionnent… jusqu'au redémarrage suivant, puis tout revient
au défaut (`CannotResolveClassException`, cache disque local).

## Cause
Constaté : les `PUT`/`POST` REST ont modifié l'état en mémoire sans écrire `gwc/blobstores.xml`
ni `gwc-layers/*.xml`. En 3.0.1, un `PUT /gwc/rest/blobstores/<nom>` a au contraire été suivi
par le fichier : le comportement dépend de la version et du module de stockage.

## Détection
Après le `PUT` : relire le fichier (`gwc/blobstores.xml`, `gwc-layers/<couche>.xml`) ou son
équivalent en base, puis redémarrer un pod et relire `GET /gwc/rest/layers/<couche>.xml`.

## Geste
- Configuration qui doit survivre : la poser au démarrage par un module Java (`@PostConstruct`
  ou écouteur de contexte, idempotent, `BlobStoreAggregator` / `GeoServerTileLayer`) ;
  classes de modules communautaires absentes de Maven Central chargées par réflexion avec
  repli journalisé.
- REST reste bon pour les gestes ponctuels (purge, amorçage de cache).
- Dans tous les cas, prouver la persistance par un redémarrage.

## Versions concernées
GeoServer 2.28 (non persistant, vécu) ; GeoServer 3.0.1 / GWC 2.0.1 (persistant pour un
BlobStore, vécu).

## Source
vécu 2026-05-24 (GeoServer 2.28) ; vécu 2026-09-17 (GeoServer 3.0.1).

## Statut
à reprouver — résultats contraires selon la version.
