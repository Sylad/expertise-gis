# Avis de cendres : le tireté de la figure normalisée lu comme « prévision », « NO VA EXP » dessiné comme une zone vide

## Symptôme
Sur une carte d'avis de cendres volcaniques, les nuages prévus sont tiretés « comme sur la
norme » alors que les couches superposées ne se distinguent pas ; ou une échéance « NO VA EXP »
n'affiche rien, ce qui se lit comme une donnée manquante.

## Cause
MODEL VAG (avis de cendres en format graphique) : quatre vignettes OBS / +6 / +12 / +18 h, un
polygone en trait fin par couche étiqueté par sa bande de niveaux (`SFC/FL090`, `FL090/150`). Dans
l'exemple 1, **le tireté distingue la couche haute de la couche basse superposée**, pas l'observé
du prévu (l'échéance est donnée par la vignette). L'échéance sans cendres porte un **encadré `NO VA
EXP`**. Aucun aplat, aucune couleur dans le modèle : aplats et couleurs des sites des centres sont
des usages.

## Détection
Sur un message à deux couches superposées, les deux contours doivent différer ; sur une
échéance `NO VA EXP`, un texte encadré est présent.

## Geste
Distinguer les couches (trait, teinte) ; distinguer la prévision par l'échéance affichée (barre
de temps, cartouche), et si l'on tirete aussi le prévu, le dire dans la légende ; encadré pour
`NO VA EXP`, libellés distincts pour `NOT AVBL` / `NOT PROVIDED`.

## Versions concernées
WMO-No. 49 Vol. II, édition 2018 mise à jour 2021 (texte commun avec l'Annexe 3 de l'OACI à cette date ; pagination : page PDF = page imprimée + 14). Les dispositions de présentation passent au PANS-MET (Doc 10157, non libre) : non vérifié dans le PANS-MET.

## Source
- WMO-No. 49 Vol. II (2018, mise à jour 2021), App. 1, MODEL VAG, exemple 1 (Mercator) p. 45
  (PDF 59) et exemple 2 (stéréographique polaire) p. 46 (PDF 60) ; figure : les vignettes de
  l'exemple 1. — https://library.wmo.int/viewer/35795
- citation vérifiée le 2026-11-16 (texte et pagination, pdftotext sur la copie de l'édition 2018 mise à jour 2021).

## Statut
prouvé — pages et intitulés recontrôlés ; l'usage du tireté est lu sur la figure.
