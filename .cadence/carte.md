# Carte du dépôt expertise-gis

Pas d'écran : un dépôt de fiches Markdown, la mécanique des écrans avec carte (`ecrans-carte/`, gabarits de tests compris) et leurs tests.

## Structure
- `fiches/<domaine>/<slug>.md` : une fiche par piège (format `docs/format-fiche.md` : titre, Symptôme, Cause, Détection, Geste, Versions concernées, Source, Statut).
- `fiches/README.md` : index par symptôme, ✅ prouvé / 🔁 à reprouver.
- `.claude-plugin/{plugin.json,marketplace.json}` + `skills/fiches-gis/` : plugin Claude Code (le dépôt entier, fiches comprises, est copié à l'installation) ; `scripts/fiches.py` (`chercher`, `references`, `domaines`) sans dépendance ; `tests/test_plugin.py`.
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

## Décisions (L3, D-1, 2026-11-16)
- 34 fiches de symbologie normalisée dans `fiches/symbologie/{fronts-et-centres,station,zones-d-avis,sigwx}/` (7 / 8 / 9 / 10 ; 25 prouvées, 9 à reprouver), tirées des cinq études de normes et de l'agent de symbologie ; 4 sections « Symbologie normalisée » dans l'index.
- Une fiche = ce que dit la norme et son piège de lecture ; aucun nom de couche, style, service ou fichier de projet ; règles résumées, pas d'extraits longs.
- Citations recontrôlées le 2026-11-16 avant « prouvé » : WMO-No. 49 Vol. II (2018 mise à jour 2021) par pdftotext sur une copie publique (page PDF = page imprimée + 14, toutes les pages citées vérifiées) ; WMO-No. 306 Att. IV (2019, sans copie publique) par le texte identique de l'appendice II-4 du Manuel du GDPFS, pagination 2019 reprise de l'étude. EUR Doc 014 (icao.int en 403) et guides WAFC / BUFR / SADIS (copies injoignables) : fiches « à reprouver ». Table 2700 : le texte public diffère de l'édition 2019 → « à reprouver ».
- Test : `fiches/symbologie/<sous-domaine>/` admis par `test_emplacement_et_nom` (modifié) ; nouveaux `test_domaine_symbologie`, `test_source_symbologie_citation_complete` (§ ou note/Table/Model, `p. …`, `PDF n`, figure), `test_prouve_symbologie_citation_verifiee` (« citation vérifiée le AAAA-MM-JJ »), `test_motifs_de_citation`. Règle reportée dans `docs/format-fiche.md`.
- Écartés : faits d'implémentation (plugin, SLD, décodeur, placement multi-échelles), cône NHC (pratique d'un producteur, citée seulement comme hors norme), TEMSI national et F215 (pas de norme), choix d'implémentation non normatifs.

## Décisions (correction de la revue L3, 2026-11-16)
- Chaque correction relue sur le texte : appendice II-4 du Manuel du GDPFS (texte et figure rendue du § 1), WMO-No. 49 Vol. II 2018 mise à jour 2021 (pdftotext, tracés vectoriels du PDF). Bilan symbologie : 26 prouvées, 8 à reprouver.
- Pression du modèle de station : `PPPP` sur la rangée de `TTT` et `C_M` (en haut à droite du cercle), `ppp` puis `a` sur la rangée du cercle ; fiche renommée `station/pression-en-haut-a-droite-du-cercle-mslp-pas-qnh`.
- Barbules : la gauche se prend en regardant de l'extrémité libre vers la station (hampe « directed … towards the centre »), face à l'aval du vent ; exemple vent d'ouest → barbules au nord.
- Turbulence (Model SN) : cotes remesurées sur les coordonnées des segments du PDF (hauteur 0,26 L, base 0,25 L, forte 0,52 L ; clé SWH 0,15 L) → reste « prouvé ».
- XXX : règle tirée de WMO-49 § 4.3.1 (SWM FL 100–FL 250, SWH au-dessus de FL 250) et Model SN § 3.3 ; le guide WAFC n'est plus la source (hors norme, non recontrôlé) → « prouvé ».
- `J 120` : « sans croix » écrit comme une déduction (le texte ne prévoit pas de croix).
- Test : `test_regles_recontrolees_revue_l3` (motifs exigés / interdits par fiche corrigée).

