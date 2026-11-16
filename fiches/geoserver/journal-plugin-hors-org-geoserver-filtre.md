# Les messages INFO d'un module Java maison n'apparaissent pas

## Symptôme
Un module ajouté dans `WEB-INF/lib` journalise en `INFO` mais rien n'apparaît dans le
journal de GeoServer ; seuls ses `WARNING` et `SEVERE` sortent.

## Cause
Les profils de journalisation de GeoServer ne règlent au niveau INFO que les journaux sous
`org.geoserver.*` (et quelques autres) ; un journal d'un autre paquet hérite d'un niveau plus
élevé.

## Détection
Le même message en `WARNING` apparaît, en `INFO` non.

## Geste
Nommer le journal du module `org.geoserver.<module>` (ou ajouter son paquet au profil de
journalisation). Pour prouver qu'un composant est chargé, un message inconditionnel en
`WARNING` au démarrage.

## Versions concernées
GeoServer 3.0.1 (vécu).

## Source
vécu 2026-09-01 (GeoServer 3.0.1, image officielle).

## Statut
prouvé
