import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test Health Check
def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

# Test Shorten URL and Redirect
def test_shorten_and_redirect(client):
    res = client.post("/api/shorten", json={"url": "https://example.com"})
    assert res.status_code == 200
    data = res.get_json()
    short_code = data["short_code"]

    # Test the redirect works
    res = client.get(f"/{short_code}")
    assert res.status_code == 302  # Should redirect

# Test Invalid URL
def test_invalid_url(client):
    res = client.post("/api/shorten", json={"url": "bad-url"})
    assert res.status_code == 400

# Test Stats
def test_stats(client):
    # First, shorten a URL
    res = client.post("/api/shorten", json={"url": "https://example.com"})
    short_code = res.get_json()["short_code"]

    # Simulate 3 redirects (clicks)
    for _ in range(3):
        client.get(f"/{short_code}")

    # Fetch stats for this short code
    stats = client.get(f"/api/stats/{short_code}").get_json()
    assert stats["clicks"] == 3
    assert stats["url"] == "https://example.com"
