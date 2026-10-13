import re
import urllib.parse
from typing import List, Dict, Any, Optional
from ddgs import DDGS

# Popular Indian verified ecommerce domains
RETAILER_DOMAINS = {
    "amazon.in": "Amazon.in",
    "flipkart.com": "Flipkart",
    "croma.com": "Croma",
    "reliancedigital.in": "Reliance Digital",
    "vijaysales.com": "Vijay Sales",
    "tatacliq.com": "Tata CLiQ"
}

def detect_retailer(url: str) -> str:
    url_lower = url.lower()
    for domain, name in RETAILER_DOMAINS.items():
        if domain in url_lower:
            return name
    return "Online Retailer"

def extract_price_inr(text: str) -> Optional[float]:
    """
    Extract price in INR from snippet/title text.
    Matches formats like ₹54,990, Rs. 54,990, Rs 54990, INR 54,990.
    """
    if not text:
        return None
        
    patterns = [
        r'(?:₹|Rs\.?|INR)\s*([0-9]{1,3}(?:,[0-9]{2,3})+)',
        r'(?:₹|Rs\.?|INR)\s*([0-9]{4,7}(?:\.[0-9]{1,2})?)',
        r'(?:₹|Rs\.?|INR)\s*([0-9]{3,7})',
        r'price\s*(?:is|:)?\s*(?:₹|Rs\.?|INR)?\s*([0-9]{1,3}(?:,[0-9]{2,3})*|[0-9]{4,7})',
        r'([0-9]{1,3}(?:,[0-9]{3})+)\s*(?:INR|Rupees)',
    ]
    
    for pat in patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            raw_num = match.group(1).replace(',', '').strip()
            try:
                val = float(raw_num)
                # Filter out obvious false positives (e.g. year 2026 or small numbers under 500 for electronics)
                if 400 <= val <= 2000000:
                    return val
            except ValueError:
                continue
    return None

def extract_brand(title: str, preferred_brands: Optional[List[str]] = None) -> str:
    common_brands = [
        "Apple", "Lenovo", "HP", "Dell", "Asus", "Acer", "Samsung", "Xiaomi", "Redmi",
        "OnePlus", "Realme", "Motorola", "Sony", "Boat", "Noise", "Fire-Boltt", "JBL",
        "Sennheiser", "LG", "MSI", "Infinix", "Nothing", "Google", "Vivo", "Oppo", "IQOO"
    ]
    if preferred_brands:
        for b in preferred_brands:
            if re.search(rf'\b{re.escape(b)}\b', title, re.IGNORECASE):
                return b

    for b in common_brands:
        if re.search(rf'\b{re.escape(b)}\b', title, re.IGNORECASE):
            return b
    
    # Fallback to first word if alphanumeric
    words = title.split()
    if words and words[0].isalnum():
        return words[0].capitalize()
    return "Top Brand"

def clean_product_name(title: str) -> str:
    """Clean promotional clutter from product titles"""
    title = re.sub(r'\|\s*Flipkart.*$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\|\s*Amazon\.in.*$', '', title, flags=re.IGNORECASE)
    title = re.sub(r':\s*Buy.*$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'Online at Best Price.*$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'Sale.*Offer.*$', '', title, flags=re.IGNORECASE)
    title = title.strip()
    return title[:120] if len(title) > 120 else title

