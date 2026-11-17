# GeoServer 2.28.3 → 3.0.1 en production : cascade WMS à 180 s, message de dimension TIME changé, erreur OWS sur deux lignes

Fiche voisine de [montee-2-28-3-a-3-0-2](montee-2-28-3-a-3-0-2.md), tirée d'un **second**
retour d'expérience reçu le 2026-11-17 : même montée 2.28.3 → 3.0.1 (bascule directe le
2026-09-08), puis deux mois de production en 3.0.1 ; pas de 3.0.2. Image dérivée de l'image
officielle, trois réplicas en grappe hz-cluster, catalogue JDBCConfig / JDBCStore sous
PostgreSQL, GeoWebCache sur S3, WPS et control-flow, ImageMosaic à index PostGIS alimentées
par REST, couches WMS en cascade, trois modules Java maison. Natures de source de cette note,
entre crochets : [commit] (message ou diff), [notes de travail] (pièges, runbooks, README
écrits au moment des faits), [mesure] (production ou banc), [lecture du code] (relu pour la
note, pas exécuté) ; [fiche <slug>] = repris d'une fiche de ce dépôt ; [déduction] = ajouté
ici, absent de la note. Sauf mention, constaté sous 3.0.1 **sans comparaison avec 2.28** :
des comportements de 3.0.1, pas forcément des régressions.

## Symptôme
1. Couche WMS en cascade à **180 s** par GetMap, sur tous les réplicas, après des erreurs du
   serveur amont. [commit] [mesure]
2. Une sonde qui classe les erreurs GeoServer par texte prend une dimension hors plage pour
   une panne : 2.x disait « Could not find match for time », 3.0.1 dit « Could not find a
   match for 'time' value » (dimension sans `nearestMatch`). [commit] [mesure]
3. Un analyseur de journaux qui lit ligne à ligne perd des erreurs OWS : en 3.0.1, l'en-tête
   de l'erreur peut être vide, le message est sur la ligne suivante. Cause d'erreur nouvelle
   relevée au banc : store JDBC non disposé. [commit] [mesure, au banc]
4. `PUT …/coverages/<c>.xml?recalculate=nativebbox,latlonbbox` sur une ImageMosaic à index
   PostGIS : 200, rien ne change, même après `POST …/coveragestores/<s>/reset` ; l'emprise
   reste celle de la création, les tuiles hors emprise ne sont pas servies. [commit] [mesure]
5. `POST …/external.imagemosaic` avec le **dossier** de la mosaïque : **202**, mais plus
   aucun granule n'entre dans l'index (deux jours) ; `reset` du store sans effet. [commit]
   [mesure]
6. Automate REST derrière le Service : `DELETE` d'un store puis `POST` de recréation 7 ms
   plus tard sur un autre réplica → 500 « already exists » ; harvest juste après la création,
   ou sur un store existant depuis des jours sur **un seul** réplica → 500 `Cannot invoke
   "java.util.Map.get(Object)" because "this.rasterManagers" is null`. [commit] [notes de
   travail] [mesure]
7. Toujours cassé en 3.0.1 (vécu dès 2.28, pas une régression) :
   `ras:Contour(data = vec:BarnesSurface(…))` ou `ras:Contour(data = <process raster>(…))`
   dans un SLD → « Parameter data is missing but has min multiplicity > 0 ». [commit] [notes
   de travail]
8. Sur le catalogue neuf, une couche que seul son producteur de données créait reste en 404
   jusqu'au cycle suivant de ce producteur. [commit] [notes de travail]
9. SQL d'initialisation de la base passé en arguments de conteneur : dollar-quoting `$$…$$`
   invalide. Ce script n'avait jamais servi (base de production restaurée, pas
   initialisée). [commit] [notes de travail]
10. Encore en 2.28.3, juste avant la bascule : mosaïque de GeoTIFF rendue uniforme (lue comme
    des zéros), `SuggestedSPI=NetCDFImageReaderSpi` réécrit par le harvest dans le
    `.properties`, **trois récidives malgré `indexer.properties`**. [commit] [mesure]
11. Encore en 2.28.3 : provisionnement lancé pendant le redémarrage des réplicas, « Time-out
    waiting for lock on GeoServerInfo.global », appels REST de plus de 15-30 s ; un `DELETE`
    « abandonné » par le client a abouti, un `PUT` est arrivé 30 s après la fin du job ; style
    purgé jamais réécrit, job sorti en succès. [commit] [mesure]

