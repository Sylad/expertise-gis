# Style par défaut déclaré mais fichier SLD absent : GetMap en erreur

## Symptôme
Un GetMap avec `STYLES=` vide échoue : `java.lang.reflect.UndeclaredThrowableException` puis
`No such resource: <style>.sld in workspace WorkspaceInfoImpl[<ws>]` (HTTP 500, ou 200 en
XML selon le chemin). Le même GetMap avec `STYLES=raster` répond une image.

## Cause
Le `StyleInfo` existe dans le catalogue (il pointe un nom de fichier) mais le fichier `.sld`
correspondant n'est pas dans les ressources (data dir perdu, volume recréé, amorçage
incomplet). Le style par défaut de la couche est utilisé dès que `STYLES` est vide. Le style
défaillant n'est pas forcément listé dans les capabilities, d'où une détection seulement par
un GetMap.

## Détection
```bash
curl -s "$GS/<ws>/wms?...&STYLES=" | head -5          # ServiceException « No such resource »
curl -s -o /dev/null -w "%{content_type}\n" "$GS/<ws>/wms?...&STYLES=raster"   # image/png
curl -s -u "$AUTH" "$GS/rest/workspaces/<ws>/styles/<style>.sld?raw=true" -o /dev/null -w "%{http_code}\n"
```

## Geste
- Immédiat : `STYLES=raster` (style générique en niveaux de gris) pour une couche raster.
- Durable : republier le corps SLD du style (REST) depuis la source versionnée, puis rejouer
  un GetMap de **chaque** couche × style servis (pas seulement la couche corrigée).

## Versions concernées
GeoServer 2.28.3 (vécu) ; GeoServer 3.x non vérifié.

## Source
vécu 2026-05-22 (GeoServer 2.28.3, catalogue en base, ressources perdues après recréation du volume).

## Statut
à reprouver — établi sur 2.28 seulement.
