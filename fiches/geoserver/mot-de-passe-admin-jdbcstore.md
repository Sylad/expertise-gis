# Changer GEOSERVER_ADMIN_PASSWORD ne change pas le mot de passe admin

## Symptôme
Après modification de `GEOSERVER_ADMIN_PASSWORD` et redémarrage, l'ancien mot de passe
`admin` (souvent le défaut `geoserver`) est toujours accepté, y compris sur `/rest`.

## Cause
- Le script de l'image officielle n'importe les identifiants que si le dossier `security/`
  est **absent** (premier démarrage) : ne jamais le pré-créer dans un amorçage.
- Avec le module **jdbcstore**, `security/` (utilisateurs, `geoserver.jceks`) est servi depuis
  la base (il n'est pas dans `ignoreDirs` par défaut) : réécrire `users.xml` sur le disque ne
  change rien.
- Un cache d'authentification garde l'ancien mot de passe valable quelques minutes (~10 min).

## Détection
```bash
curl -s -o /dev/null -w "%{http_code}\n" -u admin:<ancien> "$GS/rest/about/version.json"   # 200 = piège
```

## Geste
1. `PUT /rest/security/self/password` avec le corps `{"newPassword": "…"}`, authentifié avec
   l'**ancien** mot de passe : écrit en base, vaut pour tous les réplicas.
2. Puis seulement, mettre à jour les secrets lus par les clients et les redémarrer (dans
   l'autre ordre, ils échouent en 401 entre les deux).
3. Ne pas re-tester l'ancien mot de passe pendant ~10 min : chaque essai rafraîchit le cache.
4. Fermer `/rest` à Internet si possible.

## Versions concernées
GeoServer 3.0.1 avec jdbcstore (vécu).

## Source
- vécu 2026-09-28 (GeoServer 3.0.1, 3 réplicas, jdbcconfig + jdbcstore).
- vécu 2026-09-01 (script d'identifiants de l'image officielle 3.0.1).
- https://docs.geoserver.org/latest/en/api/#1.0.0/security.yaml

## Statut
prouvé
