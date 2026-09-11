"""Central configuration for the transparent sentiment rules."""

MAX_TEXT_LENGTH = 10_000
# A 10,000-character UTF-8 JSON request can use almost 40 KB for Unicode text.
MAX_REQUEST_BYTES = 60_000
NEGATION_WINDOW = 3
INTENSIFIER_WINDOW = 1
NEGATION_MULTIPLIER = -1.0
INTENSIFIER_MULTIPLIERS = {"very": 1.5, "really": 1.5, "extremely": 2.0,
                           "absolutely": 2.0, "incredibly": 1.8,
                           "highly": 1.5, "so": 1.3, "completely": 1.5}
POSITIVE_THRESHOLD = 0.2
NEGATIVE_THRESHOLD = -0.2
STRONG_SCORE = 0.6
