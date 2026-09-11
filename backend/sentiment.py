"""Explainable lexicon-and-rules sentiment analysis engine."""

from backend.config import (INTENSIFIER_MULTIPLIERS, INTENSIFIER_WINDOW,
                            NEGATION_MULTIPLIER, NEGATION_WINDOW,
                            NEGATIVE_THRESHOLD, POSITIVE_THRESHOLD, STRONG_SCORE)
from backend.lexicon import NEGATIONS, SENTIMENT_LEXICON
from backend.preprocessing import preprocess


def _recent_modifier(tokens: list[str], index: int, choices: set[str], window: int) -> str | None:
    """Return the closest modifier in the configurable window before a token."""
    start = max(0, index - window)
    for token in reversed(tokens[start:index]):
        if token in choices:
            return token
    return None


def _label(score: float) -> str:
    if score > POSITIVE_THRESHOLD:
        return "Positive"
    if score < NEGATIVE_THRESHOLD:
        return "Negative"
    return "Neutral"


def _strength(score: float) -> str:
    magnitude = abs(score)
    if magnitude >= STRONG_SCORE:
        return "Strong"
    if magnitude > 0:
        return "Moderate"
    return "None"


def analyze_text(text: str) -> dict[str, object]:
    """Score text locally and return all evidence used to reach the result."""
    prepared = preprocess(text)
    tokens = prepared["tokens"]
    positive_contributors: list[dict[str, object]] = []
    negative_contributors: list[dict[str, object]] = []
    detected_negations: list[str] = []
    detected_intensifiers: list[str] = []
    positive_score = 0.0
    negative_score = 0.0

    for index, token in enumerate(tokens):
        if token in NEGATIONS and token not in detected_negations:
            detected_negations.append(token)
        if token in INTENSIFIER_MULTIPLIERS and token not in detected_intensifiers:
            detected_intensifiers.append(token)
        base_score = SENTIMENT_LEXICON.get(token)
        if base_score is None:
            continue
        negation = _recent_modifier(tokens, index, NEGATIONS, NEGATION_WINDOW)
        intensifier = _recent_modifier(tokens, index, set(INTENSIFIER_MULTIPLIERS), INTENSIFIER_WINDOW)
        multiplier = INTENSIFIER_MULTIPLIERS.get(intensifier, 1.0)
        adjusted_score = float(base_score) * multiplier
        if negation:
            adjusted_score *= NEGATION_MULTIPLIER
        item = {"word": token, "score": round(adjusted_score, 2),
                "base_score": base_score, "negated_by": negation,
                "intensified_by": intensifier}
        if adjusted_score > 0:
            positive_score += adjusted_score
            positive_contributors.append(item)
        else:
            negative_score += abs(adjusted_score)
            negative_contributors.append(item)

    raw_score = positive_score - negative_score
    evidence_total = positive_score + negative_score
    normalized_score = raw_score / evidence_total if evidence_total else 0.0
    sentiment = _label(normalized_score)
    mixed = bool(positive_contributors and negative_contributors)
    explanation = _explanation(sentiment, positive_score, negative_score, mixed,
                               positive_contributors, negative_contributors)
    matched_terms = len(positive_contributors) + len(negative_contributors)
    return {
        "sentiment": sentiment, "raw_score": round(raw_score, 2),
        "score": round(normalized_score, 2), "positive_score": round(positive_score, 2),
        "negative_score": round(negative_score, 2), "sentiment_strength": _strength(normalized_score),
        "positive_contributors": positive_contributors,
        "negative_contributors": negative_contributors,
        "positive_words": [item["word"] for item in positive_contributors],
        "negative_words": [item["word"] for item in negative_contributors],
        "negations": detected_negations, "intensifiers": detected_intensifiers,
        "mixed_sentiment": mixed, "neutral_token_count": len(tokens) - matched_terms,
        **prepared, "explanation": explanation,
    }


def _explanation(sentiment: str, positive: float, negative: float, mixed: bool,
                 positives: list[dict[str, object]], negatives: list[dict[str, object]]) -> str:
    """Build a plain-language summary solely from computed evidence."""
    if not positives and not negatives:
        return "No words from the local sentiment lexicon were found, so the result is Neutral."
    parts = []
    if positives:
        parts.append(f"Positive evidence totals {positive:.2f} from {', '.join(item['word'] for item in positives)}.")
    if negatives:
        parts.append(f"Negative evidence totals {negative:.2f} from {', '.join(item['word'] for item in negatives)}.")
    if mixed:
        parts.append("Mixed sentiment was detected because both positive and negative evidence occurred.")
    parts.append(f"The normalized evidence score produces an overall {sentiment} result.")
    return " ".join(parts)
