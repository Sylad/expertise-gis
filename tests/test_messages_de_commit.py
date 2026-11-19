"""Garde des messages de commit (L13, mineur M1 de la revue L6).

Le dépôt est public : un message de commit est publié comme un fichier. Un terme
de .termes-prives (ou d'EXPERTISE_GIS_TERMES_PRIVES) dans un message est refusé
par le hook `hooks/commit-msg` (installé par `hooks/installer.sh`), et ce test
relit tout l'historique au cas où un commit aurait été fait sans le hook.
"""
import importlib.machinery
import importlib.util
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
HOOK = RACINE / "hooks" / "commit-msg"
INSTALLEUR = RACINE / "hooks" / "installer.sh"
TERME = "terme-secret-de-test"

# Commits déjà publiés qui portent un nom d'hôte : décision de Sylvain du
# 2026-11-19 (« laisse comme ça, c'est juste un nom d'hôte »), pas de réécriture
# de l'historique public. Aucun autre commit ne peut s'ajouter à cette liste.
DEJA_PUBLIES = {
    "8b400a814147938519ebdded0b32c5171583f8d3",
    "68acfc1b8aa6f3d7cba20c10d980ddcacd6f2287",
}


def charger_hook():
    chargeur = importlib.machinery.SourceFileLoader("commit_msg", str(HOOK))
    spec = importlib.util.spec_from_loader("commit_msg", chargeur)
    module = importlib.util.module_from_spec(spec)
    chargeur.exec_module(module)
    return module


