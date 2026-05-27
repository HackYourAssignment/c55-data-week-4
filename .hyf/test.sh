#!/usr/bin/env bash
# Week 4 autograder — MessyCorp Pandas pipeline
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

# ── Level 2 (20 pts): vectorized cleaning ────────────────────────────────────
code_grep "str\.strip"                      "$CLEAN" && add 2 || true
code_grep "str\.title"                      "$CLEAN" && add 1 || true
code_grep "str\.lower"                      "$CLEAN" && add 1 || true
code_grep "pd\.to_numeric"                  "$CLEAN" && add 3 || true
code_grep "pd\.to_datetime"                 "$CLEAN" && add 3 || true
# Targeted boolean row-drops (price/quantity filters, not bare dropna)
code_grep "\[.*price\b"                     "$CLEAN" && add 2 || true
code_grep "\[.*quantity\b"                  "$CLEAN" && add 2 || true
# Deduplication on transaction_id with keep="first"
code_grep "drop_duplicates"                 "$CLEAN" && \
  code_grep "transaction_id"               "$CLEAN" && \
  code_grep "keep.*=.*['\"]first['\"]"     "$CLEAN" && add 6 || true

# ── Level 3 (15 pts): customer join ──────────────────────────────────────────
TRANSFORM="$ROOT/src/transform.py"
code_grep "str\.lower"                      "$TRANSFORM" && add 2 || true
code_grep "str\.strip"                      "$TRANSFORM" && add 2 || true
code_grep "how.*=.*['\"]inner['\"]"         "$TRANSFORM" && add 5 || true
# Vectorized is_high_value — boolean expression, no row-level loop
code_grep "is_high_value"                   "$TRANSFORM" && \
  ! grep -q "iterrows\|for.*row\b"          "$TRANSFORM" && add 6 || true

# ── Level 4 (20 pts): named aggregations ─────────────────────────────────────
REPORT="$ROOT/src/report.py"
# Named agg: keyword=("col", "func") style
code_grep "total_revenue[[:space:]]*="      "$REPORT" && add 5 || true
code_grep "order_count[[:space:]]*="        "$REPORT" && add 5 || true
code_grep "isocalendar"                     "$REPORT" && \
  code_grep "\.week"                        "$REPORT" && add 5 || true
# ("customer_name", "first") pattern
code_grep "customer_name.*first\|\"first\"" "$REPORT" && add 5 || true

# ── Level 5 (10 pts): file outputs ───────────────────────────────────────────
code_grep "weekly_revenue\.csv"             "$REPORT" && add 2 || true
code_grep "customer_summary\.parquet"       "$REPORT" && add 3 || true
code_grep "category_performance\.csv"       "$REPORT" && add 2 || true
# index=False on writes
code_grep "index=False"                     "$REPORT" && add 1 || true
code_grep "savefig"                         "$REPORT" && add 2 || true

# ── Level 6 (15 pts): Azure round-trip ───────────────────────────────────────
INGEST="$ROOT/src/ingest.py"
code_grep "DefaultAzureCredential"          "$INGEST" && add 3 || true
code_grep "BlobServiceClient"               "$INGEST" && add 2 || true
# data/ must be in .gitignore (exact path entry)
grep -q "^data/" "$ROOT/.gitignore"                   && add 5 || true
# Read-back assertion with row count comparison
code_grep "assert"                          "$INGEST" && \
  code_grep "len("                          "$INGEST" && add 5 || true

# ── Level 7 (10 pts): code quality ───────────────────────────────────────────
# pathlib.Path constructor used in src/ (not just type hints)
grep -rq "Path(" "$ROOT/src/"                         && add 3 || true
# logging.X() calls present, no bare print() calls
grep -rq "logging\.\(info\|warning\|error\|debug\)" "$ROOT/src/" && add 3 || true
! grep -rq "^[[:space:]]*print(" "$ROOT/src/"         && add 0 || true  # advisory only
# All five required function names present
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

# ── Result ────────────────────────────────────────────────────────────────────
[ "$SCORE" -ge "$PASSING_SCORE" ] && PASS=true || true

cat << EOF > score.json
{
  "score": $SCORE,
  "pass": $PASS,
  "passingScore": $PASSING_SCORE,
  "ai_assist_present": $AI_ASSIST_EXISTS
}
EOF
