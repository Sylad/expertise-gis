# Une erreur WMS arrive en HTTP 200 avec un corps XML, pas une image

## Symptôme
Le client ne montre rien ou affiche une erreur de décodage : `EncodingError: The source
image cannot be decoded` (OpenLayers), `InvalidStateError: The source image could not be
decoded` (MapLibre). La couche disparaît sans message côté serveur visible du client. Une
sonde qui ne regarde que le code HTTP voit `200` et conclut « ça marche ».

## Cause
Pour un GetMap en échec, GeoServer renvoie par défaut une `ServiceExceptionReport` en
**HTTP 200** avec `Content-Type: text/xml` (ou `application/vnd.ogc.se_xml`) au lieu de
l'image (`EXCEPTIONS=application/vnd.ogc.se_xml`, défaut WMS). Le client tente de décoder
le XML comme un PNG. Causes vues derrière : `java.lang.OutOfMemoryError: Java heap space`
pendant une transformation de rendu, style introuvable, transformation inconnue, dépassement
de délai.

## Détection
```bash
curl -s "<url GetMap exacte, copiée de l'onglet réseau>" -o probe.bin \
  -w "HTTP %{http_code} type=%{content_type} size=%{size_download}\n"
file probe.bin          # « XML 1.0 document » = erreur masquée
head -c 800 probe.bin   # la ServiceException donne la vraie cause
```
Un succès a `type=image/png` (ou le format demandé) ; une erreur a `text/xml`.

## Geste
- Toujours vérifier le `Content-Type` d'un rendu, pas seulement le code HTTP ; une sonde
  qui accepte un 200 en XML est fausse.
- Lire la `ServiceException` et traiter la vraie cause (mémoire : voir
  [jvm-limite-memoire-conteneur](jvm-limite-memoire-conteneur.md) ; taille demandée trop
  grande : réduire la surface, par exemple le `ratio` d'une `ImageWMS` OpenLayers de 1,2 à
  1,0, ou poser une taille maximale de rendu dans la config WMS).
- Pour qu'un client échoue franchement : `EXCEPTIONS=application/vnd.ogc.se_inimage` (erreur
  dessinée dans l'image) ou un contrôle du type de contenu côté client.
- Derrière un CDN, cette réponse 200 peut être mise en cache : voir
  [cdn-getmap-non-mis-en-cache](cdn-getmap-non-mis-en-cache.md).

## Versions concernées
GeoServer 2.28.3 (vécu) ; comportement WMS par défaut, attendu sur toutes les versions.

## Source
- vécu 2026-05-14 (GeoServer 2.28.3, 2 Go de tas, image plein écran 4K avec transformation lourde).
- https://docs.geoserver.org/latest/en/user/services/wms/reference.html (paramètre `EXCEPTIONS`).

## Statut
prouvé
