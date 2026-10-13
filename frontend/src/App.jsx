import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import SearchConsole from './components/SearchConsole';
import ProcessingStepper from './components/ProcessingStepper';
import SpotlightRecommendations from './components/SpotlightRecommendations';
import ComparisonTable from './components/ComparisonTable';
import ProductCard from './components/ProductCard';
import EmptyState from './components/EmptyState';
import { checkBackendHealth, fetchCategories, getRecommendations } from './services/api';
import { Sparkles, AlertCircle, ShoppingCart } from 'lucide-react';

export default function App() {
  const [backendStatus, setBackendStatus] = useState(null);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('Laptops');
  const [query, setQuery] = useState('Recommend a laptop under ₹60,000 for college, programming, and everyday use');
  const [maxBudget, setMaxBudget] = useState(60000);
  const [selectedBrands, setSelectedBrands] = useState([]);
  const [selectedFeatures, setSelectedFeatures] = useState([]);
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Initialize backend health and categories
  useEffect(() => {
    async function init() {
      const health = await checkBackendHealth();
      setBackendStatus(health);

      const catData = await fetchCategories();
      if (catData?.categories) {
        setCategories(catData.categories);
      }
    }
    init();
  }, []);

  // Category switch helper
  const handleSelectCategory = (catId) => {
    setSelectedCategory(catId);
    setSelectedBrands([]);
    setSelectedFeatures([]);
    
    // Set appropriate default budget for the category
    const found = categories.find(c => c.id === catId);
    if (found?.suggested_budget) {
      setMaxBudget(found.suggested_budget);
    }
  };

  const handleToggleBrand = (brand) => {
    setSelectedBrands(prev => 
      prev.includes(brand) ? prev.filter(b => b !== brand) : [...prev, brand]
    );
  };

  const handleToggleFeature = (feat) => {
    setSelectedFeatures(prev =>
      prev.includes(feat) ? prev.filter(f => f !== feat) : [...prev, feat]
    );
  };

  const handleSearch = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const payload = {
        query: query.trim(),
        category: selectedCategory,
        max_budget: maxBudget,
        preferred_brands: selectedBrands,
        required_features: selectedFeatures,
        use_live_search: true
      };

      const response = await getRecommendations(payload);
      setResults(response);
    } catch (err) {
      console.error("Search error:", err);
      setError(err.message || "Failed to fetch shopping recommendations. Please verify backend is running.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetFilters = () => {
    setMaxBudget(80000);
    setSelectedBrands([]);
    setSelectedFeatures([]);
    setQuery(`Best ${selectedCategory.toLowerCase()} recommendations`);
  };

  return (
    <div className="app-container">
      <Header backendStatus={backendStatus} />
      <Hero />

      <SearchConsole
        categories={categories}
        selectedCategory={selectedCategory}
        onSelectCategory={handleSelectCategory}
        query={query}
        setQuery={setQuery}
        maxBudget={maxBudget}
        setMaxBudget={setMaxBudget}
        selectedBrands={selectedBrands}
        onToggleBrand={handleToggleBrand}
        selectedFeatures={selectedFeatures}
        onToggleFeature={handleToggleFeature}
        onSearch={handleSearch}
        isLoading={isLoading}
      />

      {/* Loading Stepper */}
      {isLoading && <ProcessingStepper />}

      {/* Error Banner */}
      {error && (
        <div style={{
          background: 'rgba(239, 68, 68, 0.12)',
          border: '1px solid rgba(239, 68, 68, 0.3)',
          color: '#fca5a5',
          padding: '16px 20px',
          borderRadius: 'var(--radius-md)',
          marginBottom: '32px',
          display: 'flex',
          alignItems: 'center',
          gap: '12px'
        }}>
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {/* Results View */}
      {results && !isLoading && (
        <div className="results-container">
          {/* Executive Verdict */}
          {results.executive_verdict && (
            <div className="verdict-card glass-panel">
              <div className="verdict-header">
                <span className="verdict-badge">AI Buying Verdict</span>
                <span style={{ fontSize: '0.85rem', color: 'var(--emerald-400)', fontWeight: 600 }}>
                  {results.is_live_data ? "✓ Verified Live Market Data" : "Offline Catalogue Reference"}
                </span>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginLeft: 'auto' }}>
                  {results.search_timestamp}
                </span>
              </div>
              <div className="verdict-body">
                {results.executive_verdict.split('\n\n').map((para, i) => (
                  <p key={i}>{para}</p>
                ))}
              </div>
            </div>
          )}

          {/* Empty State check */}
          {results.total_found === 0 ? (
            <EmptyState onReset={handleResetFilters} maxBudget={maxBudget} />
          ) : (
            <>
              {/* Spotlight Dual Recommendations: Best Overall & Budget Friendly */}
              <SpotlightRecommendations
                bestMatch={results.best_overall_match}
                budgetMatch={results.budget_friendly_match}
              />

              {/* Specification Comparison Table */}
              {results.comparison_aspects && results.comparison_aspects.length > 0 && (
                <ComparisonTable
                  comparisonAspects={results.comparison_aspects}
                  products={results.all_recommendations}
                />
              )}

              {/* All Shortlisted Candidates */}
              {results.all_recommendations && results.all_recommendations.length > 0 && (
                <div style={{ marginTop: '48px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                    <div>
                      <h3 style={{ fontSize: '1.4rem' }}>All Filtered Candidates ({results.total_found})</h3>
                      <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                        Deterministic ranking ordered by compatibility score and user requirements.
                      </p>
                    </div>
                  </div>

                  <div className="products-grid">
                    {results.all_recommendations.map((prod) => (
                      <ProductCard key={prod.id} product={prod} />
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      )}

      {/* Footer */}
      <footer className="app-footer">
        <p>ShopAgent AI • Powered by FastAPI, Google Gemini, and Real-Time E-Commerce Intelligence</p>
        <div className="footer-links">
          <span className="footer-link">Prices displayed in Indian Rupees (₹)</span>
          <span>•</span>
          <span className="footer-link">Verified Retailers: Amazon.in, Flipkart, Croma</span>
          <span>•</span>
          <span className="footer-link">Strict Budget Determinism</span>
        </div>
      </footer>
    </div>
  );
}
