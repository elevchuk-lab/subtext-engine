#!/usr/bin/env python3
"""
subtext_calc.py — Deterministic Pattern & Lexicon Pre-Calculator for Subtext Engine (v1.1.6).

Scope & Honest Limitations:
- This script is a deterministic REGEX & LEXICON SCANNER, NOT a semantic parser.
  It guarantees 100% mathematical reproducibility for word/sentence/syllable counts,
  known legal/financial phrases, and syntactic patterns across supported languages,
  eliminating LLM arithmetic drift.
- Because regexes match known patterns and structural combinations rather than deep
  semantics, novel paraphrases of one-sided clauses can still evade lexical matching.
  A high CSIS score in CLI output means "no known structural/lexical risk patterns
  were triggered", NOT "the contract is legally safe". Always pair CLI output with
  the structured LLM checklist in SKILL.md and human legal counsel.

Key Precision Safeguards (v1.1.6):
1. Agent-Attributed Passive Exclusion: Passives with an explicit agent ("by the auditor",
   "советом директоров", "por el comité", "vom Vorstand", "par le client") are NOT counted
   as agent-deleted predicates in ADI.
2. Deontic vs. Epistemic Modal Separation: Contractual permission ("may [verb]") is NOT
   counted as speculative modality in MFR.
3. Contextual Pronoun Shift in SDRI: Collective pronouns ("we / wir / мы") in factual
   business statements ("Wir haben die Zahlung geleistet") are NOT penalized unless
   accompanied by promotional hyperbole, weak modals, or evidential hedges (Nortje calibration).
4. Component Alert Veto Rule: If ANY individual metric enters the 'Alert' zone (e.g., CPR = MAX),
   the overall CSIS zone cannot be 'Clean' — it is capped at 'Caution (Veto: Component Alert)'
   (or 'Alert' if >= 2 metrics are in Alert).
5. Domain Relevance Check (Hamlet Guard): Flags texts with zero legal, contractual, or
   financial markers as 'LOW_DOMAIN_SIGNAL' so literary prose is not mistaken for a safe contract.
6. Multilingual Tokenization (EN, RU, ES, DE, FR, KK, ZH, AR): Full Unicode & CJK support.

Zero external dependencies (Python 3.9+ standard library only; CI-tested on 3.9, 3.12, 3.14).
"""

import argparse
import json
import re
import sys
from typing import Any, Dict, List, Optional


def clamp(x: float, low: float = 0.0, high: float = 1.0) -> float:
    return min(high, max(low, x))


def zone_upper_bad(val: Any, clean_max: float, caution_max: float) -> str:
    if val == "N/A" or val == "N/A (INSUFFICIENT_DATA)":
        return "INSUFFICIENT_DATA"
    if val == "MAX":
        return "Alert"
    v = float(val)
    if v <= clean_max:
        return "Clean"
    if v <= caution_max:
        return "Caution"
    return "Alert"


def zone_lower_bad(val: Any, clean_min: float, caution_min: float) -> str:
    if val == "N/A" or val == "N/A (INSUFFICIENT_DATA)":
        return "INSUFFICIENT_DATA"
    v = float(val)
    if v >= clean_min:
        return "Clean"
    if v >= caution_min:
        return "Caution"
    return "Alert"


