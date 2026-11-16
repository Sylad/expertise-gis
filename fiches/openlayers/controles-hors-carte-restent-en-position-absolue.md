# Contrôles déplacés par `target` : toujours en position absolue, empilés au hasard

## Symptôme
On passe `target` aux contrôles (`Zoom`, `ScaleLine`, `MousePosition`) pour les ranger dans
un conteneur de l'application ; ils y sont bien insérés dans le DOM mais se superposent,
sortent du conteneur ou se collent à un coin, au lieu de s'aligner dans le flux.

## Cause
`ol.css` positionne les contrôles **par classe** : `.ol-control { position: absolute }`,
`.ol-scale-line { position: absolute }`, `.ol-mouse-position { position: absolute; top: 8px;
right: 8px }`. L'option `target` change le parent, pas ces règles : chaque contrôle reste
positionné par rapport au premier ancêtre positionné.

## Détection
```js
getComputedStyle(document.querySelector('.ol-scale-line')).position  // 'absolute'
```
Et dans l'inspecteur, la règle qui l'impose (feuille `ol.css`, classe `.ol-control` ou
propre au contrôle).

## Geste
- Désactiver les contrôles par défaut concernés (`defaults({ zoom: false, attribution: false })`)
  et créer les siens avec `target`.
- Rétablir le flux dans le conteneur par un sélecteur plus spécifique que celui d'`ol.css` :
  ```css
  .dock .ol-control, .dock .ol-scale-line, .dock .ol-mouse-position {
    position: static; top: auto; right: auto; left: auto; bottom: auto;
  }
  ```
- Créer la carte quand les éléments cibles existent (après le rendu du gabarit, pas dans
  le constructeur d'un composant).
- Preuve d'effet : `position` vaut `static`, les contrôles suivent la mise en page.

## Versions concernées
OpenLayers 10 (vécu) ; règles relues dans `ol.css` d'OpenLayers 10.11.

## Source
- https://unpkg.com/ol@10.11.0/ol.css
- https://openlayers.org/en/latest/apidoc/module-ol_control_Control-Control.html (option `target`)
- vécu 2026-05-12 (OpenLayers 10, zoom, échelle et coordonnées rangés dans deux conteneurs).

## Statut
prouvé
