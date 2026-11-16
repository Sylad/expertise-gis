# Lire un SLD par REST sans raw=true : faux « réglage non appliqué »

## Symptôme
Après publication d'un style, `GET /rest/workspaces/<ws>/styles/<s>.sld` ne contient pas un
élément pourtant envoyé (par exemple `ChannelSelection`) : on croit que la publication n'a
pas pris.

## Cause
Sans `raw=true`, GeoServer **ré-encode** le style à partir de son modèle objet : l'encodeur
omet ou réordonne certains éléments. Le corps stocké n'est rendu tel quel qu'avec `?raw=true`.

## Détection
```bash
curl -s -u "$AUTH" "$GS/rest/workspaces/<ws>/styles/<s>.sld"          > reencode.sld
curl -s -u "$AUTH" "$GS/rest/workspaces/<ws>/styles/<s>.sld?raw=true" > stocke.sld
diff <(xmllint --format reencode.sld) <(xmllint --format stocke.sld)
```

## Geste
Comparer la source versionnée au corps lu avec `?raw=true` (comparaison octet à octet pour
un amorçage idempotent). Vérifier l'effet par un GetMap, pas par la relecture du SLD.
Voir aussi [../sld/ordre-des-elements-rastersymbolizer](../sld/ordre-des-elements-rastersymbolizer.md).

## Versions concernées
GeoServer 3.0.1 (vécu).

## Source
- vécu 2026-09-10 (GeoServer 3.0.1).
- https://docs.geoserver.org/latest/en/api/#1.0.0/styles.yaml (paramètre `raw`).

## Statut
prouvé
