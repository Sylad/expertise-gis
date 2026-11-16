# Index des fiches, par symptôme

Une fiche par piège, au format de [`docs/format-fiche.md`](../docs/format-fiche.md).
Statut : ✅ prouvé · 🔁 à reprouver (établi sur une version ancienne, ou cause non démontrée).

## La carte n'affiche rien, ou une image fausse

- ✅ Le client dit « image cannot be decoded », la sonde voit 200 → [erreur-wms-http-200-en-xml](geoserver/erreur-wms-http-200-en-xml.md)
- 🔁 GetMap en erreur « No such resource: X.sld » avec `STYLES=` vide → [style-par-defaut-fichier-sld-absent](geoserver/style-par-defaut-fichier-sld-absent.md)
- 🔁 Style listé par REST mais « StyleNotDefined » au rendu → [rest-style-cree-avec-raw-true-introuvable](geoserver/rest-style-cree-avec-raw-true-introuvable.md)
- 🔁 Style modifié par REST, rendu avec l'ancienne version → [jdbcconfig-sld-disque-perime](geoserver/jdbcconfig-sld-disque-perime.md)
- ✅ `SLD_BODY` sans effet, rendu avec le style par défaut → [endpoint-workspace-ignore-sld-body](geoserver/endpoint-workspace-ignore-sld-body.md)
- 🔁 Image GeoTIFF rendue d'une seule couleur, sonde verte → [imagemosaic-suggestedspi-netcdf-sur-geotiff](geoserver/imagemosaic-suggestedspi-netcdf-sur-geotiff.md)
- ✅ Image en trois bandes verticales répétées → [geotiff-multibande-planaire-bandes-repetees](geoserver/geotiff-multibande-planaire-bandes-repetees.md)
- ✅ Flèches et barbules mal orientées hors de Web Mercator → [rotation-de-marque-azimut-vrai-hors-mercator](sld/rotation-de-marque-azimut-vrai-hors-mercator.md)
- ✅ Légende (`GetLegendGraphic`) en exception, carte correcte → [getlegendgraphic-attributs-nuls](sld/getlegendgraphic-attributs-nuls.md)
- ✅ Chaîne construite (WKT) mal formée, espace disparu → [literal-espace-seul-vide](sld/literal-espace-seul-vide.md)
- ✅ Décoration `legend` qui couvre la carte, « Could not find decoration layout » → [decoration-legend-sans-filtre-de-couches](geoserver/decoration-legend-sans-filtre-de-couches.md)

## Le raster est pixelisé ou en escalier

- ✅ `INTERPOLATION=bicubic` sans effet → [interpolations-au-pluriel](geoserver/interpolations-au-pluriel.md)
- 🔁 Classes de couleur en marches malgré la VendorOption `interpolation` → [interpolation-avant-ou-apres-colormap](geoserver/interpolation-avant-ou-apres-colormap.md)
- 🔁 Transformation qui produit des blocs, reçoit une couverture suréchantillonnée → [lecture-native-coverage-reading-transformation](geoserver/lecture-native-coverage-reading-transformation.md)
- 🔁 `ChannelSelection` ou `ContrastEnhancement` sans effet → [ordre-des-elements-rastersymbolizer](sld/ordre-des-elements-rastersymbolizer.md)

## Le temps (dimension TIME, animation) est faux

- ✅ Une seule validité par jour, à 00:00 → [imagemosaic-index-shapefile-perd-l-heure](geoserver/imagemosaic-index-shapefile-perd-l-heure.md)
- ✅ Nouvelles validités jamais publiées malgré un harvest « OK » → [imagemosaic-harvest-200-sans-indexation](geoserver/imagemosaic-harvest-200-sans-indexation.md)
- 🔁 Couche temporelle absente des capabilities, visible par REST → [dimension-time-nearest-sans-reference](geoserver/dimension-time-nearest-sans-reference.md)
- 🔁 Animation d'une couche en cascade : même image à chaque instant → [cascade-wms-time-non-transmis](geoserver/cascade-wms-time-non-transmis.md)
- 🔁 REST 500 `UnsupportedOperationException` sur une couche en cascade → [cascade-wms-rest-metadata-500](geoserver/cascade-wms-rest-metadata-500.md)

