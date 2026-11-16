# Les 13 invariants d'un écran avec carte

Un écran avec carte (couches, légende, barre de temps, fiche au clic, export) ment dès qu'une
de ces règles casse : il montre une chose et en affirme une autre. Chaque invariant s'applique
à tout changement qui touche la carte et devient un test quand c'est possible.

Pour chacun : la règle, ce qu'on voit quand elle casse, la cause habituelle, le contrôle qui
tranche (test automatique ou mesure sur la vraie page) et les fiches liées. Les gabarits de test
cités sont dans [`gabarits/`](gabarits/README.md).

## 1. La légende correspond au rendu, réglages courants compris

- **Symptôme** : la légende montre une palette, des seuils, une unité ou des symboles qui ne sont
  pas ceux de la carte : ancienne palette après un changement de style, lettres en anglais sur la
  carte et en français dans la légende, classes en °C sur une carte en K.
- **Cause** : la légende est une copie (image figée, tableau recopié) au lieu d'être dérivée de
  la source du rendu (style, constantes, réglages) ; ou un réglage (style, langue, niveau,
  modèle) change le rendu sans repasser par la légende.
- **Contrôle** : un test compare, **pour chaque option** du réglage, la légende produite à la
  source du rendu (gabarit `legende_rendu`, fonctions `entrees_depuis_*` et
  `ecarts_legende`). Puis une capture de la vraie page, légende à côté de la carte.
- **Fiches liées** : [getlegendgraphic-attributs-nuls](../fiches/sld/getlegendgraphic-attributs-nuls.md),
  [decoration-legend-sans-filtre-de-couches](../fiches/geoserver/decoration-legend-sans-filtre-de-couches.md).

## 2. Une même grandeur a la même unité partout, et un arrondi ne change pas sa classe

- **Symptôme** : 12 kt sur la carte, 6 m/s dans la fiche au clic, 22 km/h dans le graphique ;
  ou une valeur affichée « 25 » dans la couleur de la classe « < 25 ».
- **Cause** : chaque vue convertit pour son compte, sans lire la préférence d'unité ; la classe
  est calculée sur la valeur brute, l'affichage arrondit à côté (24,96 → « 25,0 »).
- **Contrôle** : une seule fonction de conversion et de formatage, appelée par la carte, la
  légende, la fiche, les graphiques et l'export ; un test par unité qui compare leurs sorties.
  Pour l'arrondi : `classes_changees_par_arrondi` sur les valeurs autour de chaque seuil, à la
  précision affichée.

## 3. Chaque couche affiche sa source et son attribution, exactes pour ce qui est dessiné

- **Symptôme** : attribution du fond de carte seul, ou du fournisseur d'avant ; source « modèle
  A » sur une couche servie par le modèle B en repli.
- **Cause** : attribution écrite en dur dans la configuration de la couche au lieu de venir de
  la donnée effectivement chargée (métadonnées de la réponse, catalogue).
- **Contrôle** : test qui, pour chaque couche et chaque repli possible, compare l'attribution
  affichée à la source déclarée de la réponse servie.

## 4. La validité affichée est celle des données réellement dessinées

- **Symptôme** : le cartouche dit 12:00 UTC, la couche dessine 06:00 (instant le plus proche
  rendu par le serveur), ou la veille.
- **Cause** : le cartouche affiche l'instant **demandé** ; le serveur a répondu un autre instant
  (valeur la plus proche, dernière disponible).
- **Contrôle** : lire l'instant effectivement servi (en-tête ou métadonnée de la réponse,
  liste des instants publiés) et tester cartouche = instant servi quand il diffère du demandé.
- **Fiches liées** : [dimension-time-nearest-sans-reference](../fiches/geoserver/dimension-time-nearest-sans-reference.md),
  [cascade-wms-time-non-transmis](../fiches/geoserver/cascade-wms-time-non-transmis.md).

## 5. Rien de dessiné : on le dit

- **Symptôme** : carte vide sous un cartouche « valide 12:00 UTC » ; dernière image d'hier
  laissée à l'écran comme si elle était actuelle.
- **Cause** : l'absence de donnée n'est pas un état de l'interface ; le cache garde l'image
  précédente quand la nouvelle requête ne rend rien.
- **Contrôle** : test de l'état « aucune donnée » (réponse vide, aucun instant publié) : un
  message sur la couche, aucune validité affirmée, l'ancienne image retirée ou marquée
  périmée avec sa date.

## 6. La nature de la donnée est juste : prévision, observation ou analyse

- **Symptôme** : une prévision présentée comme une observation ; une prévision sans l'heure de
  son run, donc sans moyen de savoir si elle est fraîche.
- **Cause** : un seul champ « date » pour la validité et le run ; nature déduite du nom de la
  couche au lieu de la donnée.
- **Contrôle** : test que le libellé de chaque couche porte sa nature et, pour une prévision,
  l'heure du run lue dans la donnée servie.

## 7. Toutes les couches animées suivent le curseur du temps, et une réponse en retard ne remplace pas la bonne

