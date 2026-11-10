# 31. Forensic Stylometry & Composite Authorship (Burrows' Delta & Juola)

## 1. Executive Summary & Epistemological Foundation
Forensic Stylometry applies quantitative computational statistics to linguistic style, establishing non-conscious, habitual linguistic habits (**Stylistic Invariants**) that distinguish individual authors or drafting teams. Founded by **John Burrows** (*Delta Measure*, 2002) and standardized by **Patrick Juola** (Juola & Baayen, *Authorship Attribution*, 2008), stylometry deconstructs documents not by what they argue, but by the mathematical distribution of functional, non-thematic words (*prepositions, articles, conjunctions, punctuation ratios*).

In commercial litigation, corporate whistleblowing, and M&A contractology, stylometry identifies **Composite Authorship (Patchwork Texts)**: detecting when high-risk clauses were secretly inserted by hostile counsel or non-authorized parties into an agreed baseline draft.

---

## 2. Burrows' Delta ($\Delta$) Methodology
Burrows’ Delta calculates the distance between a contested text $T$ and the established baseline profile of a candidate author or drafting entity $C$ across the $N$ most frequent words (MFWs, typically $N = 100 \text{ to } 300$):

$$\Delta(T, C) = \frac{1}{N} \sum_{i=1}^N \left| \frac{f_i(T) - \mu_i(C)}{\sigma_i(C)} \right|$$

Where:
* $f_i(T)$ is the relative frequency of word $i$ in contested text $T$.
* $\mu_i(C)$ is the mean relative frequency of word $i$ in baseline corpus $C$.
* $\sigma_i(C)$ is the standard deviation of word $i$ in the reference corpus.

```
                      BURROWS' DELTA INTERPRETATION SCALE
┌──────────────────────────┬─────────────────────────────────────────────────────┐
│       DELTA VALUE        │            FORENSIC STYLOMETRIC VERDICT             │
├──────────────────────────┼─────────────────────────────────────────────────────┤
│ $\Delta < 0.80$          │ Very high probability of single/same drafting team. │
├──────────────────────────┼─────────────────────────────────────────────────────┤
│ $0.80 \le \Delta \le 1.25$│ Normal stylistic variation within institutional team│
├──────────────────────────┼─────────────────────────────────────────────────────┤
│ $1.26 \le \Delta \le 1.60$│ Stylistic discontinuity: external drafting influence│
├──────────────────────────┼─────────────────────────────────────────────────────┤
│ $\Delta > 1.60$          │ Definitive composite authorship / Foreign insertion.│
└──────────────────────────┴─────────────────────────────────────────────────────┘
```

---

## 3. Detecting "Trojan Clause" Infiltration in Commercial Drafting
During protracted multi-party negotiations (e.g., a 120-page syndicated loan or acquisition agreement), parties frequently exchange thousands of redline versions. A common predatory strategy is **Trojan Clause Infiltration**: stealthily slipping a predatory indemnity, arbitration, or IP assignment rider into an obscure schedule late at night.

### Stylometric Infiltration Markers:
1. **Z-Score Spike in Function Words:** Sudden shift in the ratio of archaic legal doublets (*"indemnify and hold harmless"*, *"by and between"* vs. modern commercial plain English).
2. **Mean Sentence Length (MSL) Divergence:** If Clauses 1–18 average $28 \pm 4$ words per sentence, and Section 19 jumps to $74 \pm 12$ words with nested passive subordinates, Section 19 is an imported, non-native insertion.
3. **Punctuation Entropy Shift:** Sudden variation in semicolon-to-comma density or parenthesis usage frequency indicates a different drafting template.

---

## 4. Stratification of Corporate Document Layers (The Geological Model)
Complex corporate memorandums and audit reports exhibit **Geological Text Layers**:

```
                       CORPORATE TEXT STRATIFICATION
┌────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: PUBLIC RELATIONS / EXECUTIVE COAT (Top layer)                 │
│ • High readability, enthusiastic adjectives, first-person plural.      │
├────────────────────────────────────────────────────────────────────────┤
│ LAYER 2: CONTROLLER / TECHNICAL SUBSTRATE (Middle layer)               │
│ • Numerical specificity, passive engineering/financial descriptors.    │
├────────────────────────────────────────────────────────────────────────┤
│ LAYER 3: DEFENSIVE LEGAL RIDER / CLAWBACK (Deep layer)                 │
│ • Labyrinthine syntax, high GSD, disclaimers, unconscionable waivers.  │
└────────────────────────────────────────────────────────────────────────┘
```
**Forensic Objective:** Strip Layer 1 and evaluate whether Layer 3 legally negates every commercial representation made in Layer 1.

---

## 5. Diagnostic Scoring & Operational Metrics
* **Composite Authorship Divergence Index ($CADI$):**
  $$CADI = \max_{j} \left( \Delta(\text{Section}_j, \text{Document Baseline}) \right)$$
  * $CADI > 1.50$ flags specific schedules or articles as covertly inserted foreign text requiring immediate legal quarantine.
* **Stylistic Entropy Variance ($SEV$):**
  $$SEV = \frac{\sigma^2(\text{Sentence Lengths across Sections})}{\mu(\text{Document Sentence Length})}$$
  * A high $SEV$ ($> 8.0$) indicates a chaotic Frankenstein agreement pasted together from conflicting legal precedents.
