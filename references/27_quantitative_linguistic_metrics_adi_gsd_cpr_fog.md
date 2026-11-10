# 27. Quantitative Forensic Linguistic Metric Suite (ADI, GSD, CPR, MFR, FMRE, HIR, TAD & CSIS/CVS)

## 1. Executive Summary & Epistemological Foundation
To reduce subjective ambiguity and provide transparent, reproducible diagnostics for legal due diligence, arbitration review, and corporate governance audits, Subtext Engine deploys a formal mathematical metric suite. This suite operationalizes qualitative psycholinguistic and jurislinguistic constructs into deterministic numerical indices.

**Methodological Calibration Note:** These indices operate as **heuristic structural risk indicators** calibrated from published psycholinguistic, readability, and legal drafting literature (Pennebaker LIWC, Halliday SFL, Matsukovsky/Oborneva Flesch adaptation, Hohfeldian correlatives, and Garner's legal lexicography). Exceeding a forensic alert threshold signals elevated structural asymmetry, cognitive friction, or liability dilution requiring targeted human review and redlining—not standalone judicial proof of subjective intent (*mens rea*).

---

## 2. Mathematical Formulations & Index Architecture

```
                     QUANTITATIVE FORENSIC METRIC SUITE
┌───────────┬───────────────────────────────────┬────────────────────────────────────────┐
│  METRIC   │            FULL NAME              │          DIAGNOSTIC TARGET             │
├───────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ 1. ADI    │ Agent Deletion Index              │ Syntactic erasure of responsibility    │
├───────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ 2. GSD    │ Genitive Stacking Density         │ Bureaucratic cognitive load            │
├───────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ 3. CPR    │ Covert Prescriptivity Ratio       │ Asymmetric unilateral coercion         │
├───────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ 4. MFR    │ Modality-to-Facticity Ratio       │ Speculative promise vs anchored fact   │
├───────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ 5. FMRE   │ Flesch-Matsukovsky Reading Ease   │ Readability friction & legalese density│
├───────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ 6. HIR    │ Hohfeldian Integrity Ratio        │ Reciprocal duty backing declared rights│
├───────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ 7. TAD    │ Term-of-Art Ambiguity Density     │ Modal & lexical ambiguity loopholes    │
├───────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ 8. CSIS   │ Composite Structural Integrity    │ Bounded [0%–100%] structural clarity   │
│   (CVS)   │ Score (legacy alias: CVS)         │ & symmetry (not factual truth)         │
└───────────┴───────────────────────────────────┴────────────────────────────────────────┘
```

---

## 3. Metric Formulations & Unified Three-Zone Threshold Grids

### 1. Agent Deletion Index ($ADI$)
Measures the proportion of verbal predicates where explicit human or institutional agency is omitted through agentless passives, impersonal reflexives, or de-agentive nominalizations.

$$ADI = \frac{N_{\text{passive without agent}} + N_{\text{impersonal reflexives}} + N_{\text{de-agentive nominals}}}{N_{\text{total verbal predicates}}}$$

* **Clean Baseline:** $ADI \le 0.20$ (Direct attribution of obligations and actions)
* **Caution Zone (Standard Corporate Formalism):** $0.21 \le ADI \le 0.28$
* **Forensic Alert Threshold (High Evasion Risk):** $ADI > 0.28$ (Elevated syntactic displacement of responsible actors; Normalization Cap: $0.50$)

---

### 2. Genitive Stacking Density ($GSD$)
In synthetic languages (Russian, German, Slavic) and prepositional languages (English *"of"*, French/Spanish *"de"*), bureaucratic complexity is marked by cascading genitive/prepositional noun chains (*канцелярит*):
* *Example (Length 6):* *"Осуществление контроля за исполнением порядка обеспечения защиты интересов участников..."*
* *Example English (Length 5):* *"The implementation of the monitoring of the execution of the terms of the settlement..."*

$$GSD = \frac{N_{\text{noun phrases with genitive/prepositional chain length } \ge 3}}{N_{\text{total sentences}}}$$

* **Clean Baseline:** $GSD \le 0.25$
* **Caution Zone (Moderate Bureaucratic Load):** $0.26 \le GSD \le 0.35$
* **Forensic Alert Threshold (Cognitive Obfuscation Risk):** $GSD > 0.35$ (Elevated syntactic nesting that increases reader cognitive load; Normalization Cap: $0.50$)

---

### 3. Covert Prescriptivity Ratio ($CPR$)
Measures the ratio of disguised, informal demands and unilateral expectations to explicit, legally balanced bilateral rights and statutory covenants.

$$CPR = \frac{N_{\text{covert prescriptions}} + N_{\text{unilateral expectations}}}{N_{\text{explicit statutory covenants}} + N_{\text{bilateral rights}}}$$

* **Clean Baseline:** $CPR \le 0.30$
* **Caution Zone (Moderate Asymmetry):** $0.31 \le CPR \le 0.50$
* **Forensic Alert Threshold (Coercive Imbalance Risk):** $CPR > 0.50$ (Disproportionate unilateral obligations relative to reciprocal rights; Normalization Cap: $0.80$)

---

### 4. Modality-to-Facticity Ratio ($MFR$)
Measures the balance between verifiable, spatio-temporally anchored facts and epistemic modals or speculative future statements.

$$MFR = \frac{N_{\text{epistemic modals}} + N_{\text{future speculative statements}}}{N_{\text{verifiable historical facts}} + N_{\text{anchored figures}}}$$

* **Clean Baseline:** $MFR \le 0.50$
* **Caution Zone (Forward-Looking Commercial Prose):** $0.51 \le MFR \le 1.00$
* **Forensic Alert Threshold (Speculative Imbalance):** $MFR > 1.00$ (Predominance of unanchored projections over verifiable historical data)

---

### 5. Flesch-Matsukovsky Reading Ease ($FMRE$)
Adapted from Rudolf Flesch by G. Matsukovsky and I. Oborneva for complex polysyllabic and synthetic syntactic structures:

$$\text{FMRE} = 206.835 - 1.3 \times \left( \frac{\text{Words}}{\text{Sentences}} \right) - 60.1 \times \left( \frac{\text{Syllables}}{\text{Words}} \right)$$

* **Clean Baseline:** $\text{FMRE} \ge 50.0$ (Accessible commercial and legal prose)
* **Caution Zone (Dense Technical/Legal Prose):** $30.0 \le \text{FMRE} < 50.0$
* **Forensic Alert Threshold (Labyrinthine Complexity):** $\text{FMRE} < 30.0$ (Extreme syntactic density associated with reader signature fatigue)

```
                       FMRE INTERPRETATION SPECTRUM
┌───────────────┬─────────────────────────────────┬──────────────────────────────┐
│  FMRE SCORE   │       DIFFICULTY LEVEL          │    FORENSIC CLASSIFICATION   │
├───────────────┼─────────────────────────────────┼──────────────────────────────┤
│ >= 50.0       │ Standard to Plain Commercial    │ Clean Baseline (Accessible)  │
│ 30.0 – 49.9   │ Difficult (Complex Legal/Tech)  │ Caution Zone (High Density)  │
│ 0.0 – 29.9    │ Very Difficult (Labyrinthine)   │ Forensic Alert (Friction)    │
│ < 0.0         │ Extreme Polysyllabic Nesting    │ Severe Readability Hazard    │
└───────────────┴─────────────────────────────────┴──────────────────────────────┘
```

---

### 6. Hohfeldian Integrity Ratio ($HIR$)
Quantifies the proportion of declared contractual or statutory rights that are backed by an explicit, enforceable correlative duty and remedy (per Treatise 28).

$$HIR = \frac{N_{\text{Operative Rights with Reciprocal Legal Duties}}}{N_{\text{Total Declared Rights / Entitlements}}}$$

* **Clean Baseline:** $HIR \ge 0.80$
* **Caution Zone:** $0.60 \le HIR < 0.80$
* **Forensic Alert Threshold (Hohfeldian Void Risk):** $HIR < 0.60$ (High prevalence of unanchored privileges or illusory entitlements)

---

### 7. Term-of-Art Ambiguity Density ($TAD$)
Quantifies the density of ambiguous modal verbs (e.g., passive or polysemous *"shall"*), diluted efforts clauses (*"commercially reasonable efforts"* where hard covenants are expected), and unanchored legal terms of art per operative clause (per Treatise 40).

$$TAD = \frac{N_{\text{Ambiguous, Diluted, or Conflicted Legal Terms of Art}}}{N_{\text{Total Operative Clauses}}}$$

* **Clean Baseline:** $TAD \le 0.05$
* **Caution Zone:** $0.06 \le TAD \le 0.15$
* **Forensic Alert Threshold (High Ambiguity Risk):** $TAD > 0.15$ (Elevated concentration of interpretive loopholes; Normalization Cap: $0.30$)

---

## 4. Minimum Discourse Pre-Condition & Zero-Denominator Specification

To guarantee total mathematical determinism across edge cases (e.g., empty inputs, isolated headers, tables without finite verbs, or purely unilateral notices), let:

$$\text{clamp}(x, a, b) = \min(b, \max(a, x))$$

1. **Minimum Evaluatable Discourse Guard (Empty / Non-Predicate Input):**
   If $\text{Words} = 0$, $\text{Sentences} = 0$, or $N_{\text{total verbal predicates}} = 0$, **no numerical metric or composite score is computed**. All indices ($ADI, GSD, CPR, MFR, FMRE, HIR, TAD$) and the composite score ($CSIS / CVS$) MUST return **`N/A (INSUFFICIENT_DATA)`**. This prevents empty or non-clausal inputs from receiving an artificial numerical score.
2. **Bounded Proportion Metrics ($ADI, GSD, TAD$) on Valid Discourse ($\text{Words} > 0, \text{Sentences} > 0, N_{\text{total verbal predicates}} > 0$):**
   If $N_{\text{Total Operative Clauses}} = 0$ (e.g., non-contractual narrative prose), $TAD$ is defined as $0.00$ and its normalized penalty is $0.00$. If a numerator exceeds its denominator (e.g., multiple stacked genitive chains in a single sentence), the raw ratio is preserved for reporting and clamped at the Normalization Cap when computing $CSIS$.
3. **Cross-Category Ratios ($CPR, MFR$):**
   - If $\text{Denominator} = 0$ and $\text{Numerator} = 0$, the metric evaluates to $0.00$ (penalty $= 0.00$).
   - If $\text{Denominator} = 0$ and $\text{Numerator} > 0$ (e.g., covert prescriptions or speculative claims appear with zero bilateral rights or zero verifiable facts), the raw ratio is formally $\infty$ (reported in scorecards as $\text{MAX}$) and its normalized penalty term in $CSIS$ is fixed at $1.00$.
4. **Hohfeldian Integrity Ratio ($HIR$):**
   If $N_{\text{Total Declared Rights / Entitlements}} = 0$, $HIR$ is reported as `N/A` (or $0.00$ if evaluating a purported rights-granting instrument that declares zero rights).
5. **Flesch-Matsukovsky Reading Ease ($FMRE$):**
   Computed only when $\text{Words} > 0$, $\text{Sentences} > 0$, and $N_{\text{total verbal predicates}} > 0$. Because raw $\text{FMRE}$ can take negative values on heavily nested sentences or values $> 100$ on monosyllabic fragments, its normalized penalty $p_{\text{FMRE}} = \text{clamp}\left(\frac{50 - \text{FMRE}}{50}, 0, 1\right)$ is strictly bounded in $[0, 1]$.

---

## 5. Multi-Metric Composite Structural Integrity Score ($CSIS$, legacy alias: $CVS$)

**Terminological Note:** This composite index is named **Composite Structural Integrity Score ($CSIS$)** (retaining $CVS$ as a legacy alias for backward compatibility) to make explicit that the formula measures **structural transparency, syntactic agency attribution, readability, and contractual symmetry**—never the factual truth of underlying real-world claims.

For any valid discourse ($\text{Words} > 0, \text{Sentences} > 0, N_{\text{total verbal predicates}} > 0$), the five primary structural indices ($ADI, GSD, CPR, TAD, FMRE$) are synthesized into a single bounded score strictly within $[0\%, 100\%]$:

$$p_{\text{ADI}} = \text{clamp}\left(\frac{ADI}{0.50}, 0, 1\right), \quad p_{\text{GSD}} = \text{clamp}\left(\frac{GSD}{0.50}, 0, 1\right), \quad p_{\text{CPR}} = \text{clamp}\left(\frac{CPR}{0.80}, 0, 1\right)$$

$$p_{\text{TAD}} = \text{clamp}\left(\frac{TAD}{0.30}, 0, 1\right), \quad p_{\text{FMRE}} = \text{clamp}\left(\frac{50 - \text{FMRE}}{50}, 0, 1\right)$$

$$CSIS = \text{clamp}\left(100 \times \left[ 1.0 - \left( 0.20\,p_{\text{ADI}} + 0.20\,p_{\text{GSD}} + 0.20\,p_{\text{CPR}} + 0.20\,p_{\text{TAD}} + 0.20\,p_{\text{FMRE}} \right) \right], 0, 100\right)$$

* **Clean Baseline (High Structural Clarity & Symmetry):** $CSIS \ge 75\%$
* **Caution Zone (Moderate Structural Risk — Requires Redlining):** $50\% \le CSIS < 75\%$
* **Forensic Alert Threshold (High Structural Hazard):** $CSIS < 50\%$
