# Des milliers de points dans une couche vecteur figent la carte en vue large

## Symptôme
Au-delà de quelques milliers de points visibles (vécu : ~14 000), la carte devient saccadée
puis figée au dézoom ; le déplacement et le zoom ne répondent plus. Aux grandes échelles
(peu de points à l'écran), tout est fluide.

## Cause
Une `VectorLayer` dessine chaque entité à chaque rendu, avec sa fonction de style : le coût
croît avec le nombre d'entités visibles.

## Détection
Compter les entités dans l'emprise visible
(`source.getFeaturesInExtent(view.calculateExtent())`.length) et mesurer la cadence
(onglet Performance, ou compteur `requestAnimationFrame`) en vue large : la chute de cadence
suit ce nombre.

## Geste
Regrouper avec la source `Cluster` d'OpenLayers, posée devant la source d'origine :
```ts
const cluster = new Cluster({ source: pointsSource, distance: 55, minDistance: 28 });
const layer = new VectorLayer({ source: cluster, style: styleFn });
// styleFn : feature.get('features') = entités regroupées ;
// longueur 1 => style normal de features[0], sinon disque + compte.
```
- Mettre en cache un `Style` par classe de taille de groupe et ne changer que son texte.
- Au clic sur un groupe de plus d'une entité, zoomer (`view.animate`) plutôt qu'ouvrir une
  fiche ; pour un groupe de 1, ouvrir la fiche de `features[0]`.
- Afficher les grands comptes en forme courte (« 1,2 k »).
- Au-delà de ~50 000 points sans besoin de regroupement : couche `WebGLPoints`.
- Preuve d'effet : même mesure, la cadence reste stable en vue large.

## Versions concernées
OpenLayers 10 (vécu) ; `Cluster` (`distance`, défaut 20 px ; `minDistance`, défaut 0)
documenté en OpenLayers 10.11.

## Source
- https://openlayers.org/en/latest/apidoc/module-ol_source_Cluster-Cluster.html
- vécu 2026-05 (OpenLayers 10, 14 000 points AIS en vue continentale ; ~35 groupes avec
  `distance: 55`).

## Statut
prouvé
