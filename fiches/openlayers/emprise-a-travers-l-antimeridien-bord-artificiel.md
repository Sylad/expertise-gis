# Emprise qui traverse l'antiméridien : bord artificiel tracé à ±180°

## Symptôme
En vue plate, le contour de l'emprise d'une couche dont l'ouest est plus grand que l'est
(elle traverse l'antiméridien, par exemple 170° → −170°) est dessiné comme deux demi-anneaux,
chacun avec un trait vertical à ±180° qui n'existe pas. Une emprise qui finit pile à ±180°
laisse en plus une moitié vide le long de la coupure.

## Cause
Pour dessiner l'emprise, le code de l'application la coupe à ±180° en deux rectangles et
trace **tous** leurs côtés, y compris ceux créés par la coupure. OpenLayers n'y est pour rien :
c'est le passage d'une emprise « ouest > est » à des géométries qui crée ces côtés.

## Détection
Tests unitaires de la fonction qui construit le contour, avec des emprises 170° → −180° et
180° → −170°, et sur les demi-largeurs de chaque moitié (cas des notes). Assertion proposée
(déduction) : aucun segment tracé n'a ses deux extrémités sur la même longitude ±180°, et
aucune moitié n'est de largeur nulle.

## Geste
Ne tracer que les vrais côtés de l'emprise, pas ceux créés par la coupure. Preuve d'effet :
les tests de la détection passent et le trait à ±180° disparaît de la carte.

## Versions concernées
OpenLayers 10.11.0 (vécu, rapporté par les notes de dépannage reçues le 2026-11-19).
Indépendant de la version : le défaut est dans le code de l'application.

## Source
- Notes de dépannage d'un autre compte, cas « O2 », reçues le 2026-11-19 (vécu, corrigé et
  couvert par des tests unitaires).
- https://openlayers.org/en/latest/apidoc/module-ol_extent.html

## Statut
prouvé
