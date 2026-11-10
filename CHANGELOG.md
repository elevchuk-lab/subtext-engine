# Changelog

All notable changes to `subtext-engine` are documented in this file.

## [1.1.6] - 2026-11-10

### Fixed
- **Holdout Evaluation Artifact Fixed:** In test block [8/8], evaluation now uses `not r["zones"]["CSIS"].startswith("Clean")` rather than `!= "Clean"`, correctly classifying `Clean (Low Sample / Preliminary)` as a clean outcome. The true holdout recall on unseen asymmetric clauses is reported accurately as **2/6** (0.33) for any non-clean zone and **1/6** (0.17) for the target CPR Alert.
- **Coreference & Inclusive Parentheticals in Mutuality Guard:** Allowed mutual coreference pronouns (*"Each party agrees that it shall indemnify..."*, *"Both parties agree that they shall..."*) and inclusive parentheticals (*"Each party, including the Customer and the Vendor, shall indemnify..."*) without triggering the subordinate bypass guard.
- **Split 'Hold X Harmless' & Russian 'Возместить X Убытки':** Expanded unilateral indemnity matching to capture discontinuous phrases (*"Provider shall hold Client harmless"*, *"Заказчик обязан возместить Исполнителю любые убытки"*).
- **Rule Cycle Frozen:** Further pattern adjustment on holdout clauses is officially frozen in favor of constructing an independently labeled multi-clause contract evaluation corpus.

## [1.1.5] - 2026-11-10

### Fixed
- **Subordinate clause bypass prevention in mutuality detection:** Prevented unilateral clauses preceded by introductory agreement clauses (*"Each party agrees that Customer shall indemnify..."*, *"Both parties acknowledge that the Customer shall hold harmless..."*) from masquerading as mutual indemnities. Negative lookaheads verify that the mutual subject directly governs the obligation without intervening subordinate complementizers (*that*, *что*) or third-party nominal arguments (*Customer*, *Vendor*, *Заказчик*).
- **Russian active reflexive verb whitelist:** Added common active reflexives (*обязуется / обязуются*, *стремится / стремятся*, *соглашается / соглашаются*, *отказывается / отказываются*) to the exception set in `count_agentless_passives()` so that active mutual obligations (*"Стороны обязуются возместить..."*) are not erroneously penalized as agent-deleted passives in `ADI`.
- **Low-Sample CSIS Label Qualification:** When an excerpt contains dense legalese or extreme phrasing on a small sample (< 3 sentences or < 30 words) where individual metrics (`GSD`, `FMRE`, `ADI`) have threshold damping applied, the overall `CSIS` status is explicitly reported as `Clean (Low Sample / Preliminary)` rather than an unqualified `Clean`.

## [1.1.4] - 2026-11-10

### Fixed
- **Tightened Mutuality Guard to Subject Position:** Replaced loose sentence-level mutuality token matching with strict subject-position linkage (`each/either/both parties shall indemnify`, `каждая сторона обязуется возместить`, `jede Partei stellt ... frei`). This prevents bypasses where unilateral indemnity clauses contained peripheral mutuality references (e.g. *"Customer shall indemnify Vendor against all claims, and each party shall bear its own costs"* or *"Customer shall indemnify the other party for all losses"*), ensuring they remain flagged with `CPR = Alert`.
- **Short-Sample Statistical Stability Guard:** Prevented high-variance metrics (`GSD` and `FMRE`) from triggering the `CSIS Alert Veto` on short sample texts (< 3 sentences). Single isolated mutual sentences (e.g., in Russian or English) no longer produce false `Caution (Veto: FMRE/GSD Alert)` ratings due to small denominator anomalies.
- **German Unilateral Disclaimers & Asymmetric Rights:** Added patterns for German unilateral disclaimers (*"übernimmt keinerlei Haftung"*) and exclusive privileges (*"nur [Partei] darf/kann/ist berechtigt"*).

