# Cône d'incertitude présenté comme partie de l'avis de cyclone OACI

## Symptôme
La carte d'avis de cyclone tropical dessine un cône autour de la trajectoire prévue et le
légende comme l'avis officiel ; ou le contour « GALE FORCE WIND » du modèle est lu comme une
incertitude.

## Cause
L'avis de cyclone (Table A2-2) donne une position observée, des positions prévues (+6 à +24 h)
et des vents maximaux, **rien d'autre** : ni rayon d'erreur, ni probabilité, ni cône ; le schéma
IWXXM (`tropicalCycloneAdvisory`) n'en a pas non plus. Le MODEL TCG montre des positions datées avec
cartouches `MAX WIND`, un contour épais **« GALE FORCE WIND »** (étendue des vents de tempête) et une
zone festonnée **« FRQ CB »** — aucun cône. Le cône est une construction d'un producteur (par
exemple le centre de prévision des ouragans américain, rayons révisés chaque année) ou un calcul
local.

## Détection
Chercher dans la légende la source du cône : si elle renvoie à l'avis OACI, c'est le piège.

## Geste
Si l'on dessine un cône : le libeller avec sa source, son horizon et l'année des rayons, ne
jamais le confondre avec l'étendue des vents.

## Versions concernées
WMO-No. 49 Vol. II, édition 2018 mise à jour 2021 (texte commun avec l'Annexe 3 de l'OACI à cette date ; pagination : page PDF = page imprimée + 14). Les dispositions de présentation passent au PANS-MET (Doc 10157, non libre) : non vérifié dans le PANS-MET. IWXXM 2025-2 (schéma de l'avis de cyclone).

## Source
- WMO-No. 49 Vol. II (2018, mise à jour 2021), App. 2, Table A2-2, p. 62 à 64 (PDF 76 à 78), et
  App. 1, MODEL TCG, p. 44 (PDF 58) ; figure : MODEL TCG. — https://library.wmo.int/viewer/35795
- Schémas IWXXM 2025-2 : https://schemas.wmo.int/iwxxm/2025-2/
- citation vérifiée le 2026-11-16 (texte et pagination, pdftotext sur la copie de l'édition 2018 mise à jour 2021).

## Statut
prouvé — pour le WMO-No. 49 ; l'absence d'élément d'incertitude dans le schéma IWXXM est relevée par l'étude, non recontrôlée.
