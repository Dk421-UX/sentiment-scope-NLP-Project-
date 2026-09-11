from app import app


def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_api_returns_analysis():
    response = client().post("/api/analyze", json={"text": "I absolutely loved it."})
    assert response.status_code == 200
    assert response.json["sentiment"] == "Positive"
    assert response.json["intensifiers"] == ["absolutely"]


def test_frontend_and_assets_load():
    test_client = client()
    assert test_client.get("/").status_code == 200
    assert test_client.get("/frontend/style.css").status_code == 200
    assert test_client.get("/frontend/script.js").status_code == 200


def test_api_rejects_empty_missing_nonstring_and_invalid_json():
    test_client = client()
    assert test_client.post("/api/analyze", json={"text": "   "}).json["error"] == "Text cannot be empty."
    assert test_client.post("/api/analyze", json={}).json["error"] == "Text is required."
    assert test_client.post("/api/analyze", json={"text": 123}).json["error"] == "Text must be a string."
    assert test_client.post("/api/analyze", data="not json", content_type="application/json").status_code == 400


def test_api_accepts_10000_and_rejects_10001_characters():
    test_client = client()
    accepted = test_client.post("/api/analyze", json={"text": "a" * 10_000})
    rejected = test_client.post("/api/analyze", json={"text": "a" * 10_001})
    assert accepted.status_code == 200
    assert rejected.status_code == 400
    assert rejected.json["error"] == "Text exceeds the 10,000 character limit."
