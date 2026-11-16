# Pression du modèle de station en haut à droite, ou QNH présenté comme pression au niveau de la mer

## Symptôme
La pression est posée en haut à droite du cercle ; ou elle finit toujours par 0 (QNH entier
d'un METAR multiplié par 10) ; ou la température est sous le temps présent.

## Cause
La figure du modèle (Att. IV § 1) fixe les positions relatives : colonne de gauche de haut en bas
`T_xT_x`/`T_nT_n`, **`TTT` au-dessus de `ww`**, `T_dT_dT_d` en dessous ; `C_H` puis `C_M`
au-dessus du cercle ; **`PPPP` sur la ligne du cercle, immédiatement à droite** ; la tendance `a`
plus à droite. L'élément `PPPP` est la **pression au niveau moyen de la mer en dixièmes d'hPa**
(chiffre des milliers omis, tracée en 3 ou 4 chiffres). Le QNH d'un METAR est une autre grandeur
(réduction en atmosphère type, entier en hPa) : il diffère de la pression réduite d'1 à 2 hPa.

## Détection
Mesurer les décalages des étiquettes par rapport au centre du cercle : pression à dy ≈ 0, dx > 0 ;
température à dy < 0 (au-dessus) de `ww`. Sur 100 stations METAR, si la pression affichée finit
toujours par 0, c'est un QNH.

## Geste
Respecter la grille du modèle ; afficher le QNH sous son nom (fiche au clic) ou prendre la vraie
pression réduite (SYNOP `4PPPP`, remarque `SLPppp`).

## Versions concernées
WMO-No. 306 Vol. I.1, édition 2019, Attachment IV (pagination A-441 à A-456 = PDF 465 à 480). Les passages cités figurent mot pour mot dans l'appendice II-4 du Manuel du GDPFS (copie publique de l'OMM) ; les éditions antérieures à 2019 du WMO-No. 306 librement diffusées s'arrêtent à l'Attachment III.

## Source
- WMO-No. 306 Vol. I.1 (2019), Attachment IV § 1, figure du modèle, p. A-441 (PDF 465), et § 2.1
  `PPPP`, p. A-447 (PDF 471).
- Texte identique : Manuel du GDPFS, appendice II-4 § 1 et § 2.1 `PPPP` — https://old.wmo.int/extranet/pages/prog/www/ISS/Meetings/IPET-DRMM_Beijing2015/Documents/IPET-DRMM-III_Doc11-5_GDPFS_Manual_Appendix_II-4.pdf
- citation vérifiée le 2026-11-16 sur le texte public de l'appendice II-4 (mot pour mot) ; pagination de l'édition 2019 relevée sur la page rendue le 2026-09-09.

## Statut
prouvé
