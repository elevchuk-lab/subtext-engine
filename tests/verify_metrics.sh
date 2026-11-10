#!/bin/sh
# Subtext Engine Automated Verification & Regression Test Suite
# Compatible with POSIX sh (macOS, Linux, WSL)

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INSTALLER="$REPO_ROOT/install.sh"
CALC_CLI="$REPO_ROOT/bin/subtext_calc.py"
PY="${PYTHON:-python3}"
echo "==> Interpreter: $("$PY" --version 2>&1) ($PY)"

echo "==> [1/8] Checking POSIX shell syntax for install.sh and verify_metrics.sh..."
sh -n "$INSTALLER"
sh -n "$0"
chmod +x "$CALC_CLI"
echo "    PASS: POSIX sh syntax valid."

echo "==> [2/8] Testing install.sh data-loss prevention on non-empty non-git directory..."
TMP_NONEMPTY="$(mktemp -d "${TMPDIR:-/tmp}/subtext_test_nonempty.XXXXXX")"
echo "user_secret_data" > "$TMP_NONEMPTY/keep_me.txt"
if SUBTEXT_INSTALL_DIR="$TMP_NONEMPTY" "$INSTALLER" >/dev/null 2>&1; then
    echo "    FAIL: install.sh succeeded on non-empty non-git directory!" >&2
    rm -rf "$TMP_NONEMPTY"
    exit 1
fi
if [ ! -f "$TMP_NONEMPTY/keep_me.txt" ]; then
    echo "    FAIL: install.sh deleted user file in non-empty directory!" >&2
    rm -rf "$TMP_NONEMPTY"
    exit 1
fi
rm -rf "$TMP_NONEMPTY"
echo "    PASS: Non-empty directory preserved and installer aborted safely."

echo "==> [3/8] Testing install.sh protection against overwriting dirty git worktree..."
TMP_GIT="$(mktemp -d "${TMPDIR:-/tmp}/subtext_test_git.XXXXXX")"
(
    cd "$TMP_GIT"
    git init -q
    git config user.email "test@example.com"
    git config user.name "Test"
    echo "initial" > tracked.txt
    git add tracked.txt
    git commit -qm "init"
    echo "uncommitted_modification" >> tracked.txt
)
if SUBTEXT_INSTALL_DIR="$TMP_GIT" "$INSTALLER" >/dev/null 2>&1; then
    echo "    FAIL: install.sh overwrote dirty git repository without SUBTEXT_FORCE_UPDATE=1!" >&2
    rm -rf "$TMP_GIT"
    exit 1
fi
if ! grep -q "uncommitted_modification" "$TMP_GIT/tracked.txt"; then
    echo "    FAIL: uncommitted modification was lost!" >&2
    rm -rf "$TMP_GIT"
    exit 1
fi
rm -rf "$TMP_GIT"
echo "    PASS: Dirty git worktree preserved and installer aborted safely."

echo "==> [4/8] Testing deterministic CLI calculator (bin/subtext_calc.py) on raw EN/RU/ES/DE/KK/ZH texts..."
"$PY" - "$CALC_CLI" << 'PYCLIEOF'
import json
import subprocess
import sys

cli = sys.argv[1]

def run_cli(text):
    return json.loads(subprocess.check_output([sys.executable, cli, "--text", text]).decode("utf-8"))

# 1. Empty text via CLI must return INSUFFICIENT_DATA
res_empty = run_cli("   ")
assert res_empty["status"] == "INSUFFICIENT_DATA", res_empty
assert res_empty["metrics"]["CSIS"] == "N/A (INSUFFICIENT_DATA)", res_empty

