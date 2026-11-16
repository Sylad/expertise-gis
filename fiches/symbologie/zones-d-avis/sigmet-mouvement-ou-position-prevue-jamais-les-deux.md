# Zone SIGMET avec flèche de mouvement ET position prévue, ou niveaux qui changent entre les deux

## Symptôme
La carte dessine pour un même SIGMET une flèche `MOV` et un second contour prévu ; ou la position
prévue est dessinée avec d'autres niveaux que la position observée.

## Cause
Table A6-1A, **note 26** : les éléments « heure et position prévues » **ne s'emploient pas avec**
l'élément « mouvement ou mouvement prévu » — un message correct n'a que l'un des deux. **Note 27** :
les niveaux du phénomène **restent fixes sur toute la période** de prévision. Afficher les deux en
même temps suppose une information que le message ne porte pas ; changer les niveaux aussi.

## Détection
Sur le jeu de messages : aucune entité ne porte à la fois une flèche et un contour prévu ; les
niveaux affichés pour la position prévue = ceux de l'observation. Un message qui contiendrait les
deux est signalé (non conforme), pas « réparé ».

## Geste
Rendu exclusif : flèche (avec vitesse si donnée) **ou** contour prévu (style distinct, par exemple
tireté) ; niveaux repris de l'observation.

## Versions concernées
WMO-No. 49 Vol. II, édition 2018 mise à jour 2021 (texte commun avec l'Annexe 3 de l'OACI à cette date ; pagination : page PDF = page imprimée + 14). Les dispositions de présentation passent au PANS-MET (Doc 10157, non libre) : non vérifié dans le PANS-MET.

## Source
- WMO-No. 49 Vol. II (2018, mise à jour 2021), App. 6, Table A6-1A, notes 26 et 27, p. 144
  (PDF 158) ; figure : aucune (règle de texte). — https://library.wmo.int/viewer/35795
- citation vérifiée le 2026-11-16 (texte et pagination, pdftotext sur la copie de l'édition 2018 mise à jour 2021).

## Statut
prouvé
