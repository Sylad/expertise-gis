# Un ogc:Literal qui ne contient qu'un espace est vidé

## Symptôme
Une chaîne construite par `Concatenate` (par exemple un WKT `LINESTRING(x y, …)`) est mal
formée : l'espace séparateur a disparu. Autre surprise du même banc : `getX`/`getY`
imprimés seuls sont arrondis à 3 décimales.

## Cause
L'analyseur du SLD supprime les blancs d'un littéral : `<ogc:Literal> </ogc:Literal>` devient
une chaîne vide. La conversion d'un nombre en texte arrondit.

## Détection
Rendre la chaîne dans un `TextSymbolizer` de test et la lire.

## Geste
- Espace : l'extraire d'une chaîne non vide, par exemple `strSubstring('x y', 1, 2)`.
- Coordonnées : passer par une opération numérique (`Add(getX(geom), 0)`) avant de concaténer.

## Versions concernées
GeoServer 3.0.1 (vécu).

## Source
vécu 2026-09-21 (GeoServer 3.0.1).

## Statut
prouvé
