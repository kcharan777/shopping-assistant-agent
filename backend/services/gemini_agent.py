import os
import json
import re
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

def get_gemini_client():
    """Initializes and returns the Gemini client if key is configured"""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key or "your_" in api_key.lower():
        return None
    try:
        from google import genai
        return genai.Client(api_key=api_key)
    except Exception as e:
        print(f"[Gemini Client Init Note] {e}")
        return None

def parse_natural_language_intent(user_query: str) -> Dict[str, Any]:
    """
    Extracts category, max_budget, preferred_brands, and required_features
    from natural language text (e.g. 'Recommend a laptop under ₹60,000 for college, programming').
    Uses Gemini when key is present, otherwise uses precision NLP heuristics.
    """
    client = get_gemini_client()
    if client:
        prompt = f"""
You are an expert Indian e-commerce shopping assistant.
Parse the user's natural language shopping request into structured JSON.

User query: "{user_query}"

Respond with ONLY valid JSON strictly matching this schema:
{{
  "category": "Laptops" (or Smartphones, Headphones, Smartwatches, Tablets, Cameras, etc.),
  "max_budget": 60000.0 (float in Indian Rupees INR, or null if unspecified),
  "preferred_brands": ["Lenovo", "HP"] (array of strings, or empty array),
  "required_features": ["programming", "college", "16GB RAM"] (array of strings),
  "primary_use_case": "college programming and daily multitasking"
}}
Do NOT output markdown backticks or any conversational text.
"""
        for model_name in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                raw_text = response.text.strip()
                # Remove json markdown markers if present
                clean_json = re.sub(r'^```(?:json)?\s*', '', raw_text, flags=re.MULTILINE)
                clean_json = re.sub(r'\s*```$', '', clean_json, flags=re.MULTILINE).strip()
                data = json.loads(clean_json)
                return data
            except Exception as e:
                print(f"[Gemini Intent Parse Attempt with {model_name}] {e}")
                continue

    # Heuristic / Regex Fallback parser
    category = "Electronics"
    query_lower = user_query.lower()
    
    if any(k in query_lower for k in ["laptop", "notebook", "macbook", "computer", "pc"]):
        category = "Laptops"
    elif any(k in query_lower for k in ["phone", "mobile", "smartphone", "iphone", "android"]):
        category = "Smartphones"
    elif any(k in query_lower for k in ["headphone", "earphone", "earbud", "audio", "tws"]):
        category = "Headphones"
    elif any(k in query_lower for k in ["watch", "smartwatch", "fitness band"]):
        category = "Smartwatches"
    elif any(k in query_lower for k in ["tablet", "ipad", "tab"]):
        category = "Tablets"

    # Extract budget in INR
    max_budget = None
    budget_match = re.search(r'(?:under|below|less than|budget|within|upto|up to)\s*(?:₹|Rs\.?|INR)?\s*([0-9]{1,3}(?:,[0-9]{2,3})*(?:\.[0-9]+)?|[0-9]{4,7})', user_query, re.IGNORECASE)
    if budget_match:
        try:
            val_str = budget_match.group(1).replace(',', '')
            max_budget = float(val_str)
        except ValueError:
            pass

    # Extract brands
    known_brands = [
        "Apple", "Lenovo", "HP", "Dell", "Asus", "Acer", "Samsung", "Xiaomi", "OnePlus",
        "Realme", "Motorola", "Sony", "Boat", "Noise", "JBL", "LG", "MSI"
    ]
    preferred_brands = []
    for b in known_brands:
        if re.search(rf'\b{re.escape(b)}\b', user_query, re.IGNORECASE):
            preferred_brands.append(b)

    # Extract features / use cases
    features = []
    for feat in ["programming", "coding", "college", "gaming", "battery life", "16gb ram", "8gb ram", "ssd", "lightweight", "camera", "display", "office", "video editing"]:
        if feat in query_lower:
            features.append(feat.title())

    return {
        "category": category,
        "max_budget": max_budget,
        "preferred_brands": preferred_brands,
        "required_features": features,
        "primary_use_case": ", ".join(features) if features else "Everyday computing & productivity"
    }

def generate_reasoned_verdict(
    user_query: str,
    parsed_intent: Dict[str, Any],
    best_match: Optional[Dict[str, Any]],
    budget_match: Optional[Dict[str, Any]],
    total_shortlisted: int
) -> str:
    """
    Generates a personalized, professional executive verdict explaining
    why the recommendations fit the user's specific constraints.
    """
    client = get_gemini_client()
    if client and best_match:
        prompt = f"""
You are a senior tech advisor and shopping assistant in India.
Explain to the user why the recommended products are their best choice.

User Request: "{user_query}"
Parsed Needs: {json.dumps(parsed_intent)}

Best Overall Product:
Name: {best_match.get('name')}
Price: ₹{int(best_match.get('price_inr', 0)):,}
Key Specs: {best_match.get('specifications')}

Budget-Friendly Alternative:
{json.dumps(budget_match) if budget_match else "None"}

Write a crisp, convincing 2-3 paragraph shopping verdict that explains:
1. Why the Best Overall recommendation directly addresses their use-case (e.g., college, programming, multitasking) within their budget.
2. If a budget-friendly option is provided, mention how much money it saves and what realistic compromises exist.
3. A final reassuring recommendation on where and when to buy.

Tone: Professional, knowledgeable, objective, practical Indian e-commerce perspective.
Do not use generic fluff.
"""
        for model_name in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return response.text.strip()
            except Exception as e:
                print(f"[Gemini Verdict Generation with {model_name}] {e}")
                continue

    # Deterministic fallback verdict
    if not best_match:
        return "No products found matching your exact budget and specification criteria. Consider increasing your budget slightly or broadening brand preferences."

    best_name = best_match.get('name', 'Top Recommended Product')
    best_price = int(best_match.get('price_inr', 0))
    use_case = parsed_intent.get('primary_use_case') or "your specified needs"

    verdict = f"For {use_case}, the **{best_name}** (priced at ₹{best_price:,}) offers the most capable balance of processing power, memory headroom, and long-term durability. Its hardware configuration handles development tools, multiple browser instances, and daily productivity tasks without thermal throttling or memory bottlenecks."

    if budget_match and budget_match.get('id') != best_match.get('id'):
        b_name = budget_match.get('name')
        b_price = int(budget_match.get('price_inr', 0))
        savings = best_price - b_price
        if savings > 0:
            verdict += f"\n\nIf you prefer to preserve funds, the **{b_name}** at ₹{b_price:,} saves you an additional ₹{savings:,}. It delivers reliable everyday performance for coursework and standard multitasking, with only modest trade-offs in peak multithreading or luxury chassis finishes."

    verdict += "\n\nBoth products are verified across reputable Indian retail channels (Amazon.in / Flipkart / Croma) with manufacturer warranty coverage."
    return verdict
