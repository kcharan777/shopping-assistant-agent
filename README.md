# 🛍️ ShopAgent AI — Autonomous E-Commerce Shopping Assistant

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-4285F4?logo=google&logoColor=white)](https://aistudio.google.com/)
[![Render Deploy](https://img.shields.io/badge/Render-Ready-46E3B7?logo=render&logoColor=white)](https://render.com)

A professional, full-stack, AI-powered **Shopping Assistant Agent** built specifically for the Indian e-commerce market. The agent queries **live real-time online data** (from Amazon.in, Flipkart, Croma, and Reliance Digital), enforces strict budget constraints in Indian Rupees (₹), performs deterministic hardware comparisons, and synthesizes reasoned buying advice via Google Gemini.

---

## 🌟 Key Features

1. **Live Real-Time Online Data**:
   - Queries live Indian e-commerce platforms (Amazon.in, Flipkart, Croma) in real-time.
   - Extracts current market prices in INR (₹), verified merchant links, and hardware specifications.
2. **Deterministic Budget & Spec Filtering**:
   - Strictly enforces budget caps (`price <= max_budget`).
   - Evaluates brand preferences and spec keywords deterministically.
3. **Dual Recommendation Strategy**:
   - **Recommended Best Overall Match**: The highest-scoring product meeting performance needs.
   - **Budget-Friendly Alternative**: A high-value alternative saving 15-30% in cost with clear trade-off explanations.
4. **Side-by-Side Comparison Matrix**:
   - Compares Processor, RAM, SSD Storage, Display, and Compatibility scores with highlighted winner cells.
5. **AI Executive Verdict (Google Gemini)**:
   - Evaluates use-cases (e.g. college programming, everyday multitasking) and explains strengths & limitations.
6. **Emerald & Charcoal UI/UX**:
   - Dark mode glassmorphism interface, interactive INR budget sliders, and mobile-responsive layout.

---

## 🏗️ System Architecture

```
User Natural Language Input / Filters
              │
              ▼
   FastAPI Orchestrator
   ├── 1. Live Web Search Engine (DDGS Indian E-commerce Scraper)
   ├── 2. Spec & Price Normalizer (Regex + Heuristics + Gemini)
   ├── 3. Deterministic Scorer & Ranker (Strict <= ₹ Budget)
   ├── 4. Dual Match Selector (Best Match + Budget Alternative)
   └── 5. Gemini 2.5 Reasoning Engine (Executive Verdict & Pros/Cons)
              │
              ▼
    React.js Dashboard
    ├── Live Processing Stepper
    ├── Spotlight Cards with Verified Links (Amazon / Flipkart)
    ├── Side-by-Side Comparison Matrix
    └── Shortlisted Product Grid
```

---

## 📁 Repository Structure

```
agents/
├── backend/
│   ├── .venv/                      # Python virtual environment
│   ├── services/
│   │   ├── online_search.py        # Live online search & price/spec extraction
│   │   ├── gemini_agent.py         # Google Gemini intent parsing & reasoning
│   │   ├── recommender.py          # Deterministic ranking & comparison matrix
│   │   └── catalog.py              # Modular reference catalogue
│   ├── models.py                   # Pydantic schemas (Product, Request, Response)
│   ├── main.py                     # FastAPI server, endpoints & static serving
│   ├── test_backend.py             # Pytest test suite (9 verified tests)
│   ├── requirements.txt            # Python dependencies
│   └── .env.example                # Backend environment template
├── frontend/
│   ├── src/
│   │   ├── components/             # Header, Hero, Console, Spotlight, Matrix, etc.
│   │   ├── services/api.js         # API client
│   │   ├── App.jsx                 # Root UI coordinator
│   │   └── index.css               # Emerald-charcoal glassmorphism design system
│   ├── package.json
│   └── vite.config.js
├── .env.example                    # Root environment template
├── .gitignore                      # Git ignore rules
├── Procfile                        # PaaS / Render process file
├── render.yaml                     # Render Infrastructure-as-Code blueprint
└── README.md                       # Documentation
```

---

## 🚀 Quickstart: Running Locally

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Node.js 18+ (tested on v24)
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/shopping-assistant-agent.git
cd shopping-assistant-agent
```

### 3. Backend Setup
```bash
# Create and activate virtual environment
python -m venv backend/.venv

# Windows Powershell
.\backend\.venv\Scripts\Activate.ps1

# Linux / macOS
source backend/.venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Configure Environment Variables
cp .env.example .env
```

Add your Google Gemini API key to `.env`:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_from_google_ai_studio
```
*(Get a free key at [Google AI Studio](https://aistudio.google.com/))*

Start the FastAPI server:
```bash
uvicorn backend.main:app --reload --port 8000
```
API Documentation will be live at: `http://localhost:8000/docs`

### 4. Frontend Setup
In a new terminal:
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 🧪 Automated Testing

Run the backend test suite:
```bash
.\backend\.venv\Scripts\python -m pytest backend/test_backend.py -v
```
All 9 tests verify:
- API Health Check (`/api/health`)
- Category & filter endpoints (`/api/categories`)
- Indian Rupee regex price parser (`₹`, `Rs.`, `INR`)
- Spec extraction (RAM, SSD, Processor)
- Retailer link identification (Amazon, Flipkart, Croma)
- Strict budget filter enforcement (`price <= max_budget`)
- Recommender scoring logic & comparison matrix generation
- End-to-end `/api/recommend` endpoint

---

## 🌐 Deploy to Render

### Option 1: Blueprint Deployment (Recommended)
1. Push your repository to GitHub.
2. In [Render Dashboard](https://dashboard.render.com/), click **New** > **Blueprint**.
3. Connect your GitHub repository.
4. Render will read `render.yaml` and configure:
   - **Backend Web Service**: Python FastAPI server.
   - **Frontend Static Site**: Built React application with API rewrites.
5. Add your `GEMINI_API_KEY` under the backend service's Environment settings.

### Option 2: Unified Single-Service Deployment
Because FastAPI in `backend/main.py` is pre-configured to automatically serve `frontend/dist` when built:
1. Build frontend: `cd frontend && npm install && npm run build && cd ..`
2. Start command on Render: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

---

## 📤 Pushing to GitHub

To push your code to your GitHub account:

```bash
# 1. Stage all files
git add .

# 2. Commit
git commit -m "feat: complete AI shopping assistant agent with live online data"

# 3. Add your GitHub remote repository (replace with your URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git

# 4. Push to main branch
git branch -M main
git push -u origin main
```

---

## 💡 Example API Usage

### Request
```http
POST /api/recommend
Content-Type: application/json

{
  "query": "Recommend a laptop under ₹60,000 for college, programming, and everyday use",
  "category": "Laptops",
  "max_budget": 60000,
  "preferred_brands": ["Lenovo", "HP", "Asus"],
  "required_features": ["16GB RAM", "SSD"],
  "use_live_search": true
}
```

### Response
```json
{
  "query_summary": "Results for 'Recommend a laptop under ₹60,000 for college, programming, and everyday use' (Budget: <= ₹60,000)",
  "best_overall_match": {
    "name": "Lenovo IdeaPad Slim 3 12th Gen Intel Core i5",
    "brand": "Lenovo",
    "price_inr": 52990.0,
    "retailer": "Amazon.in",
    "retailer_url": "https://www.amazon.in/...",
    "match_score": 93,
    "specifications": {
      "Processor": "Intel Core i5-1235U",
      "RAM": "16GB DDR4",
      "Storage": "512GB SSD"
    }
  },
  "budget_friendly_match": {
    "name": "ASUS Vivobook 15 AMD Ryzen 7 5800HS",
    "brand": "Asus",
    "price_inr": 48990.0,
    "retailer": "Amazon.in",
    "retailer_url": "https://www.amazon.in/...",
    "match_score": 87
  },
  "executive_verdict": "For college and programming, the Lenovo IdeaPad Slim 3 offers...",
  "is_live_data": true
}
```

---

## 🛠️ Troubleshooting

- **Gemini API Key Missing**: The app automatically uses deterministic heuristics if `GEMINI_API_KEY` is not supplied, preventing crashes. To activate generative reasoning, add `GEMINI_API_KEY` to `.env`.
- **CORS Errors**: Set `FRONTEND_URL` in `.env` to include your client domains (e.g. `http://localhost:5173,https://your-app.onrender.com`).
- **Live Search Rate Limiting**: The live search engine handles transient delays gracefully and falls back to verified reference data when network connectivity is restricted.