## C'est lent, ou ça sature

- ✅ GetCapabilities d'une minute, CPU au repos, amont en cascade en panne → [capabilities-lentes-amont-cascade-en-panne](geoserver/capabilities-lentes-amont-cascade-en-panne.md)
- ✅ Capabilities de 8–22 s, tri sur disque côté base → [capabilities-lentes-dimension-time-sur-vue](geoserver/capabilities-lentes-dimension-time-sur-vue.md)
- ✅ Rafales de tuiles : 502 en cascade, d'autres couches disparaissent → [rafales-de-tuiles-sur-rendu-lourd](geoserver/rafales-de-tuiles-sur-rendu-lourd.md)
- 🔁 Rendu de 10–20 s avec une interpolation IDW → [idw-sur-grille-dense](sld/idw-sur-grille-dense.md)
- ✅ Flot de lignes TRACE dans le journal → [journal-level-vide-trace](geoserver/journal-level-vide-trace.md)
- 🔁 Rechargements du catalogue en boucle sur chaque réplica → [grappe-hazelcast-sync-reload](geoserver/grappe-hazelcast-sync-reload.md)
- ✅ Échecs qui changent de couche à chaque passage, « too many connections for role » → [limite-de-connexions-du-role-geoserver](geoserver/limite-de-connexions-du-role-geoserver.md)

## Mémoire et démarrage

- 🔁 `OutOfMemoryError` à ~1 Go malgré `-Xmx6g` → [image-officielle-extra-java-opts-ecrase-xmx](geoserver/image-officielle-extra-java-opts-ecrase-xmx.md)
- ✅ Pod `OOMKilled` sans erreur Java → [jvm-limite-memoire-conteneur](geoserver/jvm-limite-memoire-conteneur.md)
- ✅ `NameNotFoundException` JNDI, repli sur localhost → [image-officielle-context-xml-ignore-jndi](geoserver/image-officielle-context-xml-ignore-jndi.md)
- ✅ « Cannot load java class » après un renommage de classe → [catalogue-persiste-noms-de-classes](geoserver/catalogue-persiste-noms-de-classes.md)
- 🔁 `NoClassDefFoundError` après ajout d'un module communautaire → [modules-communautaires-version-exacte](geoserver/modules-communautaires-version-exacte.md)
- 🔁 « Hazelcast Clustering has not been enabled », démarrage interminable → [grappe-hazelcast-enabled-false-insuffisant](geoserver/grappe-hazelcast-enabled-false-insuffisant.md)
- ✅ Réplicas seuls dans leur grappe, configuration de grappe ignorée → [grappe-hazelcast-config-et-jdbcstore](geoserver/grappe-hazelcast-config-et-jdbcstore.md)
- ✅ Pod figé mais toujours « Ready » → [sonde-index-html-reste-verte](geoserver/sonde-index-html-reste-verte.md)

## La configuration ne prend pas, ou se perd

- 🔁 Variables `GEOSERVER_JDBCCONFIG_*` ignorées, ancienne base utilisée → [jdbcconfig-fichiers-priment-sur-env](geoserver/jdbcconfig-fichiers-priment-sur-env.md)
- ✅ Fichier du data dir corrigé, aucun effet → [jdbcstore-fichiers-servis-depuis-la-base](geoserver/jdbcstore-fichiers-servis-depuis-la-base.md)
- 🔁 Configuration GWC posée par REST perdue au redémarrage → [rest-put-config-gwc-non-persistante](geoserver/rest-put-config-gwc-non-persistante.md)
- ✅ Cache de tuiles local qui grossit malgré un magasin S3 « par défaut » → [gwc-magasin-par-defaut-non-utilise](geoserver/gwc-magasin-par-defaut-non-utilise.md)
- ✅ Élément du SLD absent à la relecture REST → [rest-get-style-sans-raw-reencode](geoserver/rest-get-style-sans-raw-reencode.md)
- ✅ 500 « already exists » juste après un DELETE, réplicas incohérents → [replicas-convergence-du-catalogue](geoserver/replicas-convergence-du-catalogue.md)
- ✅ Harvest en 500 « rasterManagers is null » une fois sur N → [imagemosaic-rastermanagers-null-sur-un-replica](geoserver/imagemosaic-rastermanagers-null-sur-un-replica.md)
- ✅ Emprise des capabilities restée l'ancienne, tuiles jamais en cache → [imagemosaic-emprise-declaree-figee](geoserver/imagemosaic-emprise-declaree-figee.md)