def compute_scorecard(
    words: int,
    sentences: int,
    syllables: int,
    total_predicates: int,
    deleted_predicates: int = 0,
    chains_ge_3: int = 0,
    covert_prescriptions: int = 0,
    bilateral_rights: int = 0,
    speculative_modals: int = 0,
    anchored_facts: int = 0,
    operative_rights_with_duty: int = 0,
    total_declared_rights: int = 0,
    ambiguous_terms: int = 0,
    total_operative_clauses: int = 0,
    n_epe: int = 0,
    n_1st_sg: int = 0,
    n_coll: int = 0,
    n_weak: int = 0,
    n_strong: int = 0,
    n_gen: int = 0,
    domain_markers: Optional[int] = None,
) -> Dict[str, Any]:
    """Computes the canonical 9-metric scorecard from constituent counts."""
    if words <= 0 or sentences <= 0 or total_predicates <= 0:
        return {
            "status": "INSUFFICIENT_DATA",
            "domain_relevance": "INSUFFICIENT_DATA",
            "counts": {
                "words": words,
                "sentences": sentences,
                "syllables": syllables,
                "total_predicates": total_predicates,
            },
            "metrics": {
                "ADI": "N/A",
                "GSD": "N/A",
                "CPR": "N/A",
                "MFR": "N/A",
                "FMRE": "N/A",
                "HIR": "N/A",
                "TAD": "N/A",
                "SDRI": "N/A",
                "CSIS": "N/A (INSUFFICIENT_DATA)",
            },
            "zones": {k: "INSUFFICIENT_DATA" for k in ["ADI", "GSD", "CPR", "MFR", "FMRE", "HIR", "TAD", "SDRI", "CSIS"]},
        }

    adi = round(deleted_predicates / total_predicates, 4)
    gsd = round(chains_ge_3 / sentences, 4)
    tad = round(ambiguous_terms / total_operative_clauses, 4) if total_operative_clauses > 0 else 0.0

    if bilateral_rights == 0:
        if covert_prescriptions == 0:
            cpr: Any = 0.0
            p_cpr = 0.0
        else:
            cpr = "MAX"
            p_cpr = 1.0
    else:
        cpr = round(covert_prescriptions / bilateral_rights, 4)
        p_cpr = clamp(float(cpr) / 0.80, 0.0, 1.0)

    if anchored_facts == 0:
        mfr: Any = 0.0 if speculative_modals == 0 else "MAX"
    else:
        mfr = round(speculative_modals / anchored_facts, 4)

    fmre = round(206.835 - 1.3 * (words / sentences) - 60.1 * (syllables / words), 2)
    hir: Any = round(operative_rights_with_duty / total_declared_rights, 4) if total_declared_rights > 0 else "N/A"

    p_adi = clamp(adi / 0.50, 0.0, 1.0)
    p_gsd = clamp(gsd / 0.50, 0.0, 1.0)
    p_tad = clamp(tad / 0.30, 0.0, 1.0)
    p_fmre = clamp((50.0 - fmre) / 50.0, 0.0, 1.0)

    csis = round(
        clamp(
            100.0 * (1.0 - (0.20 * p_adi + 0.20 * p_gsd + 0.20 * p_cpr + 0.20 * p_tad + 0.20 * p_fmre)),
            0.0,
            100.0,
        ),
        1,
    )

    # SDRI with Nortje collective-pronoun calibration:
    # Collective pronouns ("we / wir / мы") are only penalized when accompanied by
    # promotional hyperbole, weak modals, or evidential hedges (n_epe + n_weak + n_gen > 0).
    d_epe = clamp((100.0 * n_epe / words) / 5.0, 0.0, 1.0)
    if (n_1st_sg + n_coll) == 0 or (n_epe + n_weak + n_gen) == 0:
        d_pron = 0.00
    else:
        d_pron = clamp(1.0 - (n_1st_sg / (n_1st_sg + n_coll)), 0.0, 1.0)
    if (n_weak + n_strong) == 0:
        d_weak = 0.00
    else:
        d_weak = clamp(n_weak / (n_weak + n_strong), 0.0, 1.0)
    d_gen = clamp((100.0 * n_gen / words) / 3.0, 0.0, 1.0)
    sdri = round(0.35 * d_epe + 0.25 * d_pron + 0.25 * d_weak + 0.15 * d_gen, 2)

    zones = {
        "ADI": zone_upper_bad(adi, 0.20, 0.28),
        "GSD": zone_upper_bad(gsd, 0.25, 0.35),
        "CPR": zone_upper_bad(cpr, 0.30, 0.50),
        "MFR": zone_upper_bad(mfr, 0.50, 1.00),
        "FMRE": zone_lower_bad(fmre, 50.0, 30.0),
        "HIR": zone_lower_bad(hir, 0.80, 0.60) if hir != "N/A" else "N/A",
        "TAD": zone_upper_bad(tad, 0.05, 0.15),
        "SDRI": zone_upper_bad(sdri, 0.35, 0.65),
    }

    # Component Alert Veto Rule on overall CSIS zone:
    # Statistical Stability Guard on short samples:
    # Metrics with extreme variance on short samples (sentences < 3 or words < 30) such as
    # GSD (fraction of sentences), FMRE (readability formula), and ADI (when total predicates <= 2)
    # are marked with insufficient statistical depth and do NOT trigger the CSIS Alert Veto unless
    # the document meets minimum evaluatable length (sentences >= 3 and words >= 30).
    raw_csis_zone = zone_lower_bad(csis, 75.0, 50.0)
    component_alerts = [k for k, z in zones.items() if z == "Alert"]
    veto_eligible_alerts = [
        k for k in component_alerts
        if not (sentences < 3 and (k in ("GSD", "FMRE") or (k == "ADI" and total_predicates <= 2)))
    ]
    sample_too_short = sentences < 3 or words < 30
    if sentences < 3:
        if zones["GSD"] == "Alert":
            zones["GSD"] = "Caution (Sample Too Short for GSD Threshold)"
        if zones["FMRE"] == "Alert":
            zones["FMRE"] = "Caution (Sample Too Short for FMRE Threshold)"
        if zones["ADI"] == "Alert" and total_predicates <= 2:
            zones["ADI"] = "Caution (Sample Too Short for ADI Threshold)"

    if raw_csis_zone == "Clean" and len(veto_eligible_alerts) >= 2:
        zones["CSIS"] = "Alert (Veto: Multiple Component Alerts)"
    elif raw_csis_zone == "Clean" and len(veto_eligible_alerts) == 1:
        zones["CSIS"] = f"Caution (Veto: {veto_eligible_alerts[0]} Alert)"
    else:
        zones["CSIS"] = raw_csis_zone

    # If the computed zone is Clean but statistical sample size is insufficient (< 3 sentences or < 30 words)
    # AND at least one metric had a short-sample threshold condition (GSD, FMRE, ADI),
    # qualify the zone label to prevent false confidence on micro-excerpts.
    short_sample_metrics_flagged = any(
        "Sample Too Short" in str(z) for z in zones.values()
    )
    if zones["CSIS"] == "Clean" and sample_too_short and short_sample_metrics_flagged:
        zones["CSIS"] = "Clean (Low Sample / Preliminary)"

    # Domain Relevance Check (Hamlet Guard)
    inferred_domain_markers = (
        domain_markers
        if domain_markers is not None
        else (
            covert_prescriptions
            + bilateral_rights
            + total_declared_rights
            + ambiguous_terms
            + anchored_facts
            + n_epe
        )
    )
    if domain_markers is not None and domain_markers == 0:
        domain_relevance = "LOW_DOMAIN_SIGNAL (No contractual, legal, or financial markers detected; score reflects general prose readability only)"
        if zones["CSIS"].startswith("Clean"):
            zones["CSIS"] = "Unverified (Non-Contractual / General Prose)"
    else:
        domain_relevance = "DOMAIN_MATCHED"

    metrics = {
        "ADI": adi,
        "GSD": gsd,
        "CPR": cpr,
        "MFR": mfr,
        "FMRE": fmre,
        "HIR": hir,
        "TAD": tad,
        "SDRI": sdri,
        "CSIS": csis,
    }

    return {
        "status": "OK",
        "domain_relevance": domain_relevance,
        "component_alerts": component_alerts,
        "counts": {
            "words": words,
            "sentences": sentences,
            "syllables": syllables,
            "total_predicates": total_predicates,
            "deleted_predicates": deleted_predicates,
            "chains_ge_3": chains_ge_3,
            "covert_prescriptions": covert_prescriptions,
            "bilateral_rights": bilateral_rights,
            "speculative_modals": speculative_modals,
            "anchored_facts": anchored_facts,
            "operative_rights_with_duty": operative_rights_with_duty,
            "total_declared_rights": total_declared_rights,
            "ambiguous_terms": ambiguous_terms,
            "total_operative_clauses": total_operative_clauses,
            "domain_markers": inferred_domain_markers,
        },
        "metrics": metrics,
        "zones": zones,
    }


# --- Deterministic Rule-Based Text Tokenizer (EN / RU / ES / DE / FR / KK / ZH / AR) ---


VOWELS_LATIN = set("aeiouyáéíóúüäöàèìòùâêîôûœæ")
VOWELS_CYRILLIC = set("аеёиоуыэюяіїєґәіңғүұқөһ")
VOWELS_ARABIC = set("اويىةأإآؤئ")


def is_cjk(ch: str) -> bool:
    cp = ord(ch)
    return 0x4E00 <= cp <= 0x9FFF or 0x3400 <= cp <= 0x4DBF


