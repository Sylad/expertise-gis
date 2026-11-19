# Job de chargement REST en échec pendant une mise à jour progressive des réplicas

## Symptôme
Le Job qui configure GeoServer par l'API REST (espaces de travail, magasins, couches) échoue
pendant une mise à jour du déploiement (`helm upgrade`) : `BackoffLimitExceeded`, avec dans
son journal des réponses `409` sur `POST …/rest/workspaces`, des appels sans réponse
(code HTTP `000` côté client) et, pour un magasin, le message relevé par les notes :
`store … sees no table (HTTP 000000)`.

## Cause
Deux causes mêlées dans le cas vécu :
- les appels REST du Job tombent, à travers le Service, sur des réplicas en cours de
  remplacement par la mise à jour progressive ; origine des `409` (déduction, les notes ne
  l'expliquent pas) : un appel coupé (`000`) puis rejoué trouve l'objet déjà créé par la
  tentative précédente ou par un autre réplica (`409`) ;
- une ressource dont dépendait un magasin (une source de données JNDI) n'était déclarée que
  sous une option du déploiement qui n'était pas activée. Le message `sees no table` relève
  plutôt de cette cause que des appels coupés (déduction, les notes ne le rattachent pas).

## Détection
Jouer la mise à jour du déploiement en environnement de test, Job compris : il doit finir
`Completed` (`kubectl get job <job> -o jsonpath='{.status.succeeded}'` → `1`). Dans son
journal, un `409` sur une création ou un `000` = le Job ne tolère pas le remplacement des
réplicas.

## Geste
- Rendre chaque appel REST idempotent : `409` sur une création = déjà fait, on continue ;
  `000` (connexion coupée) = on réessaie (déduction : avec un délai, jusqu'à une borne).
- Déclarer les ressources dont dépendent les magasins (source JNDI…) sans condition
  (déduction : ou conditionner aussi les magasins qui les utilisent).
- Preuve d'effet : la même mise à jour en test finit avec le Job `Completed`.
- Voir aussi, pour l'état du catalogue d'un réplica à l'autre juste après une écriture :
  [replicas-convergence-du-catalogue](replicas-convergence-du-catalogue.md).

## Versions concernées
GeoServer 3.0.2 sur Kubernetes, déploiement Helm à plusieurs réplicas (vécu, rapporté par les
notes de dépannage reçues le 2026-11-19). Le mécanisme ne dépend pas de la version.

## Source
- Notes de dépannage d'un autre compte, cas « G3 », reçues le 2026-11-19 (vécu :
  `BackoffLimitExceeded` pendant un `helm upgrade`, Job `Completed` après correction).
- https://docs.geoserver.org/latest/en/user/rest/index.html

## Statut
prouvé
