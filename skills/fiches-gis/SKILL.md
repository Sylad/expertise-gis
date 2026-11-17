---
name: fiches-gis
description: Trouve et sert les fiches d'expertise-gis — pièges prouvés de GeoServer, GeoTools, GeoWebCache, PostGIS, SLD, OpenLayers, MapLibre, symbologie OACI/OMM (SIGWX, fronts, modèle de station, SIGMET), montées de version (Angular, TypeScript, Node, NestJS, GeoServer) et les 13 invariants d'un écran avec carte — et écrit le bloc « references: » prêt à copier dans le cadence.yaml d'un projet. À utiliser AVANT de diagnostiquer un symptôme de carte (image vide ou fausse, erreur WMS, TIME faux, capabilities lentes, style ignoré, objets mal placés, légende fausse, barbules ou fronts mal dessinés), et quand on demande « ajoute les références GIS au cadence.yaml », « quelles fiches pour ce projet ».
---

# fiches-gis

Le plugin embarque le dépôt expertise-gis : une fiche par piège (Symptôme, Cause, Détection,
Geste, Versions concernées, Source, Statut), rangées par domaine sous `fiches/`, indexées par
symptôme dans `fiches/README.md`, et la mécanique des écrans avec carte sous `ecrans-carte/`.
Le script ci-dessous est dans le dossier de ce skill (donné au chargement : « Base directory
for this skill ») ; la racine du dépôt est deux niveaux
au-dessus de ce dossier (`<dossier du skill>/../..`).

## 1. Un symptôme de carte : chercher la fiche d'abord

```bash
python3 "<dossier du skill>/scripts/fiches.py" chercher <mots du symptôme>
# ex. : chercher image cannot be decoded   ·   chercher capabilities lentes   ·   chercher barbules
```

Il affiche les fiches les plus proches, ✅ prouvé ou 🔁 à reprouver, avec leur chemin local.

1. Lis la fiche (outil Read) avant de proposer une cause.
2. Joue sa **Détection** sur le système réel : c'est elle qui tranche, pas la ressemblance du
   symptôme. Dis le résultat obtenu.
3. Compare la version du projet aux **Versions concernées**. Une fiche 🔁, ou une version
   différente, est une piste à vérifier, jamais une conclusion.
4. Cite la fiche (chemin) dans la réponse ou le commit.

Aucune fiche ne correspond : lis l'index par symptôme (`fiches/README.md`) ; s'il n'y a rien,
diagnostique normalement. Un piège nouveau, générique et prouvé peut devenir une fiche
(format `docs/format-fiche.md`), proposée au propriétaire du dépôt, jamais écrite d'office.

Écran avec carte (légende, unités, validité, curseur du temps, lien partagé, export, fiche au
clic) : lis `ecrans-carte/invariants.md` et `ecrans-carte/interface.md` ; les gabarits de
tests légende = rendu sont dans `ecrans-carte/gabarits/` (à copier dans le projet).

## 2. Brancher un projet : le bloc references: de son cadence.yaml

```bash
python3 "<dossier du skill>/scripts/fiches.py" domaines                      # ce qui existe
python3 "<dossier du skill>/scripts/fiches.py" references --domaines geoserver,sld,ecrans-carte
```

- Choisis les domaines d'après la pile du projet (lis son `package.json`, `pom.xml`, ses
  charts, ses styles) : GeoServer → `geoserver,sld` ; PostGIS → `postgis` ; OpenLayers →
  `openlayers` ; MapLibre → `maplibre` ; cartes OACI/OMM → `symbologie` ; front Angular /
  TypeScript / Node / NestJS → `angular,typescript,nodejs,nestjs` (fiches de montée de
  version) ; tout écran avec carte → `ecrans-carte`. Sans `--domaines` : tous.
- Le bloc a la forme unique de `references:` dans cadence (L760), lue par `cadence run` comme
  par `cadence ref` : `references: { dir, run: [{ mots: [...], docs: [...] }] }`. Quand un mot
  de `run` apparaît dans une demande (sans accents ni casse, en mot entier), cadence fait lire
  les `docs` en entier. Un doc doit être un **fichier présent sur la machine** : cadence
  écarte sans erreur une URL ou un fichier absent, et les fiches cessent d'être lues sans que
  personne ne le voie. `dir` (dossier des documents de `cadence ref`, hors de tout dépôt Git)
  est propre au projet : il n'est écrit qu'avec `--dir <dossier>`.
- Les `docs` visent le clone de la place de marché,
  `~/.claude/plugins/marketplaces/expertise-gis/…` : sans numéro de version, il survit à
  `claude plugin update` (la copie `plugins/cache/<place>/<plugin>/<version>/` d'où tourne le
  script est purgée à la mise à jour), et `~` le rend identique sur toute machine où le
  plugin est installé. `--racine <dossier>` vise un autre clone. Code de sortie 3 : un doc
  est absent ici ; le dire avant de coller.
- Colle le bloc dans le `cadence.yaml` du projet, sans dupliquer de clé. Si `references:`
  existe déjà : garde son `dir` ; sous son `run:`, ajoute seulement les entrées qui manquent
  (repère : le commentaire `# expertise-gis/<domaine>`), sans toucher aux autres. Si
  `references:` y est encore une liste (ancienne forme de `cadence run`, que cadence lit avec
  un message de migration), déplace cette liste sous `run:`. Montre le diff avant d'écrire.

## Règles

- Les fiches sont génériques : n'y ajoute rien de propre à un projet, un client ou un employeur.
- Une fiche dit ce qui a été prouvé, sur quelle version. Ne la présente pas comme valable
  au-delà.
