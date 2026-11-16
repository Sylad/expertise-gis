# Maximum de vent marqué comme un centre (croix, valeur dessous) au lieu de « J 120 »

## Symptôme
Sur une carte d'isotaches ou de vent maximal, le maximum est marqué avec une croix et la vitesse
sous la croix, comme un centre de pression, ou les isotaches sont tracées tous les 10 kt sans
raison d'échelle.

## Cause
WMO-No. 306 Att. IV § 4.2.4 : isotaches **tous les 20 kt** (40, 10 et 5 « when appropriate ») ;
sur les cartes de vent maximal, le maximum est marqué **« J » suivi de la vitesse estimée**
(`J 120`) ; le texte ne prévoit pas de croix (en déduire « sans croix » est une lecture, pas une
phrase de la norme) ; les autres centres de minimum et maximum de vitesse
relèvent des pratiques nationales. § 4.2.5 : un courant-jet est un **trait épais continu** portant
des **pointes de flèche à intervalles** dans le sens de l'écoulement.

## Détection
Repérer le texte du maximum : motif `^J ?\d{2,3}$`, aucune croix sous lui ; intervalle des
isotaches = 20 kt (ou 40/10/5 justifié par l'échelle).

## Geste
Étiquette `J <kt>` au maximum, sans croix (le texte n'en prévoit pas) ; isotaches à 20 kt par défaut.

## Versions concernées
WMO-No. 306 Vol. I.1, édition 2019, Attachment IV (pagination A-441 à A-456 = PDF 465 à 480). Les passages cités figurent mot pour mot dans l'appendice II-4 du Manuel du GDPFS (copie publique de l'OMM) ; les éditions antérieures à 2019 du WMO-No. 306 librement diffusées s'arrêtent à l'Attachment III.

## Source
- WMO-No. 306 Vol. I.1 (2019), Attachment IV § 4.2.4 et § 4.2.5, p. A-454 (PDF 478) ; figure :
  aucune (règle de texte).
- Texte identique : Manuel du GDPFS, appendice II-4 § 4.2.4–4.2.5 — https://old.wmo.int/extranet/pages/prog/www/ISS/Meetings/IPET-DRMM_Beijing2015/Documents/IPET-DRMM-III_Doc11-5_GDPFS_Manual_Appendix_II-4.pdf
- citation vérifiée le 2026-11-16 sur le texte public de l'appendice II-4 (mot pour mot) ; pagination de l'édition 2019 relevée sur la page rendue le 2026-09-09.

## Statut
prouvé
