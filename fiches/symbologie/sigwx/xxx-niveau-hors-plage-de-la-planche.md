# Cartouche qui affiche « 300 » sur une carte SWM (FL 100 – FL 250) : un niveau hors de la couche de la carte s'écrit XXX

## Symptôme
Sur une carte de niveaux moyens (SWM) ou un extrait, un CB affiche son sommet réel au-dessus de la
limite haute de la carte, ou un givrage sa base sous la limite basse ; ou la plage d'une carte est
prise dans un autre produit que celui qui est dessiné.

## Cause
WMO-No. 49 Vol. II § 4.3.1 : le Model SWH couvre le temps significatif **au-dessus du FL 250**, le
Model SWM **entre FL 100 et FL 250**, le Model SWL **sous le FL 100**, et la couche de la carte doit
être indiquée clairement sur la carte. Model SN § 3.3 : les hauteurs sont en niveaux de vol, sommet
au-dessus de la base, et **`XXX`** signifie que le sommet ou la base est **hors de la couche** à
laquelle la carte s'applique. Sur un SWM, un CB de base FL 080 et de sommet FL 300 s'écrit donc
`XXX` au-dessus de `XXX` ; sur un SWH, un CB de base FL 200 et de sommet FL 390 s'écrit `390`
au-dessus de `XXX`. Le `XXX` dépend de la **couche de la carte**, pas seulement de la donnée : la
même entité s'écrit différemment sur un SWH et sur un SWM. Un produit des WAFC peut avoir ses propres
plages, à lire sur sa planche et dans son guide : ne pas les mélanger avec celles du § 4.3.1. Le cas
« niveau exactement à la limite » (FL 250, FL 100) n'est pas tranché par le texte.

## Détection
Même entité rendue avec deux couches de carte : le texte change (`390` sur SWH, `XXX` sur SWM pour
un sommet à FL 390) ; la plage utilisée pour composer `XXX` est celle imprimée sur la planche ;
carte sans couche (vue libre) : valeur brute.

## Geste
Composer le texte du cartouche au rendu avec la couche de la planche en paramètre ; valeur brute
dans une vue qui n'est pas une planche.

## Versions concernées
WMO-No. 49 Vol. II, édition 2018 mise à jour 2021 (texte commun avec l'Annexe 3 de l'OACI à cette date ; pagination : page PDF = page imprimée + 14). Non vérifié dans le PANS-MET (Doc 10157, non libre) ni dans le guide WAFC *Guidelines for interpreting WAFC T+24 SIGWX forecasts* v2.01 (plages propres au produit WAFC, non recontrôlées).

## Source
- WMO-No. 49 Vol. II (2018, mise à jour 2021), Part IV § 4.3.1, p. 188 (PDF 202), figure : aucune
  (règle de texte) ; App. 1, Model SN § 3.3 « Heights », p. 51 (PDF 65). — https://library.wmo.int/viewer/35795
- citation vérifiée le 2026-11-16 (pdftotext sur la copie de l'édition 2018 mise à jour 2021 : § 4.3.1 « between FL 100 and FL 250 », Model SN § 3.3 « When XXX is used… »).
- Hors norme, non recontrôlé : guide WAFC v2.01, § 3.6–3.8, fig. 14 — https://www2023.icao.int/WACAF/Documents/Meetings/2025/Workshop-SADIS/SIGWX%20interpretation%20Guide%20V2.01.pdf

## Statut
prouvé — règle et plages relues dans le WMO-No. 49 le 2026-11-16 ; le guide WAFC reste non recontrôlé et n'est plus la source de la règle.
