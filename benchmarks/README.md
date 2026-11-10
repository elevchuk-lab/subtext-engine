# Subtext Engine: Heuristic Calibration Methodology & Reproducible Worked Benchmarks

This directory documents the **calibration methodology**, **epistemological boundaries**, and **reproducible step-by-step worked benchmarks** for the Subtext Engine quantitative metric suite (`ADI`, `GSD`, `CPR`, `MFR`, `FMRE`, `HIR`, `TAD`, `SDRI`, and `CSIS` / legacy `CVS`).

---

## 1. Calibration Methodology & Epistemological Scope

### 1.1 Author-Defined Heuristic Operationalizations vs. Source Literature
With the exception of Flesch–Matsukovsky Reading Ease ($FMRE$), the indices in Subtext Engine (`ADI`, `GSD`, `CPR`, `MFR`, `HIR`, `TAD`, `SDRI`, `CSIS`) and their three-zone cutoffs (`Clean` | `Caution` | `Alert`) are **author-defined composite screening heuristics** constructed for this repository. They operationalize qualitative concepts from published research into reproducible mathematical formulas (executed deterministically via `bin/subtext_calc.py`), but the specific numerical thresholds do not appear as universal constants in external literature and have not been clinically validated as standalone diagnostic tests:

| Metric | Clean Baseline | Caution Zone | Forensic Alert | Literature Basis & Calibration Rationale |
| :--- | :---: | :---: | :---: | :--- |
| **ADI** *(Agent Deletion Index)* | $\le 0.20$ | $0.21\text{--}0.28$ | $> 0.28$ | Derived from Halliday (1994) SFL transitivity distributions and Fairclough (1995) CDA analyses of institutional prose, where passive/impersonal verb rates above $\sim 28\%$ shift discourse from accountable action to bureaucratic agent deletion. |
| **GSD** *(Genitive Stacking Density)* | $\le 0.25$ | $0.26\text{--}0.35$ | $> 0.35$ | Derived from Russian and Continental jurislinguistic studies of *канцелярит* (Brinev, 2009; Sternin & Baranov, Treatises 21–22), measuring sentences burdened by $\ge 3$ consecutive genitive/prepositional dependencies. |
| **CPR** *(Covert Prescriptivity Ratio)* | $\le 0.30$ | $0.31\text{--}0.50$ | $> 0.50$ | Operationalizes commercial legilinguistic asymmetry (Treatise 37) by comparing unilateral expectations and covert demands against explicit bilateral rights. |
| **MFR** *(Modality-to-Facticity Ratio)* | $\le 0.50$ | $0.51\text{--}1.00$ | $> 1.00$ | Grounded in Reality Monitoring (Johnson & Raye, 1981; Sporer, 2004, Treatise 08) and Loughran & McDonald (2011, Treatise 34) weak-modal frequency ratios. When speculative modals exceed anchored facts ($> 1.00$), narrative claims lack empirical anchoring. |
| **FMRE** *(Flesch-Matsukovsky Reading Ease)* | $\ge 50.0$ | $30.0\text{--}49.9$ | $< 30.0$ | Directly applies the Flesch Reading Ease scale as adapted by Matsukovsky (1976) and Oborneva (2006) ($206.835 - 1.3\,\text{ASL} - 60.1\,\text{ASW}$), where scores below $30.0$ correspond to graduate/legalese complexity that induces reader cognitive fatigue. |
| **HIR** *(Hohfeldian Integrity Ratio)* | $\ge 0.80$ | $0.60\text{--}0.79$ | $< 0.60$ | Operationalizes Wesley Newcomb Hohfeld's (1913, Treatise 28) jural correlatives: measures the fraction of declared entitlements backed by an enforceable reciprocal duty and remedy. |
| **TAD** *(Term-of-Art Ambiguity Density)* | $\le 0.05$ | $0.06\text{--}0.15$ | $> 0.15$ | Operationalizes Bryan A. Garner's *Black's Law Dictionary* (Treatise 40) taxonomy of polysemous *"shall"* usages, diluted efforts standards (*"commercially reasonable efforts"*), and incomplete indemnity triplets per operative clause. |
| **SDRI** *(Stanford Disclosure Risk Index, legacy: SDPS)* | $\le 0.35$ | $0.36\text{--}0.65$ | $> 0.65$ | Deterministic heuristic index operationalizing Larcker & Zakolyukina (2012) and Loughran & McDonald (2011) (Treatise 34): linear combination of bounded densities for Extreme Positive Emotion ($0.35$), 1st-Person Singular Suppression ($0.25$), Weak Modals ($0.25$), and Generalized Knowledge Hedges ($0.15$). |
| **CSIS** *(Composite Structural Integrity Score, legacy: CVS)* | $\ge 75\%$ | $50\%\text{--}74.9\%$ | $< 50\%$ | Bounded $[0\%, 100\%]$ linear aggregation of clamped structural penalty terms across $ADI, GSD, CPR, TAD,$ and $FMRE$ (equal weights of $0.20$). Evaluates structural clarity and symmetry, not factual truth. |

