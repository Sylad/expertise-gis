#!/usr/bin/env python3
"""Sert les fiches d'expertise-gis à une session Claude Code.

Deux commandes, sans dépendance :

  fiches.py chercher <mots…> [--max N]
      Cherche une fiche par symptôme : les mots (accents et casse ignorés) sont
      comptés dans le titre, le Symptôme et la ligne d'index de chaque fiche.
      Affiche, de la plus pertinente à la moins, le statut (prouvé / à
      reprouver), le chemin local de la fiche et son titre.

  fiches.py references [--domaines a,b] [--racine DOSSIER] [--dir DOSSIER]
      Écrit le bloc « references: » à copier dans le cadence.yaml d'un projet,
      sous la forme unique de cadence (L760) : references: { dir, run: [...] },
      run étant une liste de { mots: [...], docs: [...] }, une entrée par domaine
      (geoserver, postgis, sld, openlayers, maplibre, symbologie, ecrans-carte).
      Quand un mot apparaît dans une demande, cadence run fait lire les docs ; un
      doc doit être un fichier présent sur la machine (cadence écarte sans erreur
      une URL ou un fichier absent). dir (dossier des documents de cadence ref)
      n'est écrit que si --dir est donné : il est propre au projet.
      Les docs visent une copie stable : lancé depuis la copie installée du
      plugin (…/plugins/cache/<place>/<plugin>/<version>/, purgée à chaque mise
      à jour), le script écrit le clone de la place de marché
      (…/plugins/marketplaces/<place>/), sans numéro de version ; lancé depuis
      un clone ordinaire, ce clone. --racine impose un autre dossier. Un chemin
      sous le dossier personnel s'écrit « ~/… » (le même sur toute machine).
      Code 3 si un doc est absent de la racine choisie (le bloc est écrit quand même).

  fiches.py domaines
      Liste les domaines connus, avec leur nombre de fiches.

Le dépôt se trouve à partir de l'emplacement du script
(<racine>/skills/fiches-gis/scripts/fiches.py) ; EXPERTISE_GIS_RACINE le remplace.
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

# Le dépôt public (place de marché et plugin), pour l'installation.
DEPOT_GITHUB = "Sylad/expertise-gis"

# Un domaine = un dossier sous fiches/ (ou ecrans-carte/), ce qu'il couvre, et les
# mots qui, dans une demande, le font lire par cadence (comparés sans accents ni
# casse, en mot entier). Un dossier de fiches sans entrée ici fait échouer les
# tests : un domaine ajouté au dépôt doit dire quand le lire.
DOMAINES = {
    "geoserver": (
        "fiches/geoserver",
        "GeoServer / GeoTools / GeoWebCache : WMS, styles, ImageMosaic, dimension TIME, "
        "catalogue JDBC, grappe, sécurité, modules Java",
        ["geoserver", "geotools", "geowebcache", "gwc", "wms", "wmts", "wfs", "wcs", "imagemosaic", "getmap", "getcapabilities", "capabilities"],
    ),
    "postgis": (
        "fiches/postgis",
        "PostgreSQL / PostGIS / TimescaleDB : schémas, séquences, index, migrations",
        ["postgis", "postgresql", "postgres", "timescaledb", "timescale"],
    ),
    "sld": (
        "fiches/sld",
        "SLD / SE : RasterSymbolizer, transformations de rendu, GetLegendGraphic, rotation de marques",
        ["sld", "symbolizer", "rastersymbolizer", "getlegendgraphic", "colormap"],
    ),
    "openlayers": (
        "fiches/openlayers",
        "OpenLayers côté client : projections, sources WMS, couches vecteur, contrôles, performance",
        ["openlayers"],
    ),
    "maplibre": (
        "fiches/maplibre",
        "MapLibre GL JS côté client : projection globe, styles portés d'un SLD, échelles, "
        "couches WebGL personnalisées, capture",
        ["maplibre", "maplibre-gl"],
    ),
    "symbologie": (
        "fiches/symbologie",
        "Symbologie normalisée OACI / OMM : cartes SIGWX, fronts et centres, modèle de station, "
        "SIGMET et zones d'avis (norme, paragraphe, page et figure cités)",
        ["sigwx", "temsi", "sigmet", "airmet", "gamet", "barbule", "barbules", "symbologie", "modèle de station",
         # « front » seul attraperait « front-end » : des expressions seulement (revue L5).
         "front froid", "fronts froids", "front chaud", "fronts chauds", "front occlus", "fronts occlus",
         "front stationnaire", "fronts stationnaires", "front quasi stationnaire", "fronts quasi stationnaires",
         "cold front", "warm front", "occluded front", "stationary front", "symboles de fronts"],
    ),
    "ecrans-carte": (
        "ecrans-carte",
        "Écran avec carte, toute bibliothèque : les 13 invariants (légende = rendu, unités, "
        "validité, temps, partage, export), interface utilisable, gabarits de tests",
        ["carte", "cartes", "légende", "légendes", "globe", "couche", "couches"],
    ),
}

ICONES = {"prouvé": "✅", "à reprouver": "🔁"}

# Les documents qu'un domaine fait lire. Les fiches : l'index par symptôme (le même
# pour tous les domaines de fiches ; cadence ne lit qu'une fois un doc partagé) — un
# domaine compte jusqu'à 51 fiches, l'index les range par symptôme et donne le chemin
# de chacune. La mécanique des écrans : les invariants et les règles d'interface.
DOCS_ECRANS = ["ecrans-carte/invariants.md", "ecrans-carte/interface.md"]


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


def docs_du_domaine(nom):
    return ["fiches/README.md"] if DOMAINES[nom][0].startswith("fiches/") else DOCS_ECRANS


def racine_stable(rac):
    """La copie qui survit à une mise à jour du plugin.

    Claude Code installe un plugin dans <config>/plugins/cache/<place>/<plugin>/<version>/
    et purge ce dossier à la mise à jour ; le clone de la place de marché,
    <config>/plugins/marketplaces/<place>/, garde son chemin. Un clone ordinaire est
    rendu tel quel."""
    parties = rac.parts
    if len(parties) >= 5 and parties[-5:-3] == ("plugins", "cache"):
        return Path(*parties[:-4]) / "marketplaces" / parties[-3]
    return rac


def raccourcir(chemin, accueil=None):
    """« ~/… » sous le dossier personnel (le même texte d'une machine à l'autre)."""
    accueil = Path(accueil or Path.home())
    try:
        return "~/" + chemin.relative_to(accueil).as_posix()
    except ValueError:
        return chemin.as_posix()


def references(rac, domaines=None, racine_docs=None, dir_ref=None):
    """Le bloc YAML « references: » de cadence pour les domaines demandés (tous par défaut).

    Forme unique lue par cadence run et cadence ref (L760, scripts/references.mjs de cadence) :
    references: { dir, run: [{ mots: [...], docs: [...] }] }. Une liste directement sous
    references: est l'ancienne forme de cadence run : cadence la lit encore mais affiche un
    message de migration, d'où la clé run.
    racine_docs : la copie que les docs visent (par défaut racine_stable(rac)).
    dir_ref : references.dir (dossier des documents de cadence ref), écrit s'il est donné."""
    noms = list(DOMAINES) if not domaines else domaines
    inconnus = [n for n in noms if n not in DOMAINES]
    if inconnus:
        raise ValueError(f"domaine(s) inconnu(s) : {', '.join(inconnus)} "
                         f"(connus : {', '.join(DOMAINES)})")
    if dir_ref is not None and not dir_ref.strip():
        # cadence refuse un dir vide (« references.dir : chemin attendu »).
        raise ValueError("--dir : chemin attendu (vide)")
    base = Path(racine_docs) if racine_docs else racine_stable(rac)
    lignes = [
        "# expertise-gis : pièges prouvés des outils de carte, une fiche par piège",
        "# (symptôme, cause, détection, geste, version, source). Un mot de la liste",
        "# dans la demande fait lire les docs à cadence run ; l'index est rangé par symptôme.",
        "references:",
    ]
    if dir_ref is not None:
        lignes += ["  # cadence ref : dossier de ses documents, hors de tout dépôt Git",
                   f"  dir: {json.dumps(dir_ref.strip(), ensure_ascii=False)}"]
    lignes.append("  run:")
    for nom in noms:
        _, quand, mots_cles = DOMAINES[nom]
        docs = [raccourcir(base / d) for d in docs_du_domaine(nom)]
        lignes += [
            f"    # expertise-gis/{nom} : {quand} ({taille(rac, nom)})",
            f"    - mots: {json.dumps(mots_cles, ensure_ascii=False)}",
            f"      docs: {json.dumps(docs, ensure_ascii=False)}",
        ]
    return "\n".join(lignes) + "\n"


