"""Simple text preparation functions that preserve sentiment-relevant words."""

import re

WORD_PATTERN = re.compile(r"[a-zA-Z]+(?:'[a-zA-Z]+)?")
SENTENCE_PATTERN = re.compile(r"[.!?]+")


def tokenize(text: str) -> list[str]:
    """Lowercase and extract words, retaining contractions such as don't."""
    return WORD_PATTERN.findall(text.lower())


def count_sentences(text: str) -> int:
    """Count punctuation-ended sentences; text with words but no stop is one."""
    if not text.strip():
        return 0
    if not tokenize(text):
        return 0
    endings = len(SENTENCE_PATTERN.findall(text))
    return endings if endings else 1


def preprocess(text: str) -> dict[str, object]:
    """Produce the normalized tokens and accurate basic text statistics."""
    tokens = tokenize(text)
    return {
        "tokens": tokens,
        "character_count": len(text),
        "word_count": len(tokens),
        "sentence_count": count_sentences(text),
    }
