# Cercle SIGMET : coupé par la FIR pour un nuage radioactif, pas pour un cyclone tropical

## Symptôme
Deux SIGMET « nuage radioactif » au texte identique, émis par deux FIR voisines, s'affichent
comme deux disques superposés ; ou le disque d'un cyclone tropical est tronqué à la frontière.

## Cause
Guide EUR, App. C : pour `WI nnKM OF <point>` (nuage radioactif) près d'une frontière, la figure
montre un **demi-disque** tranché par la frontière de la FIR émettrice, et le texte précise que **la
FIR voisine émet un SIGMET pour la partie restante** : la FIR émettrice est un paramètre de la
géométrie. Pour `WI nnnNM OF TC CENTRE` (cyclone), la figure montre le disque **débordant** de la
FIR : pas de découpe.

## Détection
Les deux messages jumeaux : géométries complémentaires (union ≈ disque complet, intersection ≈
vide). Le cas cyclone : aire hors FIR > 0.

## Geste
Règle de découpe par phénomène et par forme, la FIR émettrice dans l'entrée du constructeur ;
disque géodésique dans les deux cas.

## Versions concernées
ICAO EUR Doc 014, *EUR SIGMET and AIRMET Guide*, 5ᵉ édition révisée en décembre 2023 (version « clean ») ; règles régionales EUR. Éditions antérieures non vérifiées.

## Source
- ICAO EUR Doc 014 (5ᵉ éd., 2023), App. C § 12, p. 78 (PDF 82), figure du demi-disque ; cyclone :
  p. 67 (PDF 71), figure des deux disques de 75 NM.
- Liste officielle des documents EUR : https://www.icao.int/EURNAT/EUR-NAT-DOCS?fid=6241
- Citation relevée sur les pages rendues le 2026-09-09 ; non recontrôlée le 2026-11-16 (le site de l'OACI répond 403 aux clients automatiques).

## Statut
à reprouver — citation non recontrôlée sur une copie publique le 2026-11-16.