# 2. Raw English SLA text via CLI must deterministically flag low CSIS & high TAD/ADI
sla_text = (
    "Vendor shall use commercially reasonable efforts to maintain 99.99% platform availability, "
    "provided that any scheduled or unscheduled downtime of the infrastructure of the data centers "
    "of third-party cloud providers shall be excluded from availability calculations. "
    "Customer is entitled to service continuity; however, adjustments to the calculation of the credits "
    "of the monthly subscription fee may be determined at Vendor's sole discretion."
)
res_sla_1 = run_cli(sla_text)
res_sla_2 = run_cli(sla_text)
assert res_sla_1 == res_sla_2, "CLI output must be 100% deterministic across runs"
assert res_sla_1["status"] == "OK"
assert res_sla_1["metrics"]["TAD"] > 0.15
assert res_sla_1["zones"]["CSIS"] in ("Alert", "Caution")

# 3. Markdown output check
md_out = subprocess.check_output([sys.executable, cli, "--text", sla_text, "--format", "markdown"]).decode("utf-8")
assert "CSIS (CVS)" in md_out and "bin/subtext_calc.py" in md_out
PYCLIEOF
echo "    PASS: bin/subtext_calc.py CLI deterministic tokenization and scoring verified."

echo "==> [5/8] Running regression tests for v1.1.0-v1.1.2 reviewer edge cases..."
"$PY" - "$REPO_ROOT" << 'PYREGEOF'
import os
import sys

sys.path.insert(0, os.path.join(sys.argv[1], "bin"))
from subtext_calc import analyze_raw_text

# Regression A1: First synonym set
synonym_contract_1 = (
    "Provider reserves the right to modify pricing at any time without notice and shall use good faith efforts "
    "to deliver services where feasible. Client waives all claims, relinquishes all statutory remedies, and "
    "Provider shall not be liable for any interruption under any circumstances."
)
res_syn1 = analyze_raw_text(synonym_contract_1)
assert res_syn1["status"] == "OK"
assert res_syn1["counts"]["covert_prescriptions"] >= 3
assert res_syn1["counts"]["ambiguous_terms"] >= 2
assert res_syn1["metrics"]["CSIS"] < 75.0

# Regression A2: Second synonym set ("cancel at any time at its absolute pleasure and owes nothing", "waives every remedy and bears all losses")
synonym_contract_2 = (
    "Vendor can cancel at any time at its absolute pleasure and owes nothing, "
    "while Customer waives every remedy and bears all losses."
)
res_syn2 = analyze_raw_text(synonym_contract_2)
assert res_syn2["status"] == "OK"
assert res_syn2["metrics"]["CPR"] == "MAX", f"Expected CPR=MAX on synonym set 2, got {res_syn2['metrics']['CPR']}"
assert res_syn2["zones"]["CSIS"] != "Clean", f"Synonym set 2 must NOT be Clean, got {res_syn2['zones']['CSIS']}"

# Regression B: Component Alert Veto Rule (single Alert in CPR vetoes overall Clean CSIS zone)
single_alert_text = "Provider can change the price whenever it wants and is not responsible for any damages."
res_veto = analyze_raw_text(single_alert_text)
assert res_veto["metrics"]["CPR"] == "MAX"
assert res_veto["zones"]["CPR"] == "Alert"
assert res_veto["zones"]["CSIS"].startswith("Caution (Veto:") or res_veto["zones"]["CSIS"].startswith("Alert"), (
    f"Component Alert Veto failed: {res_veto['zones']}"
)

# Regression C: Hamlet Guard (non-contractual literary prose must return LOW_DOMAIN_SIGNAL and Unverified CSIS)
hamlet_text = (
    "To be, or not to be, that is the question: whether tis nobler in the mind to suffer "
    "the slings and arrows of outrageous fortune, or to take arms against a sea of troubles."
)
res_hamlet = analyze_raw_text(hamlet_text)
assert res_hamlet["counts"]["domain_markers"] == 0, f"Expected 0 domain markers on Hamlet, got {res_hamlet['counts']}"
assert res_hamlet["domain_relevance"].startswith("LOW_DOMAIN_SIGNAL")
assert res_hamlet["zones"]["CSIS"] == "Unverified (Non-Contractual / General Prose)", (
    f"Hamlet must not be Clean, got {res_hamlet['zones']['CSIS']}"
)

