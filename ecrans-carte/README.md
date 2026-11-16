# Mécanique des écrans avec carte

Ce qui vaut pour tout écran qui montre une carte (couches, légende, barre de temps, fiche au
clic, export), quelle que soit la bibliothèque. Les fiches de `fiches/` décrivent un piège
d'un outil ; ce dossier décrit les règles de l'écran et comment les tester.

- [`invariants.md`](invariants.md) — les 13 invariants d'un écran avec carte : la règle, ce
  qu'on voit quand elle casse, la cause habituelle, le contrôle qui tranche, les fiches liées.
- [`interface.md`](interface.md) — les règles d'interface utilisable sur carte (mise en page
  par largeur, feuilles, toucher, contraste, téléphones réels), chacune sourcée, et les
  contrôles à jouer sur la vraie page avant de dire « fini ».
- [`gabarits/`](gabarits/README.md) — gabarits de tests sans dépendance à copier dans un
  projet : légende = rendu (Python et JavaScript), modèles de test par option du réglage,
  mesure des boîtes et du contraste dans la page.

Règle commune : la légende correspond toujours à ce qui est affiché, réglages courants
compris ; tout changement d'un rendu ou d'un réglage met à jour la légende dans le même
changement et le vérifie sur la sortie réelle (capture), pas seulement dans le code.
