# Calme dessiné par un cercle seul, vent manquant omis ou dessiné à zéro

## Symptôme
Une station calme n'a qu'un cercle (indiscernable d'une station sans vent observé), ou une
station dont la vitesse manque n'affiche rien alors que la direction est connue ; une direction
« variable » est dessinée comme une direction.

## Cause
Att. IV § 2.1 `ddff` : le **calme** est un **cercle tracé autour du cercle de station** (deux
cercles concentriques) ; une **vitesse manquante** est un **« x » au bout de la hampe** à la place
des barbules, la direction étant tracée normalement ; une **direction manquante** = **aucun vent
tracé**. Une direction « variable » (VRB d'un METAR) n'est pas une direction.

## Détection
Trois stations de test : calme → 2 cercles concentriques ; direction connue + vitesse nulle /
manquante → hampe + « x » ; direction manquante ou VRB → aucun trait de vent.

## Geste
Trois cas distincts dans le code de tracé, avec leurs tests ; ne jamais confondre « 0 kt » et
« vitesse inconnue ».

## Versions concernées
WMO-No. 306 Vol. I.1, édition 2019, Attachment IV (pagination A-441 à A-456 = PDF 465 à 480). Les passages cités figurent mot pour mot dans l'appendice II-4 du Manuel du GDPFS (copie publique de l'OMM) ; les éditions antérieures à 2019 du WMO-No. 306 librement diffusées s'arrêtent à l'Attachment III.

## Source
- WMO-No. 306 Vol. I.1 (2019), Attachment IV § 2.1, élément `ddff`, p. A-442 (PDF 466) ; figure :
  symbole de calme et exemple « x——o » sur la même page.
- Texte identique : Manuel du GDPFS, appendice II-4 § 2.1 `ddff` — https://old.wmo.int/extranet/pages/prog/www/ISS/Meetings/IPET-DRMM_Beijing2015/Documents/IPET-DRMM-III_Doc11-5_GDPFS_Manual_Appendix_II-4.pdf
- citation vérifiée le 2026-11-16 sur le texte public de l'appendice II-4 (mot pour mot) ; pagination de l'édition 2019 relevée sur la page rendue le 2026-09-09.

## Statut
prouvé