### 1.2 Epistemological Scope & Non-Equivalence to Factual Truth or *Mens Rea*
1. **Structural Clarity vs. Factual Truth:** The composite index is explicitly named **Composite Structural Integrity Score (`CSIS`, legacy alias: `CVS`)** because it evaluates **syntactic transparency, explicit agency attribution, readability, and contractual symmetry**. A factually false statement written in simple, active prose will score high on `CSIS` (structural clarity) and must be evaluated via **Mode C Statement Analysis / Reality Monitoring (`MFR`, `LDI`, CBCA)** and extrinsic evidence. Conversely, a low `CSIS` demonstrates structural obfuscation or contractual asymmetry, not standalone proof of subjective *mens rea*.
2. **Mandatory Human-in-the-Loop Verification:** Every Subtext Engine audit pairs numerical indices with a verbatim **Micro-Linguistic Evidence Log** and **Calibrated Questions (SUE / Voss Protocol)** so legal counsel or investigators can test whether an observed structural flaw is inadvertent boilerplate or strategic evasion.

---

## 2. Reproducible Worked Benchmarks

Each benchmark below provides the exact input text, explicit constituent counts, and step-by-step arithmetic verification using the canonical formulas in [`SKILL.md`](../SKILL.md), [`references/27_quantitative_linguistic_metrics_adi_gsd_cpr_fog.md`](../references/27_quantitative_linguistic_metrics_adi_gsd_cpr_fog.md), and [`references/34_forensic_financial_linguistics_earnings_calls_stanford.md`](../references/34_forensic_financial_linguistics_earnings_calls_stanford.md).

*(Note: All calculations below are automatically verified by [`tests/verify_metrics.sh`](../tests/verify_metrics.sh)).*

---

### Benchmark Case 01: Asymmetric Commercial SaaS SLA & Indemnification Clause (MODE A)

#### A. Unedited Input Text (4 Operative Clauses / 4 Sentences)
> **Clause 1:** *"Vendor shall use commercially reasonable efforts to maintain 99.99% platform availability, provided that any scheduled or unscheduled downtime of the infrastructure of the data centers of third-party cloud providers shall be excluded from availability calculations."*  
> **Clause 2:** *"Customer is entitled to service continuity; however, adjustments to the calculation of the credits of the monthly subscription fee may be determined at Vendor's sole discretion."*  
> **Clause 3:** *"Customer shall indemnify and hold harmless Vendor against any claims arising from platform use, and all obligations of the Customer under the provisions of the schedules of this Agreement must be performed strictly on time, as time is of the essence."*  
> **Clause 4:** *"In the event of any service interruption, a credit capped at 2% of the monthly fee shall constitute Customer's sole and exclusive remedy, and all other statutory or common-law liabilities are hereby waived."*

