# Transformations de rendu imbriquées : l'intérieure ne reçoit pas la source

## Symptôme
`ras:Contour(data = <ns>:Interpolation(…))` dans un `<Transformation>` : la transformation
intérieure reçoit une source vide (`data` nul ou manquant) ; le rendu échoue. Sur GeoServer
3.0.1, avec `ras:Contour(data = vec:BarnesSurface(…))` sur une couche de points, le message
est « Parameter data is missing but has min multiplicity > 0 ».

## Cause
GeoServer n'injecte la couche source que dans la transformation **la plus externe** ; une
transformation passée en paramètre d'une autre n'est pas reconnue comme transformation de rendu.
Mesuré sur 3.0.1 : avant `execute`, le moteur de rendu appelle `invertQuery` du processus
externe en évaluant ses entrées avec un contexte nul
(`ProcessFunction.evaluateInputs(null)`) ; le processus interne est alors évalué sans son `data`.

## Détection
Journal du processus intérieur : `data` nul ; ou l'exception ci-dessus dans le corps de la réponse GetMap
(lire le corps, pas seulement le code HTTP).

## Geste
Écrire un processus unique qui enchaîne les deux calculs en interne (par exemple interpolation
puis isolignes, en appelant `ContourProcess.process` depuis le code) et qui porte lui-même
`invertQuery` (en déléguant au processus d'interpolation, par exemple le `queryBuffer` de Barnes) ;
ou deux couches/styles séparés. Exemple complet :
[barnes-observations-eparses-en-transformation-de-rendu](barnes-observations-eparses-en-transformation-de-rendu.md).

## Versions concernées
GeoServer 2.28 (vécu) ; GeoServer 3.0.1 / GeoTools 35.1 (vécu, 2026-09-12).

## Source
- vécu 2026-05-13 (GeoServer 2.28, interpolation de stations suivie d'isolignes).
- vécu 2026-09-12 (GeoServer 3.0.1, `ras:Contour` sur `vec:BarnesSurface`, couche de points PostGIS).
- Code source : `org.geotools.process.function.ProcessFunction`,
  `org.geotools.renderer.lite.RenderingTransformationHelper` — https://github.com/geotools/geotools

## Statut
prouvé
