# Modèle de station sur plusieurs couches : hampes orphelines, désencombrement à décider en amont

## Symptôme
Modèle de station (nébulosité au centre, température, point de rosée, pression, barbule…)
dessiné avec une couche `symbol` par cellule :
- avec la collision de MapLibre (`allow-overlap: false`), une station perd une partie de son
  modèle : hampe de vent orpheline, température sans point de rosée ;
- avec `allow-overlap: true` partout, les modèles voisins se recouvrent en bouillie ;
- deux réseaux affichés ensemble (aéronautique et synoptique, navires, bouées) se recouvrent ;
- le choix des stations retenues change d'un rendu à l'autre au même cadrage.

## Cause
Une couche `symbol` ne porte qu'un texte et une icône : il faut une couche par cellule. La
collision de MapLibre décide **symbole par symbole** et ne sait pas lier plusieurs couches en un
groupe « tout ou rien ». Et l'ordre de parcours d'une collection non triée n'est pas stable.

## Détection
- Compter, au même cadrage, les stations dont la barbule est placée et celles dont le cercle de
  nébulosité l'est : un écart = modèles partiels.
- Test unitaire des couches : chaque filtre contient la condition de désencombrement
  (`["==",["get","plot_show"],1]`) et chaque couche est en `allow-overlap` / `ignore-placement`.
- Sur les stations retenues : aucune paire dont les centres écran sont à moins de
  `(w₁+w₂)/2` en x **et** `(h₁+h₂)/2` en y.

## Geste
Décider en JavaScript, puis laisser MapLibre tout dessiner :
1. trier chaque collection par identifiant de station (parcours stable, rendu déterministe) ;
2. projeter chaque point à l'écran (`map.project`), écarter les projections non finies ;
3. glouton : une station est retenue si aucune station déjà retenue ne chevauche son
   **emprise réservée** (celle du modèle complet, par exemple 104 × 76 px ; plus petite pour un
   mode réduit) ; grille de hachage de maille = largeur de l'emprise, 9 cellules voisines testées ;
4. poser `plot_show = 1 | 0` sur chaque entité, `setData` sur la source ;
5. toutes les couches du modèle filtrent sur `plot_show = 1` et sont en `allow-overlap: true`,
   `ignore-placement: true` ;
6. recalculer à `moveend` et quand une collection change ; une couche vidée (erreur, rechargement)
   relance le calcul pour rendre sa place aux réseaux suivants ;
7. plusieurs réseaux partagent la même liste de stations retenues, dans un ordre de priorité fixe
   (aéronautique, puis synoptique, puis navires, puis bouées) ;
8. la barbule est dessinée en dernier, au-dessus des chiffres.

## Versions concernées
MapLibre GL JS 5.24 (vécu, 2026-09-10 : modèles partiels avant le désencombrement atomique) ;
OpenLayers non vérifié.

## Source
- vécu 2026-09-10 (MapLibre GL JS 5.24, modèle de station sur deux réseaux d'observation, puis
  navires et bouées le 2026-09-14 ; test unitaire des filtres des couches du modèle).
- https://maplibre.org/maplibre-style-spec/layers/#icon-allow-overlap
- WMO-No. 306 Vol. I.1 (2019), Attachment IV (disposition du modèle de station) ; fiches
  [station](../symbologie/station/pression-en-haut-a-droite-du-cercle-mslp-pas-qnh.md).

## Statut
prouvé
