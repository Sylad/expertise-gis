# NestJS 12 en modules ES : alias `paths` non résolus à l'exécution, `__dirname` absent, `nest-winston` refusé

Fiche de montée de version. Natures de source entre crochets : [notes de version] = notes
d'un générateur de projets NestJS remis à niveau sur `@nestjs/cli@latest` ;
[registre npm, mesure du 2026-11-17] et [mesure du 2026-11-17] = recontrôlé pour cette fiche ;
[déduction] = ajouté ici, absent de la note. Une seule nature de
source pour l'essentiel : aucune application NestJS existante montée en 12 n'est attestée.

## Symptôme
1. Le build passe, l'exécution échoue sur un import d'alias (`@logger/…`) : module
   introuvable. [notes de version]
2. `ReferenceError: __dirname is not defined in ES module scope` ; import relatif sans
   extension refusé : `Error [ERR_MODULE_NOT_FOUND]: Cannot find module '…/b'`.
   [mesure du 2026-11-17, Node 22.23 avec `"type": "module"`]
3. `npm install` refuse `nest-winston` (peer dependency sur NestJS < 12) ; même refus pour
   toute bibliothèque tierce qui n'a pas publié de version compatible. [notes de version]

## Cause
1. `@nestjs/cli` génère NestJS 12 en **modules ES** (`"type": "module"` dans
   `@nestjs/core` 12) avec TypeScript 6, Vitest et oxlint ; `nest build` laisse les alias
   `paths` tels quels, et Node ne les résout pas en ESM.
   [notes de version] [registre npm, mesure du 2026-11-17]
2. En ESM, ni `__dirname` ni la résolution sans extension. [doc Node, modules ES]
   [mesure du 2026-11-17]
3. `nest-winston` n'est plus maintenu. [notes de version]

## Détection
1. `node dist/main.js` (pas seulement `nest build`) après tout changement d'alias.
   [notes de version]
2. `grep -rnE "__dirname|from '\.{1,2}/[^']*'" src/ | grep -vE "from '[^']*\.js'"` :
   `__dirname` et imports relatifs sans `.js` seulement. [déduction, commande jouée le
   2026-11-17 sur un fichier témoin]
3. `npm ls --all 2>&1 | grep -i 'peer'` ou `npm view <bibliothèque> peerDependencies`.
   [registre npm, mesure du 2026-11-17]

## Geste
1. Remplacer les alias `paths` par les subpath imports de `package.json` (`"imports"`,
   `#logger/app.logger.js`), avec `customConditions` côté TypeScript et
   `ssr.resolve.conditions` côté Vitest ; retirer `tsconfig-paths`, `vite-tsconfig-paths` et
   `baseUrl` (voir [la fiche TypeScript](../typescript/montee-5-9-a-6-baseurl-et-imports-a-effet-de-bord.md)).
   [notes de version]
2. Imports avec extension `.js` ; `__dirname` → `import.meta.dirname`. [notes de version]
3. Logger : remplacer `nest-winston` par une extension de `ConsoleLogger` ; vérifier les
   peer dependencies de chaque bibliothèque tierce avant de monter. [notes de version]
4. Node : le générateur exige Node ≥ 22.22.3 ou ≥ 24.15 (images et CI en Node 24), mais
   `@nestjs/core` 12.5.1 déclare `node >= 20` et `@nestjs/cli` 12.0.13 `>= 20.11` : la borne
   haute vient de l'outillage voisin (Angular 22, voir
   [la fiche Node](../nodejs/montee-node-24-plages-engines-des-outils.md)), pas de NestJS.
   [notes de version] [registre npm, mesure du 2026-11-17]

## Versions concernées
NestJS 12 généré par `@nestjs/cli@latest`, TypeScript 6, Node 24 (vécu sur un générateur de
projets) ; `@nestjs/core` 12.5.1 et `@nestjs/cli` 12.0.13 relus au registre npm le
2026-11-17. Montée d'une application NestJS 11 existante : non vérifié.

## Source
- Retour d'expérience reçu le 2026-11-17 (vécu, notes de version d'un générateur NestJS 12).
- https://docs.nestjs.com/
- Registre npm, 2026-11-17 : `npm view @nestjs/core@12 engines type`,
  `npm view @nestjs/cli@latest engines`.

## Statut
prouvé — sur un projet généré ; la migration d'un projet NestJS 11 n'est pas attestée.
