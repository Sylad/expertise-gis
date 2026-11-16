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

## Décisions (L2, D-1, 2026-11-16)
- 17 fiches côté client : 7 `fiches/openlayers/`, 10 `fiches/maplibre/`, tirées de l'agent OpenLayers, du skill de portage SLD → MapLibre et des mémoires de carte ; 5 sections « Carte côté client » ajoutées à l'index.
- Chaque fait de doc revérifié en ligne (doc OpenLayers 10.11, doc MapLibre GL JS 6.18, code source) ; chaque lien des fiches contrôlé (HTTP 200). Corrigé au passage : le positionnement des contrôles OpenLayers vient des classes d'`ol.css`, pas d'un style en ligne ; la fonction de mélange à l'entrée d'une couche personnalisée est `ONE, ONE_MINUS_SRC_ALPHA`.
- Test : `test_domaines_client` (les deux domaines existent) et `test_prouve_client_sur_version_courante` (« prouvé » exige OpenLayers ≥ 10 ou MapLibre ≥ 5 cité en Versions concernées).
- MapLibre GL JS 6 est la version publiée (6.18) : les faits vécus en 5.x restent « prouvé » (règle du lot : seul < 5 est à reprouver) et chaque fiche dit ce qui est vérifié ou non en 6.
- « à reprouver » : propriétés imbriquées en chaîne au clic (mécanisme d'encodage non relu).
- Écartés : WebGL générique sans lien à la bibliothèque (inversion du quad de ping-pong, anticrénelage des points, épaisseur HiDPI, algorithme de traînées), faits propres à un projet (table de correspondance d'identifiants de couches, couche activée par défaut dans un groupe replié, cible de build), goût (ombre du texte d'attribution), risques non mesurés (tuiles 256 contre 512), environnement (WebGL headless).

## Décisions (correction de la revue L2, 2026-11-16)
- `openlayers/source-wms-projection-de-la-vue` réécrite à partir du code d'OpenLayers 10.11.0 (fichiers et lignes cités) et d'une mesure scriptée des GetMap : projection égale ou absente = aucune reprojection client ; grille par défaut = celle de la vue ; un `tileGrid` sans `projection` sert pour toute vue (patchwork). L'ordre des axes (proj4 sans `+axis=neu` en WMS 1.3.0) reste une hypothèse pour le cisaillement vécu : fiche « à reprouver », 🔁 dans l'index.
- `test_prouve_client_sur_version_courante` : ne compte que les versions suivies de « (vécu » ou « (code relu et mesure », et exige qu'au moins une soit courante (`any`, plus de `max()`) ; `test_versions_vecues_seules` teste ce filtre. Règle reportée dans `docs/format-fiche.md`.
- `cluster-masque-la-regle-d-echelle` : `clusterMaxZoom` ≤ floor(seuil) − 1 (arrondi `Math.round` de l'option, tuiles GeoJSON de zoom `floor(Z)`, lu dans le code 5.24 et 6.18).
- `denominateur-d-echelle-en-zoom-tuiles-512` : les 512 px sont la constante de la caméra (monde = 512 × 2^zoom), pas l'option `tileSize` d'une source.
- La liste des termes privés vient de `EXPERTISE_GIS_TERMES_PRIVES` dans les sessions déléguées : pas de `.termes-prives` créé.
