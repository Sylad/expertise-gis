# Angular 20 → 22 : zoneless, OnPush par défaut, `?.` aligné sur JavaScript, Signal Forms

Fiche de montée de version. Chaque point dit la nature de sa source entre crochets :
[commit] et [notes de version] = historique et notes d'une équipe qui a construit des
applications en Angular 22.2 ; [doc Angular] = documentation officielle lue par elle ;
[CHANGELOG Angular, relu ici] et [registre npm, mesure du 2026-11-17] = recontrôlé pour cette
fiche. **Aucun `ng update` 20 → 21 → 22 joué sur une application existante n'est attesté** :
les applications sont nées en 22 ; les étapes de migration viennent de la doc, l'ordre des
marches est une déduction. Les pièges TypeScript 6, Node et NestJS ont leur fiche :
[typescript](../typescript/montee-5-9-a-6-baseurl-et-imports-a-effet-de-bord.md),
[nodejs](../nodejs/montee-node-24-plages-engines-des-outils.md),
[nestjs](../nestjs/montee-12-modules-es.md).

## Symptôme
1. Après passage sans `zone.js`, un écran ne se rafraîchit plus après un `setValue`,
   `patchValue` ou `FormArray.push` d'un Reactive Form, ou après une affectation directe d'un
   champ du composant ; en test, `ExpressionChangedAfterItHasBeenCheckedError`. [doc Angular]
2. En 22, une expression de gabarit `a?.b` vaut `undefined` là où elle valait `null` ; après
   `ng update`, des appels `$safeNavigationMigration(...)` apparaissent dans les gabarits ;
   nouveaux diagnostics `nullishCoalescingNotNullable` / `optionalChainNotNullable`.
   [doc Angular] [CHANGELOG Angular 22.0.0, relu ici]
3. En 22, un composant sans `changeDetection` déclaré cesse de se rafraîchir dans des cas où il
   se rafraîchissait (OnPush devient le défaut). [doc Angular] [CHANGELOG Angular 22.0.0, relu ici]
4. `app.spec.ts` produit par `ng new` en 22 échoue en `NG0201` (fournisseur manquant sur le
   composant racine). [notes de version]
5. Vitest : le premier test de chaque fichier (celui qui charge Angular et Material) dépasse le
   délai de 5 s quand la machine est chargée. [commit, notes de version]
6. `ng serve` derrière un autre nom d'hôte : `403 Blocked request`, websocket de rechargement
   refusé ; `disableHostCheck` refusé par le schéma. [notes de version]
7. `npm install` refusé ou `ng` qui s'arrête : Node ou TypeScript hors des plages de la
   majeure visée (voir Versions concernées). [registre npm, mesure du 2026-11-17]
8. Pas de script `lint`, et le `eslint --fix` du crochet de pré-commit plante au premier
   commit d'un `.ts`. [notes de version]

## Cause
1. Sans zone, Angular ne rafraîchit que sur `markForCheck` (dont `AsyncPipe`),
   `ComponentRef.setInput`, un signal lu dans le gabarit, ou un écouteur lié dans le gabarit
   ou l'hôte ; les méthodes des Reactive Forms ne planifient aucune détection. TestBed est
   zoneless par défaut, même si `zone.js` est chargé. [doc Angular]
2. Le compilateur de la 22 aligne `?.` sur JavaScript ; la migration de `ng update` enveloppe
   les expressions existantes pour garder l'ancien résultat, c'est une aide temporaire.
   [doc Angular] [CHANGELOG Angular 22.0.0, relu ici]
3. 22.0.0 : « Component with undefined `changeDetection` property are now `OnPush` by
   default ». [CHANGELOG Angular 22.0.0, relu ici]
4. Le composant racine réel demande un fournisseur que la spec générée ne déclare pas.
   [notes de version]
5. Délai par défaut de Vitest (5 s) plus court que le chargement d'Angular sous charge.
   [commit]
6. Le serveur de dev de `@angular/build` vérifie l'hôte ; `disableHostCheck` était l'option du
   serveur webpack. [notes de version]