# Regression D: Nortje collective pronoun calibration ("Wir haben die Zahlung geleistet" -> SDRI == 0.00)
de_factual_wir = "Wir haben die Zahlung von 500 EUR gemäß Vertrag fristgerecht geleistet."
res_wir = analyze_raw_text(de_factual_wir)
assert res_wir["metrics"]["SDRI"] == 0.0, f"Factual German 'Wir' must have SDRI == 0.0, got {res_wir['metrics']['SDRI']}"

# Regression E: Passive with explicit agent ('by the auditor' / 'советом директоров') must NOT trigger ADI alert
attributed_passive_en = (
    "The financial ledger was reviewed by the external auditor and the report was approved by the board."
)
res_pass_en = analyze_raw_text(attributed_passive_en)
assert res_pass_en["metrics"]["ADI"] == 0.0
assert res_pass_en["zones"]["ADI"] == "Clean"

attributed_passive_ru = (
    "Финансовый отчет был проверен аудитором, и решение было принято советом директоров."
)
res_pass_ru = analyze_raw_text(attributed_passive_ru)
assert res_pass_ru["metrics"]["ADI"] == 0.0

# Regression F: Deontic contractual 'may' ("Either party may terminate") must NOT count as speculative modal in MFR
deontic_may_text = (
    "Either party may terminate this Agreement upon 30 days written notice, and both parties may inspect the records."
)
res_may = analyze_raw_text(deontic_may_text)
assert res_may["counts"]["speculative_modals"] == 0
assert res_may["metrics"]["MFR"] == 0.0

# Regression G: Neutral 3rd-person text with zero 1st-person/collective pronouns must have SDRI == 0.00
neutral_3rd_person = (
    "The vendor delivers 100 units within 14 days and each party may terminate upon 30 days notice."
)
res_sdri = analyze_raw_text(neutral_3rd_person)
assert res_sdri["metrics"]["SDRI"] == 0.0

# Regression H: Spanish (ES), German (DE), Kazakh (KK), and Chinese (ZH) risk detection
spanish_contract = (
    "El proveedor hará esfuerzos comercialmente razonables para mantener el servicio, pero las tarifas "
    "se determinarán a su sola discreción en cualquier momento sin previo aviso. "
    "Se acordó excluir toda responsabilidad por interrupciones."
)
res_es = analyze_raw_text(spanish_contract)
assert res_es["status"] == "OK"
assert res_es["zones"]["CSIS"] != "Clean"

german_contract = (
    "Der Anbieter unternimmt wirtschaftlich angemessene Anstrengungen zur Bereitstellung der Plattform, "
    "jedoch wird die Gebühr nach eigenem Ermessen jederzeit ohne Vorankündigung festgelegt. "
    "Jegliche Haftung wird ausgeschlossen und der Kunde verzichtet auf alle Ansprüche."
)
res_de = analyze_raw_text(german_contract)
assert res_de["status"] == "OK"
assert res_de["zones"]["CSIS"] != "Clean"

# Regression I (v1.1.2): German/Kazakh/Chinese contractual vocabulary must be recognized as in-domain
for txt in (
    "Der Auftragnehmer kann die Vereinbarung jederzeit kündigen; Schadensersatzansprüche des Auftraggebers entfallen.",
    "Орындаушы келісімді кез келген уақытта бұза алады.",
    "供应商可随时解除协议。",
):
    r = analyze_raw_text(txt)
    assert r["domain_relevance"] == "DOMAIN_MATCHED", (txt, r["domain_relevance"], r["counts"])

# Regression J (v1.1.2): every raw-text result discloses pattern coverage
r = analyze_raw_text(spanish_contract)
assert "pattern_coverage" in r and r["pattern_coverage"]["patterns_triggered_total"] >= 1
assert "NOT visible" in r["pattern_coverage"]["note"]

