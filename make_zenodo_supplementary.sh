#!/usr/bin/env bash
#
# make_zenodo_supplementary.sh — build the Zenodo supplementary archive.
#
# Bundles all git-tracked source from the current working tree (paper sources, the Lean 4
# formalization sources, the Python scripts, the notes, and the top-level
# docs). Build artifacts and regenerable data are excluded automatically
# because they are .gitignore'd:
#   lean/.lake/, **/*.olean, *.csv, *.txt,
#   scripts/spectral_program/*_branches.json, *_supplementary.zip,
#   collatz_supplementary_*/, __pycache__/, .venv/, ...
# The compiled PDF for the version (produced online) is appended if present.
#
# Usage:
#   bash make_zenodo_supplementary.sh          # version v5 (default)
#   bash make_zenodo_supplementary.sh v5
#
set -euo pipefail

VERSION="${1:-v5}"
cd "$(git rev-parse --show-toplevel)"

OUT="collatz_spectral_reduction_${VERSION}_supplementary.zip"
# The compiled PDF may be named with the version suffix or with the full title.
PDF=""
for cand in \
  "paper/collatz_spectral_reduction_${VERSION}.pdf" \
  "paper/A_Spectral_Reduction_of_the_Collatz_Conjecture_via_Phantom_Orbit_Shadowing.pdf"; do
  [ -f "$cand" ] && { PDF="$cand"; break; }
done

echo "==> Building ${OUT} from tracked working-tree content at HEAD base ($(git rev-parse --short HEAD))"
rm -f "$OUT"

# 1) All tracked files as they exist in the working tree. Gitignored
#    build/data files are NOT included.
git ls-files -z | xargs -0 zip -q -9 "$OUT"

# 2) Ensure the compiled PDF is in the archive. If it is tracked, the working
#    tree archive already included it; otherwise append it.
if [ -z "$PDF" ]; then
  echo "    ! No compiled PDF found in paper/."
  echo "      Compile the .tex, save the PDF under paper/, then re-run,"
  echo "      or upload the PDF to the Zenodo record separately."
elif unzip -l "$OUT" | grep -qF "$PDF"; then
  echo "    PDF already included via tracked content: $PDF"
else
  zip -q "$OUT" "$PDF"
  echo "    + added compiled PDF: $PDF"
fi

# 3) Report and sanity-check (no giant files should appear).
echo
echo "==> Archive: ${OUT}  ($(du -h "$OUT" | cut -f1))"
echo "    Tracked top-level content included:"
git ls-files | cut -d/ -f1 | sort -u | sed 's/^/      /'
echo "    Largest 5 files in the archive:"
unzip -l "$OUT" \
  | awk 'NF>=4 && $1 ~ /^[0-9]+$/ && $NF != "files" {print $1, $NF}' \
  | sort -rn | head -5 \
  | awk '{printf "      %8.1f KB  %s\n", $1/1024, $2}'
echo
echo "==> Done. Upload ${OUT} (plus the PDF) to Zenodo record 10.5281/zenodo.20554750."
