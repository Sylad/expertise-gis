# Format d'une fiche

Une fiche décrit **un piège** : ce qu'on voit, pourquoi, comment le prouver, quoi faire.
Elle vit dans `fiches/<domaine>/<slug>.md` (`geoserver`, `postgis`, `sld`, `openlayers`, `maplibre`, …), ou
`fiches/symbologie/<sous-domaine>/<slug>.md` (`sigwx`, `fronts-et-centres`, `station`, `zones-d-avis`), le slug en
kebab-case minuscule, et elle est listée dans l'index `fiches/README.md`, rangé par symptôme.

Le test `tests/test_fiches.py` vérifie ce format pour chaque fiche.

## Gabarit

```markdown
# Titre : le piège en une phrase

## Symptôme
Ce qu'on observe, avec les messages exacts (erreur, en-tête, code HTTP).

## Cause
Le mécanisme, au niveau du code ou de la configuration.

## Détection
La commande ou la mesure qui tranche, avec le résultat attendu dans chaque cas.

## Geste
Ce qu'on fait : correctif immédiat, puis correctif durable.

## Versions concernées
Versions où le piège a été vu ou prouvé ; « non vérifié » pour les autres.

## Source
Doc officielle, ticket ou code source (lien), ou « vécu AAAA-MM-JJ » avec le contexte
technique (versions, topologie), jamais le nom d'un projet, d'un client ou d'un employeur.

## Statut
prouvé
```

## Fiche de montée de version

Une montée de version a **une fiche par bibliothèque** (`fiches/<bibliothèque>/montee-<de>-a-<vers>….md`,
la bibliothèque nommée au titre), au même gabarit : chaque section Symptôme, Cause, Détection et
Geste est une liste numérotée (le n° d'un symptôme renvoie à sa cause et à son geste), et
**chaque point dit la nature de sa source entre crochets** : `[commit]`, `[notes de version]`,
`[runbook]`, `[notes de dépannage]`, `[notes de travail]`, `[lecture du code]`, `[mesure]`, `[doc …]`, `[code source …]`, `[ticket …]`,
`[CHANGELOG …]`, `[registre npm …]`, `[conventions du projet]`, `[fiche <slug>]` pour un point
repris d'une autre fiche de ce dépôt (le slug doit exister), ou `[déduction]` pour ce qui
n'a été ni lu ni joué. Une nature venue de la note (`[commit]`, `[runbook]`…) ne s'écrit que
sur ce que la note dit vraiment ; un point ajouté porte sa propre nature. Ce qu'on a recontrôlé soi-même le dit (`relu ici`, `mesure du AAAA-MM-JJ`).
Contrôlé par `test_fiches_de_montee` ; `test_commandes_sans_globstar` refuse `**/` dans
une commande (bash sans `globstar` le lit comme `*`).

## Les sept sections

## Symptôme
Ce qu'un utilisateur ou une sonde voit, mot pour mot quand c'est un message. C'est par lui
qu'on retrouve la fiche : l'index est rangé par symptôme.

## Cause
Le mécanisme. Une hypothèse non démontrée est écrite comme telle.

## Détection
Une commande ou une mesure reproductible (`curl -w`, requête SQL, `jcmd`, comptage de
pixels…) et ce qu'elle doit montrer. Jamais « regarder si ça a l'air bon ».

## Geste
Le correctif, et sa preuve d'effet (la mesure de la détection qui change).

## Versions concernées
Les versions exactes où le fait a été établi. Un fait établi sur une version ancienne
(par exemple GeoServer 2.28 quand la version courante est 3.x) est marqué « à reprouver ».
Pour les bibliothèques côté client, la fiche « prouvé » nomme la bibliothèque avec une version
courante suivie de « (vécu » ou « (code relu et mesure » (`OpenLayers 10 (vécu)`,
`MapLibre GL JS 5.24 (vécu, …)`) : un fait établi seulement sur OpenLayers < 10 ou
MapLibre < 5 est « à reprouver », et une version citée « non vérifié » ou « documenté » ne
compte pas (contrôlé par le test).

## Source
Au moins un lien (doc officielle, ticket, code source) ou un « vécu » daté `AAAA-MM-JJ`.

Fiches de **symbologie normalisée** (`fiches/symbologie/`, contrôlé par le test) : la Source cite
le document, le **§** (ou, pour un tableau ou un modèle de carte, la `Table`, la `note` ou le
`Model` numérotés), la **page imprimée** (`p. 189`, `p. A-453`) **et** la **page PDF** (`PDF 203`),
et la **figure** (`figure : …`, ou `figure : aucune (règle de texte)`). La fiche dit ce que dit la
norme et ses pièges de lecture, jamais comment un projet l'a codée ; elle résume la règle et ne
recopie pas de longs extraits. Elle n'est « prouvé » que si la citation a été recontrôlée sur le
texte — la Source le dit par « citation vérifiée le AAAA-MM-JJ » ; une citation reprise d'une
étude sans contrôle sur le document donne « à reprouver ».

## Statut
Première ligne : `prouvé` ou `à reprouver`, éventuellement suivi d'une raison.
- **prouvé** : établi par la doc, le code source, ou une mesure vécue sur la version citée.
- **à reprouver** : établi seulement sur une version ancienne, ou cause non démontrée.
Un fait ni prouvé ni reprouvable n'a pas de fiche.

## Règles du dépôt public

- Rien de propre à un projet : ni nom de couche, d'espace de travail, de chart, de
  plugin maison, d'URL, de machine ; ni nom d'employeur ou de client.
- Aucun terme privé n'est écrit dans un fichier suivi par git, pas même dans le test.
  Le test lit la liste dans un fichier `.termes-prives` à la racine (une expression par
  ligne, ignoré par git) ou dans `EXPERTISE_GIS_TERMES_PRIVES` (séparés par des
  virgules), et contrôle tous les fichiers suivis (`git ls-files`). Sans liste, il échoue.
- Deux fiches qui décrivent le même piège sont fusionnées.
