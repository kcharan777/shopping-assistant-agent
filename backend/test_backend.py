import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.services.online_search import extract_price_inr, parse_specs_from_text, detect_retailer
from backend.services.recommender import filter_and_rank_products, calculate_product_score, generate_comparison_matrix
from backend.services.catalog import SAMPLE_CATALOGUE

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data

def test_categories_endpoint():
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert len(data["categories"]) > 0
    categories = [c["id"] for c in data["categories"]]
    assert "Laptops" in categories

def test_extract_price_inr():
    assert extract_price_inr("Buy at ₹54,990 on Amazon") == 54990.0
    assert extract_price_inr("Special discount Rs. 49,999 only") == 49999.0
    assert extract_price_inr("Flipkart price INR 62000") == 62000.0
    assert extract_price_inr("No price mentioned here") is None

def test_parse_specs_from_text():
    text = "Lenovo laptop with 16GB RAM, 512GB SSD, Intel Core i5 and 15.6 inch display"
    specs = parse_specs_from_text(text)
    assert specs.get("RAM") == "16GB RAM" or "16GB" in specs.get("RAM", "")
    assert "512GB" in specs.get("Storage", "")
    assert "Core i5" in specs.get("Processor", "")

def test_detect_retailer():
    assert detect_retailer("https://www.amazon.in/dp/B0B56CY8H2") == "Amazon.in"
    assert detect_retailer("https://www.flipkart.com/laptops/item") == "Flipkart"
    assert detect_retailer("https://www.croma.com/p/123") == "Croma"

def test_recommender_strict_budget_filter():
    max_budget = 50000.0
    best, budget, all_ranked = filter_and_rank_products(
        candidates=SAMPLE_CATALOGUE,
        max_budget=max_budget,
        category="Laptops"
    )
    # Every returned product must be strictly <= max_budget
    for p in all_ranked:
        assert p.price_inr <= max_budget

def test_recommender_scoring_with_brand_and_features():
    item = SAMPLE_CATALOGUE[0] # Lenovo IdeaPad
    score, reasons = calculate_product_score(
        product=item,
        max_budget=60000.0,
        preferred_brands=["Lenovo"],
        required_features=["16GB RAM", "Programming"]
    )
    assert score >= 70
    assert any("Lenovo" in r for r in reasons)

def test_comparison_matrix():
    best, budget, all_ranked = filter_and_rank_products(
        candidates=SAMPLE_CATALOGUE,
        max_budget=60000.0,
        category="Laptops"
    )
    aspects = generate_comparison_matrix(all_ranked)
    assert len(aspects) >= 4
    for a in aspects:
        assert len(a.product_values) > 0

def test_api_recommend_endpoint():
    req_body = {
        "query": "Recommend a laptop under ₹60,000 for college and programming",
        "category": "Laptops",
        "max_budget": 60000.0,
        "use_live_search": False # Test deterministic pipeline
    }
    response = client.post("/api/recommend", json=req_body)
    assert response.status_code == 200
    data = response.json()
    assert "best_overall_match" in data
    assert data["best_overall_match"] is not None
    assert data["best_overall_match"]["price_inr"] <= 60000.0
    assert "executive_verdict" in data
    assert len(data["comparison_aspects"]) > 0
