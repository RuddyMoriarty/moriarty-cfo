#!/usr/bin/env bash
# install.sh - Installation automatique de moriarty-cfo pour Claude Code
#
# Usage :
#   curl -fsSL https://raw.githubusercontent.com/RuddyMoriarty/moriarty-cfo/main/install.sh | bash
#   ou :
#   git clone https://github.com/RuddyMoriarty/moriarty-cfo.git && cd moriarty-cfo && ./install.sh
#
# Ce script :
#   1. Verifie les pre-requis (Python >= 3.10, git, Claude Code)
#   2. Clone le repo si besoin
#   3. Cree le symlink vers ~/.claude/skills/
#   4. Verifie l'installation (evals --quick)
#   5. Affiche les prochaines etapes

set -euo pipefail

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()  { echo -e "${BLUE}[info]${NC}  $*"; }
ok()    { echo -e "${GREEN}[ok]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[warn]${NC}  $*"; }
fail()  { echo -e "${RED}[fail]${NC}  $*"; exit 1; }

REPO_URL="https://github.com/RuddyMoriarty/moriarty-cfo.git"
SKILLS_DIR="$HOME/.claude/skills"
BUNDLE_NAME="moriarty-cfo"

echo ""
echo "  moriarty-cfo installer"
echo "  10 skills Claude pour CFO/DAF francais"
echo ""

# ─────────────────────────────────────────────
# 1. Pre-requis
# ─────────────────────────────────────────────

info "Verification des pre-requis..."

# Python >= 3.10
if command -v python3 &>/dev/null; then
    PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
    PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
    if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 9 ]; then
        ok "Python $PY_VERSION"
    else
        fail "Python >= 3.9 requis (trouve : $PY_VERSION). Installez via https://python.org"
    fi
else
    fail "Python 3 introuvable. Installez Python >= 3.10 via https://python.org"
fi

# PyYAML (requis par run_evals.py)
if python3 -c "import yaml" &>/dev/null; then
    ok "PyYAML installe"
else
    warn "PyYAML manquant, installation..."
    pip3 install --quiet pyyaml || fail "Impossible d'installer PyYAML"
    ok "PyYAML installe"
fi

# Git
if command -v git &>/dev/null; then
    ok "git $(git --version | cut -d' ' -f3)"
else
    fail "git introuvable. Installez git via https://git-scm.com"
fi

# Claude Code (optionnel mais recommande)
if command -v claude &>/dev/null; then
    ok "Claude Code detecte"
else
    warn "Claude Code non detecte dans le PATH (pas bloquant si vous utilisez Claude.ai ou l'API)"
fi

echo ""

# ─────────────────────────────────────────────
# 2. Clone si besoin
# ─────────────────────────────────────────────

# Detecter si on est deja dans le repo
if [ -f "pyproject.toml" ] && grep -q "moriarty-cfo" pyproject.toml 2>/dev/null; then
    REPO_DIR="$(pwd)"
    ok "Deja dans le repo moriarty-cfo : $REPO_DIR"
else
    TARGET_DIR="${1:-$HOME/moriarty-cfo}"
    if [ -d "$TARGET_DIR" ] && [ -f "$TARGET_DIR/pyproject.toml" ]; then
        REPO_DIR="$TARGET_DIR"
        ok "Repo existant trouve : $REPO_DIR"
    else
        info "Clonage du repo dans $TARGET_DIR..."
        git clone --depth 1 "$REPO_URL" "$TARGET_DIR"
        REPO_DIR="$TARGET_DIR"
        ok "Repo clone dans $REPO_DIR"
    fi
fi

echo ""

# ─────────────────────────────────────────────
# 3. Symlink vers ~/.claude/skills/
# ─────────────────────────────────────────────

LINK_PATH="$SKILLS_DIR/$BUNDLE_NAME"

mkdir -p "$SKILLS_DIR"

if [ -L "$LINK_PATH" ]; then
    EXISTING_TARGET=$(readlink "$LINK_PATH")
    if [ "$EXISTING_TARGET" = "$REPO_DIR" ]; then
        ok "Symlink deja en place : $LINK_PATH -> $REPO_DIR"
    else
        warn "Symlink existant pointe vers $EXISTING_TARGET"
        warn "Mise a jour vers $REPO_DIR"
        rm "$LINK_PATH"
        ln -s "$REPO_DIR" "$LINK_PATH"
        ok "Symlink mis a jour"
    fi
elif [ -e "$LINK_PATH" ]; then
    warn "$LINK_PATH existe deja (pas un symlink). Verification manuelle recommandee."
else
    ln -s "$REPO_DIR" "$LINK_PATH"
    ok "Symlink cree : $LINK_PATH -> $REPO_DIR"
fi

echo ""

# ─────────────────────────────────────────────
# 4. Verification (evals --quick)
# ─────────────────────────────────────────────

info "Verification de l'installation (evals --quick)..."
echo ""

cd "$REPO_DIR"
if python3 evals/run_evals.py --quick 2>&1; then
    echo ""
    ok "Installation verifiee avec succes"
else
    echo ""
    warn "Les evals ont echoue. L'installation est en place mais verifiez les erreurs ci-dessus."
fi

echo ""

# ─────────────────────────────────────────────
# 5. Prochaines etapes
# ─────────────────────────────────────────────

echo "─────────────────────────────────────────"
echo ""
echo "  Installation terminee."
echo ""
echo "  Pour commencer, dans Claude Code :"
echo ""
echo "    > Lance cfo-init pour ma societe SIREN 552120222"
echo ""
echo "  Cles API optionnelles (dans un fichier .env) :"
echo "    PAPPERS_API_KEY=votre_cle     # Enrichissement societe"
echo "    INSEE_API_KEY=votre_cle       # Fallback SIREN gratuit"
echo ""
echo "  Documentation :"
echo "    README        $REPO_DIR/README.md"
echo "    Securite      $REPO_DIR/SECURITY.md"
echo "    Changelog     $REPO_DIR/CHANGELOG.md"
echo ""
echo "  Commandes evals :"
echo "    python3 $REPO_DIR/evals/run_evals.py --quick"
echo "    python3 $REPO_DIR/evals/run_evals.py --full"
echo ""
echo "─────────────────────────────────────────"
