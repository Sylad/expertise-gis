# Cartouche qui affiche « 490 » sur une carte FL250–450 : un niveau hors de la plage s'écrit XXX

## Symptôme
Sur une carte de niveaux moyens (SWM, FL100–450) ou un extrait, un CB affiche son sommet réel
au-dessus de la limite haute, ou un givrage sa base sous la limite basse.

## Cause
Guide WAFC v2.01 (§ 3.6–3.8, fig. 14) : une base sous la plage de la carte et un sommet au-dessus
s'écrivent **`XXX`** (« from below the valid range of the chart… indicated by XXX ») ; sur un SWM,
un CB de base sous FL250 et de sommet au-dessus de FL450 s'écrit `OCNL / CB / XXX / XXX`. Le `XXX`
dépend donc de la **planche**, pas seulement de la donnée : la même entité s'écrit différemment sur
un SWH et sur un SWM. Le cas « base exactement à la limite » n'est pas tranché par le texte
(« below »).

## Détection
Même entité rendue avec deux plages de carte : le texte change (`490` sur SWH FL250–630, `XXX` sur
SWM) ; carte sans plage (vue libre) : valeur brute.

## Geste
Composer le texte du cartouche au rendu avec la plage de la planche en paramètre ; valeur brute
dans une vue qui n'est pas une planche.

## Versions concernées
Guide WAFC *Guidelines for interpreting WAFC T+24 SIGWX forecasts* v2.01 (7 octobre 2024, style opérationnel au 23 janvier 2025) ; guide BUFR WAFS SIGWX v4.4 (mai 2026) et guide SADIS API v1.07 là où cités. Éditions antérieures du style (avant 2025) différentes.

## Source
- Guide WAFC v2.01, § 3.6–3.8, fig. 14, p. 11 (PDF 11) ; version bilingue § 4.3.3–4.3.4,
  p. 13–14 (PDF 13–14). — https://www2023.icao.int/WACAF/Documents/Meetings/2025/Workshop-SADIS/SIGWX%20interpretation%20Guide%20V2.01.pdf
- Citation relevée sur les pages rendues en septembre 2026 ; non recontrôlée le 2026-11-16 (copie publique injoignable ce jour-là).

## Statut
à reprouver — guide WAFC non recontrôlé le 2026-11-16.
