# GetLegendGraphic en exception sur un style à expressions

## Symptôme
Le style rend bien la carte, mais `GetLegendGraphic` de la couche répond une exception
(fonction appelée sur une valeur nulle).

## Cause
La légende est dessinée sur une entité d'échantillon dont les attributs sont **nuls** : une
expression qui calcule une rotation, une taille ou un texte à partir d'un attribut échoue.

## Détection
`GET …/wms?REQUEST=GetLegendGraphic&LAYER=<ws>:<couche>&FORMAT=image/png` : `text/xml` au
lieu d'une image.

## Geste
Protéger chaque expression : `if_then_else(isNull(<attr>), <valeur neutre>, <expression>)`.
Vérifier la légende de chaque style dans le banc de rendu.

## Versions concernées
GeoServer 3.0.1 (vécu).

## Source
vécu 2026-09-21 (GeoServer 3.0.1).

## Statut
prouvé
