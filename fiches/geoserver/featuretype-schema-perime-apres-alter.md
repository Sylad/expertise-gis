# Table modifiée sous une couche publiée : « column … does not exist »

## Symptôme
Après un `ALTER TABLE` ou un `DROP`/`CREATE` de la table sous une couche vecteur, le WFS ou
le WMS répond 400 : `org.postgresql.util.PSQLException: ERROR: column "<ancienne>" does not exist`.

## Cause
GeoServer garde en cache le schéma d'attributs du type d'entités relevé à la publication et
continue de générer le SQL avec les anciennes colonnes.

## Détection
`DescribeFeatureType` de la couche liste encore l'ancienne colonne ; la table, elle, ne l'a plus.

## Geste
Recharger le schéma sans republier (on garderait styles et réglages) :
```bash
curl -s -u "$AUTH" -X PUT "$GS/rest/workspaces/<ws>/datastores/<ds>/featuretypes/<ft>/reset"
```
Si la liste d'attributs reste figée : `PUT` du featureType avec un corps
`<featureType><attributes></attributes></featureType>` sur `…/featuretypes/<ft>?recalculate=`
(liste vidée, relue depuis la table). À automatiser dans tout outil qui modifie un schéma publié.

## Versions concernées
GeoServer 2.28 (vécu) ; 3.x non vérifié.

## Source
- vécu consigné le 2026-05-11 (GeoServer 2.28, table recréée avec d'autres colonnes).
- https://docs.geoserver.org/latest/en/api/#1.0.0/featuretypes.yaml

## Statut
à reprouver — établi sur 2.28.