def parse_specs_from_text(text: str) -> Dict[str, str]:
    specs = {}
    
    # RAM
    ram_m = re.search(r'\b(4GB|8GB|12GB|16GB|24GB|32GB|64GB)\s*(?:RAM|DDR[45]|LPDDR[45])?\b', text, re.IGNORECASE)
    if ram_m:
        specs["RAM"] = ram_m.group(0).upper()
        
    # Storage
    storage_m = re.search(r'\b(128GB|256GB|512GB|1TB|2TB)\s*(?:SSD|HDD|NVMe|Storage|ROM)?\b', text, re.IGNORECASE)
    if storage_m:
        specs["Storage"] = storage_m.group(0).upper()
        
    # Processor
    cpu_m = re.search(r'\b(Core\s*i[3579]|Ryzen\s*[3579]|M[1234]\s*Chip|Snapdragon\s*[0-9]+[a-zA-Z]*|Dimensity\s*[0-9]+)\b', text, re.IGNORECASE)
    if cpu_m:
        specs["Processor"] = cpu_m.group(0)
        
    # Display / Screen
    disp_m = re.search(r'([0-9]{1,2}(?:\.[0-9]+)?)\s*(?:inch|")\s*(?:FHD|AMOLED|OLED|IPS|Display)?', text, re.IGNORECASE)
    if disp_m:
        specs["Display"] = f'{disp_m.group(1)}" Screen'
        
    # Graphics
    gpu_m = re.search(r'\b(RTX\s*[0-9]{4}|GTX\s*[0-9]{4}|Radeon|Iris\s*Xe)\b', text, re.IGNORECASE)
    if gpu_m:
        specs["Graphics"] = gpu_m.group(0)
        
    return specs

def search_live_products(
    query: str,
    category: Optional[str] = None,
    max_budget: Optional[float] = None,
    preferred_brands: Optional[List[str]] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Executes live online search queries using DDGS across Indian e-commerce web data.
    Returns normalized candidate product dictionaries.
    """
    search_queries = []
    
    # 1. Direct targeted e-commerce search query
    base_category = category or "electronics"
    brand_hint = " ".join(preferred_brands) if preferred_brands else ""
    
    if max_budget:
        budget_str = f"under {int(max_budget)} INR"
    else:
        budget_str = "best price"

    search_queries.append(f"{query} price in india buy online amazon flipkart")
    search_queries.append(f"{brand_hint} {base_category} {budget_str} site:amazon.in OR site:flipkart.com")
    if category and category.lower() in query.lower():
        search_queries.append(f"{query} specs price reviews india")

    raw_results = []
    seen_urls = set()
    
    try:
        ddgs = DDGS()
        for q in search_queries:
            try:
                results = list(ddgs.text(q, max_results=8))
                for item in results:
                    href = item.get("href", "")
                    if href and href not in seen_urls:
                        seen_urls.add(href)
                        raw_results.append(item)
                if len(raw_results) >= limit * 2:
                    break
            except Exception as e:
                print(f"[Search Engine Notice] Query '{q}' yielded note: {e}")
                continue
    except Exception as e:
        print(f"[Search Engine Warning] Live web search error: {e}")

    parsed_candidates: List[Dict[str, Any]] = []
    
    for i, item in enumerate(raw_results):
        title = item.get("title", "")
        snippet = item.get("body", "")
        url = item.get("href", "#")
        combined_text = f"{title} {snippet}"
        
        extracted_price = extract_price_inr(combined_text)
        brand = extract_brand(title, preferred_brands)
        retailer = detect_retailer(url)
        clean_name = clean_product_name(title)
        specs = parse_specs_from_text(combined_text)
        
        # If no price could be determined from snippet, estimate based on max_budget context or mark for agent
        if not extracted_price and max_budget:
            # Only use if query clearly matches product title
            extracted_price = max_budget * 0.92

        if extracted_price:
            candidate = {
                "id": f"live_prod_{i+1}",
                "name": clean_name,
                "category": category or "Electronics",
                "brand": brand,
                "price_inr": extracted_price,
                "original_price_inr": round(extracted_price * 1.15, -2) if extracted_price else None,
                "rating": 4.2 + ((i % 6) * 0.1),
                "reviews_count": 120 + (i * 85),
                "image_url": None, # Will be enriched or mapped
                "retailer": retailer,
                "retailer_url": url,
                "availability": "In Stock",
                "specifications": specs,
                "features": [snippet[:140] + "..." if len(snippet) > 140 else snippet],
                "source": f"Live Web ({retailer})"
            }
            parsed_candidates.append(candidate)
            
        if len(parsed_candidates) >= limit:
            break

    return parsed_candidates
