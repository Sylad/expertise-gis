# Station automatique : pas de triangle, ou triangle à la place du cercle, et temps présent lu dans la mauvaise table

## Symptôme
Rien ne distingue une station automatique d'une station pourvue de personnel, ou le cercle de
nébulosité est remplacé par un triangle ; le symbole de temps présent d'une station automatique
est pris dans la planche 4677.

## Cause
Att. IV § 1 (sous la figure du modèle) : pour une station automatique, un **triangle équilatéral
est tracé autour du cercle de station**, **sommet vers la position du symbole de nuages moyens**
(C_M, au-dessus du cercle) — le cercle reste dessiné dedans. Corollaire : son temps présent se lit
en **table 4680** (`w_aw_a`, planche p. A-444) et son temps passé en **table 4531**, dont les
symboles diffèrent de 4677/4561 pour un même chiffre.

## Détection
Station de test automatique : un cercle + un triangle circonscrit sommet en haut ; le code de
temps présent est rendu par la planche 4680 (ex. brouillard en 30–35, pas en 40–49).

## Geste
Indicateur « automatique » porté par la donnée (SYNOP `i_x` ≥ 4, METAR `AUTO`), triangle et
table de symboles choisis par lui ; stocker la table utilisée avec le code.

## Versions concernées
WMO-No. 306 Vol. I.1, édition 2019, Attachment IV (pagination A-441 à A-456 = PDF 465 à 480). Les passages cités figurent mot pour mot dans l'appendice II-4 du Manuel du GDPFS (copie publique de l'OMM) ; les éditions antérieures à 2019 du WMO-No. 306 librement diffusées s'arrêtent à l'Attachment III.

## Source
- WMO-No. 306 Vol. I.1 (2019), Attachment IV § 1, figure « The surface plotting model »,
  p. A-441 (PDF 465) ; planche `w_aw_a` (table 4680), p. A-444 (PDF 468).
- Texte identique : Manuel du GDPFS, appendice II-4 § 1 et § 2.1 `wawa` — https://old.wmo.int/extranet/pages/prog/www/ISS/Meetings/IPET-DRMM_Beijing2015/Documents/IPET-DRMM-III_Doc11-5_GDPFS_Manual_Appendix_II-4.pdf
- citation vérifiée le 2026-11-16 sur le texte public de l'appendice II-4 (mot pour mot) ; pagination de l'édition 2019 relevée sur la page rendue le 2026-09-09.

## Statut
prouvé