#### B. Step-by-Step Constituent Counts
* **Sentences ($N_{\text{total sentences}}$):** $4$
* **Operative Clauses ($N_{\text{Total Operative Clauses}}$):** $4$
* **Words & Syllables:** $\text{Words} = 143$, $\text{Syllables} = 269$
  * $\text{ASL} = \frac{143}{4} = 35.75$, $\text{ASW} = \frac{269}{143} \approx 1.881119$
* **Verbal Predicates ($N_{\text{total verbal predicates}} = 10$):**
  * Active with explicit agent ($4$): *"Vendor shall use"*, *"Customer is entitled"*, *"Customer shall indemnify and hold harmless"*, *"credit ... shall constitute"*.
  * Passive without agent / de-agentive ($6$): *"shall be excluded"*, *"may be determined"*, *"arising from platform use"* (nominalized), *"must be performed"*, *"service interruption"* (nominalized), *"are hereby waived"*.
* **Genitive/Prepositional Chains of Length $\ge 3$ ($N_{\text{chains } \ge 3} = 3$):**
  1. *"downtime **of** the infrastructure **of** the data centers **of** third-party cloud providers"* (Clause 1, length 3)
  2. *"adjustments **to** the calculation **of** the credits **of** the monthly subscription fee"* (Clause 2, length 3)
  3. *"obligations **of** the Customer **under** the provisions **of** the schedules **of** this Agreement"* (Clause 3, length 4)
* **Prescriptions vs. Bilateral Rights ($CPR$ components):**
  * Covert prescriptions / unilateral impositions ($N_{\text{covert/unilateral}} = 4$): unilateral downtime exclusion (Clause 1), unilateral discretion over credit calculation (Clause 2), one-way Customer-only indemnity with *"time is of the essence"* (Clause 3), complete waiver of statutory liabilities (Clause 4).
  * Explicit statutory covenants / enforceable bilateral rights ($N_{\text{bilateral}} = 2$): Customer's capped $2\%$ credit covenant (Clause 4) and Customer's indemnification covenant to Vendor (Clause 3).
* **Modality vs. Facticity ($MFR$ components):**
  * Epistemic/discretionary modals ($N_{\text{modals}} = 2$): *"commercially reasonable efforts"*, *"may be determined"*.
  * Anchored figures/facts ($N_{\text{facts}} = 2$): *"99.99%"*, *"2%"*.
* **Declared Rights vs. Reciprocal Duties ($HIR$ components):**
  * Total declared Customer entitlements ($N_{\text{Total Declared Rights}} = 2$): (1) *"99.99% platform availability"* (Clause 1), (2) *"entitled to service continuity"* (Clause 2).
  * Operative rights with enforceable reciprocal duty ($N_{\text{Operative}} = 0$): Clause 1 excludes all unscheduled third-party downtime and dilutes duty to *"commercially reasonable efforts"*; Clause 2 subjects credits to *"Vendor's sole discretion"*; Clause 4 caps total recovery at $2\%$.
* **Ambiguous / Diluted Terms of Art ($TAD$ components, $N = 5$ across $4$ clauses):**
  1. *"shall use commercially reasonable efforts"* (efforts dilution + polysemous *shall*, Clause 1)
  2. *"shall be excluded"* (passive *shall*, Clause 1)
  3. *"may be determined at Vendor's sole discretion"* (illusory promise, Clause 2)
  4. *"indemnify and hold harmless"* (omits active duty to *defend* while asymmetric against Customer, Clause 3)
  5. *"sole and exclusive remedy"* severing statutory/common-law remedies (Clause 4)

#### C. Deterministic Metric & CSIS (CVS) Calculation
1. $ADI = \frac{6}{10} = \mathbf{0.60}$ *(Alert: $> 0.28$)*. Normalized penalty: $p_{\text{ADI}} = \text{clamp}\left(\frac{0.60}{0.50}, 0, 1\right) = \mathbf{1.00}$.
2. $GSD = \frac{3}{4} = \mathbf{0.75}$ *(Alert: $> 0.35$)*. Normalized penalty: $p_{\text{GSD}} = \text{clamp}\left(\frac{0.75}{0.50}, 0, 1\right) = \mathbf{1.00}$.
3. $CPR = \frac{4}{2} = \mathbf{2.00}$ *(Alert: $> 0.50$)*. Normalized penalty: $p_{\text{CPR}} = \text{clamp}\left(\frac{2.00}{0.80}, 0, 1\right) = \mathbf{1.00}$.
4. $MFR = \frac{2}{2} = \mathbf{1.00}$ *(Caution upper boundary: $0.51\text{--}1.00$)*.
5. $\text{FMRE} = 206.835 - 1.3(35.75) - 60.1(1.881119) = 206.835 - 46.475 - 113.055 = \mathbf{47.3}$ *(Caution: $30.0\text{--}49.9$)*. Normalized penalty: $p_{\text{FMRE}} = \text{clamp}\left(\frac{50 - 47.305}{50}, 0, 1\right) \approx \mathbf{0.0539}$.
6. $HIR = \frac{0}{2} = \mathbf{0.00}$ *(Alert: $< 0.60$ — complete Hohfeldian Void)*.
7. $TAD = \frac{5}{4} = \mathbf{1.25}$ *(Alert: $> 0.15$)*. Normalized penalty: $p_{\text{TAD}} = \text{clamp}\left(\frac{1.25}{0.30}, 0, 1\right) = \mathbf{1.00}$.
8. **Composite Structural Integrity Score ($CSIS$, legacy alias: $CVS$):**
   $$CSIS = \text{clamp}\left(100 \times \left[1.0 - \left(0.20(1.00) + 0.20(1.00) + 0.20(1.00) + 0.20(1.00) + 0.20(0.0539)\right)\right], 0, 100\right)$$
   $$CSIS = 100 \times (1.0 - 0.81078) = \mathbf{18.9\%} \quad (\text{Forensic Alert: } < 50\%)$$

---

### Benchmark Case 02: Distressed Corporate Earnings Call Excerpt (MODE B)

#### A. Ground-Truth Context & Input Text
* **Source:** Publicly documented executive commentary style from pre-insolvency quarterly earnings calls (modeled on verified SEC enforcement records, e.g., *SEC v. Kenneth L. Lay, Jeffrey K. Skilling*, Litigation Release No. 18776, and Larcker & Zakolyukina 2012 corpus, Treatise 34).
* **Excerpt (3 Sentences):**
  > *"Our wholesale services and broadband divisions are experiencing unprecedented, truly phenomenal momentum that will fundamentally transform global energy markets. Certain transitional accounting adjustments were implemented during the quarter to optimize balance-sheet flexibility, and any short-term cash flow fluctuations should normalize rapidly. We believe the underlying franchise value has never been stronger, and investors can expect extraordinary long-term returns."*

#### B. Step-by-Step Constituent Counts & Calculation
* **Sentences:** $3$ | **Words:** $58$ | **Syllables:** $118$ ($\text{ASL} = 19.33$, $\text{ASW} \approx 2.03$)
* **Verbal Predicates ($N = 8$):**
  * Active predicates ($7$): *"are experiencing"*, *"will [fundamentally] transform"*, *"to optimize"*, *"should normalize"*, *"believe"*, *"has never been stronger"*, and *"can expect"*.
  * Passive verbal predicate ($1$): *"were implemented"* (deletes who authorized the accounting adjustments).
  * The de-agentive nominalization *"accounting adjustments"* adds one event to the ADI numerator but is not counted as a verbal predicate in the denominator.
  * $ADI = \frac{2}{8} = \mathbf{0.25}$ *(Caution: $0.21\text{--}0.28$)*.
* **Modality-to-Facticity Ratio ($MFR$):**
  * Epistemic modals, extreme positive hyperbole & speculative future claims ($N_{\text{speculative}} = 5$): *"unprecedented, truly phenomenal momentum"*, *"will fundamentally transform"*, *"should normalize rapidly"*, *"We believe ... never been stronger"*, *"can expect extraordinary long-term returns"*.
  * Spatio-temporally anchored historical financial figures ($N_{\text{facts}} = 0$): zero specific revenue, EBITDA, or cash-flow numbers cited.
  * **Zero-Denominator Rule Application:** Because $N_{\text{facts}} = 0$ and $N_{\text{speculative}} = 5 > 0$, $MFR = \mathbf{\text{MAX } (\infty)}$ *(Alert: $> 1.00$)*.
* **Reproducible Stanford Disclosure Risk Index ($SDRI$, Treatise 34):**
  * $N_{\text{EPE}} = 4$ (*unprecedented, phenomenal, never been stronger, extraordinary*) in $\text{Words} = 58 \implies \frac{100 \times 4 / 58}{5.0} = \frac{6.8966}{5.0} = 1.3793 \implies d_{\text{EPE}} = \text{clamp}(1.3793, 0, 1) = \mathbf{1.00}$.
  * $N_{\text{1stSg}} = 0$ (*"I"*), $N_{\text{Coll}} = 2$ (*"Our"*, *"We"*) $\implies d_{\text{PronounDrop}} = \text{clamp}\left(1.0 - \frac{0}{0 + 2}, 0, 1\right) = \mathbf{1.00}$.
  * $N_{\text{Weak}} = 3$ (*"should"*, *"believe"*, *"can expect"*), $N_{\text{Strong}} = 1$ (*"will"*) $\implies d_{\text{WeakModals}} = \text{clamp}\left(\frac{3}{3 + 1}, 0, 1\right) = \mathbf{0.75}$.
  * $N_{\text{Gen}} = 2$ (*"Certain"*, *"transitional"*) in $\text{Words} = 58 \implies \frac{100 \times 2 / 58}{3.0} = \frac{3.4483}{3.0} = 1.1494 \implies d_{\text{GenKnowledge}} = \text{clamp}(1.1494, 0, 1) = \mathbf{1.00}$.
  * **Deterministic $SDRI$ Calculation:**
    $$\text{SDRI} = 0.35(1.00) + 0.25(1.00) + 0.25(0.75) + 0.15(1.00) = 0.35 + 0.25 + 0.1875 + 0.15 = \mathbf{0.94} \quad (\text{Forensic Alert: } > 0.65)$$

---

### Benchmark Case 03: Evasive Witness Statement vs. Clean Baseline Control (MODE C)

#### A. Input Comparison (Investigative Statement Analysis — Treatises 01, 02, 06, 07)
* **Sample 3A (Evasive Statement — 6 Verbal Predicates):**
  > *"The morning audit **[1] began** at 9:00 AM and the ledger files **[2] were reviewed**. Mistakes **[3] were made** with the wire transfer authorization, and the next thing I **[4] knew**, the funds **[5] were transferred** out of the escrow account. I **[6] would** never intentionally **misappropriate** client capital."*
* **Sample 3B (Clean Baseline Control — 6 Verbal Predicates):**
  > *"I **[1] started** the morning audit at 9:00 AM and I **[2] reviewed** the ledger files. At 10:15 AM, I **[3] entered** the wrong account code on the wire form, which **[4] sent** $45,000 from escrow to the vendor account, and I **[5] reported** the error immediately. I **[6] did** not **take** the client's money."*

#### B. Comparative Quantitative & Structural Verification

| Diagnostic Parameter | Sample 3A (Evasive Statement) | Sample 3B (Clean Control) | Forensic Interpretation (Treatises 01, 02, 07, 27) |
| :--- | :---: | :---: | :--- |
| **Total Verbal Predicates ($N$)** | $6$ (*began, were reviewed, were made, knew, were transferred, would misappropriate*) | $6$ (*started, reviewed, entered, sent, reported, did [not] take*) | Identical predicate count ($N = 6$); contrasting syntactic agency. |
| **Passive / Agent-Deleted ($N_{\text{del}}$)** | $3$ (*"were reviewed"*, *"were made"*, *"were transferred"*) | $0$ | Sample 3A deletes the human actor in $3$ of $6$ predicates ($50\%$). |
| **Agent Deletion Index ($ADI$)** | $\frac{3}{6} = \mathbf{0.50}$ *(Alert $> 0.28$)* | $\frac{0}{6} = \mathbf{0.00}$ *(Clean $\le 0.20$)* | Sample 3A severs speaker agency at the critical phase of the transfer. |
| **1st-Person Singular (*"I"* / *"my"*)** | $2$ | $5$ | Pennebaker (Treatise 07) pronoun withdrawal during critical action. |
| **Temporal Lacuna Marker** | *"the next thing I knew"* | Explicit timestamp (*"At 10:15 AM"*) | Adams (Treatise 01): *"the next thing I knew"* marks an omitted time window. |
| **Denial Structure (McClish, Treatise 02)** | *"I would never intentionally misappropriate..."* | *"I did not take..."* | Sample 3A uses a subjunctive modal (*"would never"*) + qualifier (*"intentionally"*); Sample 3B uses past-tense factual denial (*"I did not"*). |

---

## 3. Edge-Case Verification Suite (Insufficient Data, Zero-Denominator & Clamping Tests)

To verify that the mathematical specification in [`SKILL.md`](../SKILL.md) never produces `NaN`, division-by-zero errors, artificial scores on empty text, or out-of-range $CSIS$ scores ($< 0\%$ or $> 100\%$):

1. **Empty or Non-Predicate Input ($\text{Words} = 0$, $\text{Sentences} = 0$, or $N_{\text{total verbal predicates}} = 0$):**
   * By the **Minimum Evaluatable Discourse Guard** (Section 3.2 of `SKILL.md` and Section 4.1 of Treatise 27), when an input contains zero words, zero sentences, or zero verbal predicates, **no numerical score is computed**.
   * Output: $ADI = \text{N/A}$, $GSD = \text{N/A}$, $CPR = \text{N/A}$, $TAD = \text{N/A}$, $\text{FMRE} = \text{N/A}$, $CSIS = \mathbf{\text{N/A (INSUFFICIENT\_DATA)}}$.
2. **Extreme Labyrinthine Clause ($\text{FMRE} = -45.0$, $ADI = 0.85$, $GSD = 0.90$, $CPR = 3.50$, $TAD = 0.75$ on Valid Discourse):**
   * Without clamping, raw penalty terms would exceed $1.0$ ($p_{\text{FMRE, raw}} = \frac{50 - (-45)}{50} = 1.90$, $p_{\text{ADI, raw}} = 1.70$), driving un-clamped $CSIS$ to $-123.5\%$.
   * With canonical $\text{clamp}(\cdot, 0, 1)$, each $p_i = 1.00$, yielding $CSIS = \text{clamp}(100 \times [1.0 - 1.0], 0, 100) = \mathbf{0.0\%} \in [0\%, 100\%]$.
3. **Ultra-Simple Plain Text ($\text{FMRE} = 95.0$, $ADI = 0.00$, $GSD = 0.00$, $CPR = 0.00$, $TAD = 0.00$ on Valid Discourse):**
   * Without lower clamping on $p_{\text{FMRE}}$, $\frac{50 - 95}{50} = -0.90$ would push $CSIS$ to $118.0\%$.
   * With canonical $\text{clamp}(\cdot, 0, 1)$, $p_{\text{FMRE}} = \text{clamp}(-0.90, 0, 1) = 0.00$, yielding $CSIS = \mathbf{100.0\%} \in [0\%, 100\%]$.