7. Plages exigées : TypeScript `>=5.8 <6.0` (20.3), `>=5.9 <6.0` en 21.0.0 puis `>=5.9 <6.1`
   en 21.2, `>=6.0 <6.1` (22) ; Node `^20.19 || ^22.12 || >=24` jusqu'en 21,
   `^22.22.3 || ^24.15.0 || >=26.0.0` en 22. [registre npm, mesure du 2026-11-17]
8. ESLint 9 et suivants ignorent `.eslintrc.json` (configuration « flat » seulement) ; le
   squelette 22 vient avec ESLint 10. [notes de version] [commit]

## Détection
1. La suite Vitest le révèle : TestBed lève `ExpressionChangedAfterItHasBeenCheckedError` sur
   un gabarit modifié sans notification. Contrôle final : `zone.js` absent des dépendances,
   des `polyfills` des cibles `build` **et** `test` d'`angular.json`, et des bundles produits
   [doc Angular] [notes de version]. Commande : `grep -rl --include='*.js' zone.js dist/`
   doit être vide (les bundles sont sous `dist/<projet>/browser/`). [déduction, jouée le
   2026-11-17 avec GNU grep sur une arborescence témoin]
2. Après `ng update` vers 22, les expressions enveloppées dans
   `$safeNavigationMigration(...)` [doc Angular] se listent par
   `grep -rn '\$safeNavigationMigration' src/`. [déduction]
3. Composants sans `changeDetection` déclaré, qui deviennent OnPush [CHANGELOG Angular
   22.0.0, relu ici] : `grep -rl --include='*.ts' '@Component' src/ | xargs -r grep -L
   changeDetection` (les seuls composants, pas les services ni les specs). [déduction, jouée
   le 2026-11-17 avec GNU grep sur une arborescence témoin]
4. `npm test` sur un projet neuf. [déduction, d'après le symptôme 4]
5. Lancer la suite pendant un build d'image en parallèle. [déduction, d'après le symptôme 5]
6. Ouvrir l'application de dev par le nom d'hôte de destination. [déduction, d'après le
   symptôme 6]
7. `npm view @angular/core@<majeure> engines` et
   `npm view @angular/compiler-cli@<majeure> peerDependencies.typescript`.
   [registre npm, mesure du 2026-11-17]
8. `npx eslint --print-config src/main.ts` : erreur tant qu'il n'y a pas d'`eslint.config.js`.
   [déduction]

## Geste
1. Zoneless : en 20, `provideZonelessChangeDetection()` au bootstrap ; en 21 et après c'est le
   défaut : vérifier qu'aucun `provideZoneChangeDetection` ne force l'ancien mode. Retirer
   `zone.js` et `zone.js/testing` des `polyfills` des cibles `build` et `test`, puis
   `npm uninstall zone.js`. Reactive Forms lus par le gabarit : relier leurs observables à
   `markForCheck()` ou passer par des signaux ; en test, préférer `await fixture.whenStable()`
   à `fixture.detectChanges()`, `provideZoneChangeDetection()` pour revenir à l'ancien mode.
   [doc Angular]
2. Attention en 21 : la 21.0.0 ne fournit plus d'ordonnanceur aux applications avec zone et
   ajoute `provideZoneChangeDetection` par une migration automatique ; après le `ng update`
   vers 21, chercher ce fournisseur et le retirer si l'application est déjà passée sans zone.
   [CHANGELOG Angular 21.0.0, relu ici] [déduction]
3. `?.` : relire chaque `$safeNavigationMigration(...)` inséré et le retirer en cessant de
   dépendre de la différence `null` / `undefined`. [doc Angular]
4. OnPush par défaut : un composant compatible OnPush (signaux, `markForCheck`) n'a rien à
   faire ; sinon `changeDetection: ChangeDetectionStrategy.Eager` garde l'ancien comportement,
   le temps de le corriger. [CHANGELOG Angular 22.0.0, relu ici]
5. Remplacer la spec générée par une spec écrite pour le composant racine réel.
   [notes de version]
6. `testTimeout: 30_000` et `hookTimeout: 30_000` dans le fichier Vitest relié par
   `runnerConfig` ; un test bloqué échoue toujours, à 30 s. [commit, notes de version]
7. `serve.options.allowedHosts: true` dans `angular.json`.
   [notes de version]
