# COG sur stockage objet : « Connection Manager failed to acquire a connection », le certificat servi a expiré

## Symptôme
Plus aucune image COG : couches vides ou en échec après 40 à 60 s. Journal de GeoServer :
`S3RangeReader … Unable to write data from S3 … Connection Manager failed to acquire a
connection within the defined timeout`, puis
`IllegalArgumentException: provided null value` (`SoftValueHashMap.put`). Un réplica neuf ne
démarre pas si un contrôle de démarrage teste le stockage objet (`curl` sort en code 60).

## Cause
Le certificat TLS servi par le stockage objet (SeaweedFS, passerelle S3 en TLS) avait expiré
(`openssl s_client` → `notAfter` passé), alors que le Secret tenu par cert-manager était
renouvelé : SeaweedFS n'avait pas rechargé son certificat. Journal SeaweedFS :
`tls: bad record MAC`. Le pool de connexions S3 « bloqué » côté GeoServer est un effet de
ces poignées de main refusées, pas la cause.

## Détection
- Comparer le certificat **servi** au certificat du Secret :
  `openssl s_client -connect <stockage>:8333 </dev/null 2>/dev/null | openssl x509 -noout -enddate`
  contre la date de fin du certificat du Secret. Servi expiré et Secret valide = piège.
- Depuis un réplica GeoServer :
  `curl -sS -o /dev/null -w '%{http_code}\n' --cacert <ca.crt> https://<stockage>:8333/` →
  `000` et code de sortie 60 = certificat refusé.

## Geste
- Redémarrer le stockage objet pour qu'il lise le certificat renouvelé (sauvegarder d'abord
  ses objets s'il est sur un stockage éphémère). Redémarrer GeoServer ne sert à rien.
- Durable : surveiller la date d'expiration du certificat **servi** (pas seulement celle du
  Secret), ou redémarrer le stockage à chaque renouvellement.
- Preuve d'effet : la commande `curl` répond un code HTTP et les couches COG se rendent.

## Versions concernées
GeoServer 3.0.2 / GeoTools 35.2, lecteur COG imageio-ext (`S3RangeReader`, client AWS CRT),
SeaweedFS en TLS (vécu, rapporté par les notes de dépannage reçues le 2026-11-19 ; version de
SeaweedFS non donnée). Rechargement à chaud du certificat par une version plus récente de
SeaweedFS : non vérifié.

## Source
- Notes de dépannage d'un autre compte, cas « G2 », reçues le 2026-11-19 (vécu : certificat
  servi expiré, Secret renouvelé, rétabli par redémarrage du stockage objet).
- https://github.com/geoserver/geoserver/blob/3.0.2/doc/en/user/community/cog/cog.md (lecture des COG distants)

## Statut
prouvé
