from typing import List, Dict, Any, Optional, Tuple
from backend.models import Product, ComparisonAspect

def calculate_product_score(
    product: Dict[str, Any],
    max_budget: Optional[float],
    preferred_brands: Optional[List[str]],
    required_features: Optional[List[str]]
) -> Tuple[int, List[str]]:
    """
    Computes a deterministic score (0 - 100) and matches justification reasons.
    """
    score = 60 # Base score
    reasons = []
    
    price = float(product.get("price_inr", 0))
    brand = product.get("brand", "").lower()
    specs = product.get("specifications", {})
    features_text = " ".join(product.get("features", [])).lower()
    specs_text = " ".join([f"{k} {v}" for k, v in specs.items()]).lower()
    full_text = f"{product.get('name', '')} {features_text} {specs_text}".lower()

    # 1. Budget efficiency
    if max_budget and max_budget > 0:
        if price <= max_budget:
            savings = max_budget - price
            savings_pct = (savings / max_budget) * 100
            if savings_pct >= 10:
                score += 12
                reasons.append(f"Comfortably under budget with ₹{int(savings):,} in savings")
            else:
                score += 8
                reasons.append(f"Maximizes performance right up to the ₹{int(max_budget):,} limit")
        else:
            score -= 25 # Penalty for exceeding budget

    # 2. Brand preference match
    if preferred_brands:
        matched_brand = False
        for pb in preferred_brands:
            if pb.lower() in brand or pb.lower() in full_text:
                score += 15
                reasons.append(f"Matches preferred brand '{pb}'")
                matched_brand = True
                break
        if not matched_brand:
            score -= 5

    # 3. Required features match
    if required_features:
        matched_reqs = 0
        for rf in required_features:
            rf_clean = rf.lower().strip()
            if rf_clean in full_text:
                matched_reqs += 1
                reasons.append(f"Includes requested feature: '{rf}'")
        
        feature_ratio = matched_reqs / max(len(required_features), 1)
        score += int(feature_ratio * 15)

    # 4. Rating boost
    rating = float(product.get("rating", 4.0))
    if rating >= 4.3:
        score += 8
        reasons.append(f"High customer satisfaction rating ({rating}★)")
    elif rating >= 4.0:
        score += 4

    # Cap score between 40 and 99
    final_score = max(40, min(99, score))
    return final_score, reasons

def filter_and_rank_products(
    candidates: List[Dict[str, Any]],
    max_budget: Optional[float] = None,
    preferred_brands: Optional[List[str]] = None,
    required_features: Optional[List[str]] = None,
    category: Optional[str] = None
) -> Tuple[Optional[Product], Optional[Product], List[Product]]:
    """
    Deterministically filters products by budget and category,
    scores them, and picks the Best Overall and Budget-Friendly alternative.
    """
    filtered = []
    
    for item in candidates:
        price = float(item.get("price_inr", 0))
        
        # Strict budget check if provided
        if max_budget and price > max_budget:
            continue
            
        # Category check if provided and item has explicit category
        if category and item.get("category"):
            item_cat = item.get("category", "").lower()
            user_cat = category.lower()
            if user_cat not in item_cat and item_cat not in user_cat and item_cat != "electronics":
                continue

        score, reasons = calculate_product_score(
            item, max_budget, preferred_brands, required_features
        )
        
        # Create product copy with assigned score
        prod_data = dict(item)
        prod_data["match_score"] = score
        if reasons:
            prod_data["match_reason"] = " • ".join(reasons)
        else:
            prod_data["match_reason"] = f"Well-balanced specifications at ₹{int(price):,}"
            
        filtered.append(prod_data)

    if not filtered:
        return None, None, []

    # Sort primarily by match_score descending, secondarily by rating
    filtered.sort(key=lambda x: (x["match_score"], x.get("rating", 0)), reverse=True)

    # Best Overall is top ranked
    best_item = filtered[0]
    best_item["is_best_overall"] = True
    best_price = float(best_item.get("price_inr", 0))

    # Look for a Budget-Friendly alternative:
    # Must be at least 12% cheaper than the best overall match
    budget_friendly_item = None
    for item in filtered[1:]:
        item_price = float(item.get("price_inr", 0))
        if item_price < best_price * 0.88 and item["match_score"] >= 65:
            budget_friendly_item = item
            budget_friendly_item["is_budget_friendly"] = True
            break
            
    # If no candidate was 12% cheaper, pick the lowest priced viable candidate among them
    if not budget_friendly_item and len(filtered) > 1:
        cheapest_other = min(filtered[1:], key=lambda x: float(x.get("price_inr", 0)))
        if float(cheapest_other.get("price_inr", 0)) < best_price:
            budget_friendly_item = cheapest_other
            budget_friendly_item["is_budget_friendly"] = True

    # Convert to Product Pydantic models
    result_models = [Product(**p) for p in filtered]
    best_model = Product(**best_item) if best_item else None
    budget_model = Product(**budget_friendly_item) if budget_friendly_item else None

    return best_model, budget_model, result_models

def generate_comparison_matrix(products: List[Product]) -> List[ComparisonAspect]:
    """
    Builds a side-by-side comparison matrix across hardware features and pricing.
    """
    if not products:
        return []
        
    shortlist = products[:4]
    aspects = []
    
    # 1. Price comparison
    prices = {p.id: f"₹{int(p.price_inr):,}" for p in shortlist}
    lowest_price_prod = min(shortlist, key=lambda p: p.price_inr)
    aspects.append(ComparisonAspect(
        feature_name="Price (INR)",
        product_values=prices,
        winner_product_id=lowest_price_prod.id,
        note=f"{lowest_price_prod.name.split()[0]} offers the most accessible entry price"
    ))
    
    # 2. Processor
    processors = {}
    for p in shortlist:
        processors[p.id] = p.specifications.get("Processor", "Standard Quad-Core / Multi-Core")
    aspects.append(ComparisonAspect(
        feature_name="Processor / CPU",
        product_values=processors,
        winner_product_id=shortlist[0].id,
        note="Higher core count delivers faster multitasking and build speeds"
    ))
    
    # 3. RAM & Multitasking
    rams = {}
    for p in shortlist:
        rams[p.id] = p.specifications.get("RAM", "8GB - 16GB Memory")
    aspects.append(ComparisonAspect(
        feature_name="System RAM",
        product_values=rams,
        winner_product_id=shortlist[0].id,
        note="16GB memory is optimal for development environments and heavy browser tabs"
    ))

    # 4. Storage
    storages = {}
    for p in shortlist:
        storages[p.id] = p.specifications.get("Storage", "512GB Fast SSD")
    aspects.append(ComparisonAspect(
        feature_name="High-speed Storage",
        product_values=storages,
        winner_product_id=shortlist[0].id,
        note="NVMe SSDs ensure rapid boot and instant application launches"
    ))

    # 5. Display & Screen
    displays = {}
    for p in shortlist:
        displays[p.id] = p.specifications.get("Display", "FHD Display")
    aspects.append(ComparisonAspect(
        feature_name="Display Quality",
        product_values=displays,
        winner_product_id=shortlist[0].id,
        note="Anti-glare full HD reduces eye strain during prolonged screen work"
    ))

    # 6. Overall Match Score
    scores = {p.id: f"{p.match_score}/100" for p in shortlist}
    aspects.append(ComparisonAspect(
        feature_name="AI Compatibility Score",
        product_values=scores,
        winner_product_id=shortlist[0].id,
        note="Deterministic ranking based on user budget, performance, and feedback"
    ))

    return aspects
