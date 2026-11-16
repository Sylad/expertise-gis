# Interface utilisable sur carte : règles et contrôles

Règles à appliquer **en codant** un écran avec carte (couches, barre de temps, légende, fiche au
clic), sur téléphone comme sur grand écran. Chaque nombre est un seuil tiré de la source citée
dans la section, pas un goût, sauf ceux marqués « * », qui sont un choix de ce document. La charte de l'application (couleurs, typographie) reste la sienne.

## 1. Une mise en page par largeur

| Largeur de fenêtre | Mise en page |
|---|---|
| < 600 px | Carte plein écran ; panneaux (couches, fiche, réglages) dans une feuille en bas ; navigation en barre en bas. |
| 600 – 839 px | Volets côte à côte (carte / panneau 50/50)* ou rail de navigation latéral*. |
| ≥ 840 px | Volets côte à côte, carte / panneau 70/30*. |
| hauteur < 480 px (paysage) | Navigation en barre* ; rien d'important sous le pli. |

Source : classes de taille de fenêtre (compact < 600, medium 600–839, expanded ≥ 840,
hauteur compacte < 480) —
https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes .
Seuls ces seuils de largeur et de hauteur viennent de cette source.

\* Choix de ce document, non tiré de la source : les partages 50/50 et 70/30 et le type
de navigation (barre ou rail) par largeur. La page citée ne les donne pas, et les guides
Material 3 qui pourraient les donner n'ont pas été relus ; à ajuster à la carte du projet,
pas à recopier comme une norme.

## 2. Feuilles et fiche au clic

- Feuille du bas à crans : aperçu, moitié, plein écran. **Une seule feuille à la fois.**
- Pour la fermer : poignée d'au moins 48 px, bouton Fermer visible, et le bouton Retour.
- Largeur maximale de la feuille : 640 px sur grand écran.
- La fiche ouverte par un clic ne cache pas l'objet cliqué : la carte se recentre au besoin.

Sources : https://github.com/material-components/material-components-android/blob/master/docs/components/BottomSheet.md ,
https://developer.apple.com/design/human-interface-guidelines/sheets

## 3. Toucher et gestes

- Cibles tactiles : 44 px visés ; **24 px minimum** (WCAG 2.5.8, niveau AA). Les épingles
  denses de la carte relèvent de l'exception « essentielle » du critère.
- Zoom par boutons + et − (WCAG 2.5.1, gestes multipoints) ; déplacer la carte sans glisser
  (WCAG 2.5.7, mouvements de glissement), par exemple flèches du clavier ou boutons.
- Barre de temps réglable d'un toucher sur la piste, avec boutons pas à pas, et l'instant
  choisi écrit en clair au-dessus.
- Ni orientation forcée (WCAG 1.3.4) ni zoom du navigateur bloqué (`user-scalable=no`,
  `maximum-scale=1` : WCAG 1.4.4).

Source : https://www.w3.org/TR/WCAG22/ (critères 1.3.4, 1.4.4, 2.5.1, 2.5.5, 2.5.7, 2.5.8)

## 4. Couleur, contraste, texte

- Contraste 4,5:1 pour le texte, 3:1 pour le grand texte (WCAG 1.4.3), les contrôles et les
  éléments graphiques utiles (WCAG 1.4.11). Un contrôle posé sur la carte garde 3:1 **sur
  tous les fonds de carte** : bordure ou ombre.
- La couleur n'est jamais seule à porter l'information (WCAG 1.4.1) : forme, motif, lettre ou
  texte en plus.
- Palettes de données perceptuellement uniformes, sans arc-en-ciel, lisibles par les
  daltoniens, toujours avec une légende chiffrée et son unité.
- La légende suit le rendu et les réglages courants (invariant 1 de
  [`invariants.md`](invariants.md)).
- Aucun libellé n'en chevauche un autre (légende, graduations d'une barre de couleurs, axes,
  étiquettes) : raisonner sur la **largeur réelle** du texte, pas sur un écart fixe, et
  renvoyer en clé ce qui ne tient pas. Cas vécu : graduations longues d'une légende de
  pression au niveau de la mer superposées malgré un écart minimal fixe entre les seuils.
- Texte agrandi à 200 % lisible (WCAG 1.4.4) ; espacements élargis supportés : interligne 1,5,
  paragraphes 2, lettres 0,12, mots 0,16 fois la taille du texte (WCAG 1.4.12).

Sources : https://www.w3.org/TR/WCAG22/ (1.4.1, 1.4.3, 1.4.4, 1.4.11, 1.4.12) ;
Crameri, Shephard et Heron, *The misuse of colour in science communication*, Nature
Communications 11, 5444 (2020), https://doi.org/10.1038/s41467-020-19160-7

## 5. Écrans de téléphone réels

- Plein écran en `100dvh`, pas `100vh` (qui passe sous la barre du navigateur mobile).
- Marges en `max(<marge>, env(safe-area-inset-*))` : barre de temps et boutons hors de
  l'encoche et de la barre du bas.
- À 320 px de large, aucun défilement horizontal hors de la carte (WCAG 1.4.10, refusion).

Sources : https://developer.mozilla.org/en-US/docs/Web/CSS/length#dynamic_viewport_units ,
https://developer.mozilla.org/en-US/docs/Web/CSS/env , https://www.w3.org/TR/WCAG22/#reflow

## 6. Montrer peu, donner accès à tout

- Peu d'options d'emblée ; le reste à un geste, sur deux niveaux au plus.
- Chaque action visible dit ce qu'elle fait. Un état vide, une erreur ou un chargement se
  voit et s'explique (invariants 5 et 12), jamais une zone vide muette.

Source : https://www.nngroup.com/articles/progressive-disclosure/

## Contrôles sur la vraie page, avant de dire « fini »

Aux largeurs **320, 390, 600, 840 et 1280 px**, et en paysage **844 × 390** :

1. **axe-core** avec `color-contrast`, `meta-viewport`, `button-name`, `aria-dialog-name`, et
   `target-size` (activée par le tag `wcag22aa`).
2. **Mesure des boîtes** (`getBoundingClientRect`, gabarit [`gabarits/boites.mjs`](gabarits/boites.mjs)) :
   cibles ≥ 24 px (44 visés) ; aucun débordement horizontal hors de la carte ; aucun texte
   coupé ni contrôle hors de son panneau ; aucun libellé d'une même légende ou d'un même axe
   qui en chevauche un autre ; feuille ≤ 640 px ; fiche qui ne couvre pas l'objet cliqué.
3. **Recherche dans le code** : `grep -rn -e '100vh' -e 'user-scalable' src/` ne rend rien.
4. **Contraste des contrôles sur la carte** : axe ne voit pas le fond WebGL. Capture, puis
   mesure des pixels autour du contrôle sur un fond clair et sur un fond sombre (gabarit :
   `contraste` dans [`gabarits/boites.mjs`](gabarits/boites.mjs)).
5. **Regarder les captures** à 390 et 1440 px, comme un humain.

Le compte rendu dit quels contrôles ont passé, lesquels ont échoué, et ce qui n'a pas pu être
contrôlé.
