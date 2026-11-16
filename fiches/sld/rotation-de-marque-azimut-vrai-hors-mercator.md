# Marque orientée par un azimut vrai : fausse hors de Web Mercator

## Symptôme
Des flèches, pointes ou barbules orientées par un azimut stocké en base sont justes en
EPSG:3857 et fausses ailleurs : ~5,6° d'écart en EPSG:4326 à 45° N, ~14° en Lambert,
jusqu'à des centaines de degrés en stéréographique polaire.

## Cause
Un azimut vrai (par rapport au nord géographique) ne donne l'angle **à l'écran** que dans une
projection conforme sans convergence des méridiens (Mercator). Dans les autres, le nord de la
carte tourne d'un point à l'autre.

## Détection
Rendre la même entité dans 3857, 4326, une conique et une polaire, avec de grandes marques
(Size 240–320), et mesurer la direction sur les pixels.

## Geste
Calculer l'angle à l'écran dans le SLD à partir de la géométrie reprojetée dans le CRS de sortie :
```xml
<Rotation>
  <ogc:Function name="endAngle">
    <ogc:Function name="geo:reproject">
      <ogc:Function name="parameter"><ogc:Literal>geometry</ogc:Literal><ogc:PropertyName>geom</ogc:PropertyName></ogc:Function>
      <ogc:Function name="parameter"><ogc:Literal>sourceCRS</ogc:Literal><ogc:Literal>EPSG:4326</ogc:Literal></ogc:Function>
      <ogc:Function name="parameter"><ogc:Literal>targetCRS</ogc:Literal><ogc:Function name="env"><ogc:Literal>wms_srs</ogc:Literal><ogc:Literal>EPSG:3857</ogc:Literal></ogc:Function></ogc:Function>
    </ogc:Function>
  </ogc:Function>
</Rotation>
```
- `endAngle`/`startAngle` rendent l'angle horaire depuis +x : à passer tel quel à `Rotation`
  (tête au départ : `startAngle + 180`).
- `geo:reproject` est une fonction-processus (syntaxe `parameter`).
- `EPSG:4326` (WMS 1.1.1) et `urn:ogc:def:crs:EPSG::4326` (1.3.0) sont décodés en lat/lon :
  les remplacer par `CRS:84` via `if_then_else(in(…))`, sinon l'angle tourne de 90°.
- Pour un point : construire un court segment tangent en WKT (`geomFromWKT(Concatenate(…))`).
- Garder l'azimut en base pour les autres clients.

## Versions concernées
GeoServer 3.0.1 (vécu).

## Source
vécu 2026-09-21 (GeoServer 3.0.1, mesuré en 3857, 4326, 3034 et 3995).

## Statut
prouvé
