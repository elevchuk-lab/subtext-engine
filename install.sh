#!/bin/sh
# Subtext Engine Universal Installer
# Compatible with POSIX sh (macOS, Linux, WSL)
# Repository: https://github.com/elevchuk-lab/subtext-engine

set -e

# ANSI Color Codes
BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
CYAN="\033[0;36m"
YELLOW="\033[1;33m"
RESET="\033[0m"

echo "${CYAN}"
cat << 'EOF'
 ____        _     _            _     _____             _            
/ ___| _   _| |__ | |_ _____  _| |_  | ____|_ __   __ _(_)_ __   ___ 
\___ \| | | | '_ \| __/ _ \ \/ / __| |  _| | '_ \ / _` | | '_ \ / _ \
 ___) | |_| | |_) | ||  __/>  <| |_  | |___| | | | (_| | | | | |  __/
|____/ \__,_|_.__/ \__\___/_/\_\\__| |_____|_| |_|\__, |_|_| |_|\___|
                                                  |___/              
EOF
echo "${RESET}"
echo "${BOLD}Subtext Engine — Global Forensic Linguistic & Manipulation Audit Engine${RESET}"
echo "------------------------------------------------------------------"

# Detect Target Environment
INSTALL_DIR=""

if [ -n "$SUBTEXT_INSTALL_DIR" ]; then
    INSTALL_DIR="$SUBTEXT_INSTALL_DIR"
elif [ -d "$HOME/.agent/skills" ]; then
    INSTALL_DIR="$HOME/.agent/skills/subtext-engine"
elif [ -d "$HOME/.claude/skills" ]; then
    INSTALL_DIR="$HOME/.claude/skills/subtext-engine"
elif [ -d "./.agent/skills" ]; then
    INSTALL_DIR="./.agent/skills/subtext-engine"
else
    # Default to global Antigravity/Agent skills directory
    INSTALL_DIR="$HOME/.agent/skills/subtext-engine"
fi

echo "${BLUE}==>${RESET} Target installation directory: ${YELLOW}$INSTALL_DIR${RESET}"

# Check if git is installed
if ! command -v git >/dev/null 2>&1; then
    echo "${YELLOW}[!] Warning:${RESET} git is not installed. Please install git or download the ZIP manually."
    exit 1
fi

# Clone or Update Repository
if [ -d "$INSTALL_DIR/.git" ]; then
    echo "${BLUE}==>${RESET} Existing installation found. Updating to latest release..."
    cd "$INSTALL_DIR"
    git fetch origin main >/dev/null 2>&1 || true
    git reset --hard origin/main >/dev/null 2>&1 || true
else
    echo "${BLUE}==>${RESET} Cloning repository..."
    mkdir -p "$(dirname "$INSTALL_DIR")"
    rm -rf "$INSTALL_DIR"
    git clone --depth 1 https://github.com/elevchuk-lab/subtext-engine.git "$INSTALL_DIR" >/dev/null 2>&1
fi

echo ""
echo "${GREEN}✓ Successfully installed Subtext Engine v1.0.0!${RESET}"
echo "------------------------------------------------------------------"
echo "${BOLD}HOW TO USE:${RESET}"
echo "  1. ${CYAN}In Antigravity / Claude Code:${RESET}"
echo "     The skill is automatically discovered from $INSTALL_DIR."
echo "     Trigger naturally in any session with:"
echo "     ${YELLOW}\"Audit this text with Subtext Engine\"${RESET} or"
echo "     ${YELLOW}\"Analyze this statement for deception and hidden manipulation\"${RESET}"
echo ""
echo "  2. ${CYAN}In ChatGPT / Claude Projects / Cursor / Ollama:${RESET}"
echo "     Check ready-to-paste prompts in:"
echo "     ${YELLOW}$INSTALL_DIR/prompts/${RESET}"
echo ""
echo "Documentation & Methodology: https://github.com/elevchuk-lab/subtext-engine"
echo "------------------------------------------------------------------"
