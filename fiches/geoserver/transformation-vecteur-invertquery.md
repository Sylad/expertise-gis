# Transformation de rendu sur source vecteur : enveloppe infinie ou attribut nul

## Symptôme
Un processus maison appliqué à une couche vecteur (PostGIS) :
- envoie à la base une requête d'emprise `-Infinity` (aucune entité, ou erreur SQL) ;
- ou reçoit les entités avec l'attribut de valeur à `null`.

## Cause
Pour une source vecteur, le pipeline appelle `invertQuery(outputBBOX, Query, GridGeometry)` ;
sans elle la requête porte une emprise non calculée. Et le moteur de rendu ne demande que les
attributs utilisés par les symboliseurs : l'attribut lu par le processus n'est pas chargé.

## Détection
`pg_stat_activity` ou le journal SQL montrent l'emprise infinie ; un `LOG` des attributs reçus
dans le processus montre la valeur nulle.

## Geste
```java
public Query invertQuery(@DescribeParameter(name = "outputBBOX") ReferencedEnvelope bbox,
                         Query targetQuery, GridGeometry targetGridGeometry) {
    Query q = new Query(targetQuery);
    q.setPropertyNames((String[]) null);   // tous les attributs
    return q;                               // interpolation globale : pas de filtre spatial
}
```
Un processus global (interpolation de stations) renvoie la requête sans filtre spatial ; un
processus local peut élargir l'emprise d'une marge.

## Versions concernées
GeoServer 3.0.1 / GeoTools 35.1 (vécu).

## Source
- vécu 2026-09-01 (GeoServer 3.0.1, processus d'interpolation sur des points PostGIS).
- Code source : `org.geotools.renderer.lite.RenderingTransformationHelper` (https://github.com/geotools/geotools).

## Statut
prouvé
