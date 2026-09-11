# SentimentScope viva guide

## Beginner Python

**What is a variable?** A named reference to a value, such as `raw_score`.

**Which data types are used?** Strings for text, integers/floats for scores, lists for tokens/contributors, dictionaries for JSON-like records, and sets for fast membership checks.

**Why use lists and dictionaries?** Lists preserve contributor order; dictionaries give meaningful keys such as `word` and `score`.

**What do loops do here?** The scoring loop visits each token once and applies the same transparent rules.

**What is a function and return?** A function groups one job; `return` sends its result to the caller. For example, `preprocess()` returns tokens and counts.

**Why modules and imports?** Modules separate responsibilities. `sentiment.py` imports vocabulary and constants instead of duplicating them.

**How are exceptions handled?** Flask’s malformed-body path uses `get_json(silent=True)` and returns a clean JSON error rather than exposing a stack trace.

## NLP fundamentals

**What is NLP?** Natural Language Processing: techniques that let software process human language.

**What are normalization and tokenization?** Normalization lowercases comparison text; tokenization splits text into usable words.

**What are stopwords, stemming, and lemmatization?** Stopwords are common words sometimes removed; stemming cuts word endings; lemmatization maps words to dictionary forms. This project does not apply them because removal or aggressive transformation could obscure a simple explanation.

**What is lexicon sentiment analysis?** It scores text from a hand-readable dictionary of words with positive or negative weights.

**Why negation and intensifiers?** “Not good” reverses good’s contribution; “very good” makes it stronger. The implementation uses a finite heuristic window.

**Can it understand sarcasm or context?** No. “Great, it broke again” can be misread because rule-based word matching lacks world knowledge and context.

## Backend and API

**What is Flask?** A lightweight Python web framework that maps URL routes to functions.

**What is HTTP POST and JSON?** POST sends data to a server; JSON is a standard structured text format. The frontend posts `{ "text": "..." }`.

**What is a REST-style API?** A clear resource/action endpoint using HTTP conventions; `/api/analyze` accepts analysis input and returns JSON.

**Why separate frontend and backend?** The browser handles presentation; Flask validates requests; Python owns NLP rules. Each part stays understandable and replaceable.

**Why validate twice?** Browser validation improves UX, but anyone can call the endpoint directly. Backend validation is the security boundary.

## Project-specific and critical questions

**Why a lexicon approach?** It is local, deterministic, inspectable, inexpensive, and appropriate for learning NLP engineering. Its trade-off is limited linguistic understanding.

**Why no external API, BERT, or LLM?** The project’s objective is transparent local scoring. Larger models add dependencies and are harder to explain line-by-line; they are not automatically more appropriate for this academic scope.

**How is the score calculated?** Add adjusted positive evidence, add absolute negative evidence, subtract for raw score, then divide by total evidence for a −1 to +1 evidence ratio. It is not probability.

**How does negation work?** A configured three-token lookback finds a negation such as `don't`; it multiplies the nearby lexicon term by −1. It is heuristic, not parsing.

**How do intensifiers work?** An immediately preceding intensifier selects a readable multiplier from `INTENSIFIER_MULTIPLIERS`.

**How is mixed sentiment detected?** It is true when both adjusted positive and adjusted negative contributors occur, while the normalized total still determines the dominant label.

**Why exactly 10,000 characters?** It gives a clear scope for an interactive educational tool and prevents unexpectedly large requests; frontend and backend both enforce it.

**What happens after Analyze?** JavaScript validates, posts JSON, Flask validates/preprocesses/scores, then JavaScript renders returned evidence and statistics.

**How would you evaluate it scientifically?** Use a held-out labeled dataset and report accuracy, precision, recall, F1-score, and a confusion matrix. Do not claim performance without this experiment.

**How would you improve it?** Expand and validate the lexicon by domain, improve linguistic handling, then add TF-IDF + Logistic Regression behind the same API and compare results fairly.
