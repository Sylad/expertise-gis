# Harvest ImageMosaic en 200 qui n'indexe rien

## Symptôme
L'ingestion dépose les nouveaux fichiers, appelle `POST …/external.imagemosaic`, reçoit 200
et journalise « OK » ; pourtant les nouvelles validités n'apparaissent pas (index figé depuis
des jours). Lors d'une recréation : `Failed to create reader` sans cause dans la réponse REST ;
ou `The specified coverageName is unavailable`.

## Cause
- Le code 200 du `harvest` ne dit pas combien de granules ont été ajoutés.
- La vraie cause d'un `Failed to create reader` n'est que dans `geoserver.log`
  (`ERROR [gce.imagemosaic]` + `Caused by`), par exemple `Schema '<nom>' already exists` (table
  d'index laissée par un essai précédent).
- Un sous-dossier dans le dossier de la mosaïque est parcouru sans `Recursive=false`.
- Le nom du coverage diffère du nom du dossier/de la table : il faut un `nativeName`.

## Détection
Compter les granules avant et après chaque `harvest`
(`GET …/coverages/<c>/index/granules.json` ou `count(*)` sur la table d'index) ; échouer si 0.
Lire `geoserver.log` dans le pod dès le premier `Failed to create reader`.

## Geste
- Tout `harvest` est suivi d'un comptage, en échec bruyant si rien n'est ajouté.
- `indexer.properties` : `Recursive=false`, `Name`, `TypeName`, `AbsolutePath=false` explicites.
- Publication avec `<nativeName>` quand coverage ≠ dossier.
- Avant de relancer une création d'index PostGIS, lister les tables, index et séquences
  existants (voir [../postgis/rename-table-garde-les-noms-d-index](../postgis/rename-table-garde-les-noms-d-index.md)).

## Versions concernées
GeoServer 3.0.1 (vécu).

## Source
vécu 2026-09-23 (GeoServer 3.0.1 : index shapefile figé 5 jours derrière des harvest « OK », migration vers PostGIS en 4 essais).

## Statut
prouvé