# Regression K (v1.1.3): Mutual indemnification with "Each party" must not trigger covert_prescriptions or CPR Alert
mutual_indemnity_text = (
    "Each party shall indemnify the other party against third-party claims arising from its own breach, subject to the same cap."
)
r_indem = analyze_raw_text(mutual_indemnity_text)
assert r_indem["counts"]["covert_prescriptions"] == 0, f"Expected 0 covert prescriptions for mutual indemnity, got {r_indem['counts']}"
assert r_indem["metrics"]["CPR"] == 0.0, f"Expected CPR == 0.0, got {r_indem['metrics']['CPR']}"
assert r_indem["zones"]["CSIS"] == "Clean", f"Expected Clean CSIS, got {r_indem['zones']['CSIS']}"

# Regression L (v1.1.3): German separable verb liability exclusions ("schließt ... aus") and unilateral scope ("gilt nur für")
de_asym_test = (
    "Der Auftragnehmer schließt jegliche Schadensersatzansprüche aus. Die Kündigungsfrist gilt nur für den Auftraggeber."
)
r_de_asym = analyze_raw_text(de_asym_test)
assert r_de_asym["counts"]["covert_prescriptions"] >= 1, f"Expected covert prescriptions, got {r_de_asym['counts']}"
assert r_de_asym["zones"]["CPR"] == "Alert", f"Expected CPR Alert, got {r_de_asym['zones']['CPR']}"
assert r_de_asym["zones"]["CSIS"] != "Clean", f"Expected non-Clean CSIS, got {r_de_asym['zones']['CSIS']}"

# Regression M (v1.1.4): Mutuality bypass tests (unilateral indemnities with peripheral mutuality tokens must be flagged)
bypass_test_1 = "Customer shall indemnify Vendor against all claims, and each party shall bear its own costs."
r_b1 = analyze_raw_text(bypass_test_1)
assert r_b1["counts"]["covert_prescriptions"] >= 1, f"Bypass 1 failed: expected covert prescriptions, got {r_b1['counts']}"
assert r_b1["zones"]["CPR"] == "Alert", f"Bypass 1 failed: expected CPR Alert, got {r_b1['zones']['CPR']}"
assert r_b1["zones"]["CSIS"] != "Clean", f"Bypass 1 failed: expected non-Clean CSIS, got {r_b1['zones']['CSIS']}"

bypass_test_2 = "Customer shall indemnify the other party for all losses, while Vendor shall not be liable for any."
r_b2 = analyze_raw_text(bypass_test_2)
assert r_b2["counts"]["covert_prescriptions"] >= 1, f"Bypass 2 failed: expected covert prescriptions, got {r_b2['counts']}"
assert r_b2["zones"]["CPR"] == "Alert", f"Bypass 2 failed: expected CPR Alert, got {r_b2['zones']['CPR']}"
assert r_b2["zones"]["CSIS"] != "Clean", f"Bypass 2 failed: expected non-Clean CSIS, got {r_b2['zones']['CSIS']}"

# Regression N (v1.1.4): German unilateral liability waiver and asymmetric rights ("übernimmt keinerlei Haftung", "Nur X darf...")
de_keinerlei = "Der Auftragnehmer übernimmt keinerlei Haftung. Nur der Auftragnehmer darf den Vertrag beenden."
r_de_k = analyze_raw_text(de_keinerlei)
assert r_de_k["counts"]["covert_prescriptions"] >= 1, f"Expected covert prescriptions, got {r_de_k['counts']}"
assert r_de_k["zones"]["CPR"] == "Alert", f"Expected CPR Alert, got {r_de_k['zones']['CPR']}"
assert r_de_k["zones"]["CSIS"] != "Clean", f"Expected non-Clean CSIS, got {r_de_k['zones']['CSIS']}"

# Regression O (v1.1.4): Short text stability (1-2 sentences with high FMRE/GSD variance do not trigger false Veto alert)
ru_mutual_short = "Каждая сторона обязана возместить другой стороне любые убытки, возникшие вследствие неисполнения обязательств по настоящему договору."
r_ru_short = analyze_raw_text(ru_mutual_short)
assert r_ru_short["zones"]["CSIS"].startswith("Clean"), f"Expected Clean CSIS on short mutual RU text, got {r_ru_short['zones']['CSIS']}"
assert "Sample Too Short" in r_ru_short["zones"]["FMRE"], f"Expected short sample note in FMRE, got {r_ru_short['zones']['FMRE']}"

