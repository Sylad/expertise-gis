# Festons de CB inversés aux coins rentrants, ou trait de base sous les festons

## Symptôme
Sur une zone de CB, quelques arcs du feston passent à l'intérieur de la zone, toujours à des coins
rentrants ; ou un trait continu court sous les arcs ; ou la zone est remplie.

## Cause
La ligne festonnée délimite les zones de temps significatif (« Scalloped line = demarcation of
areas of significant weather », Model SN). Guide WAFC fig. 15 : arcs **convexes vers l'extérieur**,
joints par des pointes rentrantes, **sans trait de base**, **sans remplissage** ; aux coins de la
zone, une jonction d'arcs tombe **au coin** et aucun arc n'entre dans la zone. Un rendu qui pose des
marques rigides le long de la ligne ne plie pas l'arc au sommet : sur un coin rentrant plus serré
qu'une période, l'arc prolonge le segment entrant et bombe dans la zone.

## Détection
Pour chaque arc, tester de quel côté du contour est son bombement (point milieu dedans/dehors
du polygone) : 0 arc dedans ; vérifier sur des zones à coins rentrants, à plusieurs échelles.

## Geste
Construire les arcs le long du contour en recommençant la série à chaque coin (calcul dans le plan
de l'image), ou accepter et documenter l'écart ; jamais de remplissage.

## Versions concernées
WMO-No. 49 Vol. II, édition 2018 mise à jour 2021 (texte commun avec l'Annexe 3 de l'OACI à cette date ; pagination : page PDF = page imprimée + 14). Les dispositions de présentation passent au PANS-MET (Doc 10157, non libre) : non vérifié dans le PANS-MET.
Guide WAFC *Guidelines for interpreting WAFC T+24 SIGWX forecasts* v2.01 (7 octobre 2024, style opérationnel au 23 janvier 2025) ; guide BUFR WAFS SIGWX v4.4 (mai 2026) et guide SADIS API v1.07 là où cités. Éditions antérieures du style (avant 2025) différentes.

## Source
- WMO-No. 49 Vol. II (2018, mise à jour 2021), App. 1, Model SN (légende des lignes), p. 51
  (PDF 65), figure : ligne festonnée. — https://library.wmo.int/viewer/35795
- Guide WAFC v2.01 § 3.7.1, fig. 15, p. 11 (PDF 11), et fig. 19, p. 13 (PDF 13). — https://www2023.icao.int/WACAF/Documents/Meetings/2025/Workshop-SADIS/SIGWX%20interpretation%20Guide%20V2.01.pdf
- Légende Model SN recontrôlée le 2026-11-16 ; Citation relevée sur les pages rendues en septembre 2026 ; non recontrôlée le 2026-11-16 (copie publique injoignable ce jour-là).

## Statut
à reprouver — la construction aux coins vient du guide WAFC, non recontrôlé le 2026-11-16.
