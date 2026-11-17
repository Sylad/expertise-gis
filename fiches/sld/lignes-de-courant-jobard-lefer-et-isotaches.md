# Lignes de courant au rendu : Jobard & Lefer en transformation, image non tuilée, isotaches en m/s

## Symptôme
Lignes de courant calculées au rendu GeoServer depuis une couverture vent (vitesse, u, v) :
- lignes qui s'agglutinent ou se croisent, densité qui varie avec le zoom ;
- image différente à chaque rendu, ou d'une tuile à l'autre : le cache de tuiles stocke du bruit ;
- lignes coupées net au bord des tuiles ;
- tourbillon déformé, directions fausses en EPSG:4326 ;
- rendu qui dépasse le délai sur un champ fin ;
- isotaches à des valeurs non rondes (10,29 au lieu de 20 kt), ou étiquettes en m/s.

## Cause
- Graines aléatoires ou régulières sans contrôle de distance : rien n'empêche deux lignes de se
  rapprocher. Jobard & Lefer (1997) arrête une ligne à `dTest·dSep` de toute autre et sème les
  suivantes à `±dSep` sur la normale des lignes déjà tracées.
- Une première graine qui dépend de l'emprise rend chaque rendu différent.
- Les graines suivantes dépendent des lignes déjà tracées **dans ce cadre** : deux tuiles
  voisines ne se raccordent jamais exactement (comme `ras:Contour`, en plus visible).
- En EPSG:4326, un degré de longitude vaut `cos φ` degré de latitude : `dx ∝ u/pxW` sans
  correction étire le champ vers l'est.
- La couverture est en m/s ; `ras:Contour` trace aux multiples entiers de `interval`.

## Détection
- Champ uniforme synthétique : lignes parallèles espacées de `dSep ± 1 px`, dans le sens du flux.
- Vortex : aucun sommet à moins de `dTest·dSep` d'une autre ligne ; en EPSG:4326, rayon constant.
- Deux rendus du même GetMap : géométries identiques (déterminisme).
- Isotaches : niveaux `value × 1,943844` multiples de l'intervalle en kt.

## Geste
- Processus Java, algorithme pur en espace pixel (u, v → direction pixel ; en CRS géographique
  `dx ∝ u/(cos φ·pxW)`, `dy ∝ −v/pxH`, interpolation bilinéaire, un voisin `NaN` = indéfini) : intégration RK4 bidirectionnelle à pas
  renormalisé (`stepPx` = 1), arrêt au bord, sur `NaN`, sous `minSpeed`, à `maxLength` ou à
  `dTest·dSep` (0,5) d'une ligne, y compris la ligne courante au-delà d'un recul d'arc ; grille de
  hachage de maille `dSep` (9 cellules testées) ; `dSep` en **pixels de sortie** (cadre lu dans
  `env('wms_bbox')`, `wms_width`, `wms_height`).
- Première graine sur un réseau **ancré au monde** (multiples de `dSep·pxW` en coordonnées du
  CRS) ; `invertGridGeometry` élargit la lecture de `2·dSep + 1` px, lignes calculées sur le cadre
  élargi puis coupées à la bbox.
- Côté client : **GetMap non tuilé** à la taille de la vue (`ImageWMS`, source `image`
  re-demandée à la fin du déplacement), pas une source tuilée.
- Garde-fous rendant un résultat **partiel** journalisé, jamais une exception : `timeBudgetMs`
  2 000, `maxLines` 4 000, 600 000 points intégrés.
- Sommets ordonnés de l'amont vers l'aval : un `LineSymbolizer` à `GraphicStroke`
  `shape://oarrow` et `stroke-dasharray` `8 40` pose une pointe tous les 48 px dans le sens du
  flux, sans géométrie de flèche à part ; au-delà de 60 kt, trait épais et `10 14`.
- Isotaches : style compagnon `ras:Contour` sur la bande vitesse, `interval` =
  `env('isotachKt', 20) × 0.514444`, étiquette `round(value × 1.943844)` « kt ».

## Versions concernées
GeoServer 3.0.1 / GeoTools 35.1 / Java 21 (vécu, 2026-09-10) ; 2.x non vérifié.

## Source
- vécu 2026-09-10 (GeoServer 3.0.1, GeoTools 35.1, couverture 3 bandes float32 vitesse / u / v,
  rendus EPSG:3857 et EPSG:4326 ; tests JUnit : champ uniforme, vortex en 4326, déterminisme,
  vrais SLD parsés par GeoTools).
- Mesure (tests JUnit sur un GeoTIFF de modèle global 181 × 121) : image 1600 × 900 → 328 lignes
  en 49–68 ms ; tuile 512 × 512 → 86 lignes en 10–16 ms.
- Jobard B., Lefer W. (1997), *Creating Evenly-Spaced Streamlines of Arbitrary Density*,
  Eurographics Workshop on Visualization in Scientific Computing.
- WMO-No. 306 Vol. I.1 (2019), Attachment IV § 4.2.4 (isotaches) et § 4.2.5 (flèches du jet),
  référence relevée, non recontrôlée ici sur le texte.
- https://docs.geoserver.org/latest/en/user/styling/sld/extensions/rendering-transform.html
- https://docs.geoserver.org/latest/en/user/styling/sld/reference/linesymbolizer.html

## Statut
prouvé
