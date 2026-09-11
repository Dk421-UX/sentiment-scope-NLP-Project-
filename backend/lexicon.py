"""Small, editable local sentiment vocabulary. Values are base strengths."""

SENTIMENT_LEXICON = {
    "good": 1, "great": 2, "excellent": 3, "amazing": 3,
    "wonderful": 3, "fantastic": 3, "love": 3, "loved": 3,
    "like": 1, "liked": 1, "brilliant": 3, "happy": 2,
    "beautiful": 2, "perfect": 3, "enjoy": 2, "enjoyed": 2,
    "success": 2, "successful": 2, "best": 3, "helpful": 2,
    "useful": 2, "impressive": 2, "awesome": 3, "pleasant": 2,
    "delightful": 3, "recommend": 2, "recommended": 2, "satisfied": 2,
    "fast": 1, "reliable": 2, "clear": 1, "easy": 1, "value": 1,
    "bad": -1, "terrible": -3, "awful": -3, "horrible": -3,
    "worst": -3, "hate": -3, "hated": -3, "dislike": -2,
    "disliked": -2, "sad": -2, "poor": -2, "failure": -3,
    "failed": -3, "boring": -2, "disappointing": -2,
    "disappointed": -2, "ugly": -2, "problem": -1, "wrong": -1,
    "useless": -3, "broken": -2, "annoying": -2, "frustrating": -2,
    "slow": -1, "confusing": -2, "difficult": -1, "waste": -2,
    "unreliable": -2, "poorly": -2, "angry": -2, "terribly": -2,
}

NEGATIONS = {
    "not", "no", "never", "don't", "doesn't", "didn't", "isn't",
    "wasn't", "can't", "cannot", "won't", "couldn't", "shouldn't",
    "wouldn't", "weren't", "aren't", "haven't", "hasn't", "hadn't",
}
