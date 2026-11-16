# Transformations de rendu imbriquées : l'intérieure ne reçoit pas la source

## Symptôme
`ras:Contour(data = <ns>:Interpolation(…))` dans un `<Transformation>` : la transformation
intérieure reçoit une source vide (`data` nul ou manquant) ; le rendu échoue.

## Cause
GeoServer n'injecte la couche source que dans la transformation **la plus externe** ; une
transformation passée en paramètre d'une autre n'est pas reconnue comme transformation de rendu.

## Détection
Journal du processus intérieur : `data` nul.

## Geste
Écrire un processus unique qui enchaîne les deux calculs en interne (par exemple interpolation
puis isolignes, en appelant `ContourProcess` depuis le code) ; ou deux couches/styles séparés.

## Versions concernées
GeoServer 2.28 (vécu) ; 3.x non vérifié.

## Source
vécu 2026-05-13 (GeoServer 2.28, interpolation de stations suivie d'isolignes).

## Statut
à reprouver — établi sur 2.28.
