# Module Java : recherche de beans qui lève au lieu de rendre null

## Symptôme
Un module maison plante à l'initialisation ou à la première requête :
- `MultipleBeansException` sur `GeoServerExtensions.bean(Catalog.class)` ;
- une exception (pas `null`) sur `GeoServerExtensions.bean("<nom>")` quand le bean manque ;
- `GWC.get()` renvoie `null` dans un `GeoServerInitializer`.
Une exception dans un écouteur d'initialisation fait tomber **toute l'application** ; le
détail n'est pas sur la sortie standard mais dans `logs/localhost.*.log` de Tomcat.

## Cause
Plusieurs beans implémentent `Catalog` (`catalog`, `rawCatalog`, `secureCatalog`…) ;
la recherche par nom lève si le bean est absent ; GeoWebCache n'est pas prêt au moment
des `GeoServerInitializer`.

## Détection
Pile d'appels dans `logs/localhost.*.log` du conteneur.

## Geste
- `GeoServerExtensions.bean("catalog")` (par nom) ; garder la référence `GeoServer` plutôt que
  rechercher le catalogue par type.
- Entourer les recherches facultatives (`try/catch`) ; ne jamais laisser une exception
  sortir d'un écouteur d'initialisation.
- Créer ce qui dépend de GWC sur `ContextLoadedEvent` (ou `ContextRefreshedEvent`), pas dans
  un `GeoServerInitializer`.
- Beans sans argument, dépendances résolues à l'exécution plutôt qu'injectées par constructeur
  (évite les problèmes d'ordre avec les beans de GeoServer).

## Versions concernées
GeoServer 3.0.1 / GWC 2.0.1 (vécu) ; recherche par type du catalogue aussi vue en 2.28.

## Source
vécu 2026-09-01 (GeoServer 3.0.1, module d'initialisation GWC) ; vécu 2026-05-27 (GeoServer 2.28, recherche du catalogue).

## Statut
prouvé
