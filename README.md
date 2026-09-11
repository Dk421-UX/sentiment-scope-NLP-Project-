# SentimentScope

**SentimentScope** is an explainable, rule-based NLP sentiment analysis system. Its purpose is to show not only a Positive, Negative, or Neutral result, but the local words and rules that created it.

## Problem, motivation, and objectives

Short text is common in reviews and feedback, but a bare label is difficult to trust or learn from. This B.Sc. Data Science & AI project demonstrates a complete NLP pipeline that is small enough to inspect: validate text, tokenize it, look up a local lexicon, apply simple negation and intensifier rules, calculate evidence scores, and return a transparent JSON result. Objectives are local processing, explainability, accurate input statistics, a polished browser interface, and meaningful automated tests.

## Features

- Local, editable weighted sentiment lexicon—no AI service, API key, database, or remote request.
- Positive, Negative, Neutral, and mixed-evidence reporting.
- Configurable finite negation window and simple intensifier multipliers.
- Raw score, normalized evidence score (not a probability), strength, contributors, modifiers, and text statistics.
- Frontend and backend enforcement of the exact 10,000-character limit.
- Safe DOM rendering: user text is never injected as HTML.

## Architecture and NLP pipeline

`frontend (HTML/CSS/JS) → POST /api/analyze → Flask validation → preprocessing → lexicon/rules → JSON → dashboard`

`backend/preprocessing.py` normalizes and tokenizes; `backend/lexicon.py` is knowledge; `backend/sentiment.py` scores and explains; `app.py` is the HTTP boundary. This separation lets a future engine keep the same API and frontend.

## Stack and structure

Python 3, Flask, vanilla HTML/CSS/JavaScript, and pytest. NLTK is intentionally not required: regular-expression tokenization is sufficient here and makes the code easier to explain.

```
app.py                 Flask API and static page route
backend/               configuration, lexicon, preprocessing, scoring
frontend/              browser interface
tests/                 pytest unit and API checks
VIVA_GUIDE.md          concise oral-exam preparation
CODE_EXPLANATION.md    implementation-linked code walkthrough
SYSTEM_FLOW.md         end-to-end process explanation
```

## Install, run, and test

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. Run tests with `python -m pytest`.

## API

`POST /api/analyze` with `Content-Type: application/json`:

```json
{"text":"I absolutely loved this movie."}
```

The response includes `sentiment`, `raw_score`, normalized `score`, positive and negative scores, strength, contributor objects, modifier lists, counts, `mixed_sentiment`, and an explanation. Errors are JSON with an `error` message and HTTP 400 (or 413 for an oversized request body).

## Scoring methodology

Every lexicon word has a readable base weight. Positive matched weights are added to `positive_score`; absolute negative matched weights are added to `negative_score`; `raw_score = positive_score - negative_score`. The normalized score is `raw_score / (positive_score + negative_score)`, yielding −1 to +1 when evidence exists. Scores above `0.2` are Positive, below `-0.2` are Negative, otherwise Neutral. This is an evidence ratio, **not a calibrated confidence or probability**.

If a negation occurs in the prior three tokens, the sentiment term is inverted. If an intensifier occurs immediately before it, its magnitude is multiplied by the named value in `config.py`. These are intentionally simple heuristics, not full grammatical understanding. Mixed sentiment is true whenever both kinds of adjusted evidence occur.

## Validation, testing, and limitations

Both layers show/enforce 10,000 characters; the server remains authoritative and also checks JSON, field presence, type, and whitespace. Tests cover labels, mixed evidence, negation, intensification, case, punctuation, repetition, nonlexicon text, malformed requests, and both length boundaries.

This system cannot reliably understand sarcasm, context, idioms, implicit sentiment, complex negation, ambiguous or domain-specific language, slang, or languages beyond its English starter lexicon. It makes no accuracy claim without a labeled evaluation dataset.

## Learning outcomes and future evolution

The project practices strings, lists, dictionaries, functions, modules, HTTP/JSON, Flask validation, tokenization, lexicons, deterministic rules, testing, and safe DOM updates. A compatible progression is: V1 lexicon/rules; V2 TF-IDF + Logistic Regression; V3 compare engines through this API; V4 measure accuracy, precision, recall, F1, and confusion matrix; V5 optionally compare a transformer—while documenting all evaluation results honestly.
