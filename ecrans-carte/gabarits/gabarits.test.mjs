// Tests des gabarits JS eux-mêmes (pas d'un projet). Lancer :
//   node --test ecrans-carte/gabarits/gabarits.test.mjs
import test from 'node:test';
import assert from 'node:assert/strict';
import {
  normaliserCouleur, entreesDepuisMaplibre, entreesDepuisSld, convertirSeuils,
  ecartsLegende, classe, valeursAutourDesSeuils, classesChangeesParArrondi,
} from './legende-rendu.mjs';
import {
  chevauchements, ciblesTropPetites, horsDuParent, couvre, contraste, contrasteMinimal,
} from './boites.mjs';

const STEP = ['step', ['get', 'v'], '#000', 10, '#FF0000', 20, 'rgb(0, 255, 0)'];
const SLD = `<sld:ColorMap type="intervals">
  <sld:ColorMapEntry color="#000000" quantity="10" opacity="0"/>
  <sld:ColorMapEntry quantity='20' color='#FF0000' label="20"/>
</sld:ColorMap>`;

test('normaliserCouleur', () => {
  assert.equal(normaliserCouleur('#ABC'), '#aabbcc');
  assert.equal(normaliserCouleur('rgba(255,0,0,0.5)'), '#ff000080');
  assert.equal(normaliserCouleur('0xFF0000'), '#ff0000');
  assert.equal(normaliserCouleur('#ff0000ff'), '#ff0000');
  assert.throws(() => normaliserCouleur('rouge'));
});

test('entrées MapLibre : step, interpolate, match', () => {
  assert.deepEqual(entreesDepuisMaplibre(STEP),
    [[null, '#000000'], [10, '#ff0000'], [20, '#00ff00']]);
  assert.deepEqual(entreesDepuisMaplibre(['interpolate', ['linear'], ['get', 'v'], 0, '#fff', 5, '#000']),
    [[0, '#ffffff'], [5, '#000000']]);
  assert.deepEqual(entreesDepuisMaplibre(['match', ['get', 'k'], ['a', 'b'], '#f00', 'c', '#0f0', '#00f']),
    [['a', '#ff0000'], ['b', '#ff0000'], ['c', '#00ff00'], ['*', '#0000ff']]);
  assert.throws(() => entreesDepuisMaplibre(['case', true, '#000', '#fff']));
});

test('entrées SLD : attributs dans tout ordre, opacité gardée', () => {
  assert.deepEqual(entreesDepuisSld(SLD), [[10, '#00000000'], [20, '#ff0000']]);
  assert.throws(() => entreesDepuisSld('<sld:ColorMap/>'));
});

test('entrées SLD : les ColorMapEntry commentés sont ignorés, comme en Python', () => {
  const commente = '<ColorMap><!-- <ColorMapEntry color="#fff" quantity="5"/> -->'
    + '<ColorMapEntry color="#000" quantity="10"/></ColorMap>';
  assert.deepEqual(entreesDepuisSld(commente), [[10, '#000000']]);
  assert.throws(() => entreesDepuisSld('<ColorMap><!-- <ColorMapEntry color="#fff" quantity="5"/> --></ColorMap>'),
    /aucun ColorMapEntry/);
});

test('entrées SLD : une entrée sans quantity est refusée (pas de NaN)', () => {
  assert.throws(() => entreesDepuisSld('<ColorMap><ColorMapEntry color="#000"/></ColorMap>'),
    /quantity/);
});

test('ecartsLegende : vide quand la légende suit le rendu, nommé sinon', () => {
  const attendu = entreesDepuisMaplibre(STEP);
  assert.deepEqual(ecartsLegende(attendu, [[null, '#000'], [10, '#f00'], [20, '#0f0']]), []);
  const ecarts = ecartsLegende(attendu, [[null, '#000'], [15, '#f00'], [20, '#00f']]);
  assert.equal(ecarts.length, 2);
  assert.match(ecarts[0], /seuil 15/);
  assert.match(ecartsLegende(attendu, attendu.slice(1))[0], /2 entrées dans la légende, 3/);
});

test('convertirSeuils : unité de l’utilisateur', () => {
  const kelvin = [[null, '#000000'], [273.15, '#ff0000']];
  assert.deepEqual(ecartsLegende(convertirSeuils(kelvin, (k) => k - 273.15),
    [[null, '#000000'], [0, '#ff0000']]), []);
});

test('classe et arrondi', () => {
  assert.equal(classe(9.99, [10, 20]), 0);
  assert.equal(classe(10, [10, 20]), 1);
  const valeurs = valeursAutourDesSeuils([25], 1);
  const afficher = (v) => Math.round(v * 10) / 10;
  const fautes = classesChangeesParArrondi(valeurs, [25], afficher);
  assert.ok(fautes.some(([v, aff]) => v < 25 && aff === 25));
  assert.deepEqual(classesChangeesParArrondi(valeurs, [25], afficher,
    (v) => classe(afficher(v), [25])), []);
});

test('boîtes : chevauchement, cibles, parent, fiche', () => {
  const a = { nom: 'a', x: 0, y: 0, largeur: 30, hauteur: 30 };
  const b = { nom: 'b', x: 29, y: 0, largeur: 30, hauteur: 30 };
  const c = { nom: 'c', x: 59, y: 0, largeur: 10, hauteur: 30 };
  assert.deepEqual(chevauchements([a, b, c]), [['a', 'b']]);
  assert.deepEqual(ciblesTropPetites([a, c]), ['c']);
  assert.deepEqual(horsDuParent([a, c], { x: 0, y: 0, largeur: 60, hauteur: 30 }), ['c']);
  assert.equal(couvre({ x: 0, y: 0, largeur: 100, hauteur: 50 }, { x: 50, y: 25 }), true);
  assert.equal(couvre({ x: 0, y: 0, largeur: 100, hauteur: 50 }, { x: 50, y: 60 }), false);
});

test('contraste WCAG', () => {
  assert.ok(Math.abs(contraste([0, 0, 0], [255, 255, 255]) - 21) < 1e-9);
  assert.ok(Math.abs(contraste([119, 119, 119], [255, 255, 255]) - 4.48) < 0.01);
  assert.ok(contrasteMinimal([255, 255, 255], [[0, 0, 0], [240, 240, 240]]) < 3);
});

test('mesure vide : refusée, jamais verte sans mesure', () => {
  assert.throws(() => contrasteMinimal([255, 255, 255], []), /aucun pixel/);
  assert.throws(() => chevauchements([]), /aucune boîte/);
  assert.throws(() => ciblesTropPetites([]), /aucune boîte/);
  assert.throws(() => horsDuParent([], { x: 0, y: 0, largeur: 10, hauteur: 10 }), /aucune boîte/);
});