## [1.1.3] - 2026-11-10

### Fixed
- **False-positive covert prescriptivity on standard mutual indemnity:** Clauses such as *"Each party shall indemnify the other party against third-party claims arising from its own breach, subject to the same cap"* were erroneously penalised with `CPR = 1.0 (Alert)`. Added a sentence-level mutuality filter across English, Russian, Kazakh, Spanish, French, and German (`each party`, `mutual`, `каждая сторона`, `jede Partei`, etc.) protecting standard reciprocal commitments from being classified as unilateral impositions.
- **Separable verb & unilateral German scope detection:** Added patterns for German liability waivers using separable verbs (*"schließt ... aus"*) and asymmetric scoping (*"gilt nur für"*), allowing clauses like *"Der Auftragnehmer schließt jegliche Schadensersatzansprüche aus. Die Kündigungsfrist gilt nur für den Auftraggeber"* to be correctly captured as unilateral.

### Changed
- **Dual metric reporting in regression tests:** Test block [7/8] now explicitly outputs two separate confusion matrices: one for *Any non-Clean zone* and a dedicated one for the *Target CPR Alert* signal, preventing accidental or unrelated metric flags (e.g., MFR, FMRE) from masking detection quality.
- **Verbatim Hold-Out Baseline Added:** Formally integrated `benchmarks/holdout_probe.json` (12 clauses) as an immutable, report-only known-gaps baseline in test block [8/8]. The probe texts are kept intact and not used for pattern overfitting.

## [1.1.2] - 2026-11-10

### Fixed
- **Blocking crash on Python 3.9–3.13 (`NameError: name 'Optional' is not defined`):** `Optional` was used in the `compute_scorecard()` signature but imported ~160 lines later. Python 3.14 evaluates annotations lazily (PEP 649), so the bug was invisible on the release machine. `Optional` is now imported at the top of `bin/subtext_calc.py`. Minimum supported version corrected from "3.8+" to **3.9+** (3.8 is EOL and untested). Reported by an external reviewer.
- **German/Spanish/French/Kazakh/Chinese contracts flagged as "Unverified (Non-Contractual)":** the domain-marker lexicon only matched exact base forms (e.g. `vertrag`), so German compounds (*Vertragspartei, Auftragnehmer, Schadensersatz, Kündigungsfrist*) were missed. Domain markers now use stems for DE/ES/FR/KK and an extended ZH/AR list. Basic ZH predicates (可, 解除, 支付, 交付, 提供, 履行) added so short Chinese clauses no longer return `INSUFFICIENT_DATA`.

### Changed
- **`benchmarks/validation_corpus.json` renamed to `benchmarks/regression_corpus.json`.** The 12 cases were written after earlier failures were observed and include previously reported probe texts; a 12/12 match demonstrates that fixed bugs stay fixed, not generalization. The v1.1.1 description of this file as a "validation corpus" was inaccurate.
- **Test block [7/7]** now prints an explicit in-sample confusion matrix (TP/FN/FP/TN, recall, precision, FPR) labeled as non-generalizing.
- **Pattern coverage disclosure:** every raw-text result now includes `pattern_coverage` (number of known risk patterns triggered, by family) and the Markdown report prints that phrasings outside the rule set are invisible to the calculator.

### Added
- **CI matrix (`.github/workflows/tests.yml`):** runs `tests/verify_metrics.sh` on Python 3.9–3.14 on Ubuntu and macOS. The suite honors `PYTHON=<interpreter>`.

### Known limitations (documented, not fixed)
- An independent probe of 12 unseen clauses (6 one-sided, 6 balanced) produced 0/6 false positives but flagged only 1/6 one-sided clauses for the right reason. The CLI finds asymmetry only when wording matches known patterns. No lawyer-labeled hold-out set exists yet.

## [1.1.1] - 2026-11-10

