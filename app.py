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
# GEMINI
# ==========================================

api_key = os.environ["GEMINI_API_KEY"]

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key
)


# ==========================================
# INPUT / OUTPUT
# ==========================================

class AgentInput(BaseModel):
    input: str = Field(description="Shopping request")


class AgentOutput(BaseModel):
    output: str


# ==========================================
# GEMINI CALL
# ==========================================

def call_gemini(prompt):

    for attempt in range(3):

        try:
            response = llm.invoke(prompt)

            if response.content:
                return response.content

        except Exception as e:

            error_text = str(e)

            if "503" not in error_text and "UNAVAILABLE" not in error_text:
                break

            time.sleep(5 * (2 ** attempt))

    return "Gemini is temporarily unavailable. Please try again."


# ==========================================
# SHOPPING ASSISTANT
# ==========================================

def shopping_assistant(user_request):

    request = user_request.lower()

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
    budget_match = re.search(
        r'₹?\s*(\d{4,6})',
        request
    )

    if budget_match:
        budget = int(budget_match.group(1))
    else:
        budget = None


    # Select products
    selected = []

    for product in PRODUCTS:

        if category and product["category"] != category:
            continue

        if budget and product["price"] > budget:
            continue

        selected.append(product)


    # If nothing matches
    if not selected:
        selected = PRODUCTS


    product_text = json.dumps(
        selected,
        indent=2
    )


    # ==========================================
    # SIMPLE OUTPUT PROMPT
    # ==========================================

    prompt = f"""
You are a simple AI Shopping Assistant.

USER REQUEST:
{user_request}

AVAILABLE PRODUCTS:
{product_text}

Give the answer in this simple format.

For laptops use:

Laptop options under ₹60,000

💻 Product Name — ₹Price
Important features

💻 Product Name — ₹Price
Important features

💻 Product Name — ₹Price
Important features

Best match: Product Name
Budget option: Product Name

For phones use:

Phone options under the user's budget

📱 Product Name — ₹Price
Important features

Best match: Product Name
Budget option: Product Name

For headphones use:

Headphone options under the user's budget

🎧 Product Name — ₹Price
Important features

Best match: Product Name
Budget option: Product Name

RULES:

1. Use only the products provided.
2. Do not invent products.
3. Do not invent prices.
4. Do not show JSON.
5. Do not show technical metadata.
6. Do not give long explanations.
7. Keep the answer short and simple.
8. Mention important features matching the user's request.
9. Use ₹ for prices.
10. Give only the final shopping answer.
11. Do not use Markdown tables.
12. Do not add unnecessary headings.
"""

    return call_gemini(prompt)


# ==========================================
# LANGSERVE
# ==========================================

def run_agent(data):

    user_input = data["input"]

    answer = shopping_assistant(user_input)

    return {
        "output": answer
    }


chain = RunnableLambda(
    run_agent
).with_types(
    input_type=AgentInput,
    output_type=AgentOutput
)


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
