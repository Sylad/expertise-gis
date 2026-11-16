# Jet de l'hémisphère sud : fanions, étiquette FL et extension verticale du mauvais côté ou dans le mauvais ordre

## Symptôme
Au sud de l'équateur, les fanions du jet restent à gauche de l'écoulement, l'étiquette `FL380` et
la ligne `280/420` sont dans l'ordre de l'hémisphère nord ; ou un jet d'est a son étiquette remise
« à l'endroit » ; ou la pointe est dessinée sur un jet coupé par le cadre.

## Cause
Guide WAFC § 3.5 (fig. 5, 7, 9) et guide BUFR § 4 (fig. 6–7) : symboles de vitesse **à gauche de
l'écoulement dans l'hémisphère nord, à droite dans le sud**, côté fixé par l'hémisphère **de départ**
du jet ; étiquette FL **du côté opposé**, tournée le long de l'axe et **lisible dans le sens de
l'écoulement** (donc à l'envers pour un jet d'est) ; au maximum ≥ 120 kt, l'extension verticale
`bbb/sss` s'ajoute **sous** `FL…` au nord et **au-dessus** au sud (le plus près de l'axe : FL au
nord, extension au sud) ; pointe omise si le jet sort du cadre.

## Détection
Jets synthétiques nord / sud / d'est / coupé par le cadre : côté des fanions, ordre des deux
lignes, sens de lecture de l'étiquette, présence de la pointe.

## Geste
Pré-calculer le côté et l'ordre par jet (hémisphère de départ) ; orientation de l'étiquette par
le sens de l'écoulement ; pointe conditionnée au cadre.

## Versions concernées
Guide WAFC *Guidelines for interpreting WAFC T+24 SIGWX forecasts* v2.01 (7 octobre 2024, style opérationnel au 23 janvier 2025) ; guide BUFR WAFS SIGWX v4.4 (mai 2026) et guide SADIS API v1.07 là où cités. Éditions antérieures du style (avant 2025) différentes.

## Source
- Guide WAFC v2.01 § 3.5, fig. 5 et 7, p. 7–8 (PDF 7–8), fig. 9, p. 9 (PDF 9). — https://www2023.icao.int/WACAF/Documents/Meetings/2025/Workshop-SADIS/SIGWX%20interpretation%20Guide%20V2.01.pdf
- Guide BUFR WAFS SIGWX v4.4 § 4, fig. 6–7, p. 17 (PDF 17).
- Citation relevée sur les pages rendues en septembre 2026 ; non recontrôlée le 2026-11-16 (copie publique injoignable ce jour-là).

## Statut
à reprouver — guides WAFC et BUFR non recontrôlés le 2026-11-16.
