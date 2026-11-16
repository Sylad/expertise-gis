// Gabarit de mesure des boîtes et du contraste (contrôles 2 et 4 de ecrans-carte/interface.md).
//
// Les fonctions pures (chevauchements, ciblesTropPetites, horsDuParent, contraste…) se
// testent sous Node. `mesurer` s'exécute DANS la page, par exemple avec Playwright :
//
//   import { mesurer, chevauchements, ciblesTropPetites } from './boites.mjs';
//   const boites = await page.evaluate(mesurer, '.legende .graduation');
//   expect(chevauchements(boites)).toEqual([]);
//   const cibles = await page.evaluate(mesurer, 'button, [role=button], input, a[href]');
//   expect(ciblesTropPetites(cibles, 24)).toEqual([]);
//
// Une boîte est { nom, x, y, largeur, hauteur } en px CSS.
//
// Une liste mesurée vide (sélecteur qui ne trouve rien, capture du fond ratée) est
// refusée par une exception : un contrôle sans mesure ne doit jamais passer au vert.

function exigerMesure(liste, quoi) {
  if (!Array.isArray(liste) || liste.length === 0) {
    throw new Error(`${quoi} : rien de mesuré (sélecteur ou capture à vérifier)`);
  }
  return liste;
}

// Évaluée dans la page : boîtes visibles des éléments du sélecteur, avec leur texte
// (ou aria-label) pour nommer chaque écart. Autonome, sans variable extérieure.
export function mesurer(selecteur) {
  return [...document.querySelectorAll(selecteur)]
    .filter((e) => {
      const s = getComputedStyle(e);
      const r = e.getBoundingClientRect();
      return s.visibility !== 'hidden' && s.display !== 'none' && r.width > 0 && r.height > 0;
    })
    .map((e) => {
      const r = e.getBoundingClientRect();
      const nom = (e.getAttribute('aria-label') || e.textContent || e.tagName).trim().slice(0, 40);
      return { nom, x: r.x, y: r.y, largeur: r.width, hauteur: r.height };
    });
}

// Évaluée dans la page : débordement horizontal du document (WCAG 1.4.10), en px.
export function debordementHorizontal() {
  return Math.max(0, document.documentElement.scrollWidth - window.innerWidth);
}

// Paires de boîtes dont l'intersection a une aire > 0 (bord commun permis).
export function chevauchements(boites) {
  exigerMesure(boites, 'aucune boîte');
  const sortie = [];
  for (let i = 0; i < boites.length; i += 1) {
    for (let j = i + 1; j < boites.length; j += 1) {
      const a = boites[i];
      const b = boites[j];
      const dx = Math.min(a.x + a.largeur, b.x + b.largeur) - Math.max(a.x, b.x);
      const dy = Math.min(a.y + a.hauteur, b.y + b.hauteur) - Math.max(a.y, b.y);
      if (dx > 0 && dy > 0) sortie.push([a.nom, b.nom]);
    }
  }
  return sortie;
}

// Cibles plus petites que `minimum` px dans une dimension (24 = WCAG 2.5.8, 44 visés).
export const ciblesTropPetites = (boites, minimum = 24) =>
  exigerMesure(boites, 'aucune boîte').filter((b) => b.largeur < minimum || b.hauteur < minimum).map((b) => b.nom);

// Boîtes qui sortent de leur parent (texte coupé, contrôle hors du panneau).
export const horsDuParent = (boites, parent) =>
  exigerMesure(boites, 'aucune boîte')
    .filter((b) => b.x < parent.x || b.y < parent.y
      || b.x + b.largeur > parent.x + parent.largeur
      || b.y + b.hauteur > parent.y + parent.hauteur)
    .map((b) => b.nom);

// Vrai si la fiche couvre tout ou partie de `objet` : un point cliqué { x, y } ou une boîte.
export function couvre(fiche, objet) {
  const largeur = objet.largeur ?? 0;
  const hauteur = objet.hauteur ?? 0;
  return objet.x + largeur >= fiche.x && objet.x <= fiche.x + fiche.largeur
    && objet.y + hauteur >= fiche.y && objet.y <= fiche.y + fiche.hauteur;
}

// Luminance relative et rapport de contraste WCAG 2.2 (définitions de « relative luminance »
// et « contrast ratio »), couleurs [r, g, b] de 0 à 255.
export function luminance([r, g, b]) {
  const lin = (c) => {
    const s = c / 255;
    return s <= 0.04045 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
  };
  return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
}

export function contraste(c1, c2) {
  const [l1, l2] = [luminance(c1), luminance(c2)].sort((a, b) => b - a);
  return (l1 + 0.05) / (l2 + 0.05);
}

// Contraste le plus faible entre la bordure d'un contrôle et les pixels du fond de carte
// mesurés autour de lui (capture lue à part, par exemple avec sharp ou un canvas).
export const contrasteMinimal = (bordure, pixelsDuFond) =>
  Math.min(...exigerMesure(pixelsDuFond, 'aucun pixel du fond').map((p) => contraste(bordure, p)));