# Regression P (v1.1.5): Mutuality bypass via introductory/attributive subordinate clauses
intro_bypass_1 = "Each party agrees that Customer shall indemnify Vendor against all claims."
r_ib1 = analyze_raw_text(intro_bypass_1)
assert r_ib1["counts"]["covert_prescriptions"] >= 1, f"Expected covert prescription in intro bypass 1, got {r_ib1['counts']}"
assert r_ib1["zones"]["CPR"] == "Alert", f"Expected CPR Alert in intro bypass 1, got {r_ib1['zones']['CPR']}"
assert not r_ib1["zones"]["CSIS"].startswith("Clean"), f"Expected non-Clean CSIS in intro bypass 1, got {r_ib1['zones']['CSIS']}"

intro_bypass_2 = "Both parties acknowledge that the Customer shall indemnify and hold harmless the Vendor."
r_ib2 = analyze_raw_text(intro_bypass_2)
assert r_ib2["counts"]["covert_prescriptions"] >= 1, f"Expected covert prescription in intro bypass 2, got {r_ib2['counts']}"
assert r_ib2["zones"]["CPR"] == "Alert", f"Expected CPR Alert in intro bypass 2, got {r_ib2['zones']['CPR']}"
assert not r_ib2["zones"]["CSIS"].startswith("Clean"), f"Expected non-Clean CSIS in intro bypass 2, got {r_ib2['zones']['CSIS']}"

# Regression Q (v1.1.5): Active reflexive verbs in Russian must not trigger false ADI passive alert
ru_active_reflexive_text = "Стороны обязуются возместить друг другу убытки, возникшие по вине каждой из них."
r_ru_ar = analyze_raw_text(ru_active_reflexive_text)
assert r_ru_ar["counts"]["deleted_predicates"] == 0, f"Expected 0 deleted predicates for active reflexive, got {r_ru_ar['counts']}"
assert r_ru_ar["zones"]["ADI"] == "Clean", f"Expected Clean ADI, got {r_ru_ar['zones']['ADI']}"

# Regression R (v1.1.6): Mutual subject coreference ("agrees that it/they shall") & inclusive parentheticals
coref_mutual_1 = "Each party agrees that it shall indemnify the other party against third-party claims arising from its own breach."
r_cm1 = analyze_raw_text(coref_mutual_1)
assert r_cm1["counts"]["covert_prescriptions"] == 0, f"Expected 0 covert prescriptions for coref mutual 1, got {r_cm1['counts']}"
assert r_cm1["zones"]["CPR"] == "Clean", f"Expected Clean CPR, got {r_cm1['zones']['CPR']}"
assert r_cm1["zones"]["CSIS"].startswith("Clean"), f"Expected Clean CSIS, got {r_cm1['zones']['CSIS']}"

coref_mutual_2 = "Each party, including the Customer and the Vendor, shall indemnify the other party against third-party claims."
r_cm2 = analyze_raw_text(coref_mutual_2)
assert r_cm2["counts"]["covert_prescriptions"] == 0, f"Expected 0 covert prescriptions for parenthetical mutual, got {r_cm2['counts']}"
assert r_cm2["zones"]["CPR"] == "Clean", f"Expected Clean CPR, got {r_cm2['zones']['CPR']}"
assert r_cm2["zones"]["CSIS"].startswith("Clean"), f"Expected Clean CSIS, got {r_cm2['zones']['CSIS']}"

# Regression S (v1.1.6): Split 'hold X harmless' and Russian 'возместить X убытки'
split_hold_harmless = "Provider shall hold Client harmless from all losses."
r_shh = analyze_raw_text(split_hold_harmless)
assert r_shh["counts"]["covert_prescriptions"] >= 1, f"Expected covert prescription in split hold harmless, got {r_shh['counts']}"
assert r_shh["zones"]["CPR"] == "Alert", f"Expected CPR Alert, got {r_shh['zones']['CPR']}"

