# Anticyclones presque absents de la carte : le seuil de détection des centres n'est pas dans la norme

## Symptôme
Une détection automatique des centres sur un champ de pression réduite au niveau de la mer
produit des dizaines de L et quasiment aucun H (cas vécu : rapport L/H > 100 sur plusieurs
jours), alors que le champ présente des anticyclones nets.

## Cause
Aucun texte normatif ne dit **quand** un extremum devient un centre : le WMO-No. 306
Att. IV § 4.1.2–4.1.3 règle l'intervalle des isobares et la représentation, le WMO-No. 49
Vol. II partie IV § 4.3.4 (cartes SWL) dit seulement que les centres *should* être marqués
d'une croix et de H ou L avec la pression centrale. Aucun seuil de proéminence, aucun rayon,
aucune obligation d'isobare fermée. Le piège est de prendre l'intervalle des isobares (4 hPa)
pour un seuil et de l'appliquer à l'identique aux dépressions (creuses) et aux anticyclones
(plats, gradients faibles). La pratique des analystes (manuel d'analyse de surface de la
NOAA) est « un extremum relatif, généralement entouré d'au moins une isobare fermée »,
isobare qui peut être intermédiaire (1–2 hPa) en gradient faible : c'est un usage, pas la norme.

## Détection
Compter les centres par nature sur un échantillon de champs ; pour chaque H de référence
repéré à la main, mesurer la proéminence (hauteur au-dessus de la plus haute isobare fermée qui
ne contient pas de centre plus fort). Si les H de référence ont tous une proéminence < seuil
appliqué, le seuil est la cause.

## Geste
Écrire le critère comme un **choix documenté** (pas « conforme OMM »), avec des paramètres
distincts pour H et L, mesurés sur un jeu de champs réels ; ne jamais marquer un centre dont
l'isobare ne se referme pas dans le domaine affiché.

## Versions concernées
WMO-No. 306 Vol. I.1, édition 2019, Attachment IV (pagination A-441 à A-456 = PDF 465 à 480). Les passages cités figurent mot pour mot dans l'appendice II-4 du Manuel du GDPFS (copie publique de l'OMM) ; les éditions antérieures à 2019 du WMO-No. 306 librement diffusées s'arrêtent à l'Attachment III.
WMO-No. 49 Vol. II, édition 2018 mise à jour 2021 (texte commun avec l'Annexe 3 de l'OACI à cette date ; pagination : page PDF = page imprimée + 14). Les dispositions de présentation passent au PANS-MET (Doc 10157, non libre) : non vérifié dans le PANS-MET.

## Source
- WMO-No. 306 Vol. I.1 (2019), Attachment IV § 4.1.2 et § 4.1.3, p. A-453 (PDF 477) ; figure :
  glyphes du § 4.1.3 (b), sans seuil — texte public identique : https://old.wmo.int/extranet/pages/prog/www/ISS/Meetings/IPET-DRMM_Beijing2015/Documents/IPET-DRMM-III_Doc11-5_GDPFS_Manual_Appendix_II-4.pdf
- WMO-No. 49 Vol. II (2018, mise à jour 2021), partie IV § 4.3.4, p. 189 (PDF 203), et
  Model SN § 4.2 (feuille des notations), p. 51 (PDF 65), figure : Model SN — https://library.wmo.int/viewer/35795
- citation vérifiée le 2026-11-16 (texte et pagination, pdftotext sur la copie de l'édition 2018 mise à jour 2021).
- citation vérifiée le 2026-11-16 sur le texte public de l'appendice II-4 (mot pour mot) ; pagination de l'édition 2019 relevée sur la page rendue le 2026-09-09.

## Statut
prouvé — pour l'absence de seuil dans ces deux textes ; la pratique NOAA citée en Cause n'est pas une norme.
