# System flow

```text
USER
 ↓
TEXTAREA
 ↓
10,000 CHARACTER VALIDATION
 ↓
POST /api/analyze
 ↓
FLASK
 ↓
BACKEND VALIDATION
 ↓
PREPROCESSING
 ↓
TOKENIZATION
 ↓
LEXICON LOOKUP
 ↓
NEGATION HANDLING
 ↓
INTENSIFIER HANDLING
 ↓
SCORING
 ↓
CLASSIFICATION
 ↓
MIXED SENTIMENT DETECTION
 ↓
EXPLANATION GENERATION
 ↓
JSON
 ↓
JAVASCRIPT
 ↓
RESULT DASHBOARD
```

1. The browser counts characters as the user types and blocks ordinary submission above 10,000. It sends JSON only after non-empty client validation.
2. Flask receives `POST /api/analyze`. It safely parses JSON and independently checks that `text` exists, is a string, is not whitespace, and is at most 10,000 characters. This prevents bypassing browser checks.
3. `preprocess()` lowercases only for comparison, extracts words with a readable regular expression, and derives character, word, and sentence counts. The original submitted text is not changed or stored in the response.
4. For each token, `analyze_text()` looks up the local `SENTIMENT_LEXICON`. A nearby word from `NEGATIONS` in the preceding three tokens inverts it. An immediately preceding intensifier applies its named multiplier.
5. Adjusted positive and negative evidence become separate totals. Their difference is the raw score and their ratio becomes the normalized score. Thresholds classify Positive, Negative, or Neutral.
6. If adjusted positive and negative contributors both exist, the result is marked mixed. The same contributor records generate the explanation, modifier details, chips, and counts—no demo output is hard-coded.
7. Flask returns JSON. JavaScript reads the JSON, uses DOM text nodes for content, and builds the dashboard from the returned values.
