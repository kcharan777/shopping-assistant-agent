import os
import json
import re

from fastapi import FastAPI
from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableLambda
from langserve import add_routes


# --------------------------------------------------
# PRODUCT DATABASE
# --------------------------------------------------

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


# --------------------------------------------------
# GEMINI MODEL
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.environ["GEMINI_API_KEY"],
    temperature=0
)


# --------------------------------------------------
# TOOLS / FUNCTIONS
# --------------------------------------------------

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


# --------------------------------------------------
# INPUT / OUTPUT MODELS
# --------------------------------------------------

class AgentInput(BaseModel):
    input: str = Field(
        description="Shopping request"
    )


class AgentOutput(BaseModel):
    output: str


# --------------------------------------------------
# SHOPPING ASSISTANT
# --------------------------------------------------

def shopping_assistant(user_request: str):

    request = user_request.lower()

    # Find category
    if "laptop" in request:
        category = "laptop"

    elif "phone" in request or "smartphone" in request:
        category = "phone"

    elif "headphone" in request:
        category = "headphones"

    else:
        category = None


    # Find budget
    budget_match = re.search(
        r'₹?\s*(\d{4,6})',
        request
    )

    if budget_match:
        budget = int(budget_match.group(1))
    else:
        budget = None


    # Select matching products
    selected = []

    for product in PRODUCTS:

        if category:
            if product["category"] != category:
                continue

        if budget:
            if product["price"] > budget:
                continue

        selected.append(product)


    # If nothing matches, use all products
    if not selected:
        selected = PRODUCTS


    # Convert products to text for Gemini
    product_text = json.dumps(
        selected,
        indent=2
    )


    # Gemini prompt
    prompt = f"""
You are an AI Shopping Assistant.

USER REQUEST:
{user_request}

AVAILABLE PRODUCTS:
{product_text}

Your job is to help the user choose a suitable product.

RULES:
1. Use ONLY the products and information provided.
2. Do not invent products.
3. Do not invent prices.
4. Do not invent specifications.
5. Mention the product name and price.
6. Mention the important matching features.
7. If multiple products match, compare them briefly.
8. Give a clear recommendation based on the user's requirements.
9. Keep the answer simple and easy to understand.
10. Do not say that the output is predefined.
"""


    # Ask Gemini to generate final answer
    response = llm.invoke(prompt)

    return response.content


# --------------------------------------------------
# LANGSERVE FUNCTION
# --------------------------------------------------

def run_agent(data):

    # Get user's input from LangServe
    user_input = data["input"]

    # Generate answer
    answer = shopping_assistant(user_input)

    # Return output
    return {
        "output": answer
    }


# --------------------------------------------------
# FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="Shopping Assistant Agent",
    version="1.0"
)


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# --------------------------------------------------
# LANGSERVE ROUTE
# --------------------------------------------------

chain = RunnableLambda(run_agent).with_types(
    input_type=AgentInput,
    output_type=AgentOutput
)

add_routes(
    app,
    chain,
    path="/agent"
)


# --------------------------------------------------
# RUN SERVER
# --------------------------------------------------

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
