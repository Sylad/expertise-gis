# GetCapabilities de 60 s ou plus quand un WMS amont en cascade est en panne

## Symptôme
Le GetCapabilities de **notre** GeoServer prend une minute ou plus (jusqu'au délai du
proxy), le client ne trouve plus les instants des couches ; CPU des pods au repos, journal vide.

## Cause
Le document de capabilities appelle `WMS.isQueryable` pour chaque couche en cascade →
`ResourcePool.getWebMapServer` → si le cache est vide, `createWebMapServer` →
`negotiateVersion`, qui interroge l'amont **une fois par version WMS tentée**. Un amont qui
répond 504 après 50 s coûte donc plusieurs fois ce délai. Le cache se vide à chaque
`POST /rest/reload` (`ResourcePool.dispose()` → `wmsCache.clear()`) : un automate qui recharge
le catalogue à chaque déploiement fait repayer l'amont mort à chaque fois.

## Détection
```bash
curl -s -o /dev/null -w "%{time_total}\n" "$GS/<ws>/wms?service=WMS&request=GetCapabilities"
# pendant la requête, dans le pod :
jcmd 1 Thread.print | grep -B2 -A30 Capabilities   # pile bloquée dans negotiateVersion / lecture SSL
```
Tester chaque amont depuis le pod (`curl -w %{time_total}`).

## Geste
- Délais sur chaque magasin WMS en cascade (`connectTimeout`, `readTimeout`, par exemple 5 et
  30 s), posés par l'amorçage à chaque déploiement : les délais seuls ne suffisent pas (plusieurs
  versions tentées).
- Ne pas faire de `POST /rest/reload` dans les automates de déploiement.
- Code possible : garder le dernier `WebMapServer` valide après un rechargement, et un client
  HTTP qui sert une copie des capabilities amont quand l'amont échoue, avec disjoncteur par hôte
  (mesuré : 61 s → 7–8 s avec l'amont toujours en panne).
- Une panne chez un tiers ne doit jamais ralentir nos capabilities : à traiter comme un défaut
  de notre plateforme.

## Versions concernées
GeoServer 3.0.1 (vécu, vérifié par `javap` dans le pod).

## Source
vécu 2026-09-23 (GeoServer 3.0.1, 3 réplicas, 6 magasins WMS en cascade dont un amont en 504).

## Statut
prouvé
