from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: str = Field(..., description="Unique product identifier")
    name: str = Field(..., description="Full product name")
    category: str = Field(..., description="Category like Laptops, Smartphones, etc.")
    brand: str = Field(..., description="Manufacturer brand e.g. Lenovo, HP, Apple")
    price_inr: float = Field(..., description="Current price in Indian Rupees (INR ₹)")
    original_price_inr: Optional[float] = Field(None, description="Original MRP in INR if discounted")
    rating: Optional[float] = Field(None, description="User rating out of 5 e.g. 4.3")
    reviews_count: Optional[int] = Field(None, description="Number of user reviews")
    image_url: Optional[str] = Field(None, description="Verified product image URL")
    retailer: str = Field("Online Retailer", description="Retailer name like Amazon.in, Flipkart, Croma")
    retailer_url: str = Field("#", description="Direct link to purchase or view on retailer")
    availability: str = Field("In Stock", description="Stock status e.g. In Stock, Few Units Left")
    specifications: Dict[str, str] = Field(default_factory=dict, description="Key hardware/feature specs")
    features: List[str] = Field(default_factory=list, description="Highlight feature bullet points")
    strengths: List[str] = Field(default_factory=list, description="Why this product stands out")
    limitations: List[str] = Field(default_factory=list, description="Downsides or trade-offs")
    match_score: int = Field(85, description="Compatibility score out of 100")
    match_reason: Optional[str] = Field(None, description="Detailed explanation of why it fits user criteria")
    is_best_overall: bool = Field(False, description="Whether this is the recommended #1 top choice")
    is_budget_friendly: bool = Field(False, description="Whether this is the value-for-money / affordable alternative")
    source: str = Field("Live Web Search", description="Data provenance: Live Web Search, Verified Retailer, etc.")

class ShoppingRequest(BaseModel):
    query: Optional[str] = Field(None, description="Natural language shopping request e.g. 'Laptop under 60000 for college'")
    category: Optional[str] = Field(None, description="Product category filter")
    max_budget: Optional[float] = Field(None, description="Maximum budget in INR (₹)")
    min_budget: Optional[float] = Field(0.0, description="Minimum budget in INR (₹)")
    preferred_brands: Optional[List[str]] = Field(default_factory=list, description="Preferred brands e.g. ['HP', 'Lenovo']")
    required_features: Optional[List[str]] = Field(default_factory=list, description="Desired features e.g. ['16GB RAM', 'SSD', 'Backlit keyboard']")
    use_live_search: bool = Field(True, description="Whether to query live Indian e-commerce search")

class ComparisonAspect(BaseModel):
    feature_name: str
    product_values: Dict[str, str] # productId -> spec text or score
    winner_product_id: Optional[str] = None
    note: Optional[str] = None

class ShoppingResponse(BaseModel):
    query_summary: str
    parsed_intent: Dict[str, Any]
    best_overall_match: Optional[Product] = None
    budget_friendly_match: Optional[Product] = None
    all_recommendations: List[Product] = Field(default_factory=list)
    comparison_aspects: List[ComparisonAspect] = Field(default_factory=list)
    executive_verdict: str = Field(..., description="High-level buying advice from AI Agent")
    total_found: int = 0
    is_live_data: bool = True
    search_timestamp: str
