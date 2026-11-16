# Cartouches qui se chevauchent ou recouvrent un jet : dans la zone d'abord, sinon hors zone avec un renvoi

## Symptôme
Les cartouches CB ou givrage se chevauchent, couvrent un axe ou une pointe de jet, ou sont posés
hors de leur zone sans lien visible ; ou chaque cartouche porte un renvoi même quand il tient dans
sa zone.

## Cause
Aucun texte ne chiffre le placement ; la planche Model SWH montre la pratique : **aucun** des 40
cartouches ne recouvre un axe, un groupe de vent ou une pointe de jet ; pas de chevauchement entre
cartouches ; un cartouche hors zone est relié par un **renvoi droit et fin** dont l'extrémité tombe
**à l'intérieur** de la zone ; volcans et rectangles de tropopause sans renvoi. Le guide BUFR WAFS
(§ 3.1 items 5–6) demande un placement automatique, une priorité **volcans > radioactivité >
cyclones tropicaux**, et que points et lettres des aérodromes ne soient pas recouverts par les
cartouches ; le guide WAFC (§ 3.7.2) et le BUFR (§ 5–6) mettent le cartouche **dans la zone sans
renvoi** quand il y tient. La forme de la tête de renvoi (pleine, en V ouvert, queue « en éclair »)
varie selon le visualiseur pour les mêmes données : convention, pas norme.

## Détection
Sur un rendu : pixels de jet sous un cartouche = 0 ; aucune paire de cartouches qui se
recouvrent ; chaque cartouche hors zone a un renvoi dont l'extrémité est dans la zone.

## Geste
Tester « tient dans la zone » (rectangle inclus dans le polygone), sinon chercher une position
hors zone avec renvoi ; garder les obstacles (jets, aérodromes, autres cartouches) ; signaler un
placement dégradé plutôt que supprimer un cartouche.

## Versions concernées
WMO-No. 49 Vol. II, édition 2018 mise à jour 2021 (texte commun avec l'Annexe 3 de l'OACI à cette date ; pagination : page PDF = page imprimée + 14). Les dispositions de présentation passent au PANS-MET (Doc 10157, non libre) : non vérifié dans le PANS-MET.
Guide WAFC *Guidelines for interpreting WAFC T+24 SIGWX forecasts* v2.01 (7 octobre 2024, style opérationnel au 23 janvier 2025) ; guide BUFR WAFS SIGWX v4.4 (mai 2026) et guide SADIS API v1.07 là où cités. Éditions antérieures du style (avant 2025) différentes.

## Source
- WMO-No. 49 Vol. II (2018, mise à jour 2021), App. 1, Model SWH, p. 40 (PDF 54), figure : la
  planche (13 renvois, 40 cartouches mesurés par l'étude). — https://library.wmo.int/viewer/35795
- Guide BUFR WAFS SIGWX v4.4, § 3.1 items 5 et 6, p. 14 (PDF 14) ; guide WAFC v2.01 § 3.7.2,
  p. 11–12 — https://www2023.icao.int/WACAF/Documents/Meetings/2025/Workshop-SADIS/SIGWX%20interpretation%20Guide%20V2.01.pdf
- Page et figure du WMO-No. 49 recontrôlées le 2026-11-16 ; Citation relevée sur les pages rendues en septembre 2026 ; non recontrôlée le 2026-11-16 (copie publique injoignable ce jour-là).

## Statut
à reprouver — niveau « pratique » (figure, pas de texte) ; guides WAFC et BUFR non recontrôlés le 2026-11-16.
