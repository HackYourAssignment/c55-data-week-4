#!/usr/bin/env bash
# Week 4 autograder — MessyCorp Pandas pipeline
# Static checks + behavioural functional tests.
# Runs from the .hyf/ directory; the project root is one level up.
set -euo pipefail

ROOT="$(cd .. && pwd)"
SCORE=0
PASS=false
PASSING_SCORE=60

add() { SCORE=$((SCORE + $1)); }

# Helper: grep code lines only (skip blank lines, comment-only lines, TODO/FIXME lines)
code_grep() {
  local pattern="$1"; shift
  grep -v '^\s*#' "$@" | grep -v 'TODO\|FIXME\|raise NotImplementedError' | grep -q "$pattern"
}

# ── Level 1 (10 pts): data exploration ───────────────────────────────────────
CLEAN="$ROOT/src/clean.py"
L1=0
code_grep "\.info()"        "$CLEAN" && L1=$((L1+1)) || true
code_grep "\.describe()"    "$CLEAN" && L1=$((L1+1)) || true
code_grep "\.isna()\.sum()" "$CLEAN" && L1=$((L1+1)) || true
code_grep "\.head("         "$CLEAN" && L1=$((L1+1)) || true
[ "$L1" -eq 4 ] && add 10

# ── Level 2 (14 pts): vectorized cleaning ────────────────────────────────────
# Trimmed: price/quantity filter greps and 2 pts from drop_duplicates moved to
# Level 9 (functional tests), because static greps cannot tell apart a real
# boolean filter from an unrelated reference to those columns.
code_grep "str\.strip"                      "$CLEAN" && add 2 || true
code_grep "str\.title"                      "$CLEAN" && add 1 || true
code_grep "str\.lower"                      "$CLEAN" && add 1 || true
code_grep "pd\.to_numeric"                  "$CLEAN" && add 3 || true
code_grep "pd\.to_datetime"                 "$CLEAN" && add 3 || true
code_grep "drop_duplicates"                 "$CLEAN" && \
  code_grep "transaction_id"               "$CLEAN" && \
  code_grep "keep.*=.*['\"]first['\"]"     "$CLEAN" && add 4 || true

# ── Level 3 (10 pts): customer join ──────────────────────────────────────────
# Trimmed: inner-join semantics and is_high_value behaviour moved to Level 9.
# Static checks here only verify that the relevant idioms appear in the file.
TRANSFORM="$ROOT/src/transform.py"
code_grep "str\.lower"                      "$TRANSFORM" && add 2 || true
code_grep "str\.strip"                      "$TRANSFORM" && add 2 || true
code_grep "how.*=.*['\"]inner['\"]"         "$TRANSFORM" && add 2 || true
code_grep "is_high_value"                   "$TRANSFORM" && \
  ! grep -q "iterrows\|for.*row\b"          "$TRANSFORM" && add 4 || true

# ── Level 4 (20 pts): named aggregations ─────────────────────────────────────
REPORT="$ROOT/src/report.py"
code_grep "total_revenue[[:space:]]*="      "$REPORT" && add 5 || true
code_grep "order_count[[:space:]]*="        "$REPORT" && add 5 || true
code_grep "isocalendar"                     "$REPORT" && \
  code_grep "\.week"                        "$REPORT" && add 5 || true
code_grep "customer_name.*first\|\"first\"" "$REPORT" && add 5 || true

# ── Level 5 (10 pts): file outputs ───────────────────────────────────────────
code_grep "weekly_revenue\.csv"             "$REPORT" && add 2 || true
code_grep "customer_summary\.parquet"       "$REPORT" && add 3 || true
code_grep "category_performance\.csv"       "$REPORT" && add 2 || true
code_grep "index=False"                     "$REPORT" && add 1 || true
code_grep "savefig"                         "$REPORT" && add 2 || true

# ── Level 6 (10 pts): Azure round-trip ───────────────────────────────────────
# Trimmed: the row-count assert check moved to Level 9. Functional tests now
# verify that all FILES are actually written under the data_dir argument.
INGEST="$ROOT/src/ingest.py"
code_grep "DefaultAzureCredential"          "$INGEST" && add 3 || true
code_grep "BlobServiceClient"               "$INGEST" && add 2 || true
grep -q "^data/" "$ROOT/.gitignore"                   && add 5 || true

