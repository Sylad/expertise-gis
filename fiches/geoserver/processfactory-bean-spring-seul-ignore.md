# Processus maison déclaré en bean Spring seulement : invisible

## Symptôme
Le jar du processus est dans `WEB-INF/lib`, son bean est déclaré dans `applicationContext.xml`,
mais le processus n'apparaît pas dans le GetCapabilities WPS et un SLD qui l'appelle
répond « Unable to find function ». Aucune erreur au démarrage.

## Cause
Les fabriques de processus sont découvertes par le mécanisme SPI de GeoTools, pas par Spring.

## Détection
`unzip -l <jar> | grep META-INF/services/org.geotools.process.ProcessFactory` : absent ⇒ piège.
Au démarrage, un module découvert journalise `Found N bindable processes in <paquet>`.

## Geste
- Fichier `META-INF/services/org.geotools.process.ProcessFactory` contenant le nom qualifié
  d'une classe concrète, constructeur sans argument, qui étend `AnnotatedBeanProcessFactory`.
- Nom du processus = nom de la classe sans le suffixe `Process`, dans l'espace de noms de la
  fabrique (`<ns>:<Nom>`).
- Dépendances GeoServer/GeoTools en `provided` dans le pom.

## Versions concernées
GeoServer 3.0.1 (vécu) et 2.28 (même recette).

## Source
- vécu 2026-09-01 (GeoServer 3.0.1) ; vécu 2026-05-13 (GeoServer 2.28).
- https://docs.geotools.org/latest/userguide/library/process/index.html

## Statut
prouvé
