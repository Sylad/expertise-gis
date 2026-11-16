# Faux symboles de temps présent, ou case vide là où la norme demande « // »

## Symptôme
Une station par ciel clair porte un symbole de neige ou de pluie (code déduit d'un texte brut
mal découpé), ou la case de temps présent est vide pour une station automatique qui n'a pas
transmis le groupe 7, ou « // » partout.

## Cause
Att. IV § 2.1, notes de l'élément `ww` (et `w_aw_a`) : quand le temps présent et passé ne sont
pas inclus parce qu'ils **ne sont pas significatifs** (`i_x` = 2 ou 5), les cases sont **laissées
vides** ; parce qu'**aucune observation** n'a été faite (`i_x` = 3 ou 6) ou que **les données
manquent** (`i_x` = 1 ou 4 pour 4677, 7 pour 4680, **sans groupe 7**), elles portent **« // »**.
Le piège courant : traiter « groupe 7 absent » comme « non significatif ». Autre piège : déduire un
code d'un message brut sans grammaire (`SN` trouvé dans un indicatif d'aérodrome).

## Détection
Table de cas : `i_x` 1–7 × groupe 7 présent/absent → vide, « // » ou symbole ; vérifier aussi
qu'un message sans phénomène ne produit aucun symbole.

## Geste
Coder la règle des notes telle quelle ; extraire le groupe de temps par une grammaire, jamais
par recherche de sous-chaîne.

## Versions concernées
WMO-No. 306 Vol. I.1, édition 2019, Attachment IV (pagination A-441 à A-456 = PDF 465 à 480). Les passages cités figurent mot pour mot dans l'appendice II-4 du Manuel du GDPFS (copie publique de l'OMM) ; les éditions antérieures à 2019 du WMO-No. 306 librement diffusées s'arrêtent à l'Attachment III.

## Source
- WMO-No. 306 Vol. I.1 (2019), Attachment IV § 2.1 `ww`, note 2, et planche `ww` (table 4677),
  p. A-443 (PDF 467) ; planche `w_aw_a`, p. A-444 (PDF 468) ; figure : les deux planches.
- Texte identique : Manuel du GDPFS, appendice II-4 § 2.1, notes de `ww` et de `wawa` — https://old.wmo.int/extranet/pages/prog/www/ISS/Meetings/IPET-DRMM_Beijing2015/Documents/IPET-DRMM-III_Doc11-5_GDPFS_Manual_Appendix_II-4.pdf
- citation vérifiée le 2026-11-16 sur le texte public de l'appendice II-4 (mot pour mot) ; pagination de l'édition 2019 relevée sur la page rendue le 2026-09-09.

## Statut
prouvé
