#!/bin/sh
# Subtext Engine Universal Installer
# Compatible with POSIX sh (macOS, Linux, WSL)
# Repository: https://github.com/elevchuk-lab/subtext-engine

set -e

# ANSI Color Codes
BOLD="\033[1m"
RED="\033[0;31m"
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
echo "${BOLD}Subtext Engine — Structured Discourse, Contractual Risk & Financial Language Audit Framework${RESET}"
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
    echo "${BLUE}==>${RESET} Existing git installation found at ${YELLOW}$INSTALL_DIR${RESET}."
    cd "$INSTALL_DIR"

    if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
        if [ "${SUBTEXT_FORCE_UPDATE:-0}" != "1" ]; then
            echo "${RED}[!] Error:${RESET} Local uncommitted changes or untracked files detected in ${YELLOW}$INSTALL_DIR${RESET}." >&2
            echo "    Aborting update to prevent data loss." >&2
            echo "    Please commit/stash your changes, or re-run with ${BOLD}SUBTEXT_FORCE_UPDATE=1${RESET} to overwrite local changes." >&2
            exit 1
        else
            echo "${YELLOW}[!] Warning:${RESET} SUBTEXT_FORCE_UPDATE=1 is set. Discarding local changes in ${YELLOW}$INSTALL_DIR${RESET}..."
        fi
    fi

    echo "${BLUE}==>${RESET} Fetching latest release from origin/main..."
    if ! git fetch origin main >/dev/null 2>&1; then
        echo "${RED}[!] Error:${RESET} Failed to fetch updates from origin/main. Check your network connection or git remote configuration." >&2
        exit 1
    fi

    if ! git reset --hard origin/main >/dev/null 2>&1; then
        echo "${RED}[!] Error:${RESET} Failed to reset repository to origin/main." >&2
        exit 1
    fi
else
    if [ -e "$INSTALL_DIR" ] && [ ! -d "$INSTALL_DIR" ]; then
        echo "${RED}[!] Error:${RESET} Target path ${YELLOW}$INSTALL_DIR${RESET} already exists and is not a directory. Aborting." >&2
        exit 1
    fi

    if [ -d "$INSTALL_DIR" ]; then
        if [ -n "$(ls -A "$INSTALL_DIR" 2>/dev/null)" ]; then
            echo "${RED}[!] Error:${RESET} Target directory ${YELLOW}$INSTALL_DIR${RESET} already exists, is non-empty, and is not a git repository." >&2
            echo "    Refusing to delete existing files. Please specify a clean path via SUBTEXT_INSTALL_DIR or empty the directory manually." >&2
            exit 1
        fi
        rmdir "$INSTALL_DIR"
    fi

    echo "${BLUE}==>${RESET} Cloning repository..."
    mkdir -p "$(dirname "$INSTALL_DIR")"
    if ! git clone --depth 1 https://github.com/elevchuk-lab/subtext-engine.git "$INSTALL_DIR" >/dev/null 2>&1; then
        echo "${RED}[!] Error:${RESET} Failed to clone repository into ${YELLOW}$INSTALL_DIR${RESET}. Check your network connection and permissions." >&2
        exit 1
    fi
fi

echo ""
echo "${GREEN}✓ Successfully installed Subtext Engine v1.1.0!${RESET}"
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
