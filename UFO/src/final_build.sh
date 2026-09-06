#!/usr/bin/env bash
set -euo pipefail

UFODIR="/nfs/104328877/temp/ufology"
OUTDIR="/nfs/104328877/outputs"
mkdir -p "$OUTDIR"

cd "$UFODIR"

# ── 1. WORD COUNT ──
echo "=== Step 1: Word count ==="
if [ ! -f main.pdf ]; then
  echo "No existing main.pdf; building one first for word count..."
  timeout 290 lualatex --interaction=nonstopmode main.tex || true
fi

# Extract English words via pdftotext
pdftotext main.pdf /tmp/ufo_text.txt 2>/dev/null
WC=$(grep -oP '\b[a-zA-Z]+\b' /tmp/ufo_text.txt | wc -l)
echo "Word count: $WC"

# ── 2. INJECT WORD COUNT ──
echo "=== Step 2: Inject word count into main.tex ==="
WC_COMMA=$(python3 -c "print('{:,}'.format($WC))")
sed -i "s/\\\\newcommand{\\\\totalwordcount}{XXXXXX}/\\\\newcommand{\\\\totalwordcount}{$WC}/" main.tex
sed -i "s/\\\\newcommand{\\\\fmtwordcount}{XXXXXX}/\\\\newcommand{\\\\fmtwordcount}{$WC_COMMA}/" main.tex
# Verify
grep -E 'totalwordcount|fmtwordcount' main.tex

# ── 3. BUILD PRINT PDF (3 passes) ──
echo "=== Step 3: Build Print PDF ==="
for i in 1 2 3; do
  echo "  Print pass $i/3"
  timeout 290 lualatex --interaction=nonstopmode main.tex || true
done

if [ ! -f main.pdf ]; then
  echo "FATAL: main.pdf not produced after print build"
  exit 1
fi

# ── 4. QUOTE GATE ──
echo "=== Step 4: Quote gate ==="
python3 quotes_check.py main.pdf
echo "Quote gate PASSED."

# ── 5. Ghostscript print PDF ──
echo "=== Step 5: Ghostscript print PDF ==="
PRINT_NAME="The Science of Ufology 1.0 - Evan Svendsen (KDP Print Interior)"
gs -dNOPAUSE -dBATCH -dQUIET \
   -sDEVICE=pdfwrite \
   -dPDFSETTINGS=/prepress \
   -dAutoRotatePages=/None \
   -sOutputFile="$UFODIR/print_final.pdf" \
   "$UFODIR/main.pdf"

mv "$UFODIR/print_final.pdf" "$OUTDIR/$PRINT_NAME.pdf"
echo "Print PDF saved: $OUTDIR/$PRINT_NAME.pdf"

# ── 6. BUILD DIGITAL PDF (3 passes) ──
echo "=== Step 6: Build Digital PDF ==="
for i in 1 2 3; do
  echo "  Digital pass $i/3"
  timeout 290 lualatex --interaction=nonstopmode digital.tex || true
done

if [ ! -f digital.pdf ]; then
  echo "FATAL: digital.pdf not produced after digital build"
  exit 1
fi

# ── 7. Quote gate for digital ──
echo "=== Step 7: Quote gate (digital) ==="
python3 quotes_check.py digital.pdf
echo "Quote gate PASSED (digital)."

# ── 8. Ghostscript digital PDF ──
echo "=== Step 8: Ghostscript digital PDF ==="
DIGI_NAME="The Science of Ufology 1.0 - Evan Svendsen (Digital, clickable links)"
gs -dNOPAUSE -dBATCH -dQUIET \
   -sDEVICE=pdfwrite \
   -dPDFSETTINGS=/prepress \
   -dAutoRotatePages=/None \
   -sOutputFile="$UFODIR/digital_final.pdf" \
   "$UFODIR/digital.pdf"

mv "$UFODIR/digital_final.pdf" "$OUTDIR/$DIGI_NAME.pdf"
echo "Digital PDF saved: $OUTDIR/$DIGI_NAME.pdf"

# ── 9. Restore placeholder ──
echo "=== Step 9: Restore placeholder ==="
sed -i "s/\\\\newcommand{\\\\totalwordcount}{$WC}/\\\\newcommand{\\\\totalwordcount}{XXXXXX}/" main.tex
sed -i "s/\\\\newcommand{\\\\fmtwordcount}{$WC_COMMA}/\\\\newcommand{\\\\fmtwordcount}{XXXXXX}/" main.tex

# ── DONE ──
echo ""
echo "======================================"
echo "BUILD COMPLETE"
echo "  Word count: $WC ($WC_COMMA)"
ls -lh "$OUTDIR/"*.pdf
echo "======================================"