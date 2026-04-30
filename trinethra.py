import re
import json
import sys
from typing import Any, Dict, List

KPI_PATTERNS = {
    "Lead Generation": [
        r"new schools",
        r"new customers",
        r"new leads",
        r"prospect",
        r"acquire.*customer",
        r"finds new",
        r"identify new",
    ],
    "Lead Conversion": [
        r"closed .* account",
        r"closed .* deal",
        r"signed .* customer",
        r"won .* business",
        r"converted .* lead",
        r"onboarded .* customer",
        r"became paying",
    ],
    "Upselling": [
        r"bigger quantities",
        r"increase.*order",
        r"larger order",
        r"upsell",
        r"more to existing",
    ],
    "Cross-selling": [
        r"packaging along with",
        r"additional product",
        r"cross[- ]sell",
        r"sell .* along with",
        r"add.*on",
    ],
    "NPS": [
        r"happy",
        r"satisfied",
        r"fewer complaints",
        r"customer satisfaction",
        r"complaint.*down",
    ],
    "PAT": [
        r"reduced waste",
        r"costs .* down",
        r"margin",
        r"profit",
        r"profitability",
        r"save.*cost",
    ],
    "TAT": [
        r"dispatch is faster",
        r"turnaround time",
        r"deadlines",
        r"on time",
        r"faster .* dispatch",
        r"delay.*down",
        r"lead time",
    ],
    "Quality": [
        r"rejection rate",
        r"defect",
        r"complaint",
        r"quality",
        r"returns",
        r"reject",
    ],
}

SYSTEMS_PATTERNS = [
    r"tracker",
    r"checklist",
    r"sop",
    r"standard operating procedure",
    r"process",
    r"template",
    r"dashboard",
    r"report",
    r"analysis",
    r"risk alert",
    r"study",
    r"system",
    r"audit",
    r"log",
    r"document",
    r"routine",
    r"workflow",
]

PROBLEM_IDENTIFICATION_PATTERNS = [
    r"noticed",
    r"identified",
    r"saw that",
    r"realized",
    r"found that",
    r"traced.*to",
    r"root cause",
    r"why .* happening",
    r"understand.*problem",
]

EXECUTION_PATTERNS = [
    r"calls",
    r"call",
    r"meets",
    r"meeting",
    r"follow up",
    r"follow-up",
    r"updates",
    r"report",
    r"prepare",
    r"send.*whatsapp",
    r"email",
    r"schedule",
    r"daily",
    r"weekly",
    r"on the floor",
    r"present",
    r"attend",
    r"help with",
    r"support",
    r"assist",
]

NEGATIVE_PATTERNS = [
    r"doesn't really push back",
    r"does not push back",
    r"only when",
    r"only if",
    r"needs constant",
    r"needs a lot of direction",
    r"sloppy",
    r"inconsistent",
    r"not motivated",
    r"not interested",
    r"can't",
    r"don't know how",
    r"spends too much time",
]

HELPFULNESS_PATTERNS = [
    r"handles all my calls",
    r"handles my calls",
    r"does my calls",
    r"takes my calls",
    r"handles my emails",
    r"does my meetings",
    r"my right hand",
    r"does everything for me",
    r"runs my meetings",
    r"I don't know how we managed before",
]

PRESENCE_PATTERNS = [
    r"always on the floor",
    r"always there",
    r"present all the time",
    r"on the floor all day",
]

CHANGE_MANAGEMENT_PATTERNS = [
    r"workers.*adopt",
    r"team.*adopt",
    r"resistance",
    r"push back",
    r"convince",
    r"train",
    r"prepare them",
    r"dealing with.*team",
    r"shopfloor",
    r"floor team",
    r"workers",
    r"supervisors",
    r"operators",
    r"people.*use",
]

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def find_sentences(text: str) -> List[str]:
    return [s.strip() for s in re.split(r"(?<=[\.\?\!])\s+", text) if s.strip()]


def match_any(text: str, patterns: List[str]) -> bool:
    normalized = normalize(text)
    return any(re.search(pattern, normalized) for pattern in patterns)


