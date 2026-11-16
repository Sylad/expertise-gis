# DO $$ … $$ dans un Job Kubernetes : « syntax error at or near "$" »

## Symptôme
Un bloc PL/pgSQL passé en ligne dans `command`/`args` d'un conteneur (Job, CronJob, script
d'initialisation d'opérateur PostgreSQL) échoue : `syntax error at or near "$" — LINE 1: DO $`.
Le rendu Helm est correct et la même requête passe à la main. Sans `ON_ERROR_STOP`, `psql`
continue et le job finit **vert** sans rien avoir fait.

## Cause
Kubernetes interprète `$(VAR)` dans `command` et `args` ; `$$` y est l'échappement de `$` et
devient `$`. `DO $$` arrive donc en `DO $`. Les fichiers montés (ConfigMap) ne sont pas
concernés.

## Détection
```bash
kubectl get pod <pod> -o jsonpath='{.spec.containers[0].args[0]}' | grep -n '\$\$'   # texte reçu par le conteneur
helm template … | grep -n '\$\$'                                                     # audit de tout le chart
```

## Geste
Dollar-quoting **nommé** (`DO $body$ … $body$;`) ou SQL dans un fichier monté ;
`psql -v ON_ERROR_STOP=1`. Pour lire le journal d'un job de hook dont les pods disparaissent :
le rejouer sous un autre nom sans annotations de hook (et `ROLLBACK` au lieu de `COMMIT`).

## Versions concernées
Kubernetes (k3s 1.3x) (vécu) ; comportement documenté de l'API.

## Source
- https://kubernetes.io/docs/tasks/inject-data-application/define-interdependent-environment-variables/ (« $$ are reduced to $ »)
- vécu 2026-09-08 et 2026-09-25 (script d'initialisation d'un opérateur PostgreSQL, Job de migration, CronJob de purge resté vert sans effet).

## Statut
prouvé
