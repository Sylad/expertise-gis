# Couche vecteur rendue visible, mais vide : `setVisible(true)` ne charge rien

## Symptôme
L'utilisateur active une couche vecteur (navires, alertes, stations) ; la case est cochée,
`layer.getVisible()` vaut `true`, aucune erreur, mais rien n'apparaît. Les couches raster
(WMS, tuiles) activées de la même façon, elles, s'affichent.

## Cause
Une source raster charge ses images à chaque rendu. Une `VectorSource` ne charge d'elle-même
que si elle a un `url` ou un `loader`, selon sa `strategy` (par défaut `all` : un seul
chargement de tout, au premier rendu ; `bbox` : à chaque emprise). Une source remplie par le
code (`addFeatures` après un `fetch` de l'application) n'est jamais chargée par la seule
visibilité : si le `fetch` n'est lancé qu'à d'autres moments (changement d'instant, boucle
de rafraîchissement démarrée ailleurs), la couche reste vide.

## Détection
Au moment de l'activation : `layer.getSource().getFeatures().length` (0 = rien chargé) et
l'onglet réseau (aucune requête vers l'API de la couche = le chargement n'a pas été lancé).

## Geste
- Soit donner à la source un `loader` (ou `url`) et une `strategy` : OpenLayers charge
  quand la couche est rendue.
- Soit, si la source est remplie par l'application, lancer le chargement dans le même
  gestionnaire que l'activation (et démarrer la boucle de rafraîchissement s'il y en a une).
- Contrôle d'activation : vérifier qu'il y a des entités, pas seulement `getVisible()`.
- Preuve d'effet : à l'activation, une requête part et le compte d'entités devient > 0.

## Versions concernées
OpenLayers 10 (vécu) ; stratégie de chargement documentée en OpenLayers 10.11.

## Source
- https://openlayers.org/en/latest/apidoc/module-ol_source_Vector-VectorSource.html (« By default an
  `all` strategy is used, a one-off strategy which loads all features at once »)
- vécu 2026-05-19 (OpenLayers 10, couches de points remplies par l'application).

## Statut
prouvé
