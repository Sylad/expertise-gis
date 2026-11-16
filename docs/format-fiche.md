# Format d'une fiche

Une fiche décrit **un piège** : ce qu'on voit, pourquoi, comment le prouver, quoi faire.
Elle vit dans `fiches/<domaine>/<slug>.md` (`geoserver`, `postgis`, `sld`, …), le slug en
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

## Source
Au moins un lien (doc officielle, ticket, code source) ou un « vécu » daté `AAAA-MM-JJ`.

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
