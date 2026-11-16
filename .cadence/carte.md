# Carte du dépôt expertise-gis

Pas d'écran : un dépôt de fiches Markdown et un test.

## Structure
- `fiches/<domaine>/<slug>.md` : une fiche par piège (format `docs/format-fiche.md` : titre, Symptôme, Cause, Détection, Geste, Versions concernées, Source, Statut).
- `fiches/README.md` : index par symptôme, ✅ prouvé / 🔁 à reprouver.
- `tests/test_fiches.py` (unittest, sans dépendance) : format, statut, source (lien ou « vécu » daté), liens internes, index complet, icône ✅/🔁 de l'index = statut de la fiche, « prouvé » exige un lien ou une version 3.x, aucun terme privé dans les fichiers suivis par git.

## Workflows
- Ajouter une fiche : écrire `fiches/<domaine>/<slug>.md`, l'ajouter à l'index, `python3 -m unittest discover -s tests`.
- Termes privés (projets, machines, chart/espace de travail propres, noms de société) : liste dans `.termes-prives` (gitignoré, une expression par ligne) ou `EXPERTISE_GIS_TERMES_PRIVES`. Aucun n'est écrit dans un fichier suivi. Sans liste, le test échoue : toute copie neuve du dépôt doit recréer `.termes-prives`.

## Décisions (L1, D-1, 2026-11-16)
- 62 fiches tirées des agents d'expertise GIS et de 59 mémoires : 51 GeoServer/GeoTools, 5 PostgreSQL/PostGIS/TimescaleDB, 6 SLD. Doublons fusionnés.
- Règle de statut : un fait établi seulement sur GeoServer 2.28 (version courante 3.0.1) est « à reprouver » ; prouvé = doc, code source, ou mesure vécue sur la version citée.
- Écartés : faits propres au projet (couches, charts, modules maison nommés), recettes sans symptôme (renommage d'espace de travail, image COG/S3, migration 2.x→3.x), faits non démontrés (`${env:VAR}` dans datastore.xml, `env()` dans un processus maison), pièges hors carto (ArgoCD, rotation de secrets, OpenLayers → L2).
- « fichiers/README.md » de la demande lu comme `fiches/README.md`.

## Décisions (correction de la revue L1, 2026-11-16)
- Le test contrôle tous les fichiers de `git ls-files` (plan, registre, carte, README compris) ; il ne contient plus aucun terme.
- Titres du plan rendus génériques (L1, L2, L4, L6) ; registre `.cadence/demandes` laissé tel quel.
- Fiches renommées : `gwc-integration-directe-ignore-sld-body` (condition = requête prise par GWC, pas l'adresse ; à reprouver), `dispatchercallback-init-service-et-requete-nuls` (les KVP sont déjà analysés à `init`).
- `processfactory-bean-spring-seul-ignore` : deux voies (bean `GeoServerProcess` ramassé par `SpringBeanProcessFactory`, ou SPI).
