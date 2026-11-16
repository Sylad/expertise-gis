# Isobares tracées à 1 002, 1 006… : la série normalisée doit contenir 1 000 hPa

## Symptôme
Les isobares sont tracées tous les 4 hPa à partir du minimum du champ (1 002, 1 006, 1 010…),
ou un gras « tous les 20 hPa » est présenté comme la norme.

## Cause
WMO-No. 306 Att. IV § 4.1.2 : intervalles de **4 ou 5 hPa** (multiples ou sous-multiples
selon l'échelle) mais, **quel que soit l'intervalle, l'isobare 1 000 hPa doit toujours appartenir
à la série**. Une série calée sur le minimum du champ glisse d'une échéance à l'autre. Rien n'est
dit d'une graisse d'isobares « principales » : le gras tous les 20 hPa est un usage.

## Détection
Lister les valeurs des isobares produites : `(v − 1000) mod intervalle == 0` pour toutes.

## Geste
Caler la série sur 1 000 hPa (`base = 1000`, pas `min(champ)`), intervalle 4 ou 5 ; présenter
le gras éventuel comme un choix de lisibilité.

## Versions concernées
WMO-No. 306 Vol. I.1, édition 2019, Attachment IV (pagination A-441 à A-456 = PDF 465 à 480). Les passages cités figurent mot pour mot dans l'appendice II-4 du Manuel du GDPFS (copie publique de l'OMM) ; les éditions antérieures à 2019 du WMO-No. 306 librement diffusées s'arrêtent à l'Attachment III.

## Source
- WMO-No. 306 Vol. I.1 (2019), Attachment IV § 4.1.2 « Isobars », p. A-453 (PDF 477) ;
  figure : aucune (règle de texte).
- Texte identique : Manuel du GDPFS, appendice II-4 § 4.1.2 — https://old.wmo.int/extranet/pages/prog/www/ISS/Meetings/IPET-DRMM_Beijing2015/Documents/IPET-DRMM-III_Doc11-5_GDPFS_Manual_Appendix_II-4.pdf
- citation vérifiée le 2026-11-16 sur le texte public de l'appendice II-4 (mot pour mot) ; pagination de l'édition 2019 relevée sur la page rendue le 2026-09-09.

## Statut
prouvé