def extract_evidence(transcript: str) -> List[Dict[str, Any]]:
    sentences = find_sentences(transcript)
    evidence: List[Dict[str, Any]] = []

    for sentence in sentences:
        normalized = normalize(sentence)
        signals: List[str] = []
        if match_any(normalized, SYSTEMS_PATTERNS):
            signals.append("systems")
        if match_any(normalized, PROBLEM_IDENTIFICATION_PATTERNS):
            signals.append("problem_identification")
        if match_any(normalized, EXECUTION_PATTERNS):
            signals.append("execution")
        if match_any(normalized, NEGATIVE_PATTERNS):
            signals.append("negative")
        if match_any(normalized, HELPFULNESS_PATTERNS):
            signals.append("helpfulness_bias")
        if match_any(normalized, PRESENCE_PATTERNS):
            signals.append("presence_bias")
        if match_any(normalized, CHANGE_MANAGEMENT_PATTERNS):
            signals.append("change_management")

        if signals:
            interpretation_parts = []
            if "systems" in signals:
                interpretation_parts.append(
                    "Evidence of systems or process work was mentioned."
                )
            if "problem_identification" in signals:
                interpretation_parts.append(
                    "Shows independent problem identification beyond assigned tasks."
                )
            if "execution" in signals and "systems" not in signals:
                interpretation_parts.append(
                    "This is visible task execution or operational support."
                )
            if "negative" in signals:
                interpretation_parts.append(
                    "Supervisor flags performance or initiative concerns."
                )
            if "helpfulness_bias" in signals:
                interpretation_parts.append(
                    "This may be task absorption rather than durable systems building."
                )
            if "presence_bias" in signals:
                interpretation_parts.append(
                    "Presence on the floor is noted, but it may not imply long-term systems value."
                )
            if "change_management" in signals:
                interpretation_parts.append(
                    "Mentions the Fellow's work with the team or adoption challenges."
                )

            evidence.append(
                {
                    "quote": sentence,
                    "signal": "positive" if "negative" not in signals else "negative",
                    "dimension": (
                        "systems_building"
                        if "systems" in signals
                        else "execution"
                        if "execution" in signals
                        else "change_management"
                    ),
                    "interpretation": " ".join(interpretation_parts),
                }
            )

    return evidence


def map_kpis(transcript: str) -> List[Dict[str, str]]:
    kpi_mapping: List[Dict[str, str]] = []
    for sentence in find_sentences(transcript):
        normalized_sentence = normalize(sentence)
        for kpi, patterns in KPI_PATTERNS.items():
            if any(re.search(pattern, normalized_sentence) for pattern in patterns):
                system_or_personal = (
                    "system"
                    if match_any(normalized_sentence, SYSTEMS_PATTERNS)
                    else "personal"
                )
                kpi_mapping.append(
                    {
                        "kpi": kpi,
                        "evidence": sentence,
                        "systemOrPersonal": system_or_personal,
                    }
                )
                break
    return kpi_mapping


def identify_gaps(evidence: List[Dict[str, Any]], kpi_mapping: List[Dict[str, str]], transcript: str) -> List[Dict[str, str]]:
    normalized = normalize(transcript)
    has_execution = any(e["dimension"] == "execution" for e in evidence)
    has_systems = any(e["dimension"] == "systems_building" for e in evidence)
    has_kpi = bool(kpi_mapping)
    has_change = match_any(normalized, CHANGE_MANAGEMENT_PATTERNS)

    gaps: List[Dict[str, str]] = []
    if not has_execution:
        gaps.append(
            {
                "dimension": "execution",
                "detail": "No clear evidence of reliable task completion, follow-up, or execution was mentioned.",
            }
        )
    if not has_systems:
        gaps.append(
            {
                "dimension": "systems_building",
                "detail": "No durable system, tracker, SOP, template, or process was described as surviving the Fellow's departure.",
            }
        )
    if not has_kpi:
        gaps.append(
            {
                "dimension": "kpi_impact",
                "detail": "The supervisor did not connect the Fellow's work to any measurable business outcome like speed, quality, cost, or customer satisfaction.",
            }
        )
    if not has_change:
        gaps.append(
            {
                "dimension": "change_management",
                "detail": "No evidence was provided about how the Fellow worked with the floor team, managed resistance, or drove adoption of new processes.",
            }
        )
    return gaps


def build_follow_up_questions(gaps: List[Dict[str, str]]) -> List[Dict[str, str]]:
    follow_ups: List[Dict[str, str]] = []
    for gap in gaps:
        if gap["dimension"] == "systems_building":
            follow_ups.append(
                {
                    "question": "If the Fellow took a week off, what would stop working and what would keep running on its own?",
                    "targetGap": "systems_building",
                    "lookingFor": "Whether the Fellow created self-sustaining systems rather than personal task work.",
                }
            )
        elif gap["dimension"] == "change_management":
            follow_ups.append(
                {
                    "question": "How do the floor workers respond when the Fellow asks them to do something differently?",
                    "targetGap": "change_management",
                    "lookingFor": "Whether the Fellow can get experienced workers to adopt new processes and handle resistance.",
                }
            )
        elif gap["dimension"] == "execution":
            follow_ups.append(
                {
                    "question": "Can you describe a typical day and whether the Fellow finishes tasks without being reminded?",
                    "targetGap": "execution",
                    "lookingFor": "Evidence of reliable task completion and independent follow-up.",
                }
            )
        elif gap["dimension"] == "kpi_impact":
            follow_ups.append(
                {
                    "question": "What business outcome improved because of the Fellow's work?",
                    "targetGap": "kpi_impact",
                    "lookingFor": "A measurable connection to speed, quality, cost, satisfaction, or revenue.",
                }
            )
    return follow_ups


