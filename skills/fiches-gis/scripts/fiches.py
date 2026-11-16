#!/usr/bin/env python3
"""Sert les fiches d'expertise-gis à une session Claude Code.

Deux commandes, sans dépendance :

  fiches.py chercher <mots…> [--max N]
      Cherche une fiche par symptôme : les mots (accents et casse ignorés) sont
      comptés dans le titre, le Symptôme et la ligne d'index de chaque fiche.
      Affiche, de la plus pertinente à la moins, le statut (prouvé / à
      reprouver), le chemin local de la fiche et son titre.

  fiches.py references [--domaines a,b] [--base URL | --local]
      Écrit le bloc « references: » à copier dans le cadence.yaml d'un projet :
      une entrée par domaine de fiches (geoserver, postgis, sld, openlayers,
      maplibre, symbologie) et pour la mécanique des écrans avec carte
      (ecrans-carte). Par défaut les adresses pointent sur le dépôt public
      (stables d'une machine et d'un compte à l'autre) ; --local donne les
      chemins de la copie installée sur cette machine.

  fiches.py domaines
      Liste les domaines connus, avec leur nombre de fiches.

Le dépôt se trouve à partir de l'emplacement du script
(<racine>/skills/fiches-gis/scripts/fiches.py) ; EXPERTISE_GIS_RACINE le remplace.
"""

import argparse
import os
import re
import sys
import unicodedata
from pathlib import Path

DEPOT_PUBLIC = "https://github.com/Sylad/expertise-gis/blob/main"

# Un domaine = un dossier sous fiches/ (ou ecrans-carte/), et ce qu'il couvre.
# Un dossier de fiches sans entrée ici fait échouer les tests : un domaine
# ajouté au dépôt doit dire quand le lire.
DOMAINES = {
    "geoserver": (
        "fiches/geoserver",
        "GeoServer / GeoTools / GeoWebCache : WMS, styles, ImageMosaic, dimension TIME, "
        "catalogue JDBC, grappe, sécurité, modules Java",
    ),
    "postgis": (
        "fiches/postgis",
        "PostgreSQL / PostGIS / TimescaleDB : schémas, séquences, index, migrations",
    ),
    "sld": (
        "fiches/sld",
        "SLD / SE : RasterSymbolizer, transformations de rendu, GetLegendGraphic, rotation de marques",
    ),
    "openlayers": (
        "fiches/openlayers",
        "OpenLayers côté client : projections, sources WMS, couches vecteur, contrôles, performance",
    ),
    "maplibre": (
        "fiches/maplibre",
        "MapLibre GL JS côté client : projection globe, styles portés d'un SLD, échelles, "
        "couches WebGL personnalisées, capture",
    ),
    "symbologie": (
        "fiches/symbologie",
        "Symbologie normalisée OACI / OMM : cartes SIGWX, fronts et centres, modèle de station, "
        "SIGMET et zones d'avis (norme, paragraphe, page et figure cités)",
    ),
    "ecrans-carte": (
        "ecrans-carte",
        "Écran avec carte, toute bibliothèque : les 13 invariants (légende = rendu, unités, "
        "validité, temps, partage, export), interface utilisable, gabarits de tests",
    ),
}

ICONES = {"prouvé": "✅", "à reprouver": "🔁"}


def racine():
    env = os.environ.get("EXPERTISE_GIS_RACINE")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[3]


def normaliser(texte):
    """Minuscules sans accents, pour comparer des mots tapés vite."""
    nfd = unicodedata.normalize("NFD", texte.lower())
    return "".join(c for c in nfd if not unicodedata.combining(c))


def mots(texte):
    return re.findall(r"[a-z0-9_.]+", normaliser(texte))


def section(texte, nom):
    m = re.search(rf"^## {re.escape(nom)}\s*$(.*?)(?=^## |\Z)", texte, re.S | re.M)
    return m.group(1).strip() if m else ""


def lignes_index(rac):
    """{chemin relatif de la fiche : ligne d'index}, depuis fiches/README.md."""
    index = rac / "fiches" / "README.md"
    resultat = {}
    if not index.exists():
        return resultat
    for ligne in index.read_text(encoding="utf-8").splitlines():
        m = re.search(r"\]\(([^)]+\.md)\)", ligne)
        if ligne.startswith("- ") and m:
            resultat["fiches/" + m.group(1)] = ligne[2:]
    return resultat


def fiches(rac):
    """Chaque fiche : chemin, titre, statut, symptôme, ligne d'index."""
    index = lignes_index(rac)
    resultat = []
    for chemin in sorted((rac / "fiches").rglob("*.md")):
        if chemin.name == "README.md":
            continue
        texte = chemin.read_text(encoding="utf-8")
        relatif = chemin.relative_to(rac).as_posix()
        titre = texte.splitlines()[0].lstrip("# ").strip() if texte else relatif
        statut = section(texte, "Statut").splitlines()
        statut = statut[0].strip() if statut else ""
        resultat.append({
            "chemin": chemin,
            "relatif": relatif,
            "titre": titre,
            "statut": "prouvé" if statut.startswith("prouvé") else "à reprouver",
            "symptome": section(texte, "Symptôme"),
            "index": index.get(relatif, ""),
        })
    return resultat