def docs_absents(texte):
    """Les docs du bloc qui ne sont pas des fichiers sur cette machine."""
    absents = []
    for ligne in texte.splitlines():
        m = re.match(r"^      docs: (.+)$", ligne)
        if m:
            absents += [d for d in json.loads(m.group(1))
                        if not Path(os.path.expanduser(d)).is_file()]
    return absents


def principal(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sous = p.add_subparsers(dest="commande", required=True)
    c = sous.add_parser("chercher", help="trouver une fiche par symptôme")
    c.add_argument("mots", nargs="+")
    c.add_argument("--max", type=int, default=8)
    r = sous.add_parser("references", help="bloc references: pour cadence.yaml")
    r.add_argument("--domaines", default="", help="liste séparée par des virgules")
    r.add_argument("--racine", default=None,
                   help="copie visée par les docs (défaut : clone de la place de marché, "
                        "ou ce clone)")
    r.add_argument("--dir", default=None, dest="dir_ref",
                   help="references.dir de cadence ref (dossier de ses documents), propre au projet")
    # Ancien nom (0.1.0) : écrit désormais la copie stable, comme le défaut.
    r.add_argument("--local", action="store_true", help=argparse.SUPPRESS)
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
        cible = Path(os.path.expanduser(args.racine)).resolve() if args.racine else None
        try:
            bloc = references(rac, domaines, cible, args.dir_ref)
        except ValueError as e:
            print(e, file=sys.stderr)
            return 2
        sys.stdout.write(bloc)
        absents = docs_absents(bloc)
        if absents:
            print("doc absent sur cette machine (cadence l'écarterait sans le dire) : "
                  + ", ".join(absents), file=sys.stderr)
            return 3
        return 0
    for nom, (_, quand, _) in DOMAINES.items():
        print(f"{nom:13} {taille(rac, nom):19} {quand}")
    return 0


if __name__ == "__main__":
    sys.exit(principal())
