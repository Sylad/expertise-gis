# Carte du dépôt expertise-gis

Pas d'écran : un dépôt de fiches Markdown et un test.

## Structure
- `fiches/<domaine>/<slug>.md` : une fiche par piège (format `docs/format-fiche.md` : titre, Symptôme, Cause, Détection, Geste, Versions concernées, Source, Statut).
- `fiches/README.md` : index par symptôme, ✅ prouvé / 🔁 à reprouver.
- `tests/test_fiches.py` (unittest, sans dépendance) : format, statut, source (lien ou « vécu » daté), liens internes, index complet, termes interdits.

## Workflows
- Ajouter une fiche : écrire `fiches/<domaine>/<slug>.md`, l'ajouter à l'index, `python3 -m unittest discover -s tests`.
- Termes privés (noms de société) : `EXPERTISE_GIS_TERMES_PRIVES` ou `.termes-prives` (gitignoré), jamais dans le dépôt.

## Décisions (L1, D-1, 2026-11-16)
- 62 fiches tirées des agents gis-expert, java-geoserver et de 59 mémoires : 51 GeoServer/GeoTools, 5 PostgreSQL/PostGIS/TimescaleDB, 6 SLD. Doublons fusionnés.
- Règle de statut : un fait établi seulement sur GeoServer 2.28 (version courante 3.0.1) est « à reprouver » ; prouvé = doc, code source, ou mesure vécue sur la version citée.
- Écartés : faits propres au projet (couches, charts, modules maison nommés), recettes sans symptôme (renommage d'espace de travail, image COG/S3, migration 2.x→3.x), faits non démontrés (`${env:VAR}` dans datastore.xml, `env()` dans un processus maison), pièges hors carto (ArgoCD, rotation de secrets, OpenLayers → L2).
- « fichiers/README.md » de la demande lu comme `fiches/README.md`.