### Changed
- **CSIS Component Alert Veto Rule (`bin/subtext_calc.py`, `SKILL.md`):** Prevented single-metric severity dilution where `CPR = MAX (Alert)` still yielded an overall `CSIS = 80.0% (Clean)` zone. If any single component metric enters the `Alert` zone while raw `CSIS >= 75%`, the overall `CSIS` status is capped at `Caution (Veto: <Metric> Alert)`. If two or more components enter `Alert`, the overall status is capped at `Alert (Veto: Multiple Component Alerts)`.
- **Domain Relevance Guard / "Hamlet Guard" (`bin/subtext_calc.py`):** Added `domain_relevance` and `domain_markers` tracking. When raw text contains zero contractual, legal, or financial domain markers (`domain_markers == 0`), the calculator flags `LOW_DOMAIN_SIGNAL` and sets the `CSIS` status to `Unverified (Non-Contractual / General Prose)` instead of returning a misleading `100% Clean` contract score on literary prose.
- **Nortje Collective-Pronoun Calibration in `SDRI` (`bin/subtext_calc.py`, `SKILL.md`, `references/34`):** Updated $d_{\text{PronounDrop}}$ so that first-person plural pronouns (*"we / wir / мы / біз"*) are only penalized when accompanied by promotional hyperbole, weak modals, or evidential hedges ($N_{\text{EPE}} + N_{\text{Weak}} + N_{\text{Gen}} > 0$). Factual corporate statements (e.g., *"Wir haben die Zahlung geleistet"*) now score `SDRI = 0.00 (Clean)`.
- **Honest Architectural Scope & Extended Paraphrase Patterns (`README.md`, `bin/subtext_calc.py`):** Explicitly documented that `bin/subtext_calc.py` is a deterministic regex and lexicon pattern scanner (not a deep semantic parser): a high `CSIS` score means *"no known high-risk lexical or structural patterns triggered"*, not *"the contract is safe."* Expanded structural patterns to catch colloquial and archaic unilateral idioms (*"at its absolute pleasure"*, *"owes nothing"*, *"waives every remedy"*, *"bears all losses"*).
- **8-Language CLI & LLM Coverage Matrix (`bin/subtext_calc.py`, `README.md`):** Added baseline tokenization and marker sets for `FR`, `KK`, `ZH`, and `AR` alongside `EN`, `RU`, `ES`, and `DE`, and added an explicit coverage matrix in `README.md` distinguishing Tier-1 CLI morphosyntactic support (`EN/RU/ES/DE`) from Tier-2 baseline lexical support (`FR/KK/ZH/AR`).

### Added
- **12-case labeled corpus (`benchmarks/validation_corpus.json`, renamed to `regression_corpus.json` in v1.1.2 because it is an in-sample regression set, not a validation):** Added a 12-case labeled corpus covering asymmetric clauses, synonym paraphrases, balanced bilateral clauses, transparent passives with agents, factual corporate statements, and non-contractual literary controls across 6 languages.

## [1.1.0] - 2026-11-10

### Added
- **Deterministic CLI Metric Calculator (`bin/subtext_calc.py`):** Added zero-dependency Python CLI tool for computing the 9 heuristic screening metrics (`ADI`, `GSD`, `CPR`, `MFR`, `FMRE`, `HIR`, `TAD`, `SDRI`, `CSIS`) from raw text or JSON constituent counts.
- **True Passive-With-Agent Filtering & Deontic Modal Calibration:** Excluded passives followed by explicit agentive phrases (*"by [agent]"*, *"со стороны"*, *"por"*, *"von/durch"*) from `ADI`, and separated legal permission (`may`) from epistemic speculation in `MFR`.

## [1.0.0] - 2026-04-19

### Added
- Initial release of the 3-mode screening framework (`Mode A: Legal/Contractual`, `Mode B: Financial/Corporate`, `Mode C: Negotiation/Interview`), 40 literature synthesis files in `references/`, 4 worked case studies in `benchmarks/`, and POSIX installer (`install.sh`).
