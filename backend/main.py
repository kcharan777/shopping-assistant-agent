import os
import datetime
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.models import ShoppingRequest, ShoppingResponse, Product
from backend.services.online_search import search_live_products
from backend.services.catalog import SAMPLE_CATALOGUE
from backend.services.recommender import filter_and_rank_products, generate_comparison_matrix
from backend.services.gemini_agent import parse_natural_language_intent, generate_reasoned_verdict, GEMINI_API_KEY

load_dotenv()

app = FastAPI(
    title="Shopping Assistant Agent API",
    description="AI-powered Shopping Assistant Agent with live Indian e-commerce search, Gemini reasoning, and deterministic comparison.",
    version="1.0.0"
)

# CORS configuration
allowed_origins_env = os.getenv("FRONTEND_URL", "http://localhost:5173,http://localhost:3000")
origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
origins.extend(["*", "http://localhost:5173", "http://127.0.0.1:5173"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for seamless deployment and local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    key_configured = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    return {
        "status": "healthy",
        "service": "Shopping Assistant Agent API",
        "gemini_configured": key_configured,
        "live_search_engine": "DDGS Online Search (India)",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/categories")
def get_categories():
    return {
        "categories": [
            {
                "id": "Laptops",
                "name": "Laptops & Notebooks",
                "icon": "Laptop",
                "suggested_budget": 60000,
                "popular_brands": ["Lenovo", "HP", "Asus", "Dell", "Acer", "Apple"],
                "popular_features": ["16GB RAM", "Intel i5", "Ryzen 7", "SSD", "Backlit Keyboard", "Lightweight"]
            },
            {
                "id": "Smartphones",
                "name": "Smartphones & Mobiles",
                "icon": "Smartphone",
                "suggested_budget": 30000,
                "popular_brands": ["Samsung", "OnePlus", "Xiaomi", "Realme", "Motorola", "Apple", "Google"],
                "popular_features": ["5G", "120Hz AMOLED", "OIS Camera", "5000mAh Battery", "Fast Charging"]
            },
            {
                "id": "Headphones",
                "name": "Headphones & Audio",
                "icon": "Headphones",
                "suggested_budget": 8000,
                "popular_brands": ["Sony", "Boat", "JBL", "Sennheiser", "Noise", "OnePlus"],
                "popular_features": ["Active Noise Cancelling", "Low Latency", "Spatial Audio", "30h Battery"]
            },
            {
                "id": "Smartwatches",
                "name": "Smartwatches & Wearables",
                "icon": "Watch",
                "suggested_budget": 5000,
                "popular_brands": ["Noise", "Fire-Boltt", "Boat", "Samsung", "Amazfit", "Apple"],
                "popular_features": ["AMOLED Display", "Bluetooth Calling", "Heart Rate Monitor", "GPS"]
            },
            {
                "id": "Tablets",
                "name": "Tablets & iPads",
                "icon": "Tablet",
                "suggested_budget": 35000,
                "popular_brands": ["Apple", "Samsung", "Lenovo", "Xiaomi", "OnePlus"],
                "popular_features": ["Stylus Support", "10-inch Display", "Keyboard Folio", "Quad Speakers"]
            }
        ]
    }

@app.post("/api/recommend", response_model=ShoppingResponse)
def get_recommendations(req: ShoppingRequest):
    # 1. Parse intent from natural language query or structured inputs
    parsed_intent = {}
    if req.query and req.query.strip():
        parsed_intent = parse_natural_language_intent(req.query.strip())
    
    # Merge explicit form overrides if provided
    final_category = req.category or parsed_intent.get("category", "Laptops")
    final_budget = req.max_budget or parsed_intent.get("max_budget")
    final_brands = req.preferred_brands or parsed_intent.get("preferred_brands", [])
    final_features = req.required_features or parsed_intent.get("required_features", [])

    query_str = req.query or f"{final_category} under ₹{final_budget or ''}"

    # 2. Fetch candidates (Priority: Live online search)
    raw_candidates: List[Dict[str, Any]] = []
    is_live = False

    if req.use_live_search:
        try:
            raw_candidates = search_live_products(
                query=query_str,
                category=final_category,
                max_budget=final_budget,
                preferred_brands=final_brands,
                limit=12
            )
            if raw_candidates:
                is_live = True
        except Exception as e:
            print(f"[Search Engine Fallback Alert] {e}")

    # Fallback to curated catalogue if live search yielded zero results or failed
    if not raw_candidates:
        raw_candidates = SAMPLE_CATALOGUE
        is_live = False

    # 3. Deterministic filtering, scoring, and ranking
    best_match, budget_match, all_ranked = filter_and_rank_products(
        candidates=raw_candidates,
        max_budget=final_budget,
        preferred_brands=final_brands,
        required_features=final_features,
        category=final_category
    )

    # 4. Generate comparison matrix
    comparison_aspects = generate_comparison_matrix(all_ranked)

    # 5. Generate AI Executive Verdict
    best_dict = best_match.model_dump() if best_match else None
    budget_dict = budget_match.model_dump() if budget_match else None
    
    verdict = generate_reasoned_verdict(
        user_query=query_str,
        parsed_intent={
            "category": final_category,
            "max_budget": final_budget,
            "preferred_brands": final_brands,
            "required_features": final_features,
            "primary_use_case": parsed_intent.get("primary_use_case", "Daily use and productivity")
        },
        best_match=best_dict,
        budget_match=budget_dict,
        total_shortlisted=len(all_ranked)
    )

    summary = f"Results for '{query_str}'"
    if final_budget:
        summary += f" (Budget: <= ₹{int(final_budget):,})"

    return ShoppingResponse(
        query_summary=summary,
        parsed_intent={
            "category": final_category,
            "max_budget": final_budget,
            "preferred_brands": final_brands,
            "required_features": final_features,
            "primary_use_case": parsed_intent.get("primary_use_case", "General use")
        },
        best_overall_match=best_match,
        budget_friendly_match=budget_match,
        all_recommendations=all_ranked,
        comparison_aspects=comparison_aspects,
        executive_verdict=verdict,
        total_found=len(all_ranked),
        is_live_data=is_live,
        search_timestamp=datetime.datetime.now(datetime.timezone.utc).strftime("%d %b %Y, %I:%M %p UTC")
    )

# Static file serving for single-service deployment on Render
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
if os.path.exists(frontend_dist):
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse

    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))