## Cause
1. `MultithreadedHttpClient.get/post` de GeoTools 35.1 jette sur un 503 / 404 amont **sans
   fermer la réponse** : le bail de connexion fuit ; après `maxConnections` (6) réponses en
   erreur, chaque requête attend `ConnectionRequestTimeout` (180 s). Diagnostic fait dans les
   sources de GeoTools 35.1 par l'émetteur, non relu ici. [commit] [mesure]
2. Formulation du message changée entre 2.x et 3.0.1 ; le même message existe pour
   ELEVATION et les dimensions personnalisées. [commit] [mesure]
3. Format de la ligne d'erreur OWS du journal en 3.0.1 (en-tête vide, message à la ligne
   suivante). [commit] [mesure, au banc]
4. Le `.properties` de la mosaïque n'a pas d'`Envelope2D` et porte « `Estimated
   extends=false` » (graphie de la note) : le lecteur garde son emprise d'origine. [commit]
   [mesure]
5. Non établie par la note (code 202 sans indexation, dossier seulement). [déduction]
6. Les requêtes REST passent par le Service et tombent sur des réplicas dont le cache de
   catalogue n'a pas encore reçu l'événement Hazelcast [commit] [notes de travail] ; lecteur
   mort : disposé par un événement de catalogue pendant un accès, mais resté dans le cache de
   ressources du nœud [commit] [mesure].
7. Le moteur évalue le process interne sans son `data` :
   `ProcessFunction.evaluateInputs(null)` depuis `invertQuery` du process externe. [commit]
   [notes de travail] [fiche transformations-imbriquees-sans-injection]
8. Un catalogue neuf ne contient que ce que le provisionnement déclare ; une couche créée
   par son producteur n'existe qu'après le passage de celui-ci. [commit] [notes de travail]
9. Kubernetes réduit `$$` en `$` dans `args`. [commit] [notes de travail] [fiche
   dollar-dollar-reduit-par-kubernetes]
10. Détection de format non déterministe au harvest quand les extensions NetCDF / GRIB sont
    installées sans servir. [commit] [mesure]
11. Contention des verrous JDBCConfig au redémarrage ; un délai côté client n'annule pas la
    requête côté serveur. [commit] [mesure]

## Détection
1. Sonde de production en échec, puis diagnostic dans les sources. [commit] [mesure] Durée
   du GetMap en cascade proche de 180 s (`curl -w '%{time_total}'`) après au moins six
   réponses non-200 de l'amont = piège. [déduction, d'après la cause 1]
2. Lister les textes d'erreur GeoServer reconnus par les sondes et les comparer à la version
   visée (`grep -rn "Could not find" <sources des sondes>`). [déduction]
3. Rechercher dans le journal les erreurs OWS dont la ligne d'en-tête n'a pas de message ;
   le message est sur la ligne suivante. [déduction, d'après le symptôme 3]
4. Comparer l'emprise des capabilities à `ST_Extent` de l'index [fiche
   imagemosaic-emprise-declaree-figee] ; `grep Envelope2D <dossier>/<store>.properties` vide =
   cause 4. [déduction]
5. Index figé alors que les fichiers arrivent sur le disque. [commit] [mesure] Compter les
   granules avant et après chaque harvest [fiche imagemosaic-harvest-200-sans-indexation].
6. Interroger chaque réplica par l'adresse de son pod, pas par le Service [fiche
   replicas-convergence-du-catalogue] ; `rasterManagers` dans le journal d'un seul réplica
   [fiche imagemosaic-rastermanagers-null-sur-un-replica].
7. Lire le corps de la réponse GetMap, pas seulement son code. [fiche
   transformations-imbriquees-sans-injection]
8. Redémarrer sur un catalogue vide, provisionnement seul, producteurs arrêtés, et comparer
   `/rest/layers.json` à la liste attendue. [déduction, d'après la règle du geste 8]
9. `kubectl get pod <pod> -o jsonpath='{.spec.containers[0].args[0]}'` : texte reçu par le
   conteneur. [fiche dollar-dollar-reduit-par-kubernetes]
10. `grep SuggestedSPI <dossier>/<store>.properties` ; nombre de couleurs de l'image. [fiche
    imagemosaic-suggestedspi-netcdf-sur-geotiff]
