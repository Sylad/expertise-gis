# TypeScript 5.9 → 6.0 : `baseUrl` refusé, imports à effet de bord vérifiés (et cache de build qui rejoue)

Fiche de montée de version. Natures de source entre crochets : [commit] / [notes de version]
= historique d'une équipe passée en TypeScript 6.0 sous Angular 22.2 ;
[mesure du 2026-11-17] = reproduit pour cette fiche avec `tsc` 6.0.3 et 7.0.2 sur un projet
minimal.

## Symptôme
1. `error TS5101: Option 'baseUrl' is deprecated and will stop functioning in TypeScript 7.0.
   Specify compilerOption '"ignoreDeprecations": "6.0"' to silence this error.`
   [commit] [mesure du 2026-11-17]
2. En TypeScript 7 : `error TS5102: Option 'baseUrl' has been removed`, et des `paths` non
   relatifs : `error TS5090: Non-relative paths are not allowed. Did you forget a leading
   './'?` (TypeScript 6 l'émet aussi dès que `baseUrl` est retiré).
   [notes de version] [mesure du 2026-11-17]
3. `error TS2882: Cannot find module or type declarations for side-effect import of
   './…generated'` sur un `import './…';` de `main.ts`, **alors que le fichier généré existe** ;
   seulement sur un clone neuf, pas dans le dossier de travail. [commit]
4. Un script qui modifie `tsconfig.app.json` / `tsconfig.spec.json` en s'ancrant sur leurs
   dernières clés casse : `outDir` a disparu des fichiers générés par Angular 22.
   [notes de version]

## Cause
1. TypeScript 6 déprécie `baseUrl` en erreur ; 7 le supprime et exige des `paths` relatifs
   au tsconfig. [mesure du 2026-11-17]
2. TypeScript 6 vérifie par défaut les imports à effet de bord : un `import './x';` sans
   fichier résolu est une erreur (en 6.0.3 comme en 7.0.2). [mesure du 2026-11-17]
3. `@angular/build` 22.2 garde le `.tsbuildinfo` dans `.angular/cache` et, depuis un worktree
   git, dans le cache du dépôt principal (cache partagé depuis 22.1) ; il rejoue les
   diagnostics par fichier d'un build antérieur où le fichier généré manquait. Le TS2882 vient
   donc d'un vieux diagnostic, pas de l'état présent. [commit]

## Détection
1. `npx tsc -p . --noEmit` sous TypeScript 6 : TS5101 tant qu'un `baseUrl` reste.
   [mesure du 2026-11-17]
2. `grep -n baseUrl tsconfig*.json` et, dans `paths`, toute valeur qui ne commence pas par
   `./`. [mesure du 2026-11-17]
3. Rejouer le build sur un clone neuf, ou avec `CI=1` (désactive tout le cache de
   `@angular/build` pour une commande) : si l'erreur disparaît, c'est le cache. [commit]

## Geste
1. Retirer `baseUrl` et écrire les `paths` relatifs au tsconfig :
   `"@core/*": ["./src/app/core/*"]`, dans chaque tsconfig (racine, app, spec). La forme
   relative compile sous 5.9, 6.0 et 7.0 : la faire dès la 5.9. `"ignoreDeprecations": "6.0"`
   ne fait que reporter à la 7. [commit] [mesure du 2026-11-17]
2. Cache qui rejoue : `"incremental": false` dans `tsconfig.json` (les autres caches restent ;
   aucune différence de durée de build mesurée) ; un test unitaire garde l'option. [commit]
3. Script qui édite un tsconfig : ancrer sur `"compilerOptions": {`, pas sur une clé générée.
   [notes de version]

## Versions concernées
TypeScript 6.0.2 / 6.0.3 sous Angular 22.2 et `@angular/build` 22.2 (vécu) ; TypeScript 6.0.3
et 7.0.2 (mesure du 2026-11-17 pour les messages TS5101, TS5102, TS5090, TS2882). Le cache
partagé entre worktrees : `@angular/build` ≥ 22.1 (vécu sur 22.2).

## Source
- Retour d'expérience reçu le 2026-11-17 (vécu, TypeScript 6.0 sous Angular 22.2).
- https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html ;
  https://aka.ms/ts6 (lien donné par le message TS5101).
- Mesure du 2026-11-17 : projet minimal (`paths` avec et sans `baseUrl`, import à effet de
  bord d'un fichier absent puis présent) compilé par `tsc` 6.0.3 et 7.0.2.

## Statut
prouvé
