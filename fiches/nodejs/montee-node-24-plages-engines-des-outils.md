# Node 24 : un contrôle « Node ≥ 22.12 » codé en dur laisse passer un Node que la CLI Angular 22 refuse

Fiche de montée de version. Natures de source entre crochets : [commit] / [notes de version]
= historique d'une équipe passée en Node 24 avec Angular 22 et NestJS 12 ;
[registre npm, mesure du 2026-11-17] = recontrôlé pour cette fiche.

## Symptôme
1. Un contrôle de prérequis du projet (« Node ≥ 22.12 ») passe, puis `ng` ou `npm ci`
   refuse le Node présent : la CLI 22 exige `^22.22.3 || ^24.15.0 || >=26.0.0`.
   [notes de version] [registre npm, mesure du 2026-11-17]
2. Chaque exécution de CI avertit d'un forçage sur Node 24 des actions `checkout` /
   `setup-node` v4. [notes de version]
3. La porte de tests lancée par un script (hook, tâche planifiée) échoue ou passe sous un
   autre Node que celui du développeur. [commit]

## Cause
1. La plage `engines.node` change à chaque majeure de l'outil : Angular 20 et 21 acceptent
   `^20.19.0 || ^22.12.0 || >=24.0.0`, Angular 22 (core et CLI)
   `^22.22.3 || ^24.15.0 || >=26.0.0` ; un seuil recopié une fois devient faux.
   [registre npm, mesure du 2026-11-17]
2. Les actions v4 visent Node 20, déprécié par le service de CI. [notes de version]
3. Un script lancé hors du shell interactif prend le Node du `PATH` courant, pas celui de
   `.nvmrc` (nvm n'est chargé que par le shell interactif). [commit]

## Détection
1. `npm view @angular/cli@<majeure> engines.node` et
   `node -p "require('@angular/cli/package.json').engines.node"` dans le projet, comparés à
   `node --version`. [registre npm, mesure du 2026-11-17]
2. Journal de la CI : avertissement de forçage de version de Node. [notes de version]
3. `node --version` écrit en tête de la porte de tests, comparé à `.nvmrc`. [commit]

## Geste
1. Lire la plage `engines.node` de l'outil installé au lieu d'un seuil codé en dur ;
   `.nvmrc` = la majeure validée (24) ; `engines.node` du projet recopié de la CLI ; Dockerfile
   et CI suivent `.nvmrc`. [notes de version]
2. Actions `checkout` / `setup-node` en v7. [notes de version]
3. La porte de tests met explicitement le Node de `.nvmrc` en tête du `PATH`. [commit]
4. Monter Node **avant** Angular 22 : 20 et 21 acceptent déjà Node 24, 22 refuse un
   Node 22 < 22.22.3. [registre npm, mesure du 2026-11-17] [déduction]

## Versions concernées
Node 24 (vécu, `.nvmrc` = 24) avec Angular CLI 22.2 ; plages relues au registre npm le
2026-11-17 : `@angular/cli` 21.2.30 et 22.2.7, `@angular/core` 20.3.35, 21.2.26, 22.2.6.
Versions des actions de CI : non revérifiées ici.

## Source
- Retour d'expérience reçu le 2026-11-17 (vécu, Node 24 sous Angular 22.2 et NestJS 12).
- https://angular.dev/reference/versions
- Registre npm, 2026-11-17 : `npm view @angular/cli@{21,22} engines`,
  `npm view @angular/core@{20.3,21,22} engines`.

## Statut
prouvé
