// Gabarit « légende = rendu » (invariants 1 et 2 de ecrans-carte/invariants.md), pour un
// front JavaScript ou TypeScript. Sans dépendance : copier ce fichier dans le projet et
// l'appeler depuis Vitest, Jest ou `node --test`. Même logique que legende_rendu.py ;
// le modèle de test est dans modele-legende.test.mjs.
//
// Une entrée est [seuil, couleur] ; seuil null = classe sous le premier seuil d'un `step`,
// valeur catégorielle pour un `match` (« * » = couleur par défaut). Une valeur égale à un
// seuil appartient à la classe qui commence à ce seuil (sémantique de `step`).

const INTERPOLATIONS = new Set(['interpolate', 'interpolate-hcl', 'interpolate-lab']);

const hex2 = (n) => n.toString(16).padStart(2, '0');
const estNombre = (x) => typeof x === 'number' && Number.isFinite(x);

export function normaliserCouleur(couleur, opacite) {
  let c = String(couleur).trim().toLowerCase();
  let alpha = 1;
  let r; let g; let b;
  const m = c.match(/^rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)$/);
  if (m) {
    [r, g, b] = [m[1], m[2], m[3]].map((x) => Math.round(Number(x)));
    if (m[4] !== undefined) alpha = Number(m[4]);
  } else {
    if (c.startsWith('0x')) c = `#${c.slice(2)}`;
    if (!/^#(?:[0-9a-f]{3}|[0-9a-f]{6}|[0-9a-f]{8})$/.test(c)) {
      throw new Error(`couleur non reconnue : ${couleur}`);
    }
    let h = c.slice(1);
    if (h.length === 3) h = [...h].map((x) => x + x).join('');
    if (h.length === 8) alpha = parseInt(h.slice(6), 16) / 255;
    [r, g, b] = [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16));
  }
  if (opacite !== undefined && opacite !== null) alpha *= Number(opacite);
  const hexa = `#${hex2(r)}${hex2(g)}${hex2(b)}`;
  return Math.abs(alpha - 1) < 1e-9 ? hexa : hexa + hex2(Math.round(alpha * 255));
}

export function entreesDepuisMaplibre(expression) {
  if (typeof expression === 'string') return [[null, normaliserCouleur(expression)]];
  const [op] = expression;
  const paires = (reste) => {
    const sortie = [];
    for (let i = 0; i < reste.length; i += 2) sortie.push([reste[i], normaliserCouleur(reste[i + 1])]);
    return sortie;
  };
  if (op === 'step') return [[null, normaliserCouleur(expression[2])], ...paires(expression.slice(3))];
  if (INTERPOLATIONS.has(op)) return paires(expression.slice(3));
  if (op === 'match') {
    const reste = expression.slice(2, -1);
    const sortie = [];
    for (let i = 0; i < reste.length; i += 2) {
      const valeurs = Array.isArray(reste[i]) ? reste[i] : [reste[i]];
      for (const v of valeurs) sortie.push([v, normaliserCouleur(reste[i + 1])]);
    }
    return [...sortie, ['*', normaliserCouleur(expression.at(-1))]];
  }
  throw new Error(`expression de couleur non prise en charge : ${op}`);
}

// Lecture des ColorMapEntry d'un SLD / SE sans DOMParser (absent de Node) : les
// commentaires XML sont ôtés (un parseur XML les ignore, comme legende_rendu.py), puis
// chaque balise est prise entière, puis ses attributs, dans n'importe quel ordre.
export function entreesDepuisSld(texteSld) {
  const sortie = [];
  const sansCommentaires = texteSld.replace(/<!--[\s\S]*?-->/g, '');
  for (const balise of sansCommentaires.matchAll(/<(?:[\w-]+:)?ColorMapEntry\b([^>]*)>/g)) {
    const attrs = Object.fromEntries(
      [...balise[1].matchAll(/([\w:-]+)\s*=\s*("([^"]*)"|'([^']*)')/g)]
        .map((a) => [a[1], a[3] ?? a[4]]),
    );
    if (attrs.quantity === undefined) throw new Error(`ColorMapEntry sans quantity : ${balise[0]}`);
    sortie.push([Number(attrs.quantity), normaliserCouleur(attrs.color ?? '#000000', attrs.opacity)]);
  }
  if (!sortie.length) throw new Error('aucun ColorMapEntry dans le style');
  return sortie;
}

export const convertirSeuils = (entrees, conversion) =>
  entrees.map(([s, c]) => [estNombre(s) ? conversion(s) : s, c]);

export function ecartsLegende(attendu, legende, tolerance = 1e-6) {
  const ecarts = [];
  if (attendu.length !== legende.length) {
    ecarts.push(`${legende.length} entrées dans la légende, ${attendu.length} dans le rendu`);
  }
  const n = Math.min(attendu.length, legende.length);
  for (let i = 0; i < n; i += 1) {
    const [sa, ca] = attendu[i];
    const [sl, cl] = legende[i];
    const egal = estNombre(sa) && estNombre(sl)
      ? Math.abs(sa - sl) <= tolerance * Math.max(1, Math.abs(sa))
      : sa === sl;
    if (!egal) ecarts.push(`entrée ${i} : seuil ${sl} dans la légende, ${sa} dans le rendu`);
    if (normaliserCouleur(cl) !== normaliserCouleur(ca)) {
      ecarts.push(`entrée ${i} : couleur ${cl} dans la légende, ${ca} dans le rendu`);
    }
  }
  return ecarts;
}

export function classe(valeur, seuils) {
  return [...seuils].sort((a, b) => a - b).filter((s) => valeur >= s).length;
}

export function valeursAutourDesSeuils(seuils, decimales) {
  const pas = 10 ** -decimales;
  return seuils.flatMap((s) => [s - pas / 2, s - pas / 10, s, s + pas / 10, s + pas / 2]);
}

// afficher(v) : le nombre que lit l'utilisateur ; classer(v) : la classe qui choisit la
// couleur (par défaut, la valeur brute). Vide quand aucune valeur ne s'affiche « 25,0 »
// dans la couleur de « < 25 ».
export function classesChangeesParArrondi(valeurs, seuils, afficher, classer) {
  const classerCouleur = classer ?? ((v) => classe(v, seuils));
  return valeurs.flatMap((v) => {
    const affichee = afficher(v);
    const cc = classerCouleur(v);
    const ca = classe(affichee, seuils);
    return cc === ca ? [] : [[v, affichee, cc, ca]];
  });
}