## Décisions (L4, D-1, 2026-11-16)
- `ecrans-carte/` hors de `fiches/` : ce sont des règles d'écran et des gabarits, pas des pièges d'un outil ; le format de fiche (Symptôme… Statut) ne s'y applique pas. Renvoi depuis `README.md` et `fiches/README.md`.
- `invariants.md` : les 13 invariants d'un écran avec carte, chacun avec Symptôme, Cause, Contrôle et fiches liées quand il y en a ; écrits sans rien de propre à un projet.
- `interface.md` : six familles de règles d'interface sur carte, chacune avec sa source liée (classes de taille de fenêtre, feuilles du bas, WCAG 2.2 par critère, MDN, NN/g, Crameri et al. 2020), et les contrôles sur la vraie page (largeurs, axe-core, mesure des boîtes, contraste sur fond WebGL, captures).
- `gabarits/` sans dépendance : `legende_rendu.py` et `legende-rendu.mjs` (même logique : entrées d'une expression MapLibre `step` / `interpolate` / `match` ou des `ColorMapEntry` d'un SLD, conversion d'unité, écarts nommés, valeur affichée dans la couleur d'une autre classe), modèles de test par option à remplir (sautés à vide, jamais verts à vide), `boites.mjs` (chevauchements, cibles, hors du panneau, fiche qui couvre l'objet, débordement, contraste WCAG).
- Arrondi (invariant 2) : la fonction compare la classe qui choisit la couleur à la classe de la valeur affichée, avec le formatage du projet ; elle ne présume pas du remède (classer sur la valeur affichée, ou plus de décimales).
- Test : `tests/test_ecrans_carte.py` (13 invariants dans l'ordre et complets, règles sourcées, seuils, liens, gabarits présentés, gabarit Python, modèle Python vide / juste / faux, gabarits JS par `node --test`, sauté sans Node).

## Décisions (correction de la revue L4, 2026-11-16)
- `boites.mjs` : `chevauchements`, `ciblesTropPetites`, `horsDuParent` et `contrasteMinimal` lèvent une exception sur une liste vide (plus d'`Infinity` ni de `[]` vert sans mesure).
- `entreesDepuisSld` (JS) ôte les commentaires XML avant la lecture, comme ElementTree en Python ; une entrée sans `quantity` est refusée dans les deux langages (fini le NaN / TypeError).
- Modèles de test : l'arrondi est sauté quand la légende n'a aucun seuil numérique (`match`).
- `tests/test_ecrans_carte.py` : `TestModeleJsRempli` remplit une copie temporaire du modèle JS (juste → vert, faux → rouge, catégoriel → arrondi sauté).
- `interface.md` : les partages 50/50, 70/30 et la navigation barre / rail sont marqués « * » comme choix du document (non tirés de la page Android citée ; Material 3 non relu).

## Décisions (L5, D-1, 2026-11-16)
- Le dépôt est à la fois marketplace et plugin (`source: "./"`) : installation identique pour les comptes perso et pro, `/plugin marketplace add Sylad/expertise-gis` puis `/plugin install expertise-gis@expertise-gis` (dépôt public, HTTP 200 sans authentification le 2026-11-16).
- Un seul skill, `fiches-gis` : chercher la fiche d'un symptôme (mots sans accents ni casse, titre et index comptés double, seuil à la moitié du meilleur score pour qu'un mot commun ne remonte pas toute la collection), puis jouer sa Détection ; écrire le bloc `references:` d'un `cadence.yaml`.
- (Remplacé par la correction de la revue, ci-dessous.) Bloc `references:` : une entrée par domaine (`nom`, `url`, `dossier`, `lire_quand`). Adresses du dépôt public par défaut, parce que le bloc est commité dans un projet partagé entre machines ; `--local` (clé `chemin`) pour une session hors ligne. Le schéma exact de la clé `references:` de cadence n'a pas été relu (hors du dépôt) : à aligner si cadence attend d'autres clés.
- `DOMAINES` (fiches.py) liste chaque dossier de `fiches/` avec ce qu'il couvre ; un dossier ajouté sans entrée fait échouer `test_chaque_dossier_de_fiches_est_un_domaine`.
- Vérifié : `claude plugin validate .` vert (seul avertissement : pas d'icône), installation réelle dans une configuration isolée (`CLAUDE_CONFIG_DIR`), `plugin details` montre le skill (~160 jetons permanents), script lancé depuis la copie installée.

## Décisions (correction de la revue L5, 2026-11-16)
- Bloc `references:` au format de `cadence run` (`v2/src/run/aiguillage.ts`, `aiguiller`) : liste de `{ mots, docs }`, une entrée par domaine, nom et description en commentaire ; valeurs écrites en listes JSON (YAML valide, lisibles sans PyYAML). Plus d'URL ni de `--base`.
- `mots` par domaine dans `DOMAINES` (troisième élément) ; `docs` : l'index `fiches/README.md` pour tous les domaines de fiches (cadence ne lit qu'une fois un doc partagé ; un domaine a jusqu'à 51 fiches, l'index les range par symptôme), `invariants.md` + `interface.md` pour `ecrans-carte`.
- Chemins : `racine_stable` remplace `…/plugins/cache/<place>/<plugin>/<version>` par `…/plugins/marketplaces/<place>` (clone de la place de marché, sans version) ; un clone ordinaire reste tel quel ; `--racine` impose un dossier ; écrit en `~/…` sous le dossier personnel. `--local` gardé caché (même effet que le défaut). Code 3 si un doc est absent.
- Test `TestLuParCadence` : le bloc écrit dans un `cadence.yaml` jetable, passé à la vraie `aiguiller` par Node (dépôt cadence : `CADENCE_RACINE` ou voisin `cadence`, sauté sinon) ; mode complet, docs retenus ; l'ancien format est refusé par cadence (témoin).
- Hors lot : `cadence ref` (`src/config.ts`, `readReferencesConfig`) attend `references: { dir }`, incompatible avec la liste de `cadence run` ; le SKILL dit de ne pas coller sur un projet qui a la forme objet.

## Décisions (L8, constat 1 de la revue L5 passe 2, 2026-11-16)
- Mots du domaine `symbologie` : « front » et « fronts » seuls retirés (cadence coupe au tiret : « front-end », « refais le front de… » passaient en mode complet). Remplacés par des expressions FR et EN : front(s) froid(s) / chaud(s) / occlus / (quasi) stationnaire(s), cold / warm / occluded / stationary front, « symboles de fronts ». Les formes au pluriel sont listées à part : la comparaison de cadence est en mot entier.
- Tests : `test_front_seulement_en_expression` (sans cadence) ; via la vraie `aiguiller`, `test_demande_frontend_ne_declenche_pas_la_symbologie` (frontend, front-end, front end, « le front de la page », « les fronts des deux applis » → léger) et `test_expressions_de_fronts_declenchent_la_symbologie`.
- Version du plugin laissée à 0.1.0 (pas encore publiée sous une autre version).
- Non traité (note de la revue, pas un constat) : « couche » / « carte » du domaine `ecrans-carte` restent larges, choix assumé pour un projet de carte.

## Décisions (L9, forme unique de references:, 2026-11-17)
- `fiches.py references` écrit `references:` puis `run:` (entrées `- mots` / `docs` indentées dessous) : la forme unique de cadence L760, lue par `cadence run` et `cadence ref` sans message de migration. Plus de liste directement sous `references:`.
- `dir` n'est écrit qu'avec `--dir <dossier>` (propre au projet, comme le dossier des documents de `cadence ref`) ; un `--dir` vide est refusé (code 2), comme cadence le refuse.
- SKILL : on garde le `dir` d'un `references:` existant et on ajoute sous son `run:` ; une ancienne liste se déplace sous `run:`. Remplace la consigne « ne colle rien sur la forme objet » de L5.
- Tests : `bloc_references` lit la nouvelle forme ; `TestLuParCadence` passe par la copie de cadence en service (`~/.local/share/cadence/service`) avant le dépôt voisin, dont le `dist/` peut précéder L760 (constaté : `dist/config.js` du 12-11 refusait `references.run`). Essais : `referencesDuDepot` sans `migration`, `referencesDir` sans avis et `dir` résolu sous `~`, témoin de l'ancienne liste qui déclenche la migration.

## Décisions (L11, note de montée reçue le 2026-11-17)
- Une fiche par bibliothèque, au gabarit commun (sept sections), listes numérotées dont chaque point porte sa nature de source entre crochets ; `[déduction]` pour ce qui n'a été ni lu ni joué, `relu ici` / `mesure du 2026-11-17` pour ce qui a été recontrôlé (registre npm, CHANGELOG Angular 21.0.0 et 22.0.0, pom GeoServer aux tags 3.0.1 et 3.0.2, GEOS-12235, `tsc` 6.0.3 et 7.0.2 sur un projet minimal). Règle dans `docs/format-fiche.md`, test `test_fiches_de_montee` (+ `test_points_et_nature`).
- Fiches : `geoserver/montee-2-28-3-a-3-0-2`, et quatre domaines neufs `angular/`, `typescript/`, `nodejs/`, `nestjs/` (entrées dans `DOMAINES`, mots du skill ; rubrique « Montées de version » de l'index).
- Écarts relevés contre la note : Angular 21.2 accepte TypeScript `<6.1` (la note dit `<6.0`, vrai pour 21.0.0) ; `@nestjs/core` 12 déclare `node >= 20` (la borne 22.22.3 / 24.15 vient de l'outillage Angular) ; GEOS-12235 est aussi dans 2.27.7 et 2.28.6 ; `gs-jdbcconfig` 2.28.4 est publié depuis ; « `context.xml` passé tel quel » à lire avec `image-officielle-context-xml-ignore-jndi` (le `conf/context.xml` global est ignoré par l'image officielle). Ajout de la 21.0.0 : la migration ajoute `provideZoneChangeDetection` aux applications avec zone (à retirer si déjà sans zone, déduction).
- Recoupe sans contredire : `grappe-hazelcast-config-et-jdbcstore` (add-opens, `ignoreDirs`, grappe distincte par version), `postgis/search-path-schema-sans-usage-ignore`, `transformation-raster-coverage-source-non-injecte` (aucun changement de code en 3.0), `modules-communautaires-version-exacte`. Fiches existantes non modifiées.
- Écartés : la partie « perso » de la pièce (note Angular 19 → 20 de ce compte, hors du lot), tout nom de projet ou d'application.
- Porte complète rouge sans liste de termes privés (ni `.termes-prives` ni `EXPERTISE_GIS_TERMES_PRIVES` dans l'environnement de la porte) : `.termes-prives` créé à la racine du clone (ignoré par git, jamais commité) avec les noms de projets, d'applications et de machines connus. Remplace, pour ce clone, la décision de L2 « pas de `.termes-prives` créé ». Test inchangé.

## Décisions (correction de la revue L11, 2026-11-17)
- Natures de source : un point absent de la note ne porte plus `[commit]` / `[notes de version]`. GeoServer : `ls … | grep hazelcast` (Détection 1) → `[déduction]` ; `has_schema_privilege` (Détection 6) et `ALTER SCHEMA` / `GRANT` (Geste 6) → `[fiche search-path-schema-sans-usage-ignore]` ; Détection 8 et Geste 8 → `[déduction, d'après le symptôme 8]`. NestJS : Symptôme 2 et Cause 2 mesurés le 2026-11-17 (Node 22.23, messages exacts recopiés) ; Détection 2 → `[déduction]`, commande refaite pour ne lister que `__dirname` et les imports relatifs sans `.js` (constat mineur 3 de la revue).
- Nouvelle nature `[fiche <slug>]` (règle dans `docs/format-fiche.md`, test `test_nature_empruntee_a_une_fiche_existe` : le slug existe).
- Angular : Détections 1 et 3 en `grep -r --include` (jouées sur une arborescence témoin) ; `test_commandes_sans_globstar` refuse `**/` dans toute commande d'une fiche.
- `.termes-prives` recréé dans ce clone (ignoré par git), sans le nom de l'auteur, qui figure à dessein dans les manifestes du plugin.

## Décisions (seconde revue L11, 2026-11-17)
- Chaque point des cinq fiches de montée relu contre la section « pro — 2026-11-17 13:20 » de la note. Une détection que la note ne donne pas (commande, reproduction du symptôme) porte `[déduction]`, éventuellement « d'après le symptôme / la cause n » ; une précision absente de la note est retirée (GeoServer Détection 4 « refus nommant le champ », Angular Geste 7 « liste des hôtes », Node « nvm », « npm ci refuse », « service de CI ») ; `[code source]` sans relecture propre remplacé par la nature de la note (`[commit] [notes de version]`, GEOS-12235).
- TypeScript Détection 3 : le TS2882 apparaît sur un clone neuf (le dossier de travail le cache) ; `CI=1` sert à l'attribuer au cache.
- NestJS : `nest-winston` 2.0.0 (2026-09-14) accepte `@nestjs/common ^12` au registre ; le refus vécu est attribué aux 1.x (déduction), titre et index disent « 1.x ».
- Commandes rejouées avec GNU grep (`/usr/bin/grep`, le `grep` de session est ugrep) : NestJS Détection 2 voit aussi les guillemets doubles, Angular Détection 3 ne liste que les fichiers `@Component`.
- Aucun test ajouté : la justesse d'une nature se juge contre la note, qui n'est pas dans le dépôt.

## Décisions (L12, seconde note de montée GeoServer, 2026-11-17)
- Fiche voisine `geoserver/montee-2-28-3-a-3-0-1-bascule-et-production` plutôt qu'un ajout à `montee-2-28-3-a-3-0-2` (déjà 21 gestes) : 11 symptômes (cascade WMS à 180 s par fuite de baux du client HTTP de GeoTools 35.1, message de dimension TIME changé, erreur OWS sur deux lignes, `recalculate`, harvest de dossier en 202, `rasterManagers`, process imbriqués, couche absente du catalogue neuf, `$$`, SPI NetCDF et verrous JDBCConfig en 2.28.3) et 15 gestes, dont modules Java 17 sur JVM 21 et `@PostConstruct` non vérifié.
- Natures exactes de la note : `[commit]` (sha retiré, propre au dépôt de l'émetteur), `[notes de travail]`, `[mesure]`, `[lecture du code]` ; les deux dernières ajoutées à `NATURE` et à `docs/format-fiche.md`. Une détection absente de la note → `[déduction]` ou `[fiche <slug>]`. Rien n'a été relu ici.
- Source de la voisine : ce qui recoupe (mot pour mot, même recette probable : **pas une confirmation indépendante**) et ce qui contredit la fiche 3.0.2 (palier 2.28.5 jamais en production, versions 2.28.3, 500 « Unknown layer » et JSON indenté non observés, `context.xml` non vérifié lu, plugins Java 17), plus les écarts avec les fiches de piège voisines (202 au lieu de 200, autre cause et autre geste pour `rasterManagers`, récidive NetCDF malgré `indexer.properties`).
- Fiche 3.0.2 : renvoi en tête, nuances aux Symptôme 8, Geste 10 et Geste 21 (`[fiche …]`), versions 2.28.3 ajoutées ; fiches de piège voisines non modifiées.
- Test : `MONTEES` + la voisine ; `test_seconde_note_geoserver_situee`.
- `.termes-prives` absent du clone : copié depuis le dépôt principal (ignoré par git).

## Décisions (correction de la revue L12, 2026-11-17)
- Fiche 3.0.2, Geste 12 : la matrice couche × style complète trois fois et le rendu au pixel, repris de la seconde note `[fiche montee-2-28-3-a-3-0-1-bascule-et-production]`, avec la réserve « même recette probable, pas une confirmation indépendante ». Le recoupement annoncé par la Source de la voisine existe donc dans la fiche.
- Voisine, Geste 15 : « Non mesurés » ne porte plus `[notes de travail]` (la note ne donne aucune nature à cette ligne) mais le mot de la note, « non attestés », sans crochets (pas de nature neuve).
- Test `test_corrections_revue_l12`. `.termes-prives` recopié depuis le dépôt principal (ignoré par git).

## Décisions (L6, mémoires de dépannage reçues le 2026-11-19)
- Pièces : `geoserver.md` (G1–G7) et `openlayers.md` (O1–O4) du compte pro. Le titre du lot disait 8 entrées GeoServer : le pro en a écarté une (LayerNotDefined, propre à son environnement).
- 10 fiches neuves, une par cas : G1 en `postgis/` (cause et geste dans les données : `ST_Subdivide` sans `ST_Segmentize`), G2–G7 en `geoserver/`, O1, O2, O4 en `openlayers/` ; nouvelle section d'index « navigation et antiméridien ».
- Doublons : O3 (`+axis=neu`, EPSG:3034) fusionnée dans `openlayers/source-wms-projection-de-la-vue` (même piège) : côté GeoServer, `WMS.toInternalSRS` (lu ici) lit la BBOX 1.3.0 nord d'abord ; la fiche reste « à reprouver » (cisaillement vécu en 3035 non rejoué). G4 (CSRF Wicket) prouve les pistes « non appliquées » du point 7 de `montee-2-28-3-a-3-0-2`, qui renvoie à elle. O1 gardée à part (symptôme différent), son mécanisme renvoie à la fiche existante.
- Liens : G1↔O1, G6↔G1 dans les deux sens ; G3 → `replicas-convergence-du-catalogue`, G5 → `ordre-des-elements-rastersymbolizer`.
- Références fichier:ligne relues ici le 2026-11-19 aux tags GeoServer 3.0.2, GeoTools 35.2, Wicket 10.11.0, OpenLayers 10.11.0 (écarts de ±2 lignes corrigés aux nôtres) ; mesures et preuves `curl` / Playwright des notes non rejouées. Ce qui vient de moi sans être dans la note est marqué « déduction » ou « explication probable ».
- Liens de doc vers `github.com/geoserver/geoserver/blob/3.0.2/doc/…` : `docs.geoserver.org/latest/en/user/…*.html` répond 404 le 2026-11-19 (y compris des liens de fiches plus anciennes, non corrigés : hors lot).
- `.cadence/raf.yaml` : un nom de machine dans un verdict de revue (commit de plan de L12) faisait échouer `test_aucun_terme_interdit` ; remplacé par « la machine d'outillage ». `.termes-prives` recopié depuis le dépôt principal (ignoré par git).
- Test `test_memoires_de_depannage_l6`.

## Décisions (L13, suites de la revue L6, 2026-11-19)
- Fiches G3, G1, G7, O1, O2 : citations des notes reprises mot pour mot (`store … sees no table (HTTP 000000)`, « regarder l'image », `labeling.md:441-443` avec `?plain=1#L441-L443`, « le code qui dessine le contour ») ; ajouts de notre cru marqués « déduction » dans leur phrase (origine des 409, borne des reprises, magasins conditionnés, unité de `ST_Segmentize`, « source XYZ », « OpenLayers n'y est pour rien »). Test `test_lettre_des_notes_revue_l6`.
- G7 : la revue disait que `geowebcache/webadmin/defaults.md` (3.0.2) ne parle pas du gutter ; il le fait (« Default gutter size », l. 137-139, relu le 2026-11-19) : source gardée, ancre de ligne ajoutée.
- `.cadence/demandes/D-1.json` non réindenté : la porte refuse toute modification du registre dans un run lancé par une consigne du lead (sans `--demande-humaine` ni `--registre`). La remise à 2 espaces (mineur M7 de la revue L6) reste à faire par un geste autorisé à toucher le registre.
- Messages de commit : `hooks/commit-msg` (Python, même lecture de la liste que les tests, repli sur le `.termes-prives` du clone principal pour un worktree, refus sans liste) posé par `hooks/installer.sh` comme relais dans le dossier de hooks commun (n'écrase pas un autre `commit-msg`, pas de `core.hooksPath` qui court-circuiterait les hooks de raf). Posé dans le clone principal le 2026-11-19. `tests/test_messages_de_commit.py` : refus et acceptation par le hook, vrai `git commit` dans un dépôt jetable et dans un worktree, et relecture de tout `git log` ; seules exceptions, les deux commits de plan déjà publiés avec un nom d'hôte (décision de Sylvain, pas de réécriture).
