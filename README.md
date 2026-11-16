# expertise-gis

Savoir générique et prouvé sur les outils de carte (GeoServer, GeoTools, PostGIS, OpenLayers, MapLibre, symbologie OACI/OMM) et sur la mécanique des écrans avec carte, partagé par les sessions Claude de Sylvain.

Une fiche par piège : symptôme, cause, détection, geste, version, source. Rien de propre à un projet, un client ou un employeur.

## Contenu

- `fiches/<domaine>/<slug>.md` — les fiches (`geoserver`, `postgis`, `sld`…), indexées par symptôme dans [`fiches/README.md`](fiches/README.md).
- `docs/format-fiche.md` — le format d'une fiche et les règles du dépôt public.
- `tests/test_fiches.py` — vérifie chaque fiche : sections, statut, source, liens, index, termes interdits.

```bash
python3 -m unittest discover -s tests -v
```

Termes qu'on ne veut pas même écrire ici (noms de société) : `EXPERTISE_GIS_TERMES_PRIVES="a,b"` ou un fichier `.termes-prives` (ignoré par git), un terme par ligne.
