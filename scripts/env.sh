# Source me:  . scripts/env.sh
# Puts OSS CAD Suite + Quartus binaries on PATH and activates the project venv
# (venv last, so its python/cocotb win over anything else on PATH).
_repo="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"
[ -f "$_repo/scripts/tooling.env" ] && . "$_repo/scripts/tooling.env"
[ -n "${OSS_CAD_SUITE_DIR:-}" ] && PATH="$OSS_CAD_SUITE_DIR/bin:$PATH"
[ -n "${QUARTUS_BIN:-}" ] && PATH="$QUARTUS_BIN:$PATH"
export PATH
[ -f "$_repo/.venv/bin/activate" ] && . "$_repo/.venv/bin/activate"
unset _repo