## Données vecteur (WFS, filtres)

- ✅ « Illegal property name » sur un filtre CQL → [postgis-cle-primaire-non-exposee](geoserver/postgis-cle-primaire-non-exposee.md)
- 🔁 « column … does not exist » après un ALTER TABLE → [featuretype-schema-perime-apres-alter](geoserver/featuretype-schema-perime-apres-alter.md)
- 🔁 Colonne JSONB reçue en chaîne → [wfs-json-colonne-jsonb-en-chaine](geoserver/wfs-json-colonne-jsonb-en-chaine.md)

## Sécurité et mots de passe

- ✅ Ancien mot de passe admin toujours accepté → [mot-de-passe-admin-jdbcstore](geoserver/mot-de-passe-admin-jdbcstore.md)
- ✅ `EncryptionOperationNotPossibleException` sur tous les magasins PostGIS → [cle-maitre-perdue-mots-de-passe-illisibles](geoserver/cle-maitre-perdue-mots-de-passe-illisibles.md)

## Cache et CDN

- ✅ `cf-cache-status: DYNAMIC` sur toutes les tuiles → [cdn-getmap-non-mis-en-cache](geoserver/cdn-getmap-non-mis-en-cache.md)
- ✅ `geowebcache-cache-result: MISS` figé à travers le CDN → [cdn-rejoue-en-tete-gwc](geoserver/cdn-rejoue-en-tete-gwc.md)

## Modules Java maison (processus, transformations, extensions)

- ✅ Transformation maison : `data` nul ou « Parameter data is missing » → [transformation-raster-coverage-source-non-injecte](geoserver/transformation-raster-coverage-source-non-injecte.md)
- ✅ Transformation sur vecteur : emprise infinie ou attribut nul → [transformation-vecteur-invertquery](geoserver/transformation-vecteur-invertquery.md)
- 🔁 Transformations imbriquées : l'intérieure ne reçoit rien → [transformations-imbriquees-sans-injection](sld/transformations-imbriquees-sans-injection.md)
- ✅ Processus absent des capabilities WPS, « Unable to find function » → [processfactory-bean-spring-seul-ignore](geoserver/processfactory-bean-spring-seul-ignore.md)
- ✅ `MultipleBeansException`, `GWC.get()` nul, application qui ne démarre pas → [plugin-java-recherche-de-beans](geoserver/plugin-java-recherche-de-beans.md)
- 🔁 `DispatcherCallback` qui ne se déclenche jamais → [dispatchercallback-init-avant-analyse-kvp](geoserver/dispatchercallback-init-avant-analyse-kvp.md)
- ✅ Messages INFO d'un module invisibles → [journal-plugin-hors-org-geoserver-filtre](geoserver/journal-plugin-hors-org-geoserver-filtre.md)

## PostgreSQL / PostGIS / TimescaleDB

- ✅ Tables créées dans `public` au lieu du schéma voulu → [search-path-schema-sans-usage-ignore](postgis/search-path-schema-sans-usage-ignore.md)
- ✅ `syntax error at or near "$"` dans un Job Kubernetes → [dollar-dollar-reduit-par-kubernetes](postgis/dollar-dollar-reduit-par-kubernetes.md)
- ✅ Bloc `DO` annulé en silence par un `ALTER SEQUENCE … OWNER` → [alter-sequence-owner-sequence-liee](postgis/alter-sequence-owner-sequence-liee.md)
- ✅ « relation … already exists » après un RENAME TABLE → [rename-table-garde-les-noms-d-index](postgis/rename-table-garde-les-noms-d-index.md)
- ✅ « cannot create a unique index without the column » sur une hypertable → [timescaledb-index-unique-sans-colonne-de-temps](postgis/timescaledb-index-unique-sans-colonne-de-temps.md)