- **Symptôme** : à la lecture, une couche reste figée ou saute d'un pas ; après un déplacement
  rapide du curseur, la carte montre un instant qui n'est plus le sien.
- **Cause** : couche oubliée dans la liste des couches animées ; réponses traitées dans leur
  ordre d'arrivée, sans vérifier qu'elles répondent au dernier instant demandé.
- **Contrôle** : test qui avance le curseur et compare, pour chaque couche animée, l'instant
  de sa dernière requête au curseur ; test qui fait arriver la réponse de l'instant N après
  celle de N+1 (jeton ou numéro de requête, réponse périmée ignorée).
- **Fiches liées** : [animation-wms-instants-sans-granule](../fiches/maplibre/animation-wms-instants-sans-granule.md).

## 8. Un réglage s'applique partout où la chose apparaît

- **Symptôme** : unité changée sur la carte, pas dans l'export ; langue des lettres changée dans
  la légende, pas dans la fiche au clic ni le widget.
- **Cause** : le réglage est lu à l'ouverture de chaque vue au lieu d'être un état partagé
  auquel chaque vue s'abonne.
- **Contrôle** : test par réglage qui le change une fois et lit la carte, la légende, la fiche,
  l'export, l'impression et les widgets.

## 9. Le lien partagé restaure exactement la vue

- **Symptôme** : le lien ouvre la bonne zone mais un autre instant, l'autre modèle, une couche
  en moins ; un instant devenu indisponible remplacé en silence par le dernier.
- **Cause** : une partie de l'état n'est pas sérialisée dans l'URL, ou restaurée avant que la
  liste des couches et des instants soit chargée.
- **Contrôle** : test aller-retour état → URL → état (couches, instant, modèle, projection,
  cadrage) ; test d'un instant indisponible : message visible, pas de substitution muette.

## 10. Changer de projection ne change que la projection

- **Symptôme** : passage au globe ou à une projection polaire : une couche disparaît, l'instant
  revient au présent, la légende décrit un rendu que le nouveau moteur ne fait pas.
- **Cause** : changement de projection fait en recréant la carte sans reporter tout l'état ;
  couche non prise en charge par le nouveau moteur retirée sans le dire.
- **Contrôle** : test qui compare couches, instant et cadrage avant et après le changement ;
  capture de la légende dans chaque moteur.
- **Fiches liées** : [projection-globe-ignoree-au-constructeur](../fiches/maplibre/projection-globe-ignoree-au-constructeur.md),
  [source-wms-projection-de-la-vue](../fiches/openlayers/source-wms-projection-de-la-vue.md),
  [entites-mal-placees-hors-3857](../fiches/openlayers/entites-mal-placees-hors-3857.md).

## 11. L'export et l'impression montrent ce qu'on voit

- **Symptôme** : PNG exporté vide ou noir ; export sans légende, sans instant ni sources ;
  impression d'un autre cadrage.
- **Cause** : capture du canvas WebGL sans tampon conservé ; export qui ne compose que la
  carte, pas les éléments qui l'expliquent.
- **Contrôle** : test de l'export (image non vide, mesure des pixels) et de sa composition :
  légende, instant, validité et sources présents.
- **Fiches liées** : [capture-du-canvas-vide](../fiches/maplibre/capture-du-canvas-vide.md),
  [decoration-legend-sans-filtre-de-couches](../fiches/geoserver/decoration-legend-sans-filtre-de-couches.md).

## 12. Un échec de chargement se voit sur la couche concernée

- **Symptôme** : couche cochée, rien à l'écran, aucun message : on croit qu'il n'y a pas de
  phénomène alors que le serveur a répondu une erreur.
- **Cause** : erreur avalée (tuile en échec ignorée, erreur de serveur en HTTP 200 au format
  XML que le client ne sait pas décoder) ; état « échec » absent de la couche.
- **Contrôle** : test qui fait échouer le chargement (500, réponse XML, délai) et vérifie
  l'état d'erreur sur la couche concernée, distinct de l'état « aucune donnée » (invariant 5).
- **Fiches liées** : [erreur-wms-http-200-en-xml](../fiches/geoserver/erreur-wms-http-200-en-xml.md),
  [couche-vecteur-visible-mais-vide](../fiches/openlayers/couche-vecteur-visible-mais-vide.md).

## 13. Un clic sur un objet ouvre la fiche de cet objet, à l'instant affiché

- **Symptôme** : la fiche au clic montre l'objet voisin, l'instant courant au lieu de l'instant
  affiché, d'autres unités ou d'autres lettres que la carte.
- **Cause** : requête d'information sans le paramètre de temps de la couche ; formatage de la
  fiche différent de celui de la carte ; tolérance de clic qui attrape un autre objet.
- **Contrôle** : test qui clique un objet connu à un instant passé et compare la fiche
  (identifiant, instant, valeurs, unités, lettres) à ce que la carte dessine.
- **Fiches liées** : [proprietes-imbriquees-en-chaine-au-clic](../fiches/maplibre/proprietes-imbriquees-en-chaine-au-clic.md).
