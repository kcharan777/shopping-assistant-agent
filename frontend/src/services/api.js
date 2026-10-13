// API client for Shopping Assistant Agent

const API_BASE = import.meta.env.VITE_API_URL || '';

export async function checkBackendHealth() {
  try {
    const res = await fetch(`${API_BASE}/api/health`);
    if (!res.ok) throw new Error(`Health check returned status ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn("Backend health check failed:", err.message);
    return { status: "offline", error: err.message };
  }
}

export async function fetchCategories() {
  try {
    const res = await fetch(`${API_BASE}/api/categories`);
    if (!res.ok) throw new Error("Failed to load categories");
    return await res.json();
  } catch (err) {
    console.warn("Categories fetch fallback:", err.message);
    return {
      categories: [
        { id: "Laptops", name: "Laptops", suggested_budget: 60000, popular_brands: ["Lenovo", "HP", "Asus", "Dell"], popular_features: ["16GB RAM", "SSD", "Programming"] },
        { id: "Smartphones", name: "Smartphones", suggested_budget: 30000, popular_brands: ["Samsung", "OnePlus", "Xiaomi"], popular_features: ["5G", "120Hz", "Fast Charging"] },
        { id: "Headphones", name: "Headphones", suggested_budget: 8000, popular_brands: ["Sony", "Boat", "JBL"], popular_features: ["ANC", "30h Battery"] }
      ]
    };
  }
}

export async function getRecommendations(payload) {
  const res = await fetch(`${API_BASE}/api/recommend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Server returned error code ${res.status}`);
  }

  return await res.json();
}