ru_direct_unilat = "Заказчик обязан возместить Исполнителю любые убытки."
r_rdu = analyze_raw_text(ru_direct_unilat)
assert r_rdu["counts"]["covert_prescriptions"] >= 1, f"Expected covert prescription in direct RU indemnity, got {r_rdu['counts']}"
assert r_rdu["zones"]["CPR"] == "Alert", f"Expected CPR Alert, got {r_rdu['zones']['CPR']}"

print("    PASS: All v1.1.0-v1.1.6 reviewer regression cases verified.")
PYREGEOF

echo "==> [6/8] Running deterministic mathematical & benchmark verification tests..."
"$PY" - "$REPO_ROOT" << 'PYEOF'
import math
import os
import sys

sys.path.insert(0, os.path.join(sys.argv[1], "bin"))
from subtext_calc import compute_scorecard

# 1. Empty / Non-predicate input guard test
empty_res = compute_scorecard(words=0, sentences=0, syllables=0, total_predicates=0)
assert empty_res["status"] == "INSUFFICIENT_DATA", f"Expected INSUFFICIENT_DATA, got {empty_res}"
assert empty_res["metrics"]["CSIS"] == "N/A (INSUFFICIENT_DATA)"

no_pred_res = compute_scorecard(words=10, sentences=1, syllables=15, total_predicates=0)
assert no_pred_res["status"] == "INSUFFICIENT_DATA"
assert no_pred_res["metrics"]["CSIS"] == "N/A (INSUFFICIENT_DATA)"

# 2. Benchmark Case 01 verification
c1 = compute_scorecard(
    words=143,
    sentences=4,
    syllables=269,
    total_predicates=10,
    deleted_predicates=6,
    chains_ge_3=3,
    covert_prescriptions=4,
    bilateral_rights=2,
    speculative_modals=2,
    anchored_facts=2,
    operative_rights_with_duty=0,
    total_declared_rights=2,
    ambiguous_terms=5,
    total_operative_clauses=4,
)["metrics"]
assert math.isclose(c1["ADI"], 0.60, abs_tol=1e-6)
assert math.isclose(c1["GSD"], 0.75, abs_tol=1e-6)
assert math.isclose(c1["CPR"], 2.00, abs_tol=1e-6)
assert math.isclose(c1["MFR"], 1.00, abs_tol=1e-6)
assert math.isclose(c1["FMRE"], 47.30, abs_tol=1e-2)
assert math.isclose(c1["HIR"], 0.00, abs_tol=1e-6)
assert math.isclose(c1["TAD"], 1.25, abs_tol=1e-6)
assert math.isclose(c1["CSIS"], 18.9, abs_tol=1e-6)

# 3. Benchmark Case 02 verification (including SDRI and zero-denominator MFR)
c2 = compute_scorecard(
    words=58,
    sentences=3,
    syllables=118,
    total_predicates=8,
    deleted_predicates=2,
    speculative_modals=5,
    anchored_facts=0,
    n_epe=4,
    n_1st_sg=0,
    n_coll=2,
    n_weak=3,
    n_strong=1,
    n_gen=2,
)["metrics"]
assert math.isclose(c2["ADI"], 2.0 / 8.0, abs_tol=1e-6)
assert c2["MFR"] == "MAX"
assert math.isclose(c2["SDRI"], 0.94, abs_tol=1e-6), f"Expected 0.94, got {c2['SDRI']}"

# 4. Benchmark Case 03 verification (6 predicates in Sample 3A and Sample 3B)
c3a = compute_scorecard(words=44, sentences=3, syllables=66, total_predicates=6, deleted_predicates=3)["metrics"]
c3b = compute_scorecard(words=52, sentences=3, syllables=77, total_predicates=6, deleted_predicates=0)["metrics"]
assert math.isclose(c3a["ADI"], 0.50, abs_tol=1e-6), f"Expected 0.50, got {c3a['ADI']}"
assert math.isclose(c3b["ADI"], 0.00, abs_tol=1e-6), f"Expected 0.00, got {c3b['ADI']}"

