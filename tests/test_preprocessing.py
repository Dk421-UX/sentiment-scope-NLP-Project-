from backend.preprocessing import count_sentences, preprocess, tokenize


def test_tokenization_lowercases_and_keeps_contractions():
    assert tokenize("I DON'T Like It!") == ["i", "don't", "like", "it"]


def test_statistics_count_words_characters_and_sentences():
    result = preprocess("Great! Really good.")
    assert result["character_count"] == 19
    assert result["word_count"] == 3
    assert result["sentence_count"] == 2


def test_punctuation_only_has_no_sentences():
    assert count_sentences("!!!") == 0
