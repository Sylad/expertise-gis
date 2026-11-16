# Dossier security/ perdu : mots de passe des magasins indéchiffrables

## Symptôme
Toute requête qui touche un magasin PostGIS échoue avec
`org.jasypt.exceptions.EncryptionOperationNotPossibleException` ; même le `DELETE` REST du
magasin répond 500 (GeoServer désérialise l'objet avant de le supprimer).

## Cause
Les mots de passe des magasins sont stockés chiffrés (`crypt1:…`) avec la clé maîtresse du
keystore (`security/geoserver.jceks` et ce qui la protège). Recréer le data dir ou le volume
sans `security/` génère une nouvelle clé : les anciens secrets ne se déchiffrent plus, et les
mots de passe d'origine ne sont pas récupérables.

## Détection
Le message Jasypt dans le journal ; magasins vecteur en erreur, magasins raster (sans mot de
passe) intacts.

## Geste
- Prévention : sauvegarder `security/` avant toute suppression de volume ou de data dir, et
  le restaurer avant le premier démarrage. Avec jdbcstore, `security/` est en base : ne pas
  vider la table des ressources.
- Réparation : retirer les objets cassés (magasin, types d'entités, couches) — par le
  catalogue en base si l'API REST refuse —, redémarrer pour purger le cache, recréer les
  magasins avec les mots de passe, puis republier les styles perdus avec le volume.

## Versions concernées
GeoServer 2.28.3 avec catalogue JDBCConfig (vécu) ; mécanisme documenté (chiffrement des
mots de passe par clé maîtresse) sur les versions courantes.

## Source
- https://docs.geoserver.org/latest/en/user/security/passwd.html
- vécu 2026-05-15 (GeoServer 2.28.3, volume recréé pour passer en accès multiple ; ~1 h de réparation).

## Statut
prouvé
