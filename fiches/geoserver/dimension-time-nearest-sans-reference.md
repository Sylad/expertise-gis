# Dimension TIME en « nearest » sans valeur de référence : couche absente des capabilities

## Symptôme
Une couche temporelle est visible par REST (`/rest/layers`) mais n'apparaît pas dans le
GetCapabilities WMS/WFS. Le journal n'a qu'un WARN :
`No reference value given for time dimension default value 'nearest' strategy`.

## Cause
La valeur par défaut de la dimension est en stratégie `NEAREST` sans `referenceValue` ;
l'encodage des capabilities lève une exception pour cette couche, qui est sautée en silence.

## Détection
```bash
curl -s "$GS/<ws>/wms?service=WMS&version=1.3.0&request=GetCapabilities" | grep -c "<Name><ws>:<couche></Name>"
curl -s -u "$AUTH" "$GS/rest/workspaces/<ws>/coveragestores/<s>/coverages/<c>.xml" | grep -A3 defaultValue
```

## Geste
`<defaultValue><strategy>MAXIMUM</strategy></defaultValue>` (dernier instant disponible) ou
`NEAREST` **avec** `<referenceValue>` explicite. Revérifier la présence de chaque couche dans
les capabilities après publication.

## Versions concernées
GeoServer 2.27 et 2.28.2 (vécu) ; 3.x non vérifié.

## Source
vécu consigné le 2026-05-11 (GeoServer 2.27/2.28.2, quatre couvertures temporelles).

## Statut
à reprouver — établi sur 2.27/2.28.
