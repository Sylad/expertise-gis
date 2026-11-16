// Modèle de test « légende = rendu » à copier dans un front (Vitest, Jest ou node:test :
// remplacer l'import de `node:test` par celui du lanceur du projet).
//
// Remplir les fonctions marquées À REMPLIR. Tant que OPTIONS est vide ou qu'une fonction
// n'est pas remplie, les tests sont sautés (jamais verts à vide).
import test from 'node:test';
import assert from 'node:assert/strict';
import {
  classe, classesChangeesParArrondi, convertirSeuils, ecartsLegende,
  entreesDepuisMaplibre, valeursAutourDesSeuils,
} from './legende-rendu.mjs';

// À REMPLIR : les valeurs du réglage qui changent le rendu ou la légende.
const OPTIONS = [];

const NON_REMPLI = Symbol('non rempli');
// À REMPLIR : l'expression de couleur que le code produit vraiment pour `option`.
const expressionCouleurDuRendu = (option) => NON_REMPLI;
// À REMPLIR : entrées [seuil, couleur] de la légende affichée (modèle ou DOM), unité affichée.
const legendeAffichee = (option) => NON_REMPLI;
// À REMPLIR : { conversion: (seuilDonnee) => seuilAffiche, unite: '°C' } selon la préférence.
const conversionVersUniteAffichee = (option) => NON_REMPLI;
// À REMPLIR : le libellé d'unité lu dans la légende.
const uniteAfficheeParLaLegende = (option) => NON_REMPLI;
// À REMPLIR : formatage du projet, et choix de couleur d'une valeur (null = valeur brute).
const afficher = (v) => Math.round(v * 10) / 10;
const DECIMALES_AFFICHEES = 1;
const classer = null; // null = valeur brute ; sinon (valeur, seuils) => indice

const rempli = (...valeurs) => OPTIONS.length > 0 && valeurs.every((v) => v !== NON_REMPLI);

for (const option of OPTIONS.length ? OPTIONS : ['(aucune option)']) {
  test(`légende = rendu — ${option}`, (t) => {
    const expr = expressionCouleurDuRendu(option);
    const legende = legendeAffichee(option);
    const unite = conversionVersUniteAffichee(option);
    if (!rempli(expr, legende, unite)) { t.skip('modèle non rempli'); return; }
    const attendu = convertirSeuils(entreesDepuisMaplibre(expr), unite.conversion);
    assert.deepEqual(ecartsLegende(attendu, legende), []);
  });

  test(`unité de la préférence — ${option}`, (t) => {
    const unite = conversionVersUniteAffichee(option);
    const lue = uniteAfficheeParLaLegende(option);
    if (!rempli(unite, lue)) { t.skip('modèle non rempli'); return; }
    assert.equal(lue, unite.unite);
  });

  test(`arrondi sans changement de classe — ${option}`, (t) => {
    const legende = legendeAffichee(option);
    if (!rempli(legende)) { t.skip('modèle non rempli'); return; }
    const seuils = legende.map(([s]) => s).filter((s) => typeof s === 'number');
    if (!seuils.length) { t.skip('aucun seuil numérique (légende catégorielle)'); return; }
    const valeurs = valeursAutourDesSeuils(seuils, DECIMALES_AFFICHEES);
    assert.deepEqual(classesChangeesParArrondi(valeurs, seuils, afficher,
      classer ? (v) => classer(v, seuils) : (v) => classe(v, seuils)), []);
  });
}
