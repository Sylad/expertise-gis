#!/bin/sh
# Pose le hook commit-msg du dépôt (termes privés dans les messages de commit).
# Le hook posé est un relais vers hooks/commit-msg du clone courant : il suit les
# mises à jour du dépôt et sert à tous ses worktrees (dossier de hooks commun).
# Un autre hook commit-msg déjà présent n'est pas remplacé (code 1).
set -e
dossier="$(git rev-parse --git-common-dir)/hooks"
cible="$dossier/commit-msg"
marque="# >>> expertise-gis : termes privés dans les messages de commit"
if [ -e "$cible" ] && ! grep -qF "$marque" "$cible"; then
  echo "un autre hook commit-msg existe déjà ($cible) : y ajouter à la main" \
       "« python3 \"\$(git rev-parse --show-toplevel)/hooks/commit-msg\" \"\$1\" »" >&2
  exit 1
fi
mkdir -p "$dossier"
cat > "$cible" <<'RELAIS'
#!/bin/sh
# >>> expertise-gis : termes privés dans les messages de commit
racine=$(git rev-parse --show-toplevel)
[ -f "$racine/hooks/commit-msg" ] || exit 0
exec python3 "$racine/hooks/commit-msg" "$1"
# <<< expertise-gis
RELAIS
chmod +x "$cible"
echo "hook commit-msg posé : $cible"
