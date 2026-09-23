import os, json
from fastapi import FastAPI
from langserve import add_routes
from langchain_core.tools import tool
from langchain_core.runnables import RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from pydantic import BaseModel, Field

PRODUCTS = [
    {'name':'Acer Aspire 5','category':'laptop','price':54990,'brand':'Acer','rating':4.3,'features':'16GB RAM, 512GB SSD, 15.6 inch display'},
    {'name':'Lenovo IdeaPad Slim 5','category':'laptop','price':59990,'brand':'Lenovo','rating':4.5,'features':'16GB RAM, 512GB SSD, OLED display'},
    {'name':'HP 15','category':'laptop','price':49990,'brand':'HP','rating':4.2,'features':'16GB RAM, 512GB SSD, 15.6 inch display'},
    {'name':'Samsung Galaxy A55','category':'phone','price':27999,'brand':'Samsung','rating':4.4,'features':'5G, 50MP camera, AMOLED, 5000mAh battery'},
    {'name':'OnePlus Nord 4','category':'phone','price':29999,'brand':'OnePlus','rating':4.5,'features':'5G, 50MP camera, AMOLED, fast charging'},
    {'name':'Nothing Phone 3a','category':'phone','price':24999,'brand':'Nothing','rating':4.3,'features':'5G, AMOLED, good camera, long battery life'},
    {'name':'Sony WH-1000XM5','category':'headphones','price':29990,'brand':'Sony','rating':4.6,'features':'ANC, wireless, long battery life'},
    {'name':'JBL Live 770NC','category':'headphones','price':9999,'brand':'JBL','rating':4.4,'features':'ANC, wireless, 65-hour battery'}
]

@tool
def search_products(query: str) -> str:
    '''Search products by name, category, brand or feature.'''
    q=query.lower(); matches=[]
    for p in PRODUCTS:
        text=f"{p['name']} {p['category']} {p['brand']} {p['features']}".lower()
        if any(w in text for w in q.split() if len(w)>2): matches.append(p)
    return json.dumps(matches[:6]) if matches else 'No matching products found.'

@tool
def filter_by_budget(category: str, max_price: float) -> str:
    '''Find products in a category within the maximum price.'''
    matches=[p for p in PRODUCTS if p['category'].lower()==category.lower() and p['price']<=max_price]
    return json.dumps(matches) if matches else 'No products found within that budget.'

@tool
def compare_products(product_names: str) -> str:
    '''Compare comma-separated product names.'''
    names=[n.strip().lower() for n in product_names.split(',')]
    matches=[p for p in PRODUCTS if any(n in p['name'].lower() for n in names)]
    return json.dumps(matches) if matches else 'No matching products found.'

tools=[search_products,filter_by_budget,compare_products]
llm=ChatGoogleGenerativeAI(model='gemini-2.5-flash',api_key=os.environ['GEMINI_API_KEY'],temperature=0)
agent=create_agent(model=llm,tools=tools,system_prompt='You are an AI Shopping Assistant. Use tools for product data. Never invent prices, ratings or specifications. Respect the user budget and explain recommendations clearly.')

class AgentInput(BaseModel):
    input: str = Field(description='Shopping request')

def format_for_agent(x):
    return {'messages':[('user', x['input'] if isinstance(x,dict) else x.input)]}

def extract_text(result):
    messages=result.get('messages',[]) if isinstance(result,dict) else []
    if messages:
        return getattr(messages[-1],'content',str(messages[-1]))
    return str(result)

chain=(RunnableLambda(format_for_agent)|agent|RunnableLambda(extract_text)).with_types(input_type=AgentInput,output_type=str)
app=FastAPI(title='Shopping Assistant Agent',version='1.0')
add_routes(app,chain,path='/agent')

@app.get('/health')
def health(): return {'status':'healthy'}

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app,host='0.0.0.0',port=int(os.environ.get('PORT',8000)))
