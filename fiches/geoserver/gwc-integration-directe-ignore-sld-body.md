# SLD_BODY ignoré en silence quand l'intégration directe de GeoWebCache prend la requête

## Symptôme
Un GetMap avec `SLD_BODY` modifié répond 200 avec le style **par défaut** de la couche :
0 pixel de la couleur témoin. Aucune erreur.

## Cause
Quand l'intégration directe de GeoWebCache au WMS est active, `CachingWebMapService` confie à
GWC toute requête GetMap tuilée et alignée sur une grille (`TILED=true`, ou toute requête
alignée si `requireTiledParameter` est faux). Dans `org.geoserver.gwc.GWC`, la vérification
qui écarterait les requêtes portant `SLD` ou `SLD_BODY` est **en commentaire**
(« REVISIT: should these be taken into account? ») : GWC sert alors la tuile du cache, ou la
rend avec le style de la couche, sans tenir compte de `SLD_BODY`. Rien dans ce code ne
distingue `/geoserver/wms` de `/geoserver/<ws>/wms` : l'adresse ne protège pas.

Observation non expliquée : sur le banc qui a révélé le piège, la même requête montrait la
modification sur `/geoserver/wms` et pas sur `/geoserver/<ws>/wms` (en-tête
`geowebcache-cache-result: MISS` présent sur la seconde). La condition établie par le code est
la prise en charge par GWC, pas l'adresse.

Autres pièges du même banc (observés) :
- le `NamedLayer/Name` du SLD doit être le nom de la couche, sinon le style est ignoré sans erreur ;
- au-delà de ~8 Ko, l'URL est refusée (414) : passer en `POST` form-urlencoded ; ce `POST`
  n'a pas été honoré sur l'adresse d'espace de travail.

## Détection
- En-tête `geowebcache-cache-result` présent sur la réponse ⇒ GWC a pris la requête.
- Compter les pixels d'une couleur témoin introduite dans le `SLD_BODY`.

## Geste
Tout banc d'essai de style :
- envoyer une requête que GWC ne prend pas : sans `TILED=true` (avec `requireTiledParameter`
  laissé vrai), ou non alignée sur une grille, ou avec un paramètre absent des
  `parameterFilters` de la couche ;
- vérifier l'absence de l'en-tête `geowebcache-cache-result` ;
- contrôler le contenu (pixels de la couleur témoin) avant de croire un rendu.

## Versions concernées
GeoServer 3.0.1 (code gs-gwc relu, et vécu). Versions antérieures non vérifiées.

## Source
- Code source : `org.geoserver.gwc.GWC` (vérification de `SLD` / `SLD_BODY` en commentaire) et
  `org.geoserver.gwc.wms.CachingWebMapService` (condition tuilée / `requireTiledParameter`),
  module `src/gwc` de https://github.com/geoserver/geoserver, relus en 3.0.1.
- vécu 2026-09-16 et 2026-09-21 (GeoServer 3.0.1 ; 0 contre 19 335 pixels de la couleur témoin).

## Statut
à reprouver — la condition tirée du code n'a pas été rejouée sur un banc (requête tuilée contre
non tuilée sur la même adresse) ; l'écart entre adresses observé reste non expliqué.
