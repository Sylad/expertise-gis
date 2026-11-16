# Magasin de tuiles « par défaut » déclaré mais pas utilisé

## Symptôme
Un BlobStore S3 est déclaré et actif, pourtant le cache disque local du data dir continue de
grossir ; une partie des couches tuilées écrit encore en local.

## Cause
Chaque couche tuilée a son `blobStoreId` ; une couche sans `blobStoreId` utilise le magasin
marqué `default`. Constaté : un amorçage qui réenvoyait le magasin avec `default="false"`
après qu'un autre composant l'avait mis à `true`, et une assignation par liste de couches
écrite en dur qui ne couvrait pas les nouvelles.

## Détection
```bash
curl -s -u "$AUTH" "$GS/gwc/rest/blobstores/<nom>.xml" | grep -o 'default="[a-z]*"'
curl -s -u "$AUTH" "$GS/gwc/rest/layers/<ws>:<couche>.xml" | grep blobStoreId
```
Preuve d'usage réel : deux GetMap tuilés (MISS puis HIT) sur une couche non assignée, et le
nombre de fichiers du cache local de cette couche **inchangé**.

## Geste
Un seul composant déclare le magasin et son drapeau `default` ; pas de liste de couches en dur.
Pour corriger à chaud : `GET` du XML du magasin, modification, `PUT` du même XML. Puis purger le
cache local devenu orphelin, par un job qui échoue bruyamment s'il ne supprime rien (droits du
conteneur : GeoServer écrit souvent en root avec des dossiers en 0750).

## Versions concernées
GeoServer 3.0.1 / GWC 2.0.1 (vécu).

## Source
vécu 2026-09-17 (GeoServer 3.0.1, 3 réplicas, BlobStore S3 compatible ; 57 couches tuilées sur 75 écrivaient encore en local).

## Statut
prouvé