def chercher(rac, requete, maximum=8):
    """Fiches classées par nombre de mots de la requête trouvés (titre compté double)."""
    voulus = [m for m in mots(" ".join(requete)) if len(m) > 2] or mots(" ".join(requete))
    classees = []
    for f in fiches(rac):
        titre = set(mots(f["titre"] + " " + f["index"] + " " + f["relatif"]))
        corps = set(mots(f["symptome"]))
        score = sum(2 if m in titre else 1 if m in corps else 0 for m in voulus)
        # préfixe : « capabilit » trouve « capabilities »
        score += sum(0.5 for m in voulus
                     if m not in titre and m not in corps
                     and any(t.startswith(m) for t in titre | corps))
        if score:
            classees.append((score, f))
    classees.sort(key=lambda x: (-x[0], x[1]["relatif"]))
    # Seules les fiches à au moins la moitié du meilleur score : un mot commun
    # (« image », « couche ») ne remonte pas toute la collection.
    seuil = classees[0][0] / 2 if classees else 0
    return [f for score, f in classees[:maximum] if score >= seuil]


def compter(rac, dossier):
    return sum(1 for p in (rac / dossier).rglob("*.md") if p.name != "README.md")


def taille(rac, nom):
    dossier = DOMAINES[nom][0]
    if dossier.startswith("fiches/"):
        return f"{compter(rac, dossier)} fiches"
    return "règles et gabarits"


def references(rac, domaines=None, base=DEPOT_PUBLIC, local=False):
    """Le bloc YAML « references: » pour les domaines demandés (tous par défaut)."""
    noms = list(DOMAINES) if not domaines else domaines
    inconnus = [n for n in noms if n not in DOMAINES]
    if inconnus:
        raise ValueError(f"domaine(s) inconnu(s) : {', '.join(inconnus)} "
                         f"(connus : {', '.join(DOMAINES)})")
    lignes = [
        "# expertise-gis : pièges prouvés des outils de carte, une fiche par piège",
        "# (symptôme, cause, détection, geste, version, source). Lire la fiche avant",
        "# de diagnostiquer ; l'index fiches/README.md est rangé par symptôme.",
        "references:",
    ]
    for nom in noms:
        dossier, quand = DOMAINES[nom]
        # Point d'entrée : l'index par symptôme pour les fiches, le README sinon.
        entree = "fiches/README.md" if dossier.startswith("fiches/") else f"{dossier}/README.md"
        adresse = (lambda chemin: (rac / chemin).as_posix()) if local else (
            lambda chemin: f"{base.rstrip('/')}/{chemin}")
        cle = "chemin" if local else "url"
        lignes += [
            f"  - nom: expertise-gis/{nom}",
            f"    {cle}: {adresse(entree)}",
            f"    dossier: {adresse(dossier)}",
            f"    lire_quand: \"{quand} ({taille(rac, nom)})\"",
        ]
    return "\n".join(lignes) + "\n"


def principal(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sous = p.add_subparsers(dest="commande", required=True)
    c = sous.add_parser("chercher", help="trouver une fiche par symptôme")
    c.add_argument("mots", nargs="+")
    c.add_argument("--max", type=int, default=8)
    r = sous.add_parser("references", help="bloc references: pour cadence.yaml")
    r.add_argument("--domaines", default="", help="liste séparée par des virgules")
    groupe = r.add_mutually_exclusive_group()
    groupe.add_argument("--base", default=DEPOT_PUBLIC, help="adresse de base du dépôt")
    groupe.add_argument("--local", action="store_true", help="chemins de la copie locale")
    sous.add_parser("domaines", help="domaines connus et nombre de fiches")
    args = p.parse_args(argv)
    rac = racine()

    if args.commande == "chercher":
        trouvees = chercher(rac, args.mots, args.max)
        if not trouvees:
            print("aucune fiche ne correspond ; lire l'index par symptôme : "
                  f"{(rac / 'fiches' / 'README.md').as_posix()}")
            return 1
        for f in trouvees:
            print(f"{ICONES[f['statut']]} {f['chemin'].as_posix()}\n   {f['titre']}")
        return 0
    if args.commande == "references":
        domaines = [d.strip() for d in args.domaines.split(",") if d.strip()]
        try:
            sys.stdout.write(references(rac, domaines, args.base, args.local))
        except ValueError as e:
            print(e, file=sys.stderr)
            return 2
        return 0
    for nom, (_, quand) in DOMAINES.items():
        print(f"{nom:13} {taille(rac, nom):19} {quand}")
    return 0


if __name__ == "__main__":
    sys.exit(principal())
