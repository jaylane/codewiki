#!/usr/bin/env bash
# codewiki manual installer.
# Usage:
#   ./install.sh --global              # install to ~/.claude/
#   ./install.sh --project /path/repo  # install to <repo>/.claude/

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET=""

usage() {
  cat <<EOF
codewiki installer

Usage:
  $0 --global
  $0 --project <path-to-project>

Then run \`pip install --user "$SCRIPT_DIR"\` once to install the Python helpers.
EOF
}

case "${1:-}" in
  --global)
    TARGET="$HOME/.claude"
    ;;
  --project)
    [[ -n "${2:-}" ]] || { usage; exit 2; }
    TARGET="$2/.claude"
    ;;
  -h|--help|"")
    usage
    exit 0
    ;;
  *)
    usage
    exit 2
    ;;
esac

mkdir -p "$TARGET/skills" "$TARGET/commands"

echo "Installing skill → $TARGET/skills/codewiki"
rm -rf "$TARGET/skills/codewiki"
cp -R "$SCRIPT_DIR/skills/codewiki" "$TARGET/skills/codewiki"

echo "Installing commands → $TARGET/commands/wiki"
rm -rf "$TARGET/commands/wiki"
cp -R "$SCRIPT_DIR/commands/wiki" "$TARGET/commands/wiki"

cat <<EOF

Installed to $TARGET.

Final step — install the Python helpers (one-time):

  pip install --user "$SCRIPT_DIR"

Then inside any git repo:

  /wiki:bootstrap
EOF
