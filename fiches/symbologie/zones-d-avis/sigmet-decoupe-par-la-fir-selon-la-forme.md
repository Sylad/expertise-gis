# Zone SIGMET amputée à la frontière de la FIR, ou demi-plan qui déborde : la découpe dépend de la forme

## Symptôme
Un polygone `WI` qui dépasse volontairement la FIR est coupé à sa frontière ; ou un `NE OF LINE`
s'étend jusqu'au bord de la carte ; ou une FIR en fer à cheval donne une zone qui couvre la FIR
voisine.

## Cause
Le guide EUR (App. C) répond différemment selon la forme : un **polygone `WI` se rend tel quel**
— des États choisissent des sommets qui englobent une frontière découpée, la marge hors FIR est
voulue (§ 2) ; les **demi-plans, bandes, quadrants et `ENTIRE FIR`** n'ont de sens que **∩ FIR**,
intersection booléenne avec le polygone réel, concave compris (cas du fer à cheval : zone en forme
de « 7 ») ; un `X OF LINE` qui donnerait deux morceaux disjoints appelle deux SIGMET. Piège associé :
le sens de parcours des sommets n'est pas fiable (horaire recommandé en TAC, antihoraire en IWXXM,
les deux observés) — ne jamais en déduire l'intérieur.

## Détection
Cas tests du guide : polygone débordant (aire hors FIR > 0 conservée) ; demi-plan dans une FIR
concave (zone ⊂ FIR, creux de la FIR voisine vide).

## Geste
Découper seulement les formes qui l'exigent ; signaler (par exemple contour pointillé) la part
d'un `WI` hors FIR sans l'amputer ; orienter les anneaux soi-même.

## Versions concernées
ICAO EUR Doc 014, *EUR SIGMET and AIRMET Guide*, 5ᵉ édition révisée en décembre 2023 (version « clean ») ; règles régionales EUR. Éditions antérieures non vérifiées.

## Source
- ICAO EUR Doc 014 (5ᵉ éd., 2023), App. C § 2, p. 49 (PDF 53), figure du polygone débordant ;
  figures des demi-plans p. 51 à 53 (PDF 55 à 57) ; fer à cheval p. 69 (PDF 73) ; App. B
  (coordonnées, sens horaire), p. 43 (PDF 47) ; § 3.4.3.1.7 (location), p. 19–21 (PDF 23–25).
- Liste officielle des documents EUR (le guide n° 014) : https://www.icao.int/EURNAT/EUR-NAT-DOCS?fid=6241
- Citation relevée sur les pages rendues le 2026-09-09 ; non recontrôlée le 2026-11-16 (le site de l'OACI répond 403 aux clients automatiques).

## Statut
à reprouver — citation non recontrôlée sur une copie publique le 2026-11-16.
