# Plusieurs réplicas : une mutation REST pas encore vue par le réplica suivant

## Symptôme
Un automate fait `DELETE …/coveragestores/<s>?recurse=true` (200) puis, quelques
millisecondes plus tard, `POST …/coveragestores` : **500 « Store '<s>' already exists »**.
Ou, après un `PUT` du style par défaut d'une couche, un réplica rend avec le nouveau style et
un autre avec l'ancien.

## Cause
Derrière un Service, chaque requête peut tomber sur un réplica différent ; le cache de
catalogue de chaque réplica converge avec un retard (événements de grappe, rechargement depuis
la base). Ce n'est pas un échec de la première requête.

## Détection
Interroger chaque réplica par l'adresse de son pod (`http://<ip-pod>:8080/geoserver/rest/…`) ;
`kubectl port-forward svc/…` épingle un seul pod et ne le montre pas.

## Geste
- Après chaque mutation : attendre N réponses consécutives dans l'état voulu par le Service
  (par exemple 6 GET à 2 s d'intervalle, plafond 60 s ; une réponse contraire remet la série
  à zéro), puis seulement la mutation suivante.
- Réessayer un `POST` qui répond 500 « already exists » (5 s, plafond 60 s).
- En dernier recours, `POST /rest/reset` sur chaque réplica par l'adresse de son pod.

## Versions concernées
GeoServer 3.0.1, 3 réplicas jdbcconfig + Hazelcast (vécu) ; GeoServer 2.28, 2 réplicas (vécu).

## Source
vécu 2026-09-10 (GeoServer 3.0.1, `already exists` 7 ms après le `DELETE`) ; vécu 2026-05-15 (GeoServer 2.28, style par défaut).

## Statut
prouvé
