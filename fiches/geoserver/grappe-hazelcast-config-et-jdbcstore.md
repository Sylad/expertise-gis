# Grappe Hazelcast avec jdbcstore : configuration ignorée, membres qui ne se voient pas

## Symptôme
Les réplicas démarrent chacun seuls (`size=1`), ou la configuration de grappe posée sur le
disque n'est pas prise en compte ; sous Java 21, erreurs d'accès réflexif au démarrage du module.

## Cause
- Avec **jdbcstore**, le dossier `cluster/` est lu en base sauf s'il figure dans `ignoreDirs` :
  `cluster.properties` et `hazelcast.xml` posés sur le disque sont ignorés.
- La découverte DNS Kubernetes (`<kubernetes><service-dns>`) ne trouve que les pods publiés par
  le Service : un Service headless sans `publishNotReadyAddresses: true` ne publie pas un pod
  qui démarre (pas encore prêt), donc il ne rejoint jamais.
- Java 21 exige `--add-modules java.se --add-opens …` pour Hazelcast.

## Détection
Ligne `Hazelcast cluster <nom> initialized. Local member=…, size=N, members=[…]` : `N` doit
valoir le nombre de réplicas.

## Geste
- `ignoreDirs=…,cluster` dans `jdbcstore.properties`.
- Service headless dédié avec `publishNotReadyAddresses: true`.
- Options `--add-opens` dans les options Java.
- Nom de grappe distinct pendant une montée de version roulante : jamais deux versions de
  GeoServer dans la même grappe (arrêter tout puis redémarrer, ou grappe séparée).
- Avec `session_sharing=true`, déclarer seulement le filtre `HzSessionShareFilter`.

## Versions concernées
GeoServer 3.0.1, module `gs-hz-cluster`, Java 21 (vécu).

## Source
vécu 2026-09-01 (GeoServer 3.0.1, Kubernetes) ; vécu 2026-09-08 (montée 2.28 → 3.0.1, grappe distincte).

## Statut
prouvé