11. Relire après la fin du job ce qu'il a écrit ; « Time-out waiting for lock » dans le
    journal pendant le redémarrage. [déduction, d'après le symptôme 11]

## Geste
1. Immédiat : un `PUT` idempotent du store WMS recrée le pool (200 en 0,2 s). Durable :
   client HTTP de remplacement qui ferme la réponse avant de jeter et borne l'attente d'un
   bail au délai de connexion. Non vérifié sur GeoTools 34.x. [commit] [mesure]
2. Ajouter la formulation 3.0.1, restreinte à la dimension `time`. Tout classement d'erreurs
   GeoServer par texte se relit à chaque montée. [commit] [mesure]
3. L'analyseur prend la ligne suivante quand l'en-tête d'une erreur OWS est vide. [commit]
   [mesure, au banc]
4. **Poser** l'emprise : `<nativeBoundingBox>` et `<latLonBoundingBox>` explicites, sans
   `recalculate` ; valeur = union de l'emprise déclarée et de `ST_Extent` de l'index
   (monotone : un granule manquant un instant ne rétrécit pas l'emprise) ; `PUT` seulement si
   le SRS natif est EPSG:4326 (`ST_Extent` est en degrés). [commit] [mesure]
5. Harvester **chaque fichier** écrit (même `POST` avec le chemin du fichier ; idempotent,
   pas de doublon) ; le dossier seulement à la création du store ; réconciliation index ↔
   disque à chaque cycle. [commit] [mesure]
6. Convergence : attendre **6 lectures consécutives** dans l'état voulu avant l'étape
   suivante ; réessayer le seul 500 `rasterManagers` jusqu'à un plafond, toute autre erreur
   remonte [commit] [notes de travail]. Lecteur mort : un `PUT` du coveragestore, même sans
   changement, est un événement propagé à tous les réplicas et évince le lecteur ; puis
   **une** nouvelle tentative, sinon l'erreur remonte [commit] [mesure].
7. Un seul process Java qui délègue aux deux calculs. [commit] [notes de travail]
8. Déclarer la couche dans le provisionnement du catalogue : un catalogue neuf doit pouvoir
   être reconstruit entier par le provisionnement, sans attendre les producteurs. [commit]
   [notes de travail]
9. Étiquettes nommées `$fn$…$fn$`. [commit] [notes de travail]
10. Retirer de l'image les extensions qui ne servent pas (fait dans l'image 3.0.1) **et**
    écrire `SuggestedFormat` + `SuggestedSPI` explicites dans `indexer.properties`. [commit]
    [mesure]
11. Plus aucun `DELETE` ; comparer puis écrire, relecture bit à bit, tout écart = échec
    visible ; délais d'écriture de 120 s. [commit] [mesure]
12. Modules Java maison : compilés en **Java 17**, ils ont tourné tels quels sur la JVM 21 de
    l'image 3.0.1 (bytecode compatible) ; la bascule n'a pas exigé de les recompiler pour
    Java 21. [commit] [mesure : en production depuis le 2026-09-08] Les modules écrits après
    sont compilés en 21. [commit] [lecture du code]
13. Initialisation au démarrage par `ApplicationListener<ContextRefreshedEvent>`, pas par
    `@PostConstruct` (qui se déclenche avant que les beans de GeoServer soient prêts) : rien à
    passer de `javax.annotation` à `jakarta.annotation`. Ce que Spring 7 fait d'un
    `@PostConstruct` en `javax.annotation` : **non vérifié**, à contrôler dans un module qui en
    dépend. [lecture du code]
14. Marches : palier 2.28.5 construit et démarré **en local seulement** ; production passée
    de 2.28.3 à 3.0.1 **en une fois**, sur un catalogue neuf (schéma PostgreSQL séparé) et un
    volume neuf, répétée d'abord dans un espace de noms isolé ; retour arrière = tag 2.28,
    catalogue et volume intacts. Aucune commande de migration propre à GeoServer :
    variables de build, versions des poms, nouveau déploiement. [commit] [notes de travail]
15. Vérifications : matrice couche × style complète trois fois, rendu des isolignes et de
    l'interpolation identique au pixel face à 2.28, dimension TIME transmise aux serveurs
    cascadés, GeoWebCache S3, grappe formée [commit] ; smoke et tests d'animation rejoués, le
    moteur raster ayant changé (ImageN) [commit]. Derrière un CDN, en-tête
    `geowebcache-cache-result` lu avec un paramètre non déclaré dans les `parameterFilters` :
    `MISS` puis `HIT`, et `HIT` sur chaque réplica [notes de travail] [mesure] [fiche
    cdn-rejoue-en-tete-gwc]. Non mesurés : durée d'indisponibilité, retour arrière réel en
    2.28 (non attestés, dit la note).

## Versions concernées
GeoServer 2.28.3 → 3.0.1 (vécu, bascule le 2026-09-08 puis production jusqu'au 2026-11) ;
2.28.5 construite, jamais en production. GeoTools 34.3 → 35.1, GeoWebCache 1.28.2 → 2.0.1,
Spring 5.3.39 → 7.0.8, Jakarta / Tomcat 11, JVM 21, JAI → ImageN, Hazelcast 5.3.8,
JDBCConfig / JDBCStore 2.28.3 → 3.0.1, pilote PostgreSQL JDBC 42.7.4 inchangé, modules
maison en Java 17 sur la JVM 21 (vécu). Symptômes 10 et 11 : 2.28.3 seulement (vécu), 3.x non
vérifié. Fuite de baux : non vérifiée sur GeoTools 34.x. 3.0.2 : non vécu par cette équipe.

## Source
- Second retour d'expérience reçu le 2026-11-17 (vécu 2026-09-08 à 2026-10-18, GeoServer
  3.0.1, trois réplicas hz-cluster, catalogue JDBC ; natures de source citées point par point,
  aucune relue ici).
- Ce qui **recoupe** [montee-2-28-3-a-3-0-2](montee-2-28-3-a-3-0-2.md) (même fait, mêmes
  chiffres) : versions de 3.0.1 (GeoTools 35.1, GeoWebCache 2.0.1, Spring 7.0.8, Jakarta /
  Tomcat 11, Java 21, ImageN, Hazelcast 5.3.8) ; 2.28.4 abandonnée faute de modules
  communautaires publiés ; `curl --retry` sur SourceForge ; aucun changement de code des
  modules et `invertGridGeometry` ; catalogue neuf, retour arrière par le tag ; tables 2.28
  dans `public` et `search_path` ; `currentSchema` sans `,public` ; `ignoreDirs=…,cluster` ;
  `--add-opens` ; nom de grappe par version ; provisionnement non destructif ; matrice
  couche × style trois fois et rendu au pixel. Ces points sont presque mot pour mot ceux de la
  première note, avec les mêmes chiffres, vraisemblablement d'une même recette : leur accord
  n'est **pas une confirmation indépendante**.
- Ce qui **contredit** ou nuance [montee-2-28-3-a-3-0-2](montee-2-28-3-a-3-0-2.md) :
  (a) le palier 2.28.5 (Geste 10) n'a jamais tourné en production ici : il n'a rien prouvé
  en exploitation ; (b) en 2.28.3 : GeoTools 34.3, GeoWebCache 1.28.2, Spring 5.3.39 ;
  (c) GeoWebCache 3.0.1 « 500 Unknown layer, jamais 404 » (Symptôme 8) : non observé ici, un
  test local simule même un 400 jamais confronté au serveur, à vérifier avant de s'y fier ;
  (d) JSON indenté de `GetLegendGraphic` : ni confirmé ni contredit (non lu en JSON) ;
  (e) `context.xml` « compatible Tomcat 11 tel quel » : même réserve, copié n'est pas lu
  (Geste 21) ; (f) Java 21 de l'image : les modules compilés en 17 n'ont pas eu à être
  recompilés (Geste 12 ci-dessus).
- Ce qui recoupe les fiches de piège du dépôt, vécues sur la même topologie :
  [imagemosaic-emprise-declaree-figee](imagemosaic-emprise-declaree-figee.md) (la note ajoute
  la cause `Envelope2D` et la borne EPSG:4326),
  [imagemosaic-harvest-200-sans-indexation](imagemosaic-harvest-200-sans-indexation.md) (ici
  **202**, harvest d'un dossier, geste « chaque fichier »),
  [replicas-convergence-du-catalogue](replicas-convergence-du-catalogue.md),
  [imagemosaic-rastermanagers-null-sur-un-replica](imagemosaic-rastermanagers-null-sur-un-replica.md)
  (autre cause — lecteur disposé resté en cache — et autre geste — `PUT` du coveragestore
  propagé, au lieu d'un `reset` sur le seul réplica),
  [transformations-imbriquees-sans-injection](../sld/transformations-imbriquees-sans-injection.md),
  [imagemosaic-suggestedspi-netcdf-sur-geotiff](imagemosaic-suggestedspi-netcdf-sur-geotiff.md)
  (récidives malgré `indexer.properties` : retirer aussi les extensions inutiles),
  [dollar-dollar-reduit-par-kubernetes](../postgis/dollar-dollar-reduit-par-kubernetes.md),
  [cdn-rejoue-en-tete-gwc](cdn-rejoue-en-tete-gwc.md).

## Statut
prouvé — vécu en 3.0.1 ; sauf les symptômes 10 et 11 (établis en 2.28.3, à reprouver en
3.x), la fuite de baux sur GeoTools 34.x et `@PostConstruct` en `javax.annotation` sous
Spring 7 (non vérifiés).