8. Karma → Vitest (expérimental sur un projet existant, exige le constructeur
   `application`) : la cible `test` de `@angular/build:unit-test` n'accepte plus `polyfills`,
   `assets`, `styles` (les mettre dans une configuration de build dédiée) ; options Vitest
   dans le fichier relié par `runnerConfig`. [doc Angular]
9. Une majeure à la fois : « If you want to update across multiple major versions, perform
   each update one major version at a time. » [doc Angular]
10. Ordre proposé depuis 20.3 + zone.js + Node 22 + Vitest, chaque marche appuyée sur un fait
    ci-dessus : (a) Node 24 ≥ 24.15 (ou 22 ≥ 22.22.3) ; (b) zoneless en restant en 20.3, la
    suite de tests révèle les composants à reprendre ; (c) `ng update` vers 21, TypeScript 5.9,
    retirer `baseUrl` dès maintenant ; (d) `ng update` vers 22, TypeScript 6.0, OnPush et `?.`,
    `"incremental": false` si le build tourne dans des worktrees git ; (e) Signal Forms ensuite,
    formulaire par formulaire. Ordre jamais joué de bout en bout. [déduction]
11. Signal Forms (adoption, rien ne l'impose à la montée) : modèle dans un `signal`,
    `form(model)`, `[formField]` sur chaque contrôle, Material compris ; import depuis
    `@angular/forms/signals` (`form`, `FormField` dans les `imports` du composant). Un champ
    dont le texte appartient à un état global : `linkedSignal(() => ({ text:
    state.query() }))` comme modèle (un effacement de l'état vide le champ), un `effect` qui
    renvoie la saisie à l'état ; le gestionnaire `(input)` ne lit plus `event.target.value`.
    [commit, conventions du projet]
12. Alignements faits en même temps sur un squelette 22 : aucun `changeDetection` déclaré ;
    fichiers et classes nommés comme `ng generate` récent (`busy-card.ts` / `BusyCard`) ;
    lectures par `httpResource`, écritures sur `HttpClient` ; `DOCUMENT` importé de
    `@angular/core` ; Material : `matButton="filled|outlined|tonal|elevated"`, `matIconButton`,
    `matFab`, `matMiniFab` au lieu de `mat-flat-button`, `mat-icon-button`. [notes de version]
    [conventions du projet]
13. ESLint : `ng add angular-eslint` (cible `lint`) et un `eslint.config.js` en flat config ;
    puis formater tout le code avec le Prettier du projet, sinon environ 360 erreurs de
    format sur des fichiers non touchés. [notes de version]
14. Vérifier sur un **clone neuf** : `npm ci`, `npm run build`, `npm test -- --no-watch`, lint
    (le dossier de travail cachait une erreur de build, voir la fiche TypeScript). [commit]

## Versions concernées
Angular 22.2 (`@angular/build` 22.2.4, TypeScript ~6.0.2, Vitest ^5.0.0, jsdom ^30) (vécu,
applications nées en 22) ; Angular 20.3.35, 21.2.26, 22.2.6 (plages relues au registre npm le
2026-11-17). Montée `ng update` 20 → 21 → 22 sur une application existante : non vérifié.

## Source
- Retour d'expérience reçu le 2026-11-17 (vécu, applications Angular 22.2 dont une
  cartographique sous OpenLayers ; natures de source citées point par point).
- https://angular.dev/reference/versions ; https://angular.dev/guide/zoneless ;
  https://angular.dev/update-guide ; https://angular.dev/guide/testing/migrating-to-vitest ;
  https://angular.dev/guide/forms/signals/overview
- https://github.com/angular/angular/blob/main/CHANGELOG.md (sections 21.0.0 et 22.0.0,
  relues le 2026-11-17).
- Registre npm, 2026-11-17 : `npm view @angular/core@{20.3,21,22} engines`,
  `npm view @angular/compiler-cli@{20.3,21.0.0,21,22} peerDependencies.typescript`.

## Statut
prouvé — sauf l'ordre des marches et le point 2 du Geste, déductions jamais jouées ; les
commandes de détection sont ajoutées ici (`[déduction]`), la note n'en donne pas.