def count_word_syllables(word: str) -> int:
    cjk_chars = sum(1 for ch in word if is_cjk(ch))
    if cjk_chars > 0:
        return cjk_chars
    w = "".join(ch for ch in word.lower() if ch.isalpha())
    if not w:
        return 1
    if any(ch in VOWELS_CYRILLIC for ch in w):
        return max(1, sum(1 for ch in w if ch in VOWELS_CYRILLIC))
    if any(ch in VOWELS_ARABIC for ch in w):
        return max(1, sum(1 for ch in w if ch in VOWELS_ARABIC))
    count = 0
    prev_vowel = False
    for ch in w:
        is_v = ch in VOWELS_LATIN
        if is_v and not prev_vowel:
            count += 1
        prev_vowel = is_v
    if w.endswith("e") and count > 1 and not w.endswith(("le", "de", "se", "te", "ne", "re")):
        count -= 1
    return max(1, count)


def count_agentless_passives(text_lower: str) -> int:
    """
    Counts passive / impersonal verbal predicates ONLY when no responsible agent
    follows via 'by [agent]' (EN), 'со стороны / кем-то' (RU/KK), 'por [agent]' (ES),
    'von/vom/durch [agent]' (DE), or 'par [agent]' (FR).
    """
    count = 0

    # 1. English passives
    en_passive_iter = re.finditer(
        r"\b(?:was|were|is|are|been|be)\s+(?:not\s+|never\s+|hereby\s+|strictly\s+|unilaterally\s+)?([a-z]+ed|made|taken|done|given|sent|paid|held|kept|lost|waived|excluded|determined|transferred|implemented|reviewed|performed|terminated|modified|amended|cancelled|suspended|written|approved|signed)\b(?!\s+by\s+(?:the\s+|a\s+|an\s+|our\s+|their\s+|his\s+|her\s+|its\s+)?[a-z]{2,})",
        text_lower,
    )
    for m in en_passive_iter:
        participle = m.group(1)
        if participle in {"entitled", "located", "situated", "based", "interested", "concerned", "required", "obligated"}:
            continue
        count += 1

    # 2. Russian & Kazakh passives / impersonal forms
    ru_active_reflexives = {
        "обязуется", "обязуются", "стремится", "стремятся",
        "соглашается", "соглашаются", "отказывается", "отказываются",
        "надеется", "надеются", "заботится", "заботятся",
        "является", "являются", "остается", "остаются", "касается", "находится", "находятся"
    }
    ru_kk_passive_iter = re.finditer(
        r"\b(?:(?:было|были|будет|будут)\s+[а-яё]+(?:но|ны|на|ты|та|то)|принято\s+решение|возникла\s+необходимость|допущены\s+ошибки|[а-яё]{4,}(?:ется|ются|ась|ось|ись)|қабылданды|анықталады|шектеледі|алынып\s+тасталады|орындалады)\b(?!\s+(?:со\s+стороны|исполнителем|заказчиком|поставщиком|клиентом|покупателем|продавцом|арендатором|арендодателем|советом|комитетом|судом|директором|руководителем|аудитором|банком|партнером|партнёром|сторонами|тарапынан))",
        text_lower,
    )
    for m in ru_kk_passive_iter:
        phrase = m.group(0)
        if phrase in ru_active_reflexives:
            continue
        count += 1

    # 3. Spanish & French passives
    es_fr_passive_iter = re.finditer(
        r"\b(?:se\s+(?:acordó|decidió|determinó|estableció|excluye|excluyen|realizó|realizaron|transfirieron|cometieron|modificará|cancelará|suspenderá|aplicará|considerará)|(?:fue|fueron|será|serán|sea|sean|sido)\s+[a-záéíóúñ]+(?:ado|ada|ados|adas|ido|ida|idos|idas)|(?:est|sont|sera|seront|été)\s+(?:exclu\w*|déterminé\w*|modifié\w*|annulé\w*|transféré\w*|décidé\w*))\b(?!\s+(?:por|par)\s+(?:el\s+|la\s+|los\s+|las\s+|un\s+|una\s+|le\s+|les\s+)?[a-záéíóúñàèùêîôûç]{3,})",
        text_lower,
    )
    for _ in es_fr_passive_iter:
        count += 1

    # 4. German passives
    de_passive_iter = re.finditer(
        r"\b(?:wurde|wurden|wird|werden)\b(?![^.;,]{0,45}\b(?:von|vom|durch)\s+(?:dem|der|den|die|das|einem|einer)?\s*[a-zäöüß]{3,})[^.;,]{1,45}\b(?:[a-zäöüß]*ge[a-zäöüß]+(?:t|en)|[a-zäöüß]+iert|ausgeschlossen|bestimmt|festgelegt|überwiesen|getroffen|angepasst|gekündigt|aufgehoben)\b",
        text_lower,
    )
    for _ in de_passive_iter:
        count += 1

    # 5. Chinese & Arabic passive / agentless markers
    zh_ar_passive_iter = re.finditer(
        r"(?:被排除|被免除|不承担|予以免除|تم\s+اتخاذ|يتم\s+تحديد|تُستثنى|يُعفى)",
        text_lower,
    )
    for _ in zh_ar_passive_iter:
        count += 1

    return count


