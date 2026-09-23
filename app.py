import os
import json
import re
import time

from fastapi import FastAPI
from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableLambda
from langserve import add_routes


# ==========================================
# PRODUCT DATABASE
# ==========================================

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


# ==========================================
# GEMINI MODELS
# ==========================================

api_key = os.environ["GEMINI_API_KEY"]

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key
)

# Backup model
backup_llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=api_key
)


# ==========================================
# PRODUCT FUNCTIONS
# ==========================================

def search_products(query: str):

    words = query.lower().split()
    matches = []

    for product in PRODUCTS:

        text = (
            product["name"]
            + " "
            + product["category"]
            + " "
            + product["brand"]
            + " "
            + product["features"]
        ).lower()

        for word in words:

            if len(word) > 2 and word in text:
                matches.append(product)
                break

    return matches


def filter_by_budget(category: str, max_price: float):

    return [
        product
        for product in PRODUCTS
        if product["category"].lower() == category.lower()
        and product["price"] <= max_price
    ]


def compare_products(product_names: str):

    names = [
        name.strip().lower()
        for name in product_names.split(",")
    ]

    return [
        product
        for product in PRODUCTS
        if product["name"].lower() in names
    ]


# ==========================================
# INPUT / OUTPUT
# ==========================================

class AgentInput(BaseModel):

    input: str = Field(
        description="Shopping request"
    )


class AgentOutput(BaseModel):

    output: str


# ==========================================
# GEMINI CALL WITH RETRY
# ==========================================

def call_gemini(prompt):

    # Try Gemini 3.6 Flash up to 3 times

    for attempt in range(3):

        try:

            response = llm.invoke(prompt)

            if response.content:
                return response.content

        except Exception as e:

            error_text = str(e)

            if "503" not in error_text and "UNAVAILABLE" not in error_text:
                break

            wait_time = 5 * (2 ** attempt)

            time.sleep(wait_time)


    # Try backup model

    try:

        response = backup_llm.invoke(prompt)

        if response.content:
            return response.content

    except Exception as e:

        error_text = str(e)

        return (
            "Gemini is temporarily unavailable. "
            "Please try again after a few minutes.\n\n"
            f"Error: {error_text}"
        )

    return "Gemini did not return a response. Please try again."


# ==========================================
# SHOPPING ASSISTANT
# ==========================================

def shopping_assistant(user_request: str):

    request = user_request.lower()


    # --------------------------------------
    # Detect category
    # --------------------------------------

    if "laptop" in request:

        category = "laptop"

    elif "phone" in request or "smartphone" in request:

        category = "phone"

    elif "headphone" in request:

        category = "headphones"

    else:

        category = None


    # --------------------------------------
    # Detect budget
    # --------------------------------------

    budget_match = re.search(
        r'₹?\s*(\d{4,6})',
        request
    )

    if budget_match:

        budget = int(budget_match.group(1))

    else:

        budget = None


    # --------------------------------------
    # Select matching products
    # --------------------------------------

    selected = []

    for product in PRODUCTS:

        if category:

            if product["category"] != category:
                continue

        if budget:

            if product["price"] > budget:
                continue

        selected.append(product)


    # If no exact match
    if not selected:

        selected = PRODUCTS


    # --------------------------------------
    # Convert products to JSON
    # --------------------------------------

    product_text = json.dumps(
        selected,
        indent=2
    )


    # --------------------------------------
    # Gemini prompt
    # --------------------------------------

    prompt = f"""
You are an AI Shopping Assistant.

USER REQUEST:
{user_request}

AVAILABLE PRODUCTS:
{product_text}

Help the user choose a suitable product.

Rules:

1. Use only the products provided above.
2. Do not invent products.
3. Do not invent prices.
4. Do not invent specifications.
5. Mention product names and prices.
6. Mention important matching features.
7. Compare products when several match.
8. Consider the user's budget and requirements.
9. Give a clear and useful recommendation.
10. Keep the answer simple and easy to understand.
"""


    # --------------------------------------
    # Call Gemini
    # --------------------------------------

    answer = call_gemini(prompt)

    return answer


# ==========================================
# LANGSERVE
# ==========================================

def run_agent(data):

    user_input = data["input"]

    answer = shopping_assistant(user_input)

    return {
        "output": answer
    }


# ==========================================
# FASTAPI
# ==========================================

app = FastAPI(
    title="Shopping Assistant Agent",
    version="1.0"
)


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ==========================================
# LANGSERVE PLAYGROUND
# ==========================================

chain = RunnableLambda(
    run_agent
).with_types(
    input_type=AgentInput,
    output_type=AgentOutput
)


add_routes(
    app,
    chain,
    path="/agent"
)


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    import uvicorn

    port = int(
        os.environ.get("PORT", 8000)
    )

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )
