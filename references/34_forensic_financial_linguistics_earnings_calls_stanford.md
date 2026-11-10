# 34. Forensic Financial Linguistics & Earnings Calls (Stanford / Larcker & Zakolyukina)

## 1. Executive Summary & Epistemological Foundation
Grounded in the empirical findings of **David F. Larcker** and **Anastasia A. Zakolyukina** (Stanford Graduate School of Business / Rock Center for Corporate Governance, *Detecting Deceptive Discussions in Conference Calls*, Journal of Accounting Research, 2012) and the specialized financial lexicography of **Tim Loughran & Bill McDonald** (University of Notre Dame, *When Is a Word Negatory?*, Journal of Finance, 2011), this pillar applies computational linguistics to quarterly earnings calls, CEO/CFO investor presentations, and M&A diligence disclosures.

Larcker and Zakolyukina demonstrated that corporate executives whose firms subsequently experienced accounting restatements exhibit statistically significant linguistic shifts in conference calls compared to non-restating peers—specifically elevated extreme positive emotion words, reduced first-person singular pronouns (*"I"*), and elevated generalized knowledge appeals.

---

## 2. The Stanford Conference Call Linguistic Markers

```
                   STANFORD EARNINGS CALL LINGUISTIC MARKERS
┌─────────────────────────────────┬──────────────────────────────────────────────┐
│       LINGUISTIC FEATURE        │     OBSERVED SHIFT IN RESTATING FIRMS        │
├─────────────────────────────────┼──────────────────────────────────────────────┤
│ 1. Extreme Positive Emotions    │ ELEVATED (Hyperbolic praise: "fantastic",    │
│    (Extreme POS Emotion)        │ "unprecedented", "phenomenal", "extraordinary")│
├─────────────────────────────────┼──────────────────────────────────────────────┤
│ 2. First-Person Singular        │ SUPPRESSED (Avoidance of "I", shifting to    │
│    (1st-Person "I", "me", "my") │ collective "We", "our", or passive voice)    │
├─────────────────────────────────┼──────────────────────────────────────────────┤
│ 3. References to Shareholders   │ SUPPRESSED (Reduced direct reference to      │
│    ("Shareholders", "Investors")│ shareholder value accountability)            │
├─────────────────────────────────┼──────────────────────────────────────────────┤
│ 4. Generalized Knowledge Claims │ ELEVATED (Invoking "everyone knows",         │
│    & Evidential Hedges          │ "as is standard", "obviously", "certain")    │
├─────────────────────────────────┼──────────────────────────────────────────────┤
│ 5. Short Uninformative Answers  │ Elevated lexical omission on granular Q&A;   │
│    (Word Count Compression)     │ long deflective narrative answers on fluff   │
└─────────────────────────────────┴──────────────────────────────────────────────┘
```

---

## 3. Loughran & McDonald Financial Sentiment Dictionaries
General sentiment dictionaries (such as Harvard General Inquirer) misclassify financial prose because routine operational nouns like *"liability"*, *"tax"*, *"cost"*, or *"depreciation"* are tagged as negative.

Loughran and McDonald engineered **Finance-Specific Dictionaries** calibrated to SEC filings (10-K, 10-Q, S-1):

| LM Dictionary Category | Target Financial Lexicon | Forensic Risk Signal |
| :--- | :--- | :--- |
| **Negative Financial** | *abandon, adverse, breach, cancel, default, deteriorate, impairment, litigation, restructuring* | Spike in MD&A section signals operational or balance-sheet stress. |
| **Litigious Words** | *claimant, plaintiff, tort, subpoena, indemnification, jurisdiction, arbitration* | Elevated litigation or regulatory exposure. |
| **Weak Modal Verbs** | *could, may, might, possibly, potentially, conceivable, should* | Hedged commitment to announced forward guidance. |
| **Constraining Words** | *covenant, encumber, bind, restrict, limit, pledge, impair, forbid* | Creditor restrictions and debt-covenant proximity. |

---

## 4. CEO vs. CFO Linguistic Asymmetry
* **The CEO Pattern:** CEOs typically act as high-level narrative communicators. Under operational stress or restatement risk, deceptive CEOs in the Larcker-Zakolyukina sample relied heavily on **Extreme Positive Emotion** and **Aggressive Optimism** (*"This is the strongest pipeline in corporate history"*).
* **The CFO Pattern:** CFOs are detail-oriented financial officers. Under reporting stress, deceptive CFOs exhibited **Syntactic Complexity**, **Passive Nominal Stacking**, and **Excessive Modal Hedges** (*"To the extent that baseline assumptions align with historical seasonality, amortization may approximate projected parameters"*).

---

## 5. Reproducible Heuristic Metric Specification: SDRI & LMWR

Because the original Larcker-Zakolyukina (2012) logistic regression coefficients ($\beta_i$) were estimated on proprietary LIWC category frequencies across a specific historical SEC corpus, directly claiming a calibrated statistical *probability* on arbitrary texts without their proprietary training pipeline is methodologically invalid.