# 5. Extreme Clamping Verification (FMRE < 0 and FMRE > 50)
extreme_low = compute_scorecard(
    words=100,
    sentences=1,
    syllables=300,
    total_predicates=10,
    deleted_predicates=9,
    chains_ge_3=5,
    covert_prescriptions=5,
    bilateral_rights=1,
    ambiguous_terms=5,
    total_operative_clauses=2,
)["metrics"]
assert extreme_low["FMRE"] < 0.0
assert math.isclose(extreme_low["CSIS"], 0.0, abs_tol=1e-6)

extreme_high = compute_scorecard(
    words=10,
    sentences=2,
    syllables=10,
    total_predicates=2,
    deleted_predicates=0,
    chains_ge_3=0,
    covert_prescriptions=0,
    bilateral_rights=2,
    ambiguous_terms=0,
    total_operative_clauses=2,
)["metrics"]
assert extreme_high["FMRE"] > 50.0
assert math.isclose(extreme_high["CSIS"], 100.0, abs_tol=1e-6)

print("    PASS: All mathematical, boundary, and benchmark assertions verified.")
PYEOF

echo "==> [7/8] Evaluating in-sample regression corpus (benchmarks/regression_corpus.json; NOT a validation)..."
"$PY" - "$REPO_ROOT" << 'PYCORPUSEOF'
import json
import os
import sys

repo_root = sys.argv[1]
sys.path.insert(0, os.path.join(repo_root, "bin"))
from subtext_calc import analyze_raw_text

corpus_path = os.path.join(repo_root, "benchmarks", "regression_corpus.json")
with open(corpus_path, "r", encoding="utf-8") as f:
    corpus = json.load(f)

cases = corpus["cases"]
assert len(cases) >= 12, f"Expected >= 12 validation cases, got {len(cases)}"

passed = 0
for case in cases:
    cid = case["id"]
    res = analyze_raw_text(case["text"])
    assert res["status"] == case["expected_status"], f"[{cid}] status mismatch: {res['status']}"
    assert res["domain_relevance"].startswith(case["expected_domain_relevance"]), (
        f"[{cid}] domain_relevance mismatch: {res['domain_relevance']} vs {case['expected_domain_relevance']}"
    )
    if "expected_csis_zone" in case:
        assert res["zones"]["CSIS"] == case["expected_csis_zone"], (
            f"[{cid}] expected CSIS zone {case['expected_csis_zone']}, got {res['zones']['CSIS']}"
        )
    if "expected_non_clean_csis" in case:
        is_non_clean = res["zones"]["CSIS"] != "Clean"
        assert is_non_clean == case["expected_non_clean_csis"], (
            f"[{cid}] expected_non_clean_csis={case['expected_non_clean_csis']}, got zone={res['zones']['CSIS']} (metrics={res['metrics']})"
        )
    if "expected_cpr_alert" in case:
        is_cpr_alert = res["zones"]["CPR"] == "Alert"
        assert is_cpr_alert == case["expected_cpr_alert"], (
            f"[{cid}] expected_cpr_alert={case['expected_cpr_alert']}, got CPR={res['metrics']['CPR']} ({res['zones']['CPR']})"
        )
    if "expected_max_sdri" in case:
        assert res["metrics"]["SDRI"] <= case["expected_max_sdri"], (
            f"[{cid}] SDRI {res['metrics']['SDRI']} exceeded {case['expected_max_sdri']}"
        )
    passed += 1

# Confusion matrix on the binary label "one-sided (expected_non_clean_csis=True)" vs "balanced".
# Computed both for ANY non-clean zone and specifically for the target signal (CPR Alert).
# Clean variants like "Clean (Low Sample / Preliminary)" represent Clean classifications.
tp_any = fp_any = tn_any = fn_any = 0
tp_cpr = fp_cpr = tn_cpr = fn_cpr = 0
for case in cases:
    if "expected_non_clean_csis" not in case:
        continue
    r = analyze_raw_text(case["text"])
    flagged_any = not r["zones"]["CSIS"].startswith("Clean")
    flagged_cpr = r["zones"]["CPR"] == "Alert"
    positive = case["expected_non_clean_csis"]
    
    tp_any += positive and flagged_any
    fn_any += positive and not flagged_any
    fp_any += (not positive) and flagged_any
    tn_any += (not positive) and not flagged_any
    
    tp_cpr += positive and flagged_cpr
    fn_cpr += positive and not flagged_cpr
    fp_cpr += (not positive) and flagged_cpr
    tn_cpr += (not positive) and not flagged_cpr

