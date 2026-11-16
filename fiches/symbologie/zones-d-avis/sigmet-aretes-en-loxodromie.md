# Zone SIGMET décalée de plusieurs kilomètres : les côtés sont des loxodromies, pas des géodésiques

## Symptôme
Un SIGMET à côtés longs est-ouest à haute latitude (`S OF LINE` de 800 km vers 65° N, côté de
polygone sur un parallèle) n'a pas la même forme que chez un autre fournisseur ; l'écart atteint des
dizaines de kilomètres au milieu du segment. Un bord `N OF N54` tracé avec deux sommets « bombe »
vers le pôle.

## Cause
WMO-No. 49 Vol. II, App. 6, Table A6-1A, **note 22** : la ligne droite entre deux points est
celle d'une **carte en projection de Mercator**, ou qui **coupe les méridiens sous un angle
constant** — une loxodromie. La note porte sur les côtés de polygone `WI`, les lignes `OF LINE` et
l'axe des couloirs `WID LINE`. Les rayons (`WI nnKM OF`) et demi-largeurs de couloir restent des
distances sur l'ellipsoïde. Un client qui densifie en grand cercle (ou relie deux sommets en ligne
droite sur un globe) trace autre chose ; un parallèle est une loxodromie à cap 90°.

## Détection
Pour un segment, mesurer l'écart maximal (au milieu) entre la loxodromie et le grand cercle :
nul sur un méridien, ~27 km pour 964 km vers 63° N (sphère de 6 371 km). Comparer la zone tracée
à une densification loxodromique de référence (IoU ≈ 1).

## Geste
Densifier les arêtes à cap constant (fonctions « rhumb » d'une bibliothèque géodésique) avant
toute découpe ou reprojection ; rayons et largeurs en géodésique.

## Versions concernées
WMO-No. 49 Vol. II, édition 2018 mise à jour 2021 (texte commun avec l'Annexe 3 de l'OACI à cette date ; pagination : page PDF = page imprimée + 14). Les dispositions de présentation passent au PANS-MET (Doc 10157, non libre) : non vérifié dans le PANS-MET.

## Source
- WMO-No. 49 Vol. II (2018, mise à jour 2021), App. 6, Table A6-1A, note 22, p. 143 (PDF 157) ;
  figure : aucune (règle de texte). — https://library.wmo.int/viewer/35795
- citation vérifiée le 2026-11-16 (texte et pagination, pdftotext sur la copie de l'édition 2018 mise à jour 2021).

## Statut
prouvé
