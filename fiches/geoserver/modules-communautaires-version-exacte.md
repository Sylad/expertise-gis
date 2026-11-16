# Module communautaire (jdbcconfig, jdbcstore…) : NoClassDefFoundError au démarrage

## Symptôme
`java.lang.NoClassDefFoundError: org/geoserver/util/SortedProperties` (ou autre classe) au
démarrage après ajout d'un module communautaire ; ou téléchargement en 404 depuis la page
des extensions.

## Cause
Les modules communautaires ne sont pas publiés avec les extensions officielles
(SourceForge `/extensions/`) ; le site de construction nocturne publie des instantanés de la
branche de développement, incompatibles avec une version stable.

## Détection
Comparer la version du jar du module à celle de GeoServer (`/rest/about/version`).

## Geste
Prendre le jar de la **même version exacte** sur le dépôt Maven OSGeo :
`https://repo.osgeo.org/repository/release/org/geoserver/community/gs-<module>/<VER>/gs-<module>-<VER>.jar`,
le cuire dans l'image ; extraire au besoin les scripts SQL d'initialisation qu'il embarque.
Vérifier au démarrage (`Initialization SQL script run successfully`, aucune
`NoClassDefFoundError`). À la montée de version, mettre à jour ces jars en même temps.

## Versions concernées
GeoServer 2.28.0 à 2.28.3 (vécu) ; 3.x non vérifié.

## Source
- vécu 2026-05-11 (GeoServer 2.28.3).
- https://repo.osgeo.org/repository/release/org/geoserver/community/

## Statut
à reprouver — établi sur 2.28.
