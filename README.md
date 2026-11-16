# expertise-gis

Savoir générique et prouvé sur les outils de carte (GeoServer, GeoTools, PostGIS, OpenLayers, MapLibre, symbologie OACI/OMM) et sur la mécanique des écrans avec carte, partagé par des sessions Claude.

Une fiche par piège : symptôme, cause, détection, geste, version, source. Rien de propre à un projet, un client ou un employeur.

## Contenu

- `fiches/<domaine>/<slug>.md` — les fiches (`geoserver`, `postgis`, `sld`, `openlayers`, `maplibre`…, et `symbologie/<sous-domaine>/` pour la symbologie OACI/OMM), indexées par symptôme dans [`fiches/README.md`](fiches/README.md).
- `ecrans-carte/` — la mécanique des écrans avec carte : les 13 invariants (`invariants.md`), les règles d'interface utilisable sur carte et leurs contrôles (`interface.md`), des gabarits de tests légende = rendu, mesure des boîtes et contraste, sans dépendance, à copier dans un projet (`gabarits/`).
- `docs/format-fiche.md` — le format d'une fiche et les règles du dépôt public.
- `tests/test_fiches.py` — vérifie chaque fiche (sections, statut, source, liens, index) et l'absence de termes privés dans tous les fichiers suivis.
- `tests/test_ecrans_carte.py` — vérifie les 13 invariants et les règles sourcées d'`ecrans-carte/`, et fait tourner les gabarits (Python, et JavaScript par `node --test` si Node est présent).

```bash
python3 -m unittest discover -s tests -v
```

Termes privés (projets, machines, noms de société…) : aucun n'est écrit dans un fichier suivi par git. Le test les lit dans un fichier `.termes-prives` à la racine (une expression par ligne, ignoré par git) ou dans `EXPERTISE_GIS_TERMES_PRIVES="a,b"`. Sans liste, il échoue en disant quoi faire.
