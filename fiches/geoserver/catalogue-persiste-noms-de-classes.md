# Classe Java renommée ou retirée : les réplicas ne démarrent plus

## Symptôme
Après avoir renommé (paquet ou classe) ou retiré une fabrique de processus, une fabrique de
marques ou un bean, GeoServer ne démarre plus :
`ConversionException: Cannot load java class <ancien.nom.Qualifie>` (ou
`CannotResolveClassException`) ; réplicas en redémarrage en boucle.

## Cause
La configuration persistée référence des classes par **nom qualifié** sérialisé par XStream :
par exemple la configuration du service WPS (`processGroups/factoryClass`). Avec un catalogue
en base (jdbcconfig), ces noms sont dans les blobs de la table des objets ; sur disque, dans
`wps.xml`. Changer le jar et `applicationContext.xml` ne suffit pas. Même effet pour un bean
Spring déclaré avec un nom de classe périmé.

## Détection
```sql
-- catalogue jdbcconfig (lecture seule) : doit répondre 0 après migration
SELECT count(*) FROM <schéma>.object WHERE blob LIKE '%<ancien.prefixe>%';
```
Sur disque : `grep -rl '<ancien.prefixe>' $GEOSERVER_DATA_DIR`. Dans les sources :
`grep -rn '<ancien.prefixe>'` doit être vide (code, fichiers SPI, `applicationContext.xml`).

## Geste
- Migrer la configuration **dans la même livraison** que l'image : sauvegarde, remplacement de
  l'ancien préfixe, contrôle « 0 résidu », puis démarrage de la nouvelle image.
- Pour retirer une fabrique sans migrer : garder une classe vide de même nom (qui étend
  `AnnotatedBeanProcessFactory` sans processus) jusqu'à la prochaine remise à zéro du catalogue.
- Tester l'image localement (`docker run`) ou au moins `jar tf` + relecture des
  `applicationContext.xml` avant de livrer.

## Versions concernées
GeoServer 2.28 (vécu) et 3.0.1 (vécu).

## Source
vécu 2026-09-25 (GeoServer 3.0.1, renommage des paquets de plusieurs modules, retour arrière) ; vécu 2026-05-14 (GeoServer 2.28.3, fabrique absente de l'image).

## Statut
prouvé
