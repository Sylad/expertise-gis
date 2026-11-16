# Transformation de rendu maison : le coverage source n'arrive pas (« data » manquant)

## Symptôme
Un SLD appelle un processus maison dans `<Transformation>` avec
`<ogc:Function name="parameter"><ogc:Literal>data</ogc:Literal></ogc:Function>` (injection
automatique de la source) et le rendu échoue :
- `execute()` reçoit `data = null` (« data parameter required ») ;
- ou, avant même l'appel, `Parameter data is missing`.

## Cause
1. `AnnotationDrivenProcessFactory` n'enveloppe le bean dans un `InvokeMethodRenderingProcess`
   (reconnu comme `RenderingTransformation`) **que si** la classe a au moins une méthode nommée
   `invertGridGeometry`, `invertQuery`, `customizeReadParams` ou `clipOnRenderingArea`
   (détection par réflexion sur le nom). Sinon c'est une simple `ProcessFunction` : le pipeline
   de rendu n'injecte pas la source.
2. La multiplicité des paramètres est validée **avant** l'injection : un `data` obligatoire
   (`min=1`) échoue en « missing ».

## Détection
Lire la classe : aucune des quatre méthodes ⇒ cause 1. Message « Parameter data is missing »
⇒ cause 2.

## Geste
```java
// marqueur : rend la classe reconnaissable comme transformation de rendu raster
public GridGeometry invertGridGeometry(Query targetQuery, GridGeometry targetGridGeometry) {
    return targetGridGeometry;
}
@DescribeProcess(...)
public GridCoverage2D execute(@DescribeParameter(name = "data", min = 0) GridCoverage2D data, ...) { ... }
```
Pour une source raster, ce sont `invertGridGeometry` / `customizeReadParams` /
`clipOnRenderingArea` qui servent ; pour une source vecteur, voir
[transformation-vecteur-invertquery](transformation-vecteur-invertquery.md).

## Versions concernées
Introduit entre GeoServer 2.26.1 et 2.26.2 ; vérifié dans les sources GeoTools 35.1
(GeoServer 3.0.1), logique de recherche par nom inchangée.

## Source
- Code source : `org.geotools.process.factory.AnnotationDrivenProcessFactory#create`,
  `org.geotools.renderer.lite.RenderingTransformationHelper`
  (https://github.com/geotools/geotools).
- vécu 2026-05-13 (GeoServer 2.28, processus d'interpolation maison) et 2026-09-08 (sources GeoTools 35.1 relues lors d'une montée en 3.0.1, sans changement de code nécessaire).

## Statut
prouvé
