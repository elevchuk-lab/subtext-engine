# 34. Forensic Financial Linguistics & Earnings Calls (Stanford / Larcker & Zakolyukina)

## 1. Executive Summary & Epistemological Foundation
Developed by **David F. Larcker** and **Anastasia A. Zakolyukina** (Stanford Graduate School of Business / Rock Center for Corporate Governance, *Detecting Deceptive Discussions in Conference Calls*, Journal of Accounting Research, 2012) and augmented by the specialized financial lexicography of **Tim Loughran & Bill McDonald** (University of Notre Dame, *When Is a Word Negatory?*, Journal of Finance, 2011), this pillar applies computational linguistics to quarterly earnings calls, CEO/CFO investor presentations, and M&A diligence disclosures.

This methodology demonstrates that corporate executives who engage in financial statement manipulation, revenue overstatement, or liability concealment exhibit statistically significant, involuntary linguistic shifts in unscripted Q&A sessions.

---

## 2. The Stanford Deceptive Conference Call Model
Larcker and Zakolyukina trained natural language classifiers on thousands of earnings call transcripts cross-referenced with subsequent SEC restatements, accounting irregularities, and class-action fraud lawsuits. Deceptive CEOs and CFOs operate under intense cognitive load, generating specific verbal evasion markers:

```
                  STANFORD DECEPTIVE EARNINGS CALL MARKERS
┌─────────────────────────────────┬──────────────────────────────────────────────┐
│       LINGUISTIC FEATURE        │      BEHAVIOR OF DECEPTIVE EXECUTIVES        │
├─────────────────────────────────┼──────────────────────────────────────────────┤
│ 1. Extreme Positive Emotions    │ STATISTICALLY ELEVATED (Hyperbolic praise,   │
│    (Extreme POS Emotion)        │ "fantastic", "unprecedented", "phenomenal"). │
├─────────────────────────────────┼──────────────────────────────────────────────┤
│ 2. First-Person Singular        │ STATISTICALLY SUPPRESSED (Avoidance of "I",  │
│    (1st-Person "I", "me", "my") │ shifting to collective "We" or "the company")│
├─────────────────────────────────┼──────────────────────────────────────────────┤
│ 3. References to Shareholders   │ STATISTICALLY SUPPRESSED (Deceptive execs    │
│    ("Shareholders", "Investors")│ avoid naming the party they are defrauding). │
├─────────────────────────────────┼──────────────────────────────────────────────┤
│ 4. Generalized Knowledge Claims │ STATISTICALLY ELEVATED (Invoking "everyone   │
│                                 │ knows", "as is standard", "obviously").      │
├─────────────────────────────────┼──────────────────────────────────────────────┤
│ 5. Short Uninformative Answers  │ Elevated lexical omission on granular Q&A;   │
│    (Word Count Compression)     │ long deflective narrative answers on fluff.  │
└─────────────────────────────────┴──────────────────────────────────────────────┘
```

---

## 3. Loughran & McDonald Financial Sentiment Dictionaries
General sentiment dictionaries (like LIWC or Harvard General Inquirer) fail catastrophically in finance because words like *"liability"*, *"tax"*, *"cost"*, or *"capital"* are treated as negative, whereas they are routine operational nouns. 

Loughran and McDonald engineered **Finance-Specific Dictionaries** calibrated to SEC filings (10-K, 10-Q, S-1):

| LM Dictionary Category | Target Financial Lexicon | Forensic Red Flag |
| :--- | :--- | :--- |
| **Negative Financial** | *abandon, adverse, breach, cancel, default, deteriorate, impairment, litigation, restructuring* | Spike in MD&A section indicates unacknowledged operational collapse. |
| **Litigious Words** | *claimant, plaintiff, tort, subpoena, indemnification, jurisdiction, arbitration* | Concealed class actions or pending regulatory enforcement. |
| **Weak Modal Verbs** | *could, may, might, possibly, potentially, conceivable* | Management lacking confidence in announced forward guidance. |
| **Constraining Words** | *covenant, encumber, bind, restrict, limit, pledge, impair, forbid* | Creditor chokeholds and debt-covenant proximity. |

---

## 4. CEO vs. CFO Linguistic Asymmetry
* **The CEO Pattern:** CEOs are typically visionary, high-level communicators. When a CEO commits deception, they rely heavily on **Extreme Positive Emotion** and **Aggressive Optimism** (*"This is the strongest pipeline in corporate history"*).
* **The CFO Pattern:** CFOs are detail-oriented and risk-averse. When a CFO commits deception, they exhibit **Extreme Syntactic Complexity**, **Passive Nominal Stacking**, and **Excessive Hedges** (*"To the extent that baseline assumptions align with historical seasonality, amortization may approximate projected parameters"*).

---

## 5. Diagnostic Scoring & Operational Metrics
* **Stanford Deception Probability Score ($SDPS$):**
  $$SDPS = \sigma \left( \beta_0 + \beta_1 (\text{PosEmotion}) - \beta_2 (\text{Pronoun } I) - \beta_3 (\text{ShareholderRefs}) + \beta_4 (\text{GeneralKnowledge}) \right)$$
  * $SDPS > 0.65$ indicates high probability of unannounced financial restatement or accounting irregularities within 12–24 months.
* **Loughran-McDonald Modal Weakness Ratio ($LMWR$):**
  $$LMWR = \frac{N_{\text{Weak Modals (could, may, might)}}}{N_{\text{Strong Modals (will, shall, must)}}}$$
  * An earnings call where $LMWR > 1.20$ during guidance discussions reveals executive awareness that public targets are unachievable.