def env_propre(**ajouts):
    """Environnement sans variables GIT_* héritées (la suite peut tourner dans un hook)."""
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("GIT_") and k != "EXPERTISE_GIS_TERMES_PRIVES"}
    env.update(GIT_AUTHOR_NAME="test", GIT_AUTHOR_EMAIL="test@example.invalid",
               GIT_COMMITTER_NAME="test", GIT_COMMITTER_EMAIL="test@example.invalid",
               GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
    env.update(ajouts)
    return env


class TestHookCommitMsg(unittest.TestCase):
    def jouer(self, message, env):
        with tempfile.TemporaryDirectory() as dossier:
            fichier = Path(dossier, "COMMIT_EDITMSG")
            fichier.write_text(message, encoding="utf-8")
            return subprocess.run(["python3", str(HOOK), str(fichier)], cwd=dossier,
                                  env=env, capture_output=True, text=True)

    def test_hook_present_et_executable(self):
        self.assertTrue(HOOK.exists(), "hooks/commit-msg manquant")
        self.assertTrue(os.access(HOOK, os.X_OK), "hooks/commit-msg non exécutable")

    def test_message_avec_terme_prive_refuse(self):
        env = env_propre(EXPERTISE_GIS_TERMES_PRIVES=TERME)
        for message in (f"plan: L99 ouvert ({TERME})\n",
                        f"feat(L99): titre\n\nCorps qui cite {TERME.upper()}.\n"):
            with self.subTest(message=message):
                sortie = self.jouer(message, env)
                self.assertNotEqual(sortie.returncode, 0, "message privé accepté")
                self.assertIn("terme privé", sortie.stderr)

    def test_message_propre_accepte(self):
        env = env_propre(EXPERTISE_GIS_TERMES_PRIVES=TERME)
        sortie = self.jouer("feat(L99): fiche neuve\n", env)
        self.assertEqual(sortie.returncode, 0, sortie.stderr)

    def test_commentaires_de_git_ignores(self):
        # Les lignes « # » et tout ce qui suit la ligne de ciseaux ne sont pas commités.
        env = env_propre(EXPERTISE_GIS_TERMES_PRIVES=TERME)
        message = (f"feat(L99): fiche\n# Sur la branche {TERME}\n"
                   "# ------------------------ >8 ------------------------\n"
                   f"diff --git a/{TERME} b/{TERME}\n")
        sortie = self.jouer(message, env)
        self.assertEqual(sortie.returncode, 0, sortie.stderr)

    def test_sans_liste_refuse(self):
        # Comme test_aucun_terme_interdit : sans liste, on ne peut rien garantir.
        sortie = self.jouer("feat(L99): fiche\n", env_propre())
        self.assertNotEqual(sortie.returncode, 0)
        self.assertIn(".termes-prives", sortie.stderr)

    def test_liste_lue_dans_le_depot(self):
        hook = charger_hook()
        with tempfile.TemporaryDirectory() as vide:
            Path(vide, ".termes-prives").write_text(f"# note\n\n {TERME} \n", encoding="utf-8")
            self.assertEqual(hook.termes_prives(vide, {"EXPERTISE_GIS_TERMES_PRIVES": "a,"}),
                             ["a", TERME])


@unittest.skipUnless(shutil.which("git"), "git absent")
class TestCommitRefuseDansUnDepot(unittest.TestCase):
    """De bout en bout : un vrai `git commit`, hook posé par l'installeur."""

    def git(self, depot, *args, env):
        return subprocess.run(["git", *args], cwd=depot, env=env,
                              capture_output=True, text=True)

    def test_commit_refuse_puis_accepte(self):
        with tempfile.TemporaryDirectory() as depot:
            env = env_propre()
            self.git(depot, "init", "-q", env=env)
            shutil.copytree(RACINE / "hooks", Path(depot, "hooks"))
            Path(depot, ".termes-prives").write_text(TERME + "\n", encoding="utf-8")
            Path(depot, "a.txt").write_text("a\n", encoding="utf-8")
            pose = subprocess.run(["sh", str(Path(depot, "hooks", "installer.sh"))],
                                  cwd=depot, env=env, capture_output=True, text=True)
            self.assertEqual(pose.returncode, 0, pose.stderr)
            self.git(depot, "add", "a.txt", "hooks", env=env)

            refus = self.git(depot, "commit", "-q", "-m", f"plan: L1 ({TERME})", env=env)
            self.assertNotEqual(refus.returncode, 0, "commit privé accepté")
            self.assertNotEqual(self.git(depot, "rev-parse", "-q", "--verify", "HEAD",
                                         env=env).returncode, 0, "un commit a été créé")

            ok = self.git(depot, "commit", "-q", "-m", "plan: L1 ouvert", env=env)
            self.assertEqual(ok.returncode, 0, ok.stderr)

    def test_worktree_sans_liste_lit_celle_du_clone_principal(self):
        with tempfile.TemporaryDirectory() as dossier:
            depot, arbre = Path(dossier, "principal"), Path(dossier, "arbre")
            env = env_propre()
            depot.mkdir()
            self.git(depot, "init", "-q", env=env)
            shutil.copytree(RACINE / "hooks", depot / "hooks")
            Path(depot, ".gitignore").write_text(".termes-prives\n", encoding="utf-8")
            self.git(depot, "add", ".", env=env)
            self.assertEqual(self.git(depot, "commit", "-q", "--no-verify", "-m", "init",
                                      env=env).returncode, 0)
            Path(depot, ".termes-prives").write_text(TERME + "\n", encoding="utf-8")
            pose = subprocess.run(["sh", "hooks/installer.sh"], cwd=depot, env=env,
                                  capture_output=True, text=True)
            self.assertEqual(pose.returncode, 0, pose.stderr)
            self.git(depot, "worktree", "add", "-q", str(arbre), env=env)
            self.assertFalse((arbre / ".termes-prives").exists())
            refus = self.git(arbre, "commit", "-q", "--allow-empty", "-m",
                             f"plan: L1 ({TERME})", env=env)
            self.assertNotEqual(refus.returncode, 0, "commit privé accepté dans le worktree")
            ok = self.git(arbre, "commit", "-q", "--allow-empty", "-m", "plan: L1", env=env)
            self.assertEqual(ok.returncode, 0, ok.stderr)

    def test_installeur_ne_remplace_pas_un_autre_hook(self):
        with tempfile.TemporaryDirectory() as depot:
            env = env_propre()
            self.git(depot, "init", "-q", env=env)
            shutil.copytree(RACINE / "hooks", Path(depot, "hooks"))
            autre = Path(depot, ".git", "hooks", "commit-msg")
            autre.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            pose = subprocess.run(["sh", "hooks/installer.sh"], cwd=depot, env=env,
                                  capture_output=True, text=True)
            self.assertNotEqual(pose.returncode, 0)
            self.assertEqual(autre.read_text(encoding="utf-8"), "#!/bin/sh\nexit 0\n")
            # Rejouer l'installeur sur son propre hook est sans effet.
            autre.unlink()
            for _ in range(2):
                pose = subprocess.run(["sh", "hooks/installer.sh"], cwd=depot, env=env,
                                      capture_output=True, text=True)
                self.assertEqual(pose.returncode, 0, pose.stderr)


@unittest.skipUnless((RACINE / ".git").exists(), "pas un dépôt git")
class TestHistorique(unittest.TestCase):
    def test_aucun_terme_prive_dans_les_messages_de_commit(self):
        hook = charger_hook()
        termes = hook.termes_prives(RACINE, os.environ)
        self.assertTrue(termes, hook.MESSAGE_SANS_LISTE)
        sortie = subprocess.run(["git", "log", "--format=%H%x00%B%x01"], cwd=RACINE,
                                capture_output=True, text=True, check=True).stdout
        for bloc in sortie.split("\x01"):
            sha, _, message = bloc.strip().partition("\x00")
            if not sha or sha in DEJA_PUBLIES:
                continue
            with self.subTest(commit=sha[:7]):
                self.assertEqual(hook.termes_trouves(message, termes), [],
                                 f"terme privé dans le message du commit {sha[:7]}")

    def test_exceptions_bornees(self):
        # Les exceptions désignent des commits réels de l'historique, et seulement deux.
        self.assertEqual(len(DEJA_PUBLIES), 2)
        for sha in DEJA_PUBLIES:
            with self.subTest(commit=sha[:7]):
                existe = subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"],
                                        cwd=RACINE)
                self.assertEqual(existe.returncode, 0)


if __name__ == "__main__":
    unittest.main()