def analyze_raw_text(text: str) -> Dict[str, Any]:
    cleaned = text.strip()
    if not cleaned:
        return compute_scorecard(0, 0, 0, 0)

    sentences_list = [s.strip() for s in re.split(r"[.!?。！？؛]+", cleaned) if s.strip()]
    # Extract CJK characters as individual tokens plus standard Unicode words
    cjk_tokens = re.findall(r"[\u4e00-\u9fff]", cleaned)
    non_cjk_text = re.sub(r"[\u4e00-\u9fff]", " ", cleaned)
    alpha_tokens = re.findall(r"[\w%$€₸£¥-]+", non_cjk_text, flags=re.UNICODE)
    words_list = alpha_tokens + cjk_tokens

    if not words_list or not sentences_list:
        return compute_scorecard(0, 0, 0, 0)

    words_count = len(words_list)
    sentences_count = len(sentences_list)
    syllables_count = sum(count_word_syllables(w) for w in words_list)
    lower_text = cleaned.lower()
    lower_words = [w.lower().strip(".,:;()\"'«»„“”¿¡") for w in words_list]

    deleted_predicates = count_agentless_passives(lower_text)

    # Active & finite verbal predicates across EN / RU / ES / DE / FR / KK / ZH / AR
    verb_patterns = [
        # EN verbs (including cancel, owe, bear, forfeit, disclaim, etc.)
        r"\b(?:shall|must|may|will|would|should|can|could|might|did|does|do|is|are|was|were|has|have|had|began|started|reviewed|entered|sent|reported|believe|believes|expect|expects|maintain|maintains|indemnify|indemnifies|transform|normalize|provide|provides|pay|pays|terminate|terminates|cancel|cancels|modify|modifies|change|changes|reserve|reserves|waive|waives|relinquish|relinquishes|forfeit|forfeits|bear|bears|owe|owes|assume|assumes|disclaim|disclaims|limit|limits|cap|caps|exclude|excludes|determine|determines|agree|agrees|acknowledge|acknowledges|warrant|warrants|guarantee|guarantees|assure|assures|deliver|delivers|perform|performs|breach|breaches|liable|entitled|written|approved)\b",
        r"\b[a-z]{4,}ed\b",
        # RU & KK verbs
        r"\b(?:обязан\w*|вправе|имеет\s+право|приложит|ожидает|гарантирует|несет|несёт|оплачивает|предоставляет|стал|обещали|может|могут|должен|должны|будет|будут|было|были|изменить|расторгнуть|отказаться|ограничивается|исключается|определяется|производится|считается|влечет|влечёт|міндетті|құқылы|құқығы\s+бар|кепілдік\s+береді|жауапты\s+болмайды|шектеледі|анықталады|қабылданды|өзгертуге|бас\s+тартады)\b",
        r"\b[а-яёәіңғүұқөһ]{3,}(?:ал|ала|али|ил|ила|или|ет|ут|ют|ит|ат|ят|ться|тся|лся|лась|лись|ады|еді|йды|йді|ған|ген|қан|кен)\b",
        # ES & FR verbs
        r"\b(?:deberá|deberán|podrá|podrán|puede|pueden|tiene|tienen|tendrá|tendrán|será|serán|fue|fueron|está|están|garantiza|indemnizará|limita|excluye|determina|reserva|renuncia|modifica|cancela|asume|responde|doit|doivent|peut|peuvent|sera|seront|est|sont|garantit|indemnisera|limite|exclut|détermine|réserve|renonce|modifie|annule|assume)\b",
        r"\b[a-záéíóúñàèùêîôûç]{3,}(?:ar|er|ir|ó|aron|ieron|ará|arán|erá|erán|irá|irán|ado|ido|ando|iendo|era|eront|é|ée|és|ées)\b",
        # DE verbs
        r"\b(?:ist|sind|war|waren|wird|werden|wurde|wurden|hat|haben|hatte|hatten|kann|können|muss|müssen|soll|sollen|darf|dürfen|haftet|gewährleistet|verpflichtet|berechtigt|behält|verzichtet|begrenzt|ausgeschlossen|bestimmt|ändert|kündigt|trägt|schuldet)\b",
        r"\b[a-zäöüß]{4,}(?:en|et|te|ten)\b",
        # ZH & AR verbs
        r"(?:应当|必须|可以|可|有权|解除|支付|交付|提供|履行|同意|违约|保留|免除|放弃|承担|赔偿|保证|决定|修改|终止|取消|不承担|يجب|يجوز|يحق|يتحمل|يلتزم|يضمن|يحدد|يعفى|يتنازل|يعدل|يفسخ)",
    ]
    raw_predicates = sum(len(re.findall(p, lower_text)) for p in verb_patterns)
    total_predicates = max(deleted_predicates, raw_predicates)

    # Genitive / Prepositional chains >= 3 per sentence
    chains_ge_3 = 0
    for s in sentences_list:
        sl = s.lower()
        en_prep = len(re.findall(r"\b(?:of|to|under|from|in|for|by|with)\s+(?:the|any|all|such|this|each)\b", sl))
        ru_gen = len(re.findall(r"\b[а-яёәіңғүұқөһ]{4,}(?:ия|ения|ания|ости|еля|ика|оров|ат|ов|ей|ам|ами|ның|нің|дың|дің|тың|тің)\b", sl))
        es_fr_prep = len(re.findall(r"\b(?:de\s+la|de\s+los|de\s+las|del|en\s+el|en\s+la|por\s+el|du|des|de\s+l')\b", sl))
        de_gen = len(re.findall(r"\b(?:des|der|eines|einer|von\s+den|in\s+den|für\s+die|nach\s+den)\b", sl))
        if en_prep >= 3 or ru_gen >= 3 or es_fr_prep >= 3 or de_gen >= 3:
            chains_ge_3 += 1

    # Covert prescriptions / unilateral impositions & liability waivers (including structural combinations like 'at its pleasure', 'owes nothing', 'bears all losses')
    covert_patterns = [
        # EN unilateral discretion, pleasure/will, modification/cancellation at any time, waivers, zero-liability, bearing all losses
        r"\b(?:sole\s+discretion|absolute\s+discretion|unfettered\s+discretion|at\s+(?:its|his|her|their)\s+(?:sole\s+|absolute\s+|own\s+)?(?:pleasure|will|discretion|option|election)|unilateral\w*|at\s+any\s+time\s+without\s+(?:prior\s+)?notice|(?:cancel|terminate|modify|change|amend|suspend|revoke)\s+[^.;]{0,35}\bat\s+any\s+time|reserves\s+the\s+right\s+to\s+(?:modify|change|amend|terminate|suspend|alter|cancel)|as\s+determined\s+(?:solely\s+)?by|deems\s+(?:appropriate|necessary|fit)|in\s+its\s+sole\s+judgment|shall\s+indemnify|agrees\s+to\s+indemnify|hold\s+(?:[^.;]{1,25}\s+)?harmless|hereby\s+waived|(?:waives|relinquishes|forfeits|surrenders)\s+(?:all|any|every|each)\s+(?:claim\w*|remed\w*|right\w*|action\w*|damages)|(?:bears|assumes|absorbs)\s+(?:all|every|any|entire)\s+(?:loss\w*|risk\w*|cost\w*|liabilit\w*|damage\w*)|owes\s+(?:nothing|no\s+duty|no\s+compensation|zero)|no\s+liability|shall\s+not\s+be\s+liable|not\s+responsible\s+for\s+any|under\s+no\s+circumstances\s+shall|to\s+the\s+maximum\s+extent\s+permitted|as\s+is\s+without\s+warranty|without\s+recourse|non-refundable|strictly\s+on\s+time|time\s+is\s+of\s+the\s+essence|sole\s+and\s+exclusive\s+remedy|liquidated\s+damages|penalty\s+of)\b",
        # RU & KK
        r"\b(?:по\s+(?:своему\s+)?усмотрению|в\s+одностороннем\s+порядке|без\s+объяснения\s+причин|без\s+предварительного\s+уведомления|в\s+любой\s+момент\s+измен\w+|оставляет\s+за\s+собой\s+право|не\s+несет\s+ответственности|не\s+несёт\s+ответственности|освобождается\s+от\s+ответственности|ответственность\s+[^.;]{0,25}ограничивается|отказывается\s+от\s+(?:всех\s+|любых\s+|всяких\s+)?(?:претензий|прав|требований)|несет\s+все\s+(?:убытки|риски|расходы)|возместить\s+[^.;]{0,25}убытки|штраф\s+в\s+размере|неустойк\w+|не\s+подлежит\s+возврату|өз\s+қалауы\s+бойынша|біржақты\s+тәртіппен|жауапты\s+болмайды|жауапкершіліктен\s+босатылады|барлық\s+шығындарды\s+көтереді)\b",
        # ES & FR
        r"\b(?:a\s+su\s+(?:sola|exclusiva|entera)\s+discreción|unilateralmente|en\s+cualquier\s+momento\s+sin\s+previo\s+aviso|sin\s+necesidad\s+de\s+justificación|se\s+reserva\s+el\s+derecho|no\s+será\s+responsable|exime\s+de\s+toda\s+responsabilidad|renuncia\s+a\s+(?:cualquier|todo)\s+(?:reclamo|recurso|derecho)|asume\s+todas\s+las\s+pérdidas|indemnizará\s+y\s+mantendrá\s+indemne|recurso\s+único\s+y\s+exclusivo|à\s+sa\s+seule\s+discrétion|unilatéralement|à\s+tout\s+moment\s+sans\s+préavis|décline\s+toute\s+responsabilité|renonce\s+à\s+tout\s+recours|supporte\s+toutes\s+les\s+pertes)\b",
        # DE
        r"\b(?:nach\s+(?:eigenem|freiem|alleinigem)\s+(?:ermessen|belieben)|einseitig|jederzeit\s+ohne\s+(?:vorankündigung|ankündigung|angabe\s+von\s+gründen)|behält\s+sich\s+das\s+recht\s+vor|übernimmt\s+(?:keine|keinerlei)\s+haftung|haftung\s+ist\s+ausgeschlossen|haftung\s+wird\s+auf\s+[^.;]{0,25}begrenzt|schließt\s+[^.;]{0,35}aus|nur\s+[^.;]{1,30}\b(?:darf|kann|ist\s+berechtigt)|gilt\s+nur\s+für\s+(?:den|die|das)|verzichtet\s+auf\s+(?:alle|jegliche|sämtliche)\s+(?:ansprüche|rechtsmittel)|trägt\s+alle\s+(?:verluste|risiken|kosten)|schuldet\s+nichts|freizustellen\s+und\s+schadlos\s+zu\s+halten|einzige\s+und\s+ausschließliche\s+abhilfe|vertragsstrafe)\b",
        # ZH & AR
        r"(?:单方面|自行决定|随时修改|不承担任何责任|免除一切责任|放弃一切索赔|承担全部损失|배상|بإرادته\s+المنفردة|دون\s+إشعار\s+مسبق|لا\s+يتحمل\s+أي\s+مسؤولية|يتنازل\s+عن\s+جميع\s+المطالبات|يتحمل\s+كافة\s+الخسائر)",
    ]
    covert_prescriptions = sum(len(re.findall(p, lower_text)) for p in covert_patterns)

    # Mutuality guard (v1.1.6):
    # To prevent mutual commitments (indemnity, reciprocal hold-harmless, mutual releases)
    # from being flagged as covert prescriptions, the mutuality marker MUST occupy subject
    # position governing the reciprocal commitment ("each party shall indemnify", "beide Parteien
    # stellen ... frei", "каждая сторона обязуется возместить").
    # Subordinate clauses where another nominal subject follows "that" (e.g., "Each party agrees
    # that Customer shall indemnify Vendor") do NOT qualify, but coreference pronouns ("that it / they")
    # and inclusive parentheticals ("Each party, including X and Y, shall...") are preserved.
    mutual_subject_obligation_patterns = [
        # EN: (each/either/both party/parties) ... (shall indemnify | agree to indemnify | hold harmless | shall not be liable)
        r"\b(?:each\s+(?:of\s+the\s+)?part(?:y|ies)|either\s+party|both\s+parties|the\s+parties|neither\s+party)\b"
        r"(?:,\s*including\b[^,]{1,60},)?"
        r"(?![^.;]{0,45}\b(?:that\s+(?:the\s+|a\s+|an\s+)?(?!it\b|they\b|such\s+part\w*\b)[a-z]{3,}|заказчик\w*|исполнител\w*|покупател\w*|поставщик\w*|customer|vendor|client|provider|buyer|seller|licensor|licensee)\b)"
        r"[^.;]{0,45}\b(?:shall\s+(?:not\s+be\s+liable|be\s+liable|indemnify|mutually\s+indemnify)|agrees?\s+(?:that\s+(?:it|they|such\s+party)\s+shall\s+indemnify|to\s+indemnify)|hold\s+harmless|hold\s+[^.;]{0,20}\s+harmless|disclaim\w*)\b",
        r"\b(?:mutually|reciprocally)\b[^.;]{0,30}\b(?:indemnify|hold\s+harmless)\b",
        r"\b(?:indemnify|hold\s+harmless)\b[^.;]{0,35}\b(?:each\s+other|one\s+another)\b",
        # RU & KK:
        r"\b(?:каждая\s+(?:из\s+)?сторон\w*|обе\s+стороны|стороны)\b(?![^.;]{0,45}\b(?:что\s+(?!она\b|они\b)[а-яё]{3,}|заказчик\w*|исполнител\w*|покупател\w*|поставщик\w*|клиент\w*|арендатор\w*|арендодател\w*)\b)[^.;]{0,40}\b(?:обязан\w*\s+возместить|обязу\w+\s+возместить|возмеща\w+|не\s+нес\w+\s+ответственност\w+|освобожда\w+|взаимно\s+возмеща\w+)\b",
        r"\b(?:взаимно|друг\s+другу)\b[^.;]{0,30}\b(?:возмеща\w+|освобожда\w+)\b",
        r"\b(?:әр\s+тарап\w*|екі\s+тарап\w*)\b(?![^.;]{0,45}\b(?:тапсырыс\w*|орындаушы\w*)\b)[^.;]{0,45}\b(?:өтейді|жауапты\s+болмайды)\b",
        # DE:
        r"\b(?:jede\s+partei|beide\s+parteien)\b(?![^.;]{0,45}\b(?:dass\s+(?!sie\b)[a-zäöüß]{3,}|auftraggeber|auftragnehmer|kunde|anbieter)\b)[^.;]{0,70}\b(?:stellt|übernimmt|haftet|verpflichtet)\b[^.;]{0,50}\b(?:frei|haftung|schadlos)?",
        r"\b(?:gegenseitig|wechselseitig)\b[^.;]{0,30}\b(?:freistell\w*|haft\w*)\b",
        # ES & FR:
        r"\b(?:cada\s+parte|ambas\s+partes)\b(?![^.;]{0,45}\b(?:que\s+(?!ella\b|ellas\b)[a-záéíóúñ]{3,}|cliente|proveedor)\b)[^.;]{0,45}\b(?:indemnizará|mantendrán?\s+indemne|no\s+será\s+responsable)\b",
        r"\b(?:chaque\s+partie|les\s+deux\s+parties)\b(?![^.;]{0,45}\b(?:que\s+(?!elle\b|elles\b)[a-zàèùêîôûç]{3,}|client|fournisseur)\b)[^.;]{0,45}\b(?:indemnisera|dégage\s+de\s+responsabilité)\b",
    ]
    compiled_mutual = [re.compile(p, re.IGNORECASE) for p in mutual_subject_obligation_patterns]
    reciprocable_obligation = re.compile(
        r"\b(?:shall\s+indemnify|agrees\s+to\s+indemnify|hold\s+(?:[^.;]{1,25}\s+)?harmless|shall\s+not\s+be\s+liable|no\s+liability|"
        r"liquidated\s+damages|penalty\s+of|возместить\s+[^.;]{0,25}убытки|штраф\s+в\s+размере|неустойк\w+|"
        r"ответственность\s+[^.;]{0,25}ограничивается|indemnizará\s+y\s+mantendrá\s+indemne|"
        r"freizustellen\s+und\s+schadlos\s+zu\s+halten|haftung\s+wird\s+auf\s+[^.;]{0,25}begrenzt|vertragsstrafe)\b"
    )
    mutual_reciprocal_matches = 0
    for s in sentences_list:
        sl = s.lower()
        if any(p.search(sl) for p in compiled_mutual):
            mutual_reciprocal_matches += len(reciprocable_obligation.findall(sl))
    covert_prescriptions = max(0, covert_prescriptions - mutual_reciprocal_matches)

    bilateral_patterns = [
        r"\b(?:mutually\s+agreed|mutual\s+consent|both\s+parties\s+may|either\s+party\s+may|each\s+party\s+may|each\s+party\s+shall\s+indemnify\s+the\s+other|reciprocal|взаимн\w+\s+согласи\w+|обе\s+стороны|каждая\s+из\s+сторон\s+вправе|по\s+соглашению\s+сторон|екі\s+тарап|тараптардың\s+келісімі\s+бойынша|mutuo\s+acuerdo|ambas\s+partes|cualquiera\s+de\s+las\s+partes|d'un\s+commun\s+accord|chaque\s+partie\s+peut|gegenseitig\w*|beide\s+parteien|jede\s+partei\s+ist\s+berechtigt|im\s+gegenseitigen\s+einvernehmen)\b",
        r"(?:双方同意|双方均可|باتفاق\s+الطرفين|لكل\s+طرف\s+الحق)",
    ]
    bilateral_rights = sum(len(re.findall(p, lower_text)) for p in bilateral_patterns)

    # Epistemic / speculative modals vs anchored facts
    speculative_patterns = [
        r"\b(?:may\s+be\b|might\b|could\b|should\b|would\s+never|potentially|possibly|conceivably|approximately|believe|expect|anticipate|project|unprecedented|phenomenal|extraordinary|commercially\s+reasonable\s+efforts|reasonable\s+efforts|best\s+efforts|good\s+faith\s+efforts|endeavor\s+to|strive\s+to|as\s+practicable|where\s+feasible)\b",
        r"\b(?:может\s+быть|возможно|вероятно|предположительно|ожидает\w*|полагаем|надеемся|приложит\s+[^.;]{0,25}усилия|постарается|по\s+мере\s+возможности|беспрецедентн\w+|уникальн\w+|феноменальн\w+|временно|мүмкін|ықтимал|ақылға\s+қонымды\s+күш-жігер)\b",
        r"\b(?:podría|podrían|quizás|tal\s+vez|posiblemente|probablemente|esperamos|creemos|esfuerzos\s+(?:comercialmente\s+)?razonables|mejores\s+esfuerzos|en\s+la\s+medida\s+de\s+lo\s+posible|sin\s+precedentes|fenomenal|extraordinario|pourrait|pourraient|peut-être|efforts\s+raisonnables)\b",
        r"\b(?:könnte|könnten|möglicherweise|vielleicht|voraussichtlich|wahrscheinlich|wir\s+glauben|wir\s+erwarten|wirtschaftlich\s+angemessene\s+anstrengungen|nach\s+besten\s+kräften|bemühen|beispiellos|phänomenal|außergewöhnlich)\b",
        r"(?:合理努力|最大努力|可能|预计|前所未有|جهود\s+معقولة|من\s+المحتمل|نتوقع|غير\s+مسبوق)",
    ]
    speculative_modals = sum(len(re.findall(p, lower_text)) for p in speculative_patterns)

    anchored_facts = len(
        re.findall(
            r"(?:\b\d+(?:[.,]\d+)?%|\$\s*\d+(?:[.,]\d+)?|\b\d+(?:[.,]\d+)?\s*(?:usd|eur|gbp|rub|kzt|тенге|руб\w*|дней|дня|часов|месяц\w*|күн|теңге|days|hours|months|years|units|días|horas|meses|jours|mois|tage|stunden|monate|€|₸|£|¥|元|天|يوم|ريال|درهم)\b|\b\d{1,2}:\d{2}\b|\b20\d{2}-\d{2}-\d{2}\b)",
            lower_text,
        )
    )

    # Declared rights & Hohfeldian duty/void check
    total_declared_rights = len(
        re.findall(
            r"\b(?:is\s+entitled\s+to|has\s+the\s+right\s+to|shall\s+receive|availability|service\s+continuity|имеет\s+право|вправе\s+требовать|гарантирует\w*|работоспособност\w+|бесперебойн\w+|құқығы\s+бар|кепілдік\s+береді|tiene\s+derecho\s+a|garantiza\s+la\s+disponibilidad|a\s+le\s+droit\s+de|hat\s+anspruch\s+auf|ist\s+berechtigt|verfügbarkeit)\b|(?:享有权利|保证可用性|يحق\s+له|يضمن)",
            lower_text,
        )
    )
    void_carveouts = len(
        re.findall(
            r"\b(?:however|provided\s+that|subject\s+to\s+[^.;]{0,20}discretion|sole\s+discretion|at\s+(?:its|his|her)\s+(?:sole\s+|absolute\s+)?pleasure|shall\s+be\s+excluded|not\s+liable|owes\s+nothing|однако|при\s+условии|по\s+усмотрению|исключается\s+из|ограничивается|алайда|өз\s+қалауы\s+бойынша|sin\s+embargo|a\s+su\s+sola\s+discreción|quedará\s+excluido|toutefois|à\s+sa\s+seule\s+discrétion|jedoch|nach\s+eigenem\s+ermessen|ausgeschlossen)\b|(?:但|自行决定|不承担|إلا\s+أنه|بإرادته\s+المنفردة)",
            lower_text,
        )
    )
    operative_rights_with_duty = max(0, total_declared_rights - void_carveouts)

    # Ambiguous / diluted terms of art (Garner / Black's Law & structural equivalents)
    ambiguous_patterns = [
        r"\b(?:commercially\s+reasonable\s+efforts|reasonable\s+efforts|best\s+efforts|good\s+faith\s+efforts|endeavor\s+to|as\s+soon\s+as\s+practicable|where\s+feasible|sole\s+discretion|absolute\s+discretion|at\s+(?:its|his|her|their)\s+(?:sole\s+|absolute\s+)?(?:pleasure|will|discretion)|in\s+its\s+sole\s+judgment|deems\s+appropriate|at\s+any\s+time\s+without\s+notice|owes\s+nothing|waives\s+(?:all|every|any)\s+(?:claim\w*|remed\w*)|bears\s+all\s+losses|sole\s+and\s+exclusive\s+remedy|shall\s+be\s+excluded|material\s+adverse\s+effect|to\s+the\s+maximum\s+extent\s+permitted)\b",
        r"\b(?:разумные\s+(?:коммерческие\s+)?усилия|максимальные\s+усилия|по\s+мере\s+возможности|в\s+кратчайшие\s+сроки|по\s+(?:своему\s+)?усмотрению|в\s+одностороннем\s+порядке|без\s+объяснения\s+причин|без\s+предварительного\s+уведомления|исключительным\s+средством\s+защиты|существенное\s+неблагоприятное\s+изменение|өз\s+қалауы\s+бойынша|біржақты\s+тәртіппен|ақылға\s+қонымды\s+күш-жігер)\b",
        r"\b(?:esfuerzos\s+(?:comercialmente\s+)?razonables|mejores\s+esfuerzos|a\s+su\s+(?:sola|exclusiva)\s+discreción|sin\s+previo\s+aviso|en\s+la\s+medida\s+de\s+lo\s+posible|recurso\s+único\s+y\s+exclusivo|efecto\s+adverso\s+significativo|à\s+sa\s+seule\s+discrétion|sans\s+préavis|efforts\s+raisonnables)\b",
        r"\b(?:wirtschaftlich\s+angemessene\s+anstrengungen|angemessene\s+bemühungen|nach\s+besten\s+kräften|nach\s+(?:eigenem|freiem|alleinigem)\s+(?:ermessen|belieben)|ohne\s+vorankündigung|soweit\s+machbar|einzige\s+und\s+ausschließliche\s+abhilfe|wesentliche\s+nachteilige\s+auswirkung)\b",
        r"(?:合理努力|自行决定|随时修改|放弃一切索赔|بإرادته\s+المنفردة|جهود\s+معقولة|دون\s+إشعار\s+مسبق)",
    ]
    ambiguous_terms = sum(len(re.findall(p, lower_text)) for p in ambiguous_patterns)

    # General contractual/financial domain vocabulary check (for Hamlet Guard)
    general_domain_vocab = len(
        re.findall(
            r"\b(?:"
            # EN
            r"part(?:y|ies)|agreements?|contracts?|vendors?|customers?|clients?|providers?|suppliers?|licens\w*|fees?|payments?|prices?|pricing|sla|services?|liabilit\w*|indemn\w*|warrant\w*|remed\w*|clauses?|terminat\w*|notice|recourse|breach\w*|damages|audit\w*|ledger|escrow|revenue|ebitda|quarter\w*|shareholder\w*|dividend\w*"
            # RU
            r"|договор\w*|сторон\w*|заказчик\w*|исполнител\w*|поставщик\w*|арендатор\w*|арендодател\w*|оплат\w*|ответственност\w*|убытк\w*|штраф\w*|неустойк\w*|расторж\w*|претензи\w*|выручк\w*|дивиденд\w*"
            # KK
            r"|шарт\w*|келісім\w*|тарап\w*|төле\w*|жауапкершілі\w*|орындаушы\w*|тапсырыс\w*|өнім\w*|айыппұл\w*"
            # ES
            r"|contrat\w*|proveedor\w*|client\w*|arrendat\w*|tarifa\w*|pago\w*|responsabilidad\w*|indemniza\w*|rescisi\w*|resoluci\w*|incumplimiento\w*|garant\w*|cláusula\w*|penalidad\w*"
            # FR
            r"|fournisseur\w*|prestataire\w*|paiement\w*|responsabilité\w*|résiliation\w*|indemnit\w*|préavis|pénalit\w*|redevance\w*"
            # DE (compounds: Vertragspartei, Auftragnehmer, Schadensersatz, Kündigungsfrist, ...)
            r"|vertrag\w*|vereinbarung\w*|anbieter\w*|auftragnehmer\w*|auftraggeber\w*|lieferant\w*|kunde\w*|kunden\w*|zahlung\w*|vergütung\w*|entgelt\w*|haftung\w*|gebühr\w*|kündig\w*|schadens\w*|gewährleist\w*|leistung\w*|frist\w*|vertragsstrafe\w*"
            r")\b"
            # ZH / AR (no word boundaries)
            r"|(?:合同|协议|甲方|乙方|供应商|客户|付款|费用|价格|责任|赔偿|賠償|违约|解除|终止|عقد|الطرف|مسؤولية|دفع|تعويض|إنهاء)",
            lower_text,
        )
    )

    # Stanford SDRI components
    epe_prefixes = (
        "unprecedented", "phenomenal", "extraordinary", "fantastic", "incredible", "revolutionary",
        "беспрецедент", "уникальн", "феноменальн", "колоссальн", "невероятн",
        "extraordinari", "fenomenal", "increíble", "revolucionari", "exceptionnel",
        "beispiellos", "phänomenal", "außergewöhnlich", "fantastisch", "einzigartig",
    )
    n_epe = sum(1 for w in lower_words if w.startswith(epe_prefixes))
    if "never been stronger" in lower_text or "лучший в истории" in lower_text or "sin precedentes" in lower_text or "前所未有" in lower_text:
        n_epe += 1

    sg_pronouns = {"i", "my", "me", "mine", "я", "мне", "меня", "мой", "моя", "мои", "мен", "менің", "yo", "mi", "mis", "je", "mon", "ma", "ich", "mein", "meine", "mir", "mich", "我"}
    coll_pronouns = {"we", "our", "us", "ours", "мы", "наш", "наша", "наши", "нас", "нам", "команда", "біз", "біздің", "nosotros", "nuestro", "nuestra", "nous", "notre", "wir", "unser", "unsere", "uns", "我们"}
    n_1st_sg = sum(1 for w in lower_words if w in sg_pronouns)
    n_coll = sum(1 for w in lower_words if w in coll_pronouns)

    weak_modals_set = {
        "should", "might", "could", "possibly", "potentially", "believe", "expect", "hope",
        "ожидает", "ожидаем", "возможно", "вероятно", "надеемся", "полагаем", "мүмкін",
        "podría", "podrían", "posiblemente", "probablemente", "esperamos", "creemos", "pourrait",
        "könnte", "könnten", "möglicherweise", "voraussichtlich", "wahrscheinlich", "glauben", "erwarten",
    }
    strong_modals_set = {
        "will", "did", "must", "achieved", "completed", "delivered", "geleistet",
        "обязуется", "гарантирует", "выполнили", "завершили", "достигли",
        "logramos", "completamos", "garantiza", "cumplió",
        "haben", "erreicht", "abgeschlossen", "garantiert", "verpflichtet",
    }
    n_weak = sum(1 for w in lower_words if w in weak_modals_set)
    n_strong = sum(1 for w in lower_words if w in strong_modals_set)

    gen_hedges_set = {
        "certain", "transitional", "generally", "obviously", "clearly", "standard",
        "некоторые", "определенные", "временные", "очевидно", "общеизвестно",
        "ciertos", "ciertas", "transicionales", "obviamente", "claramente",
        "gewisse", "bestimmte", "vorübergehend", "offensichtlich", "bekanntlich",
    }
    n_gen = sum(1 for w in lower_words if w in gen_hedges_set)

    total_domain_markers = (
        general_domain_vocab
        + covert_prescriptions
        + bilateral_rights
        + total_declared_rights
        + ambiguous_terms
        + anchored_facts
        + n_epe
    )

    res = compute_scorecard(
        words=words_count,
        sentences=sentences_count,
        syllables=syllables_count,
        total_predicates=total_predicates,
        deleted_predicates=deleted_predicates,
        chains_ge_3=chains_ge_3,
        covert_prescriptions=covert_prescriptions,
        bilateral_rights=bilateral_rights,
        speculative_modals=speculative_modals,
        anchored_facts=anchored_facts,
        operative_rights_with_duty=operative_rights_with_duty,
        total_declared_rights=total_declared_rights,
        ambiguous_terms=ambiguous_terms,
        total_operative_clauses=sentences_count,
        n_epe=n_epe,
        n_1st_sg=n_1st_sg,
        n_coll=n_coll,
        n_weak=n_weak,
        n_strong=n_strong,
        n_gen=n_gen,
        domain_markers=total_domain_markers,
    )
    # Honest coverage disclosure: the CLI only sees phrasings that its rule set knows.
    triggered = {
        "unilateral_or_disclaimer_patterns": covert_prescriptions,
        "diluted_term_of_art_patterns": ambiguous_terms,
        "agentless_passives": deleted_predicates,
        "genitive_chains_ge_3": chains_ge_3,
        "speculative_modals": speculative_modals,
        "promotional_hyperbole": n_epe,
        "evidential_hedges": n_gen,
    }
    res["pattern_coverage"] = {
        "patterns_triggered_total": sum(triggered.values()),
        "by_family": triggered,
        "note": (
            "Regex/lexicon scanner: only known phrasings are counted. Asymmetric clauses worded "
            "outside the rule set are NOT visible to the CLI; a Clean CSIS is not evidence of balance."
        ),
    }
    return res