Instead, Subtext Engine operationalizes the directional findings of Larcker & Zakolyukina (2012) and Loughran & McDonald (2011) into a **fully deterministic, reproducible heuristic index**: the **Stanford Disclosure Risk Index ($SDRI$, legacy alias: $SDPS$)**.

### 5.1 Pre-Condition & Normalized Feature Definitions
If $\text{Words} = 0$, $\text{SDRI}$ returns `N/A (INSUFFICIENT_DATA)`. Otherwise, let $\text{clamp}(x, a, b) = \min(b, \max(a, x))$ and define four bounded sub-components in $[0, 1]$:

1. **Extreme Positive Emotion Density ($d_{\text{EPE}}$):**
   $$d_{\text{EPE}} = \text{clamp}\left(\frac{100 \times N_{\text{EPE}} / \text{Words}}{5.0}, 0, 1\right)$$
   where $N_{\text{EPE}}$ counts extreme positive hyperbole tokens (*unprecedented, phenomenal, extraordinary, fantastic, incredible, revolutionary, never been stronger, best-in-history*). Saturates at $5.0\%$ of total words.

2. **First-Person Singular Suppression ($d_{\text{PronounDrop}}$, with Nortje Collective Calibration):**
   $$d_{\text{PronounDrop}} = \begin{cases} 0.00 & \text{if } N_{\text{1stSg}} + N_{\text{Coll}} = 0 \text{ or } N_{\text{EPE}} + N_{\text{Weak}} + N_{\text{Gen}} = 0 \\ \text{clamp}\left(1.0 - \frac{N_{\text{1stSg}}}{N_{\text{1stSg}} + N_{\text{Coll}}}, 0, 1\right) & \text{otherwise} \end{cases}$$
   where $N_{\text{1stSg}}$ counts singular self-references (*I, me, my, mine*) and $N_{\text{Coll}}$ counts collective/institutional references (*we, us, our, ours, the company, management*). When a third-person contract contains zero first-person or collective pronouns ($N_{\text{1stSg}} + N_{\text{Coll}} = 0$), OR when a factual corporate statement uses *"we / wir / мы"* without any promotional hyperbole, weak modals, or evidential hedges ($N_{\text{EPE}} + N_{\text{Weak}} + N_{\text{Gen}} = 0$), $d_{\text{PronounDrop}} = 0.00$. Equals $1.00$ when speaker agency is shifted from *"I"* to *"We/Company"* alongside promotional or hedged claims.

3. **Modal Weakness Fraction ($d_{\text{WeakModals}}$):**
   $$d_{\text{WeakModals}} = \begin{cases} 0.00 & \text{if } N_{\text{Weak}} + N_{\text{Strong}} = 0 \\ \text{clamp}\left(\frac{N_{\text{Weak}}}{N_{\text{Weak}} + N_{\text{Strong}}}, 0, 1\right) & \text{otherwise} \end{cases}$$
   where $N_{\text{Weak}}$ counts weak/hedged modals (*could, may, might, should, possibly, potentially, believe, expect*) and $N_{\text{Strong}}$ counts definite factual/deontic commitments (*will, must, did, achieved, completed*).

4. **Generalized Knowledge & Evidential Hedging Density ($d_{\text{GenKnowledge}}$):**
   $$d_{\text{GenKnowledge}} = \text{clamp}\left(\frac{100 \times N_{\text{Gen}} / \text{Words}}{3.0}, 0, 1\right)$$
   where $N_{\text{Gen}}$ counts generalized appeals and vague qualifiers (*everyone knows, obviously, clearly, as is standard, certain, transitional*). Saturates at $3.0\%$ of total words.

### 5.2 Deterministic SDRI Formula & Threshold Grid
$$\text{SDRI} = 0.35\,d_{\text{EPE}} + 0.25\,d_{\text{PronounDrop}} + 0.25\,d_{\text{WeakModals}} + 0.15\,d_{\text{GenKnowledge}} \in [0.00, 1.00]$$

* **Clean Baseline:** $\text{SDRI} \le 0.35$ (Grounded, accountable financial disclosure)
* **Caution Zone:** $0.36 \le \text{SDRI} \le 0.65$ (Elevated promotional framing or modal hedging)
* **Forensic Alert Threshold:** $\text{SDRI} > 0.65$ (High concentration of hyperbolic optimism, pronoun distancing, and modal hedging; warrants forensic audit of underlying financial schedules)

### 5.3 Loughran-McDonald Modal Weakness Ratio ($LMWR$)
$$LMWR = \begin{cases} 0.00 & \text{if } N_{\text{Weak}} = 0 \text{ and } N_{\text{Strong}} = 0 \\ \text{MAX } (\infty) & \text{if } N_{\text{Weak}} > 0 \text{ and } N_{\text{Strong}} = 0 \\ \frac{N_{\text{Weak}}}{N_{\text{Strong}}} & \text{otherwise} \end{cases}$$
* **Clean Baseline:** $LMWR \le 0.50$ | **Caution Zone:** $0.51 \le LMWR \le 1.20$ | **Forensic Alert:** $LMWR > 1.20$.
