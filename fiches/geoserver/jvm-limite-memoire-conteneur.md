# Limite mémoire du conteneur égale au -Xmx : OOMKilled

## Symptôme
Le pod GeoServer est tué (`OOMKilled`, code 137) sans `OutOfMemoryError` Java, souvent en
plein rendu lourd ; ou, sans `ExitOnOutOfMemoryError`, la JVM survit en zombie après un OOM
et ne sert plus rien.

## Cause
La JVM consomme au-delà du tas : métaspace, piles de threads, cache de code, tampons natifs
(rendu, encodage d'images). Une limite de conteneur égale ou inférieure à `-Xmx` laisse le
noyau tuer le processus avant que Java ne lève l'erreur.

## Détection
```bash
kubectl get pod <pod> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'   # OOMKilled
kubectl get pod <pod> -o jsonpath='{.spec.containers[0].resources.limits.memory}'
kubectl exec <pod> -- sh -c "tr '\0' ' ' < /proc/1/cmdline" | grep -oE 'Xmx[0-9]+[gm]'
```

## Geste
- `limits.memory ≥ -Xmx + 1 Gi` ; dériver les deux d'une seule valeur dans le chart pour
  qu'ils ne divergent plus.
- `-XX:+ExitOnOutOfMemoryError` (le pod redémarre proprement) et
  `-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=…` (analyse après coup).
- Avant d'augmenter le tas, vérifier que la requête est raisonnable (taille d'image demandée).

## Versions concernées
GeoServer 2.28 sous Kubernetes (vécu) ; indépendant de la version (comportement JVM et cgroups).

## Source
- vécu 2026-05-19 (tas 6 Go, limite 5 Gi : 5 OOMKilled dans la journée ; corrigé à 7 Gi).
- https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html (`ExitOnOutOfMemoryError`, `HeapDumpOnOutOfMemoryError`)

## Statut
prouvé
