# Barbules à 180° : la hampe pointe sous le vent parce qu'on a ajouté 180° à une direction « d'où vient »

## Symptôme
Sur le modèle de station, la hampe d'une station à vent de nord pointe vers le sud ; les barbules
d'observation contredisent les flèches de vent d'un modèle sur la même carte.

## Cause
Att. IV § 2.1 `ddff` : `dd` est la **direction vraie d'où vient le vent** ; la hampe est
dirigée le long de l'axe du vent **vers le centre du cercle de station** et s'arrête à sa
circonférence. Une hampe vers le nord = vent du nord. Le piège : réutiliser pour les observations
la rotation +180° écrite pour une direction « vers où va le vent » (composantes u/v d'un modèle,
flèches).

## Détection
Station de test à `dd = 0` (vent du nord) : la hampe part du cercle vers le **nord** ; à
`dd = 90` vers l'est. Une rotation de 180° se voit immédiatement.

## Geste
Deux fonctions de rotation distinctes et nommées : « depuis direction d'où vient » (identité,
observations) et « depuis direction vers où va » (+180°, champs u/v) ; test unitaire sur dd = 0.

## Versions concernées
WMO-No. 306 Vol. I.1, édition 2019, Attachment IV (pagination A-441 à A-456 = PDF 465 à 480). Les passages cités figurent mot pour mot dans l'appendice II-4 du Manuel du GDPFS (copie publique de l'OMM) ; les éditions antérieures à 2019 du WMO-No. 306 librement diffusées s'arrêtent à l'Attachment III.

## Source
- WMO-No. 306 Vol. I.1 (2019), Attachment IV § 2.1, élément `ddff`, p. A-442 (PDF 466) ; figure :
  symbole de calme et exemple « x——o » sur la même page.
- Texte identique : Manuel du GDPFS, appendice II-4 § 2.1 `ddff` — https://old.wmo.int/extranet/pages/prog/www/ISS/Meetings/IPET-DRMM_Beijing2015/Documents/IPET-DRMM-III_Doc11-5_GDPFS_Manual_Appendix_II-4.pdf
- citation vérifiée le 2026-11-16 sur le texte public de l'appendice II-4 (mot pour mot) ; pagination de l'édition 2019 relevée sur la page rendue le 2026-09-09.

## Statut
prouvé
