from backend.sentiment import analyze_text


def test_positive_negative_and_neutral_text():
    assert analyze_text("This is amazing and brilliant.")["sentiment"] == "Positive"
    assert analyze_text("This is terrible and useless.")["sentiment"] == "Negative"
    assert analyze_text("The product arrived yesterday.")["sentiment"] == "Neutral"


def test_mixed_sentiment_is_visible():
    result = analyze_text("The design is amazing but the performance is terrible.")
    assert result["mixed_sentiment"] is True
    assert result["positive_words"] == ["amazing"]
    assert result["negative_words"] == ["terrible"]


def test_negation_inverts_nearby_sentiment():
    result = analyze_text("I don't like this product.")
    assert result["sentiment"] == "Negative"
    assert result["negative_contributors"][0]["negated_by"] == "don't"


def test_intensifier_increases_magnitude():
    plain = analyze_text("I love this product.")
    boosted = analyze_text("I really love this product.")
    assert boosted["positive_score"] > plain["positive_score"]
    assert boosted["intensifiers"] == ["really"]


def test_uppercase_punctuation_repeated_and_nonlexicon_input():
    assert analyze_text("AMAZING!!!")["sentiment"] == "Positive"
    assert analyze_text("good good good")["raw_score"] == 3
    assert analyze_text("12345 !!!")["neutral_token_count"] == 0