recall_any = tp_any / (tp_any + fn_any) if (tp_any + fn_any) else float("nan")
precision_any = tp_any / (tp_any + fp_any) if (tp_any + fp_any) else float("nan")
fpr_any = fp_any / (fp_any + tn_any) if (fp_any + tn_any) else float("nan")

recall_cpr = tp_cpr / (tp_cpr + fn_cpr) if (tp_cpr + fn_cpr) else float("nan")
precision_cpr = tp_cpr / (tp_cpr + fp_cpr) if (tp_cpr + fp_cpr) else float("nan")
fpr_cpr = fp_cpr / (fp_cpr + tn_cpr) if (fp_cpr + tn_cpr) else float("nan")

print(f"    PASS: {passed}/{len(cases)} regression cases match expected labels.")
print(f"    In-sample (Any non-Clean): TP={tp_any} FN={fn_any} FP={fp_any} TN={tn_any} | recall={recall_any:.2f} precision={precision_any:.2f} FPR={fpr_any:.2f}")
print(f"    In-sample (Target CPR Alert): TP={tp_cpr} FN={fn_cpr} FP={fp_cpr} TN={tn_cpr} | recall={recall_cpr:.2f} precision={precision_cpr:.2f} FPR={fpr_cpr:.2f}")
print("    NOTE: in-sample regression figures (cases written after failures were seen); they do NOT estimate generalization.")
PYCORPUSEOF

echo "==> [8/8] Reporting known-gaps baseline on external probe (benchmarks/holdout_probe.json; report-only, never tuned)..."
"$PY" - "$REPO_ROOT" << 'PYPROBEEOF'
import json
import os
import sys

repo_root = sys.argv[1]
sys.path.insert(0, os.path.join(repo_root, "bin"))
from subtext_calc import analyze_raw_text

with open(os.path.join(repo_root, "benchmarks", "holdout_probe.json"), "r", encoding="utf-8") as f:
    cases = json.load(f)["cases"]
assert len(cases) == 12, f"holdout_probe.json must stay unchanged (12 cases), got {len(cases)}"

tp_any = tp_cpr = fn_any = fp = tn = 0
misses = []
for c in cases:
    r = analyze_raw_text(c["text"])
    assert r["status"] == "OK", (c["id"], r["status"])  # only hard requirement: the scanner must run
    flagged = not r["zones"]["CSIS"].startswith("Clean")
    cpr_alert = r["zones"]["CPR"] == "Alert"
    if c["expected_non_clean_csis"]:
        if flagged:
            tp_any += 1
        else:
            fn_any += 1
            misses.append(c["id"])
        tp_cpr += cpr_alert
    else:
        fp += flagged
        tn += not flagged

pos = tp_any + fn_any
neg = fp + tn
print(f"    Asymmetric flagged for ANY reason: {tp_any}/{pos} (recall {tp_any/pos:.2f})")
print(f"    Asymmetric flagged for the RIGHT reason (CPR Alert): {tp_cpr}/{pos} (recall {tp_cpr/pos:.2f})")
print(f"    Balanced false positives: {fp}/{neg} (FPR {fp/neg:.2f})")
print(f"    Missed asymmetric clauses: {', '.join(misses) if misses else 'none'}")
print("    NOTE: report-only known-gaps baseline written by an external LLM reviewer (not lawyer-labeled).")
print("          Misses do NOT fail the suite and these texts must NOT be used to tune patterns.")
PYPROBEEOF

echo "==> All automated verification checks passed!"