# ── Level 7 (10 pts): code quality ───────────────────────────────────────────
grep -rq "Path(" "$ROOT/src/"                         && add 3 || true
grep -rq "logging\.\(info\|warning\|error\|debug\)" "$ROOT/src/" && add 3 || true
grep -q "def download_inputs"  "$INGEST"  && \
  grep -q "def upload_outputs" "$INGEST"  && \
  grep -q "def clean_sales"    "$CLEAN"   && \
  grep -q "def join_customers" "$TRANSFORM" && \
  grep -q "def build_reports"  "$REPORT"  && add 4 || true

# ── Level 8: AI_ASSIST.md (qualitative) ──────────────────────────────────────
AI_ASSIST_EXISTS=false
if [ -f "$ROOT/AI_ASSIST.md" ] && [ "$(wc -l < "$ROOT/AI_ASSIST.md")" -gt 5 ]; then
  AI_ASSIST_EXISTS=true
fi

# ── Level 9 (16 pts): behavioural correctness ────────────────────────────────
# 8 functional tests × 2 pts each. These import the student's code and run
# synthetic inputs through it to catch bugs static greps cannot detect:
# dropna() vs boolean filter, indentation bugs, hardcoded paths, etc.
L9=0
FUNCTIONAL_RESULT="not run"
if command -v python3 >/dev/null 2>&1 && [ -f "$ROOT/.hyf/functional_tests.py" ]; then
  # Install minimal deps quietly. Azure SDKs are required because
  # src/ingest.py imports them at module-load time.
  python3 -m pip install --quiet --disable-pip-version-check \
    pandas pytest azure-storage-blob azure-identity >/dev/null 2>&1 || true

  pytest_output=$(cd "$ROOT" && python3 -m pytest .hyf/functional_tests.py --no-header -q 2>&1 || true)
  passed=$(echo "$pytest_output" | grep -oE "[0-9]+ passed" | tail -1 | grep -oE "[0-9]+" || echo 0)
  failed=$(echo "$pytest_output" | grep -oE "[0-9]+ failed" | tail -1 | grep -oE "[0-9]+" || echo 0)
  errors=$(echo "$pytest_output" | grep -oE "[0-9]+ error" | tail -1 | grep -oE "[0-9]+" || echo 0)
  : "${passed:=0}"; : "${failed:=0}"; : "${errors:=0}"
  L9=$((passed * 2))
  if [ "$L9" -gt 16 ]; then L9=16; fi
  FUNCTIONAL_RESULT="${passed} passed, ${failed} failed, ${errors} errors"
fi
add "$L9"

# ── Result ───────────────────────────────────────────────────────────────────
[ "$SCORE" -ge "$PASSING_SCORE" ] && PASS=true || true

cat << EOF > score.json
{
  "score": $SCORE,
  "pass": $PASS,
  "passingScore": $PASSING_SCORE,
  "ai_assist_present": $AI_ASSIST_EXISTS,
  "functional_tests": "$FUNCTIONAL_RESULT"
}
EOF

# ── Human-readable summary (captured into test-output.txt by CI) ─────────────
PASS_ICON="❌"; [ "$PASS" = "true" ] && PASS_ICON="✅" || true
echo "Week 4 autograder — MessyCorp Pandas pipeline"
echo "=============================================="
echo ""
echo "Behavioural tests (L9): $L9 / 16  ($FUNCTIONAL_RESULT)"
echo "Static checks (L1-L7):  $((SCORE - L9)) / 84"
echo "AI_ASSIST.md present:   $AI_ASSIST_EXISTS"
echo ""
echo "Total: $SCORE / 100  $PASS_ICON  (passing score: $PASSING_SCORE)"
if [ -n "${pytest_output:-}" ] && [ "$L9" -lt 16 ]; then
  echo ""
  echo "Functional test output:"
  echo "$pytest_output"
fi