def score_transcript(transcript: str) -> Dict[str, Any]:
    normalized = normalize(transcript)
    evidence = extract_evidence(transcript)
    kpi_mapping = map_kpis(transcript)
    gaps = identify_gaps(evidence, kpi_mapping, transcript)
    follow_up_questions = build_follow_up_questions(gaps)

    has_negative = match_any(normalized, NEGATIVE_PATTERNS)
    has_helpfulness_bias = match_any(normalized, HELPFULNESS_PATTERNS)
    has_presence_bias = match_any(normalized, PRESENCE_PATTERNS)
    has_systems = any(e["dimension"] == "systems_building" for e in evidence)
    has_problem = match_any(normalized, PROBLEM_IDENTIFICATION_PATTERNS)
    has_execution = any(e["dimension"] == "execution" for e in evidence)
    has_change = match_any(normalized, CHANGE_MANAGEMENT_PATTERNS)

    score = 6
    label = "Reliable and Productive"
    band = "Productivity"
    confidence = "medium"
    justification_parts: List[str] = []

    if has_negative:
        score = 4
        label = "Careless and Inconsistent"
        band = "Productivity"
        justification_parts.append(
            "Supervisor includes negative performance or initiative concerns."
        )
    elif not has_execution and not has_systems:
        score = 3
        label = "Motivated but Directionless"
        band = "Need Attention"
        justification_parts.append(
            "The transcript lacks evidence of execution and systems building."
        )
    elif has_systems:
        score = 7
        label = "Problem Identifier"
        band = "Performance"
        justification_parts.append(
            "The supervisor describes systems work or process improvements."
        )
        if has_problem:
            score = max(score, 7)
            justification_parts.append(
                "There is evidence of independent problem identification."
            )
        if has_change:
            score = max(score, 8)
            label = "Problem Solver"
            band = "Performance"
            justification_parts.append(
                "The Fellow also worked with the team or on adoption."
            )
        if kpi_mapping:
            score = max(score, 8)
            label = "Problem Solver"
            justification_parts.append(
                "Business outcomes are connected to the Fellow's work."
            )
        if has_helpfulness_bias and not has_problem and not has_change:
            score = min(score, 6)
            justification_parts.append(
                "This may be task absorption rather than durable systems building."
            )
        if score >= 8 and ("tracker" in normalized or "system" in normalized or "dashboard" in normalized):
            score = max(score, 9)
            label = "Innovative and Experimental"
            justification_parts.append(
                "The work description suggests a tool or workflow built by the Fellow."
            )
    else:
        if has_helpfulness_bias and not has_systems:
            score = 5
            label = "Consistent Performer"
            band = "Productivity"
            justification_parts.append(
                "The Fellow is absorbing requests and helping operationally."
            )
        elif has_execution:
            score = 6
            label = "Reliable and Productive"
            band = "Productivity"
            justification_parts.append(
                "Task execution is described reliably, but no durable system is evident."
            )
        else:
            score = 4
            label = "Careless and Inconsistent"
            band = "Productivity"
            justification_parts.append(
                "Execution is weak or only partially described."
            )

    if score >= 9 and has_change and kpi_mapping:
        label = "Exceptional Performer"
        band = "Performance"
        justification_parts.append(
            "The Fellow appears to build systems, drive adoption, and deliver measurable impact."
        )

    if score == 6 and has_helpfulness_bias and not has_systems:
        justification_parts.append(
            "High praise is likely due to task absorption rather than a self-sustaining process."
        )
    if score == 7 and not has_change:
        justification_parts.append(
            "The score is based on system identification but change management evidence is missing."
        )

    if has_presence_bias and score < 7:
        justification_parts.append(
            "Strong presence on the floor is noted, but it does not by itself raise the score."
        )

    if score <= 3 and not has_systems:
        band = "Need Attention"
        label = "Motivated but Directionless" if score == 3 else label

    return {
        "score": {
            "value": score,
            "label": label,
            "band": band,
            "justification": " ".join(justification_parts) if justification_parts else "Scored based on the presence of execution, systems building, and business impact evidence.",
            "confidence": confidence,
        },
        "evidence": evidence,
        "kpiMapping": kpi_mapping,
        "gaps": gaps,
        "followUpQuestions": follow_up_questions,
    }


def main() -> None:
    if len(sys.argv) > 1:
        transcript = " ".join(sys.argv[1:])
        result = score_transcript(transcript)
        print(json.dumps(result, indent=2))
    else:
        print("This module provides a transcript scoring API for Fellow assessments.")
        print("Usage: python trinethra.py 'transcript text here'")
        print("Use score_transcript(transcript_text) from Python to get structured output.")


if __name__ == "__main__":
    main()
