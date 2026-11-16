# Ligne de givrage « T » : ticks dessinés vers l'extérieur de la zone

## Symptôme
Au style WAFC 2025, les zones de givrage sont bordées d'une ligne violette tiretée à ticks
perpendiculaires ; ici les ticks pointent hors de la zone (et dans la zone autour d'un trou).

## Cause
Guide WAFC § 3.8.2 et fig. 17 : ligne « T » violette, **un tick perpendiculaire par tiret, orienté
vers le côté rempli** — vers l'intérieur de la zone, et sur un trou vers l'extérieur du trou (donc
toujours vers le remplissage). Piège de lecture vécu : la figure, petite, se lit facilement à
l'envers ; la lire en zoom natif au pixel. Second piège : la position du tick le long du tiret n'est
pas canonique sur les cartes WAFC (elle dérive) ; la figure ne fixe que le côté. Le style legacy (et
SADIS : « feston, ligne T ou autre style distinct ») admet aussi un feston.

## Détection
Masque intérieur de la zone (rendu rempli) contre masque des ticks : ≥ 90 % des pixels de tick
dans la zone (le reste = base du tick sur le tiret) ; idem autour d'un trou, vers le remplissage.

## Geste
Orienter les anneaux (extérieur et trous) de façon connue, poser les ticks du côté rempli ;
documenter la position choisie le long du tiret.

## Versions concernées
Guide WAFC *Guidelines for interpreting WAFC T+24 SIGWX forecasts* v2.01 (7 octobre 2024, style opérationnel au 23 janvier 2025) ; guide BUFR WAFS SIGWX v4.4 (mai 2026) et guide SADIS API v1.07 là où cités. Éditions antérieures du style (avant 2025) différentes.

## Source
- Guide WAFC v2.01 § 3.8.2, fig. 17, p. 12 (PDF 12) ; annexe A-3, p. 20 (PDF 20), figure : carte
  EUR SWM. — https://www2023.icao.int/WACAF/Documents/Meetings/2025/Workshop-SADIS/SIGWX%20interpretation%20Guide%20V2.01.pdf
- Guide SADIS API v1.07 § 7.4, table 15, p. 47 (PDF 47).
- Citation relevée sur les pages rendues en septembre 2026 ; non recontrôlée le 2026-11-16 (copie publique injoignable ce jour-là).

## Statut
à reprouver — guide WAFC non recontrôlé le 2026-11-16.
