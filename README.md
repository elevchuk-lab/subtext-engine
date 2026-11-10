# Subtext Engine: Structured Discourse, Contractual Risk & Financial Language Audit Framework

[![ORCID: 0009-0006-7103-0823](https://img.shields.io/badge/ORCID-0009--0006--7103--0823-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0006-7103-0823)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version: v1.1.1](https://img.shields.io/badge/Version-v1.1.6-blue.svg)](https://github.com/elevchuk-lab/subtext-engine/releases/tag/v1.1.6)
[![Architecture: CLI_+_LLM_Skill](https://img.shields.io/badge/Architecture-Python_CLI_%2B_LLM_Skill-teal.svg)](#what-this-repository-actually-is-architecture--honest-scope)
[![Corpus: 40 Literature Syntheses](https://img.shields.io/badge/Corpus-40_Literature_Syntheses-purple.svg)](#repository-structure)
[![Multi-Model: Universal](https://img.shields.io/badge/Multi--Model-Universal-orange.svg)](#multi-model--local-deployment)

> **Subtext Engine** is an open-source **hybrid analytical toolkit** combining a **deterministic Python CLI metric calculator (`bin/subtext_calc.py`)** with a **structured multi-model LLM verification checklist (`SKILL.md` + 40 author-compiled literature syntheses in `references/`)**. It is designed for preliminary screening of commercial contracts, shareholder agreements (SHA), financial disclosures, earnings call transcripts, and negotiation dialogues.

Developed by **[elevchuk-lab](https://github.com/elevchuk-lab)**, Subtext Engine structures legal, financial, and pragmatic text review into reproducible checklists rather than ad-hoc intuitive reading.

---

## What This Repository Actually Is (Architecture & Honest Scope)

To prevent any ambiguity between software execution and prompt-driven analysis, Subtext Engine explicitly separates its two layers:

1. **Deterministic CLI Pre-Processor (`bin/subtext_calc.py` — Regex & Lexicon Software Layer):**
   - A dependency-free Python 3 script that deterministically tokenizes input text (or evaluates explicit constituent counts) to compute word/sentence/syllable counts, passive/de-agentive verb rates, genitive chains, Garner/Loughran–McDonald lexicon matches, and the 9 composite indices (`ADI`, `GSD`, `CPR`, `MFR`, `FMRE`, `HIR`, `TAD`, `SDRI`, `CSIS`).
   - Running `python3 bin/subtext_calc.py --file contract.txt --format markdown` produces identical, reproducible numbers across every run.
   - **Honest Scope of Regex Screening:** `bin/subtext_calc.py` is a **rule-based regex and lexicon pattern scanner, not a deep semantic parser**. It detects known legal boilerplate, structural patterns, and common unilateral formulations, but cannot understand arbitrary novel paraphrases outside its rule set. A high `CSIS` score means **"no known high-risk lexical or structural patterns were triggered"**, **not** **"the contract is safe."** When input text contains zero contractual, legal, or financial domain markers (`domain_markers == 0`), the calculator flags `LOW_DOMAIN_SIGNAL` and marks `CSIS` as `Unverified (Non-Contractual / General Prose)` so literary prose (e.g., *Hamlet*) does not receive a misleading `100% Clean` contract score.
2. **Structured LLM Checklist & Reference Corpus (`SKILL.md` & `references/` — Prompt Layer):**
   - A structured instruction protocol and **40 author-compiled literature syntheses** (digesting primary academic and legal works) that guide an LLM through a systematic audit checklist.
   - **Important LLM Limitation:** When `SKILL.md` is used in **Pure Prompt Mode** (inside a chat window without running `bin/subtext_calc.py` first), the LLM estimates constituent counts within its attention window. On long documents, pure-LLM counts are **approximations** that can vary across runs. For exact, reproducible numbers, always run `bin/subtext_calc.py` first and feed its output table to the LLM.
3. **Not a Lie Detector or Clinical Diagnostic Tool:**
   - Subtext Engine is a **preliminary contract, disclosure, and negotiation screening aid**. It does **not** detect subjective *mens rea*, does **not** diagnose personality disorders from text, and does **not** replace qualified legal counsel or judicial expertise.

---

## Core Primary Pillars vs. Supplementary Theoretical Lenses

Rather than treating 40 diverse sources with equal weight in every prompt (which dilutes LLM focus), Subtext Engine prioritizes **three primary operational pillars** and treats the remaining files in `references/` as **supplementary contextual lenses** invoked only when relevant:

### Primary Operational Pillars (Core Checklist)
1. **Legal Drafting & Contractual Symmetry (Mode A Core — Syntheses 22, 27, 28, 37, 40):**
   - Wesley Newcomb Hohfeld's jural correlatives (detecting declared "rights" that lack enforceable reciprocal duties — *Hohfeldian voids*), Bryan A. Garner & *Black's Law Dictionary* canons (*"shall"* ambiguities, *"commercially reasonable efforts"* dilution, indemnity scope), and *contra proferentem* asymmetry screening.
2. **Financial Disclosure & Modality Analysis (Mode B Core — Syntheses 06–08, 26, 34):**
   - Loughran & McDonald (2011) financial sentiment/modality lexicons, Larcker & Zakolyukina (2012) executive call markers (extreme positive hyperbole vs. missing numerical anchors), and FrameNet slot omissions.
3. **Pragmatic Evasion & Question Generation (Mode C Core — Syntheses 18, 19, 23–25, 35):**
   - Gricean maxim flouting and paltering, Hallidayan transitivity (passive agent deletion), cross-cultural baseline calibration (Nortje, 2019), and calibrating non-accusatory follow-up questions using the Strategic Use of Evidence (SUE, Kebbell & Brewer) and Chris Voss negotiation frameworks.

### Supplementary Reference Syntheses (`references/`)
```
                               SUBTEXT ENGINE 40-SYNTHESIS REFERENCE CORPUS
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ MODULE I: STATEMENT & DISCOURSE HEURISTICS (Syntheses 01–21)                               │
│ • 01–03. Adams (1996), McClish (2001), FBI Discourse: Unvalidated question-generation      │
│          heuristics (used ONLY to spot conditional denials/time gaps for follow-up queries)│
│ • 04–05. Steller & Köhnken (1989) CBCA, Vrij (2005): Witness memory criteria & load        │
│ • 06–08. Pennebaker LIWC (2003, 2011), Sporer Reality Monitoring: Pronoun & sensory ratios │
│ • 09–14. Hassan BITE, Biderman, IDT, Lefebvre, Luria, Porshnev: High-pressure influence    │
│ • 15–21. Sartori, Porter, Arce & Fariña (SEG), Kebbell (SUE), Nortje, Moscow School        │
├────────────────────────────────────────────────────────────────────────────────────────────┤
│ MODULE II: JURISLINGUISTICS, PRAGMATICS & QUANTITATIVE SUITE (Syntheses 22–27)             │
│ • 22. Jurislinguistics & Legal Textology: Brinev, Golev, RFTSSE (assertions vs opinions)   │
│ • 23–26. Fairclough/van Dijk CDA, Halliday SFL, Grice/Searle Pragmatics, Fillmore FrameNet │
│ • 27. Author-Defined Quantitative Heuristic Suite: ADI, GSD, CPR, MFR & FMRE Readability   │
├────────────────────────────────────────────────────────────────────────────────────────────┤
│ MODULE III: FORMAL ENTITLEMENT LOGIC & STRUCTURAL MODELS (Syntheses 28–33)                 │
│ • 28. Hohfeldian Legal Entitlements & Void Detection: Wesley Newcomb Hohfeld (1913)        │
│ • 29–30. Incentive Compatibility (Hurwicz/Maskin) & Deontic Modal Deadlock Checks          │
│ • 31–33. Stylometry (Burrows' Delta), Semiotic Framing (Lotman), Clause Dependency Graphs  │
├────────────────────────────────────────────────────────────────────────────────────────────┤
│ MODULE IV: COMMERCIAL DUE DILIGENCE & NEGOTIATION TACTICS (Syntheses 34–40)                │
│ • 34. Financial Linguistics: Larcker & Zakolyukina (2012), Loughran & McDonald (2011)      │
│ • 35. Negotiation Question Design: FBI Chris Voss Tactical Empathy & Harvard PON           │
│ • 36. Coercive Negotiation Rhetoric: Surface pressure & blame-shifting tactics (non-clinical)│
│ • 37–39. Contractual Asymmetry, ACFE Fraud Triangle / PEACE Model, Brignull Dark Patterns  │
│ • 40. Black's Law Dictionary & Bryan Garner: Terms of Art, Shall Deconstruction, Canons    │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## The Three Specialized Operational Modes

* **MODE A: Commercial Contract, SHA & SLA Screening:**  
  Focused on Shareholder Agreements, MSAs, and Vendor SLAs. Screens clauses for Hohfeldian voids (Synthesis 28), Garner *"shall"* and efforts dilutions (Synthesis 40), unilateral discretion traps, and remedy caps (Synthesis 37).
* **MODE B: M&A Due Diligence, Pitch Deck & Financial Disclosure Review:**  
  Focused on investment memos, pitch decks, and earnings call transcripts. Evaluates the ratio of speculative modality to verifiable numerical anchors ($MFR$) and computes the heuristic Stanford Disclosure Risk Index ($SDRI$, Synthesis 34).
* **MODE C: Negotiation Discourse & Clarifying Question Preparation:**  
  Focused on negotiation transcripts and dispute correspondence. Identifies passive responsibility diffusion ($ADI$), temporal gaps, and conditional non-denials to generate concrete, non-accusatory clarifying questions (SUE / Voss protocol, Syntheses 18, 35).

---

## Quantitative Heuristic Suite (Author-Defined Operationalizations)

**Methodological Transparency:** With the exception of the Flesch–Matsukovsky Reading Ease formula ($FMRE$), the indices below (`ADI`, `GSD`, `CPR`, `MFR`, `HIR`, `TAD`, `SDRI`, `CSIS`) and their 3-zone thresholds (`Clean` | `Caution` | `Alert`) are **author-defined composite heuristics engineered for this repository**. While inspired by concepts in Halliday (SFL), Hohfeld, Garner, and Larcker–Zakolyukina, the specific mathematical formulas and numerical cutoffs do not appear as universal constants in external literature and have not undergone large-scale clinical psychometric validation. They serve as **structured screening aids** to highlight dense legalese or asymmetric drafting for human review:

* **ADI (Agent Deletion Index):** Proportion of passive/impersonal verbal predicates lacking an explicit responsible actor (Clean: $\le 0.20$ | Caution: $0.21\text{--}0.28$ | Alert: $> 0.28$ flags elevated passive agency omission; keep in mind that passive voice is common in benign standard legal drafting and must be checked in context).
* **GSD (Genitive Stacking Density):** Fraction of sentences containing $\ge 3$ nested genitive/prepositional noun phrases (Clean: $\le 0.25$ | Caution: $0.26\text{--}0.35$ | Alert: $> 0.35$ flags heavy bureaucratic nominalization).
* **CPR (Covert Prescriptivity Ratio):** Ratio of unilateral impositions/discretionary carve-outs to balanced bilateral rights (Clean: $\le 0.30$ | Caution: $0.31\text{--}0.50$ | Alert: $> 0.50$ flags one-sided drafting).
* **MFR (Modality-to-Facticity Ratio):** Ratio of epistemic modals and unanchored superlatives to verifiable figures/dates (Clean: $\le 0.50$ | Caution: $0.51\text{--}1.00$ | Alert: $> 1.00$ flags speculative narrative imbalance).
* **FMRE (Flesch-Matsukovsky Reading Ease):** Standard readability formula adapted for English/Slavic syllable lengths (Clean: $\ge 50.0$ | Caution: $30.0\text{--}49.9$ | Alert: $< 30.0$ flags complex legalese).
* **HIR (Hohfeldian Integrity Ratio):** Fraction of declared rights backed by an enforceable reciprocal duty and remedy (Clean: $\ge 0.80$ | Caution: $0.60\text{--}0.79$ | Alert: $< 0.60$ flags unanchored rights).
* **TAD (Term-of-Art Ambiguity Density):** Density of diluted efforts standards (*"commercially reasonable efforts"*), *"sole discretion"* qualifiers, and ambiguous *"shall"* usages per operative clause (Clean: $\le 0.05$ | Caution: $0.06\text{--}0.15$ | Alert: $> 0.15$).
* **SDRI (Stanford Disclosure Risk Index, legacy alias: SDPS):** Author-defined $[0.00, 1.00]$ composite heuristic combining extreme positive emotion words, collective pronoun shifts, weak modals, and hedging (Clean: $\le 0.35$ | Caution: $0.36\text{--}0.65$ | Alert: $> 0.65$). **Nortje Collective-Pronoun Calibration:** First-person plural pronouns (*"we / wir / мы / біз"*) are only penalized ($d_{\text{PronounDrop}} > 0$) when accompanied by promotional hyperbole, weak modals, or evidential hedges ($N_{\text{EPE}} + N_{\text{Weak}} + N_{\text{Gen}} > 0$), preventing false flags on factual corporate statements.
* **CSIS (Composite Structural Integrity Score, legacy alias: CVS):** Bounded $[0\%, 100\%]$ summary index aggregating clamped penalties across $ADI, GSD, CPR, TAD,$ and $FMRE$ (Clean: $\ge 75\%$ | Caution: $50\%\text{--}74.9\%$ | Alert: $< 50\%$; returns `N/A (INSUFFICIENT_DATA)` if $\text{Words} = 0$, $\text{Sentences} = 0$, or $N_{\text{total verbal predicates}} = 0$).
  * **Component Alert Veto Rule:** To prevent a single severe indicator (such as `CPR = MAX`) from being diluted into an overall `Clean` zone by its $20\%$ weight, if **any single component metric is in `Alert`**, the overall `CSIS` status is capped at **`Caution (Veto: <Metric> Alert)`** (or **`Alert (Veto: Multiple Component Alerts)`** if $\ge 2$ components are in `Alert`).
  * **Domain Relevance Guard ("Hamlet Guard"):** If `domain_markers == 0`, the `CSIS` status is marked **`Unverified (Non-Contractual / General Prose)`** rather than `Clean`. Measures syntactic clarity and pattern absence, **not** factual truth or substantive legal safety.

---

## Evidentiary Context, SCAN Caveats & Methodological Boundaries

1. **Relationship to SCAN and Statement Analysis (Syntheses 01–03):**
   - Commercial SCAN (*Scientific Content Analysis*, Sapir) has failed empirical validation and *Daubert* hearings (e.g., Bogaard et al., 2014).
   - Because FBI Statement Analysis (Adams, 1996) and Mark McClish's *"Reliable Denial"* rules (Syntheses 01–02) belong to the same historical Statement Analysis family and **lack independent empirical validation of their error rates**, Subtext Engine **never** uses them to declare a speaker deceptive. They are retained in Mode C strictly as **conversational prompts** to help an interviewer notice conditional phrasing (*"I would never intentionally..."*) and ask a direct factual follow-up question.
2. **Narrow Scope of Judicial Frameworks (CBCA, SEG, RFTSSE):**
   - Criteria-Based Content Analysis (CBCA, recognized by the German Federal Court of Justice in BGH 1 StR 618/98) and the Ibero-American SEG protocol were validated specifically for **evaluating witness testimony in criminal proceedings (primarily child witnesses in abuse cases)**—**not** for commercial contracts, M&A pitch decks, or corporate earnings calls.
   - References to Daubert, BGH, SEG, and RFTSSE (РФЦСЭ Минюста) in this repository describe the **historical origin of the underlying academic literature**, **not** judicial certification of Subtext Engine itself. Outputs of Subtext Engine are **not** court-admissible expert evidence.
3. **No Remote Psychological or Clinical Diagnosis (Synthesis 36):**
   - Tools such as the B-Scan 360 (Babiak & Hare) require trained clinical/organizational assessors with multi-source behavioral history. Subtext Engine evaluates **only surface rhetorical tactics in text** (e.g., blame shifting, artificial urgency, coercive framing) and strictly prohibits labeling individuals with clinical or personality-disorder terms.

---

## Unstructured Ad-Hoc Prompting vs. Checklist-Driven Screening (`subtext-engine`)

Modern frontier LLMs can already spot obvious contract issues when asked generically (*"Review this contract"*). The practical value of `subtext-engine` is **consistency and structured completeness**—ensuring that every review systematically checks the same syntactic, Hohfeldian, and modality dimensions and pairs every flag with a concrete redline or clarifying question:

| Screening Dimension | Typical Ad-Hoc Prompt (*"Review this text"*) | Checklist-Driven Audit (`subtext-engine`) |
| :--- | :--- | :--- |
| **Effort & Discretion Qualifiers** | Often notes *"commercially reasonable efforts"* qualitatively, but may miss its interaction with downtime exclusions across separate clauses. | Explicitly pairs **Garner Term-of-Art Screening (`TAD`)** with **Hohfeldian Duty Mapping (`HIR`)** to check whether carve-outs reduce the core obligation to a non-binding privilege. |
| **Remedy & Indemnity Symmetry** | Flags low liability caps in general terms. | Cross-checks the **Remedy Cap** against one-way **Indemnification (`CPR`)** and drafts a reciprocal redline amendment. |
| **Earnings Call & Pitch Deck Puffery** | Summarizes management's optimistic tone. | Explicitly contrasts **Extreme Positive Emotion & Modals** against the count of **Verifiable Numerical Anchors (`MFR`, `SDRI`)** and lists missing data slots. |
| **Follow-Up Question Formulation** | Suggests generic legal or business takeaways. | Formulates verbatim **SUE / Voss Calibrated Questions** (*"How..." / "What..."*) tied to each specific ambiguous clause or time gap. |

*(Note: Quantitative recall/precision uplift over baseline prompting depends on the underlying LLM and document domain; see [`benchmarks/README.md`](benchmarks/README.md) for three reproducible worked examples verifying the mathematical formulas, and [`benchmarks/regression_corpus.json`](benchmarks/regression_corpus.json) for a 12-case regression set).*

> **This is a regression set, not a validation.** The 12 cases were written *after* earlier failures were observed and include previously reported probe texts, so a 12/12 match only shows that fixed bugs stay fixed. It says nothing about the scanner's ability to find asymmetry in unseen wording. An independent external probe of 6 one-sided + 6 balanced unseen clauses found **0/6 false positives** on balanced text but **only 1/6 one-sided clauses flagged for the right reason** (CPR), confirming that the CLI detects asymmetry only when the wording matches known patterns. A genuine hold-out set (real contracts, labeled by a lawyer *before* running the calculator) has not yet been built. Those 12 probe texts are kept verbatim in [`benchmarks/holdout_probe.json`](benchmarks/holdout_probe.json) as a **report-only known-gaps baseline**: test block [8/8] prints their recall and FPR on every run but never fails on misses, and they are not used to tune patterns (once published, they are no longer hold-out). Current result (v1.1.2): balanced FPR **0/6**; asymmetric clauses flagged for any reason **2/6**, for the right reason (CPR) **1/6**.

---

## Multilingual & Cross-Linguistic Support (EN / RU / ES / DE / FR / ZH / KK / AR)

While Subtext Engine's core specification is written in English, it processes documents across languages and explicitly distinguishes between the coverage of the **CLI regex scanner (`bin/subtext_calc.py`)** and the **LLM checklist (`SKILL.md`)**:

| Language Group | CLI Layer (`bin/subtext_calc.py`) | LLM Checklist Layer (`SKILL.md` + `references/`) |
| :--- | :--- | :--- |
| **Tier 1: `EN`, `RU`, `ES`, `DE`** | **Full Morphosyntactic & Regex Calibration:** Agentless passive detection (with explicit agent-phrase exclusion: *"by"*, *"со стороны"*, *"por"*, *"von/durch"*), genitive chain counting, deontic vs. epistemic modal separation, and unilateral clause patterns. | Full 6-section structural, Hohfeldian, and pragmatic audit with native redline generation. |
| **Tier 2: `FR`, `KK`, `ZH`, `AR`** | **Baseline Tokenization & Core Lexical Screening:** Word/CJK/syllable tokenization, core passive markers, and primary unilateral/disclaimer keywords. | Full cross-linguistic morphosyntactic adaptation and native output generation via the LLM's multilingual capabilities. |

* **Slavic / Russian & Turkic / Kazakh (Pro-Drop & Bureaucratic Register):** Accounts for natural pronoun dropping in inflected verbs, focusing on impersonal passive chains (*«было принято решение»*, *«қабылданды»*) and heavy nominalizations (*канцелярит*), while recognizing that passive constructions are standard in benign statutory/contractual templates unless they erase which party bears a specific contractual duty.
* **Romance / Spanish & French:** Accounts for reflexive and periphrastic passives (*se acordó*, *est exclu*) and subjunctive hedging.
* **Germanic / German:** Accounts for modal particle density (*ja, halt, eben, eigentlich*) and state/process passives (*wird ausgeschlossen*).
* **High-Context / Asian, Middle Eastern & Post-Soviet (Nortje Calibration):** Prevents false-positive flags on collective pronouns (*"we / wir / мы / біз / 我们 / نحن"*) and polite indirectness when no promotional hyperbole or hedging modals are present ($d_{\text{PronounDrop}} = 0.00$).

**Adaptive Output Protocol:** Subtext Engine outputs its 6-section screening report in the language requested by the user or the language of the source document.

---

## Repository Structure

```
subtext-engine/
├── bin/
│   └── subtext_calc.py        # Deterministic Python 3 CLI tokenizer & metric calculator
├── install.sh                 # Safe two-phase POSIX sh installer with backup & rollback
├── SKILL.md                   # Structured LLM audit checklist & mathematical specification
├── README.md                  # Architecture, methodological boundaries & usage guide
├── CHANGELOG.md               # Version history and formula/threshold change log
├── CITATION.cff               # Citation metadata (ORCID: 0009-0006-7103-0823)
├── LICENSE                    # MIT License
├── references/                # 40 Author-compiled literature syntheses & digests (.md)
│   ├── 01_susan_adams_1996_statement_analysis.md
│   ├── ...
│   └── 40_blacks_law_dictionary_legal_terms_of_art_garner.md
├── benchmarks/                # Worked arithmetic examples & regression corpus
│   ├── README.md              # Step-by-step worked calculations (Cases 01–03)
│   ├── regression_corpus.json # 12-case in-sample regression set (NOT a validation)
│   └── holdout_probe.json     # 12 external probe clauses: report-only known-gaps baseline
├── tests/                     # Automated verification & regression test suite
│   └── verify_metrics.sh      # POSIX sh + Python tests: CLI, regression set, probe report, installer
└── prompts/                   # Multi-model system prompt templates
    ├── claude_system_prompt.txt
    ├── chatgpt_custom_gpt.txt
    ├── cursor_rules.txt
    └── ollama_modelfile.txt
```

---

## Quickstart & Safe Installation

### Option 1: Direct Git Clone (Recommended — Inspectable & No Remote Script Execution)
```bash
git clone https://github.com/elevchuk-lab/subtext-engine.git ~/.agent/skills/subtext-engine
```

### Option 2: Run the Deterministic Python CLI Calculator (`bin/subtext_calc.py`)
Compute exact, reproducible metrics on any contract or transcript file locally (requires only Python 3 standard library):
```bash
python3 ~/.agent/skills/subtext-engine/bin/subtext_calc.py --file path/to/contract.txt --format markdown
```

### Option 3: Inspect & Run `install.sh` (Two-Phase Rollback-Safe POSIX Installer)
If you use the shell installer, download and inspect `install.sh` before executing:
```bash
curl -fsSL https://raw.githubusercontent.com/elevchuk-lab/subtext-engine/main/install.sh -o install.sh
less install.sh
sh install.sh
```

---

## Multi-Model & Local Deployment

| Platform / Environment | Template File | Deployment Instructions |
| :--- | :--- | :--- |
| **Claude (Anthropic)** | [`prompts/claude_system_prompt.txt`](prompts/claude_system_prompt.txt) | Paste into Claude Project Instructions or System Prompt. |
| **ChatGPT (OpenAI)** | [`prompts/chatgpt_custom_gpt.txt`](prompts/chatgpt_custom_gpt.txt) | Paste into Custom GPT "Instructions" field. |
| **Cursor / Windsurf** | [`prompts/cursor_rules.txt`](prompts/cursor_rules.txt) | Copy to project root as `.cursorrules` or `.windsurfrules`. |
| **Ollama (Offline)** | [`prompts/ollama_modelfile.txt`](prompts/ollama_modelfile.txt) | Run `ollama create subtext-engine -f prompts/ollama_modelfile.txt` |

---

## Citation

```bibtex
@software{levchuk_subtext_2026,
  author       = {Levchuk, Yevgeniy},
  title        = {{Subtext Engine: Structured Discourse, Contractual Risk \& Financial Language Audit Framework}},
  version      = {v1.1.6},
  year         = {2026},
  month        = nov,
  publisher    = {GitHub},
  url          = {https://github.com/elevchuk-lab/subtext-engine},
  note         = {ORCID: https://orcid.org/0009-0006-7103-0823}
}
```

---

## License

Released under the [MIT License](LICENSE).  
Authored and maintained by **[Yevgeniy Levchuk](https://orcid.org/0009-0006-7103-0823)** ([@elevchuk-lab](https://github.com/elevchuk-lab)).
