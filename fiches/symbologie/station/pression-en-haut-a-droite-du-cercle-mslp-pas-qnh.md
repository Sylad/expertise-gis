# Pression du modèle de station posée à droite du cercle, ou QNH présenté comme pression au niveau de la mer

## Symptôme
La pression est posée sur la rangée du cercle, juste à sa droite (là où va la tendance) ; ou elle
finit toujours par 0 (QNH entier d'un METAR multiplié par 10) ; ou la température est sous le
temps présent.

## Cause
La figure du modèle (Att. IV § 1) fixe les positions relatives dans une grille de cases (5 colonnes,
le cercle `N` au centre) : rangée du haut `T_xT_xT_x`/`T_nT_nT_n`, `C_H`, `E` ; rangée suivante
`TTT`, `C_M` puis **`PPPP` (ou `a_3hhh`)**, donc **`PPPP` sur la rangée de `TTT` et de `C_M`, en
haut à droite du cercle** ; sur la rangée du cercle : `VV`, `ww`, `N`, puis **`ppp` puis `a`** (valeur
et caractéristique de la tendance) ; sous `TTT`, `T_dT_dT_d`. `TTT` est donc au-dessus de `ww`.
L'élément `PPPP` est la **pression au niveau moyen de la mer en dixièmes d'hPa** (chiffre des
milliers omis, tracée en 3 ou 4 chiffres). Le QNH d'un METAR est une autre grandeur (réduction en
atmosphère type, entier en hPa) : il diffère de la pression réduite d'1 à 2 hPa.

## Détection
Mesurer les décalages des étiquettes par rapport au centre du cercle (y vers le bas) : pression à
dy < 0 (au-dessus du centre, même rangée que la température), dx > 0 ; tendance `ppp` à dy ≈ 0,
dx > 0, et `a` encore plus à droite ; température à dy < 0 (au-dessus) de `ww`. Sur 100 stations
METAR, si la pression affichée finit toujours par 0, c'est un QNH.

## Geste
Respecter la grille du modèle ; afficher le QNH sous son nom (fiche au clic) ou prendre la vraie
pression réduite (SYNOP `4PPPP`, remarque `SLPppp`).

## Versions concernées
WMO-No. 306 Vol. I.1, édition 2019, Attachment IV (pagination A-441 à A-456 = PDF 465 à 480). Les passages cités figurent mot pour mot dans l'appendice II-4 du Manuel du GDPFS (copie publique de l'OMM) ; les éditions antérieures à 2019 du WMO-No. 306 librement diffusées s'arrêtent à l'Attachment III.

## Source
- WMO-No. 306 Vol. I.1 (2019), Attachment IV § 1, figure du modèle, p. A-441 (PDF 465), et § 2.1
  `PPPP`, p. A-447 (PDF 471) ; `ppp` est décrit plus loin dans le même § 2.1 (page 2019 non relevée).
- Texte identique : Manuel du GDPFS, appendice II-4 § 1 (figure du modèle) et § 2.1
  `PPPP`, `ppp` — https://old.wmo.int/extranet/pages/prog/www/ISS/Meetings/IPET-DRMM_Beijing2015/Documents/IPET-DRMM-III_Doc11-5_GDPFS_Manual_Appendix_II-4.pdf
- citation vérifiée le 2026-11-16 sur le texte public de l'appendice II-4 (mot pour mot) ; position des cases relue le 2026-11-16 sur la figure rendue de l'appendice II-4 (`PPPP/PoPoPo` dans la case à droite de `C_M` ; à droite de `N`, une case imprimée « PPP » — l'élément `ppp` de la tendance, décrit au § 2.1 — puis `a`) ; pagination de l'édition 2019 relevée sur la page rendue le 2026-09-09.

## Statut
prouvé
