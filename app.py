import os
import json
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI


# -------------------------------------------------
# PRODUCT DATA
# -------------------------------------------------

PRODUCTS = [
    {
        "name": "Acer Aspire 5",
        "category": "laptop",
        "price": 54990,
        "brand": "Acer",
        "rating": 4.3,
        "features": "16GB RAM, 512GB SSD, 15.6 inch display"
    },
    {
        "name": "Lenovo IdeaPad Slim 5",
        "category": "laptop",
        "price": 59990,
        "brand": "Lenovo",
        "rating": 4.5,
        "features": "16GB RAM, 512GB SSD, OLED display"
    },
    {
        "name": "HP 15",
        "category": "laptop",
        "price": 49990,
        "brand": "HP",
        "rating": 4.2,
        "features": "16GB RAM, 512GB SSD, 15.6 inch display"
    },
    {
        "name": "Samsung Galaxy A55",
        "category": "phone",
        "price": 27999,
        "brand": "Samsung",
        "rating": 4.4,
        "features": "5G, 50MP camera, AMOLED, 5000mAh battery"
    },
    {
        "name": "OnePlus Nord 4",
        "category": "phone",
        "price": 29999,
        "brand": "OnePlus",
        "rating": 4.5,
        "features": "5G, 50MP camera, AMOLED, fast charging"
    },
    {
        "name": "Nothing Phone 3a",
        "category": "phone",
        "price": 24999,
        "brand": "Nothing",
        "rating": 4.3,
        "features": "5G, AMOLED, good camera, long battery"
    },
    {
        "name": "Sony WH-1000XM5",
        "category": "headphones",
        "price": 29990,
        "brand": "Sony",
        "rating": 4.6,
        "features": "ANC, wireless, long battery"
    },
    {
        "name": "JBL Live 770NC",
        "category": "headphones",
        "price": 9999,
        "brand": "JBL",
        "rating": 4.4,
        "features": "ANC, wireless, 65-hour battery"
    }
]


# -------------------------------------------------
# MODEL
# -------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.environ["GEMINI_API_KEY"],
    temperature=0
)


# -------------------------------------------------
# PRODUCT SEARCH FUNCTIONS
# -------------------------------------------------

def search_products(query: str):
    words = query.lower().split()

    matches = []

    for product in PRODUCTS:
        text = (
            product["name"] + " " +
            product["category"] + " " +
            product["brand"] + " " +
            product["features"]
        ).lower()

        if any(word in text for word in words if len(word) > 2):
            matches.append(product)

    if not matches:
        matches = PRODUCTS

    return matches


def filter_by_budget(category: str, max_price: float):
    return [
        p for p in PRODUCTS
        if p["category"].lower() == category.lower()
        and p["price"] <= max_price
    ]


def compare_products(product_names: str):
    names = [x.strip().lower() for x in product_names.split(",")]

    results = []

    for product in PRODUCTS:
        if product["name"].lower() in names:
            results.append(product)

    return results


# -------------------------------------------------
# INPUT
# -------------------------------------------------

class AgentInput(BaseModel):
    input: str = Field(description="Shopping request")


# -------------------------------------------------
# SHOPPING ASSISTANT
# -------------------------------------------------

def shopping_assistant(user_request: str):

    request = user_request.lower()

    selected = []

    # Detect category
    if "laptop" in request:
        category = "laptop"
    elif "phone" in request or "smartphone" in request:
        category = "phone"
    elif "headphone" in request:
        category = "headphones"
    else:
        category = None

    # Detect budget
    import re

    budget_match = re.search(r'₹?\s*(\d{4,6})', request)

    if budget_match:
        budget = int(budget_match.group(1))
    else:
        budget = None

    # Filter products
    for product in PRODUCTS:

        if category and product["category"] != category:
            continue

        if budget and product["price"] > budget:
            continue

        selected.append(product)

    # If nothing found
    if not selected:
        selected = PRODUCTS

    # Prepare product information
    product_text = json.dumps(selected, indent=2)

    prompt = f"""
You are an AI Shopping Assistant.

User request:
{user_request}

Available products:
{product_text}

Give a clear shopping recommendation.

Rules:
1. Only use the products and information provided above.
2. Never invent prices or specifications.
3. Mention the price of suitable products.
4. Mention important matching features.
5. If several products match, compare them briefly.
6. Keep the answer easy to understand.
"""

    response = llm.invoke(prompt)

    return response.content


# -------------------------------------------------
# FASTAPI
# -------------------------------------------------

app = FastAPI(
    title="Shopping Assistant Agent",
    version="1.0"
)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/agent")
def agent_endpoint(data: AgentInput):

    answer = shopping_assistant(data.input)

    return {
        "output": answer
    }
