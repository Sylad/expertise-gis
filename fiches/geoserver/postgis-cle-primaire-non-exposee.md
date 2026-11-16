# Clé primaire non exposée : « Illegal property name » sur un filtre

## Symptôme
`CQL_FILTER=<col>='…'` sur une couche PostGIS répond 400
`Illegal property name: <col> for feature type <ws>:<couche>`, seulement pour certaines tables
(celles dont la colonne fait partie de la clé primaire). `DescribeFeatureType` n'a pas la colonne.

## Cause
Le paramètre de connexion du magasin PostGIS **`Expose primary keys`** vaut `false` par défaut :
les colonnes de la clé primaire ne sont pas des attributs, elles servent seulement à fabriquer
l'identifiant d'entité (`table.<v1>.<v2>`). Le réglage se perd quand on recrée le magasin sans lui.

## Détection
```bash
curl -s -u "$AUTH" "$GS/rest/workspaces/<ws>/datastores/<ds>.xml" | grep -i "Expose primary keys"
```
Absent ou `false` + colonne de clé absente du `DescribeFeatureType`.

## Geste
Ajouter `<entry key="Expose primary keys">true</entry>` aux `connectionParameters` (PUT du
magasin), puis `POST /rest/reload` et recalculer les attributs de chaque type (corps
`<featureType><attributes></attributes></featureType>` en `PUT …/featuretypes/<ft>?recalculate=`,
voir [featuretype-schema-perime-apres-alter](featuretype-schema-perime-apres-alter.md)). Le mettre dans tout amorçage déclaratif
des magasins, avec `validate connections=true` et `Loose bbox=true`.

## Versions concernées
GeoServer 2.28 (vécu) ; paramètre documenté sur les versions courantes.

## Source
- https://docs.geoserver.org/latest/en/user/data/database/postgis.html (option « Expose primary keys »)
- vécu 2026-05-17 (GeoServer 2.28.3, magasin recréé lors d'un passage du catalogue en base).

## Statut
prouvé
