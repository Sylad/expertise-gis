# expertise-gis

Savoir générique et prouvé sur les outils de carte (GeoServer, GeoTools, PostGIS, OpenLayers, MapLibre, symbologie OACI/OMM) et sur la mécanique des écrans avec carte, partagé par des sessions Claude.

Une fiche par piège : symptôme, cause, détection, geste, version, source. Rien de propre à un projet, un client ou un employeur.

## Contenu

- `fiches/<domaine>/<slug>.md` — les fiches (`geoserver`, `postgis`, `sld`, `openlayers`, `maplibre`…, et `symbologie/<sous-domaine>/` pour la symbologie OACI/OMM), indexées par symptôme dans [`fiches/README.md`](fiches/README.md).
- `ecrans-carte/` — la mécanique des écrans avec carte : les 13 invariants (`invariants.md`), les règles d'interface utilisable sur carte et leurs contrôles (`interface.md`), des gabarits de tests légende = rendu, mesure des boîtes et contraste, sans dépendance, à copier dans un projet (`gabarits/`).
- `skills/fiches-gis/` — le skill du plugin Claude Code : trouve la fiche d'un symptôme
  (`scripts/fiches.py chercher …`) et écrit le bloc `references:` à copier dans le
  `cadence.yaml` d'un projet (`scripts/fiches.py references --domaines …`).
- `.claude-plugin/` — le dépôt est à la fois une marketplace et un plugin Claude Code.
- `docs/format-fiche.md` — le format d'une fiche et les règles du dépôt public.
- `tests/test_fiches.py` — vérifie chaque fiche (sections, statut, source, liens, index) et l'absence de termes privés dans tous les fichiers suivis.
- `tests/test_plugin.py` — vérifie les manifestes du plugin, le skill, la recherche par symptôme et le bloc `references:`, passé à la fonction `aiguiller` de cadence quand son dépôt est à côté (`CADENCE_RACINE`) et Node présent.
- `tests/test_ecrans_carte.py` — vérifie les 13 invariants et les règles sourcées d'`ecrans-carte/`, et fait tourner les gabarits (Python, et JavaScript par `node --test` si Node est présent).

```bash
python3 -m unittest discover -s tests -v
```

## Installer le plugin (tout compte Claude Code)

Le dépôt est public : un compte perso comme un compte pro l'installent de la même façon,
dans Claude Code :

```text
/plugin marketplace add Sylad/expertise-gis
/plugin install expertise-gis@expertise-gis
```

ou en ligne de commande : `claude plugin marketplace add Sylad/expertise-gis` puis
`claude plugin install expertise-gis@expertise-gis`. Mise à jour :
`claude plugin marketplace update expertise-gis` puis `claude plugin update expertise-gis@expertise-gis`
(une nouvelle version demande d'augmenter `version` dans `.claude-plugin/plugin.json` et
`marketplace.json`). Le skill `fiches-gis` se déclenche sur un symptôme de carte, ou à la demande :

```bash
python3 <dossier du skill>/scripts/fiches.py chercher capabilities lentes
python3 <dossier du skill>/scripts/fiches.py references --domaines geoserver,sld,ecrans-carte
```

Le bloc `references:` a le format que lit `cadence run` : une liste de
`{ mots: [...], docs: [...] }` ; un mot de la liste dans une demande fait lire les `docs`.
Ce sont des fichiers locaux (cadence écarte sans erreur une URL ou un fichier absent), pris
dans le clone de la place de marché, `~/.claude/plugins/marketplaces/expertise-gis/` : sans
numéro de version, il survit aux mises à jour du plugin. `--racine <dossier>` vise un autre
clone ; le script sort avec le code 3 si un doc manque sur la machine.

Termes privés (projets, machines, noms de société…) : aucun n'est écrit dans un fichier suivi par git. Le test les lit dans un fichier `.termes-prives` à la racine (une expression par ligne, ignoré par git) ou dans `EXPERTISE_GIS_TERMES_PRIVES="a,b"`. Sans liste, il échoue en disant quoi faire.
