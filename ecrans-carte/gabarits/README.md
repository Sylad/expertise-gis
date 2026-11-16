# Gabarits de tests : légende = rendu, boîtes et contraste

Fichiers sans dépendance, à copier dans le dépôt d'un projet. Chacun est testé ici
(`tests/test_ecrans_carte.py`, qui lance aussi les tests Node).

| Fichier | Rôle | Invariants / contrôles |
|---|---|---|
| [`legende_rendu.py`](legende_rendu.py) | Lit les entrées (seuil, couleur) d'une expression MapLibre (`step`, `interpolate`, `match`) ou des `ColorMapEntry` d'un SLD, convertit les seuils dans l'unité affichée, liste les écarts avec la légende, détecte les valeurs affichées dans la couleur d'une autre classe. | invariants 1 et 2 |
| [`legende-rendu.mjs`](legende-rendu.mjs) | La même chose en JavaScript (front, Vitest, Jest, `node --test`). | invariants 1 et 2 |
| [`modele_test_legende.py`](modele_test_legende.py) | Modèle de test par option du réglage, à remplir (fonctions « À REMPLIR ») ; sauté tant qu'il ne l'est pas. | invariants 1 et 2 |
| [`modele-legende.test.mjs`](modele-legende.test.mjs) | Le même modèle en JavaScript. | invariants 1 et 2 |
| [`boites.mjs`](boites.mjs) | Mesure dans la page (`page.evaluate(mesurer, sélecteur)`) et vérifie : chevauchements de libellés, cibles < 24 px, éléments hors de leur panneau, fiche qui couvre l'objet cliqué, débordement horizontal, contraste WCAG d'un contrôle sur les pixels du fond de carte. | contrôles 2 et 4 d'[`interface.md`](../interface.md) |

## Mode d'emploi

1. Copier `legende_rendu.py` (ou `.mjs`) et le modèle à côté des tests du projet.
2. Remplir le modèle : `OPTIONS` (toutes les valeurs du réglage qui changent le rendu :
   style, unité, langue des lettres, niveau, modèle…), l'expression de couleur **produite par
   le code** pour chaque option (jamais recopiée à la main), la légende **affichée** (modèle
   de la légende ou DOM rendu), la conversion d'unité de la préférence, le formatage.
3. Ajouter une option au réglage ajoute un cas au test ; une légende qui ne suit plus le
   rendu fait échouer le test avec l'entrée fautive (« entrée 2 : seuil 15 dans la légende,
   10 dans le rendu »).
4. Le test ne remplace pas la capture : la règle des cartes exige aussi de regarder la
   légende sur la vraie page.

## Conventions

- Une valeur égale à un seuil appartient à la classe qui commence à ce seuil (sémantique de
  `step` de MapLibre et des `ColorMap type="intervals"` du SLD).
- Couleurs comparées normalisées en `#rrggbb` (`#rrggbbaa` si l'opacité n'est pas 1) : `#F00`,
  `rgb(255,0,0)` et `0xFF0000` sont égales.
- Arrondi : avec la couleur choisie sur la valeur brute, une valeur de 24,96 s'affiche
  « 25,0 » dans la couleur de « < 25 ». `classes_changees_par_arrondi` le détecte ; remède :
  choisir la couleur sur la valeur affichée, ou afficher plus de décimales.
- Contraste : formule de la luminance relative et du rapport de contraste de WCAG 2.2
  (https://www.w3.org/TR/WCAG22/#dfn-relative-luminance).
- Mesure vide : `chevauchements`, `ciblesTropPetites`, `horsDuParent` et `contrasteMinimal`
  lèvent une exception sur une liste vide (sélecteur qui ne trouve rien, capture ratée) ;
  un contrôle sans mesure n'est jamais vert.
- SLD : les `ColorMapEntry` en commentaire sont ignorés et une entrée sans `quantity` est
  refusée, en Python comme en JavaScript.
- Arrondi : sans seuil numérique (légende catégorielle, `match`), le test d'arrondi des
  modèles est sauté, pas vert à vide.
