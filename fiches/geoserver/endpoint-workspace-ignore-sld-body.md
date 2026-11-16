# SLD_BODY ignoré en silence sur l'adresse WMS d'un espace de travail

## Symptôme
Un GetMap avec `SLD_BODY` modifié répond 200 avec le style **par défaut** : 0 pixel de la
couleur témoin. Le même GetMap sur `/geoserver/wms` montre la modification.

## Cause
Sur `/geoserver/<ws>/wms`, l'intégration directe de GeoWebCache sert l'image sans tenir
compte de `SLD_BODY` (en-tête `geowebcache-cache-result: MISS` présent). Le SLD est pourtant
analysé (un SLD invalide lève bien une `ServiceException`). Autres pièges du même banc :
- le `NamedLayer/Name` du SLD doit être le nom de la couche, sinon le style est ignoré sans erreur ;
- au-delà de ~8 Ko, l'URL est refusée (414) : passer en `POST` form-urlencoded sur
  `/geoserver/wms` (le `POST` n'est pas honoré non plus sur l'adresse d'espace de travail).

## Détection
Compter les pixels d'une couleur témoin introduite dans le `SLD_BODY` ; présence de l'en-tête
`geowebcache-cache-result` sur la réponse.

## Geste
Tout banc d'essai de style : `GET` (ou `POST` form) sur `/geoserver/wms` ou `/geoserver/ows`,
jamais sur l'adresse d'un espace de travail, et un contrôle de contenu (pixels) avant de croire
un rendu.

## Versions concernées
GeoServer 3.0.1 (vécu).

## Source
vécu 2026-09-16 et 2026-09-21 (GeoServer 3.0.1 ; 0 contre 19 335 pixels de la couleur témoin).

## Statut
prouvé
