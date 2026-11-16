# Processus maison déclaré en bean Spring sans `GeoServerProcess` : invisible

## Symptôme
Le jar du processus est dans `WEB-INF/lib`, son bean est déclaré dans `applicationContext.xml`,
mais le processus n'apparaît pas dans le GetCapabilities WPS et un SLD qui l'appelle
répond « Unable to find function ». Aucune erreur au démarrage.

## Cause
Un processus n'est vu (en WPS comme en fonction de SLD) que s'il est enregistré par une
fabrique de processus. Il y a deux voies :
- **un bean Spring qui implémente `org.geoserver.wps.gs.GeoServerProcess`** : le bean
  `geoserverProcessFactory` (classe `org.geoserver.wps.jts.SpringBeanProcessFactory`, préfixe
  `gs`, déclaré dans l'`applicationContext.xml` de gs-wps-core) ramasse tous ces beans et
  s'enregistre auprès de `Processors` et du `ProcessFunctionFactory` ;
- **une fabrique découverte par le SPI de GeoTools** (`META-INF/services/org.geotools.process.ProcessFactory`),
  typiquement une sous-classe d'`AnnotatedBeanProcessFactory` avec son propre espace de noms.

Un bean Spring qui n'implémente pas `GeoServerProcess` et qu'aucune fabrique SPI ne déclare
n'est enregistré par personne : il est ignoré en silence.

## Détection
- Le bean implémente-t-il `GeoServerProcess` ? Si oui, ce piège n'est pas le bon : chercher le
  processus sous le préfixe `gs:` et une autre cause (le doubler d'une fabrique SPI créerait un
  processus en double).
- Sinon : `unzip -l <jar> | grep META-INF/services/org.geotools.process.ProcessFactory` ;
  absent ⇒ piège.
- Au démarrage, une fabrique SPI découverte journalise `Found N bindable processes in <paquet>`.

## Geste
Choisir **une** des deux voies :
- implémenter `GeoServerProcess` (le processus s'appelle alors `gs:<Nom>`) ;
- ou fichier `META-INF/services/org.geotools.process.ProcessFactory` contenant le nom qualifié
  d'une classe concrète, constructeur sans argument, qui étend `AnnotatedBeanProcessFactory` ;
  nom du processus = nom de la classe sans le suffixe `Process`, dans l'espace de noms de la
  fabrique (`<ns>:<Nom>`).

Dans les deux cas, dépendances GeoServer/GeoTools en `provided` dans le pom.

## Versions concernées
GeoServer 3.0.1 (code gs-wps-core relu, et vécu) ; 2.28 (vécu, même recette SPI).

## Source
- Code source : `org.geoserver.wps.jts.SpringBeanProcessFactory` et le bean
  `geoserverProcessFactory` de `src/extension/wps/wps-core/src/main/java/applicationContext.xml`
  (https://github.com/geoserver/geoserver), relus en 3.0.1.
- https://docs.geotools.org/latest/userguide/library/process/index.html
- vécu 2026-09-01 (GeoServer 3.0.1, voie SPI) ; vécu 2026-05-13 (GeoServer 2.28, voie SPI).

## Statut
prouvé
