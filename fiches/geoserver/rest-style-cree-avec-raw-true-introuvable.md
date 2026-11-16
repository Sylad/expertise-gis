# Style créé par REST avec raw=true : listé mais « StyleNotDefined » au rendu

## Symptôme
Le style apparaît dans `GET /rest/workspaces/<ws>/styles.xml`, son descripteur et son corps
se lisent, mais `GetMap … STYLES=<ws>:<s>` répond `StyleNotDefined: No such style`.
Ni `POST /rest/reload`, ni `POST /rest/reset`, ni un redémarrage ne corrigent.

## Cause
Constaté : le corps avait été envoyé par `PUT …/styles/<s>?raw=true`, qui stocke le flux sans
l'analyser (documenté : « forgo parsing and encoding »). L'hypothèse d'un style jamais
enregistré comme utilisable au rendu (catalogue en base, rendu lisant le disque) n'est pas
démontrée.

## Détection
GetMap avec `STYLES=<ws>:<s>` : `StyleNotDefined` alors que le style est listé.

## Geste
Séquence qui a corrigé :
```bash
# 1. entrée du catalogue
curl -u "$AUTH" -X POST -H 'Content-Type: text/xml' \
  -d '<style><name>s</name><filename>s.sld</filename></style>' "$GS/rest/workspaces/<ws>/styles"
# 2. corps, analysé (SLD 1.0 ; SE 1.1 : application/vnd.ogc.se+xml)
curl -u "$AUTH" -X PUT -H 'Content-Type: application/vnd.ogc.sld+xml' \
  --data-binary @s.sld "$GS/rest/workspaces/<ws>/styles/s"
```
Sans `raw=true`, une erreur de syntaxe revient en 400 au lieu d'un style fantôme.
Garder `raw=true` pour la **lecture** de vérification (voir
[rest-get-style-sans-raw-reencode](rest-get-style-sans-raw-reencode.md)).

## Versions concernées
GeoServer 2.28.3 avec catalogue JDBCConfig (vécu) ; 3.x non vérifié.

## Source
- vécu 2026-05-14 (GeoServer 2.28.3, 3 réplicas, catalogue JDBCConfig).
- https://docs.geoserver.org/latest/en/api/#1.0.0/styles.yaml (paramètre `raw`).

## Statut
à reprouver — vu sur 2.28 ; la cause exacte n'est pas démontrée.
