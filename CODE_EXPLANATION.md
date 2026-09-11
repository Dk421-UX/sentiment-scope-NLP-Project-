# Code explanation

This guide corresponds to the current implementation. The engine is intentionally function-based, so a viva explanation follows the same flow as execution.

## `app.py`: HTTP boundary

```python
data = request.get_json(silent=True)
if not isinstance(data, dict):
    return jsonify(error="Request body must be valid JSON."), 400
```

This safely parses JSON and refuses malformed bodies. It exists so invalid client input becomes a useful API response rather than an exception; successful parsing connects to field validation.

```python
if "text" not in data: ...
text = data["text"]
if not isinstance(text, str): ...
if not text.strip(): ...
if len(text) > MAX_TEXT_LENGTH: ...
return jsonify(analyze_text(text))
```

These checks ensure text exists, is a string, contains visible content, and meets the exact limit. Without them, a direct API caller could bypass frontend restrictions or cause later code to receive unsuitable data. Only validated text reaches `analyze_text`.

## `preprocessing.py`: prepare text and statistics

```python
WORD_PATTERN = re.compile(r"[a-zA-Z]+(?:'[a-zA-Z]+)?")
return WORD_PATTERN.findall(text.lower())
```

The expression extracts alphabetic words and contractions such as `don't`; lowercase makes lexicon comparison case-insensitive. It does not erase negation or intensifier words. Without tokenization, scoring would compare a whole sentence to the lexicon.

```python
return {"tokens": tokens, "character_count": len(text),
        "word_count": len(tokens), "sentence_count": count_sentences(text)}
```

This keeps preprocessing’s responsibility small: return reusable tokens and counts derived from the actual input. `sentiment.py` receives this dictionary for scoring.

## `lexicon.py` and `config.py`: inspectable knowledge and rules

```python
SENTIMENT_LEXICON = {"good": 1, "excellent": 3, "terrible": -3}
NEGATIONS = {"not", "no", "never", "don't", ...}
```

The real file contains a larger starter vocabulary. Values are understandable base strengths, while the separate negation set is used only as a modifier. Keeping both local means students can inspect and edit the knowledge without an opaque model.

```python
NEGATION_WINDOW = 3
NEGATION_MULTIPLIER = -1.0
INTENSIFIER_MULTIPLIERS = {"very": 1.5, "extremely": 2.0, ...}
POSITIVE_THRESHOLD = 0.2
```

Named constants state the design choices in one place. Without them, unexplained values would be scattered through the scoring code and difficult to tune or defend.

## `sentiment.py`: modifier lookup and classification

```python
start = max(0, index - window)
for token in reversed(tokens[start:index]):
    if token in choices:
        return token
```

`_recent_modifier` searches only the configured words before a sentiment word and returns the closest matching modifier. This implements a simple finite window rather than pretending to understand grammar. It supplies negation or intensifier evidence to the main loop.

```python
base_score = SENTIMENT_LEXICON.get(token)
negation = _recent_modifier(tokens, index, NEGATIONS, NEGATION_WINDOW)
intensifier = _recent_modifier(tokens, index, set(INTENSIFIER_MULTIPLIERS), INTENSIFIER_WINDOW)
adjusted_score = float(base_score) * multiplier
if negation:
    adjusted_score *= NEGATION_MULTIPLIER
```

For every lexicon token, this takes its base value, optionally boosts magnitude, then optionally reverses polarity. A contributor dictionary records the exact word, adjusted score, and modifiers. Without this record, the UI explanation could not faithfully show why a score changed.

```python
raw_score = positive_score - negative_score
evidence_total = positive_score + negative_score
normalized_score = raw_score / evidence_total if evidence_total else 0.0
sentiment = _label(normalized_score)
mixed = bool(positive_contributors and negative_contributors)
```

Separate totals preserve conflicting evidence. The raw score is the net amount; normalization produces a bounded evidence ratio, avoiding a misleading probability claim. `_label` applies the configured thresholds, and `mixed` exposes evidence conflict rather than hiding it.

```python
explanation = _explanation(...)
return {"sentiment": sentiment, ..., "explanation": explanation}
```

The returned API contract is assembled only after all calculations. `_explanation` uses computed contributors and totals, so it cannot be a hard-coded demo message. Flask serializes this dictionary, and the frontend renders it.
