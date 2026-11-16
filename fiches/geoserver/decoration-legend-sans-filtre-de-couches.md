# Décorations WMS : légende de toutes les couches, expressions mixtes refusées

## Symptôme
- La décoration `legend` d'une mise en page (`format_options=layout:<nom>`) dessine la légende
  de **toutes** les couches de la requête et couvre la carte.
- Une mise en page dont un attribut combine deux expressions (`${…},${…}`) n'est plus trouvée :
  `Could not find decoration layout`.
- `angle=` tourne la carte mais pas les marques ni les étiquettes.

## Cause
La décoration `legend` n'accepte que `legend_options` et `opacity`, sans filtre de couches.
Les attributs acceptent une expression `${cql}` unique ; un mélange texte + plusieurs
expressions casse l'analyse du gabarit. La rotation de `angle` s'applique aux géométries.

## Détection
Rendu d'un GetMap avec la mise en page ; `GET /rest/resource/layouts/<nom>.xml` pour lire le
gabarit réellement stocké.

## Geste
- Légende d'une partie des couches : pré-rendre une image (`GetLegendGraphic`) et la poser par
  une décoration `image`.
- Construire un attribut composé avec **une** expression :
  `${Concatenate(round(X*env('k','1')), ',', round(Y*env('k','1')))}`.
- Avec `angle=`, composer la rotation des marques avec `env('map_angle')` dans les styles.

## Versions concernées
GeoServer 3.0.1 (vécu, doc 3.0 lue).

## Source
- vécu 2026-09-24 (GeoServer 3.0.1, gabarits d'essai supprimés après).
- https://docs.geoserver.org/latest/en/user/services/wms/decoration.html

## Statut
prouvé