def format_markdown_table(res: Dict[str, Any]) -> str:
    m = res["metrics"]
    z = res["zones"]
    lines = [
        "### Deterministic Quantitative Scorecard (`bin/subtext_calc.py` v1.1.6)",
        "",
    ]
    if res.get("domain_relevance", "").startswith("LOW_DOMAIN_SIGNAL"):
        lines.append(f"> **Warning:** `{res['domain_relevance']}`")
        lines.append("")
    lines.extend(
        [
            "| Metric | Value | Clean Baseline | Alert Threshold | Status |",
            "| :--- | :---: | :---: | :---: | :--- |",
            f"| **CSIS (CVS)** | **{m['CSIS']}{'%' if isinstance(m['CSIS'], (int, float)) else ''}** | >= 75.0% | < 50.0% | {z['CSIS']} |",
            f"| **ADI** | {m['ADI']} | <= 0.20 | > 0.28 | {z['ADI']} |",
            f"| **GSD** | {m['GSD']} | <= 0.25 | > 0.35 | {z['GSD']} |",
            f"| **CPR** | {m['CPR']} | <= 0.30 | > 0.50 | {z['CPR']} |",
            f"| **MFR** | {m['MFR']} | <= 0.50 | > 1.00 | {z['MFR']} |",
            f"| **FMRE** | {m['FMRE']} | >= 50.0 | < 30.0 | {z['FMRE']} |",
            f"| **HIR** | {m['HIR']} | >= 0.80 | < 0.60 | {z['HIR']} |",
            f"| **TAD** | {m['TAD']} | <= 0.05 | > 0.15 | {z['TAD']} |",
            f"| **SDRI** | {m['SDRI']} | <= 0.35 | > 0.65 | {z['SDRI']} |",
        ]
    )
    cov = res.get("pattern_coverage")
    if cov:
        lines.append("")
        lines.append(
            f"> **Pattern coverage:** {cov['patterns_triggered_total']} known risk pattern(s) triggered. "
            "Phrasings outside the rule set are not visible to the calculator; "
            "a Clean CSIS means only that no known pattern fired, not that the text is balanced."
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Subtext Engine Deterministic Metric Calculator (Pattern & Lexicon Scanner v1.1.6)"
    )
    parser.add_argument("--text", type=str, help="Raw input text to tokenize and score")
    parser.add_argument("--file", type=str, help="Path to input text file to tokenize and score")
    parser.add_argument("--counts-json", type=str, help="JSON string of explicit constituent counts")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format")
    args = parser.parse_args()

    if args.counts_json:
        data = json.loads(args.counts_json)
        res = compute_scorecard(**data)
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            res = analyze_raw_text(f.read())
    elif args.text is not None:
        res = analyze_raw_text(args.text)
    else:
        res = analyze_raw_text(sys.stdin.read())

    if args.format == "markdown":
        print(format_markdown_table(res))
    else:
        print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
