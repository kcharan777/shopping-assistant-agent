import React from 'react';
import { Search, Sliders, Laptop, Smartphone, Headphones, Watch, Tablet, Sparkles } from 'lucide-react';

const CATEGORY_ICONS = {
  Laptops: Laptop,
  Smartphones: Smartphone,
  Headphones: Headphones,
  Smartwatches: Watch,
  Tablets: Tablet,
};

export default function SearchConsole({
  categories,
  selectedCategory,
  onSelectCategory,
  query,
  setQuery,
  maxBudget,
  setMaxBudget,
  selectedBrands,
  onToggleBrand,
  selectedFeatures,
  onToggleFeature,
  onSearch,
  isLoading
}) {
  const currentCategoryData = categories.find(c => c.id === selectedCategory) || categories[0] || {};
  const popularBrands = currentCategoryData.popular_brands || ["Lenovo", "HP", "Asus", "Dell", "Apple", "Samsung"];
  const popularFeatures = currentCategoryData.popular_features || ["16GB RAM", "SSD", "Programming", "College", "Fast Charging"];

  const examplePrompts = [
    "Recommend a laptop under ₹60,000 for college, programming, and everyday use",
    "Best smartphone under ₹30,000 with 120Hz display and great battery",
    "Active noise cancelling headphones under ₹8,000 for work calls"
  ];

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      onSearch();
    }
  };

  return (
    <div className="search-console glass-panel">
      {/* Category Tabs */}
      <div className="console-tabs">
        {categories.map((cat) => {
          const IconComp = CATEGORY_ICONS[cat.id] || Laptop;
          const isActive = selectedCategory === cat.id;
          return (
            <button
              key={cat.id}
              className={`category-tab ${isActive ? 'active' : ''}`}
              onClick={() => onSelectCategory(cat.id)}
              type="button"
            >
              <IconComp size={18} />
              <span>{cat.name}</span>
            </button>
          );
        })}
      </div>

      {/* Natural Language Query Input */}
      <div className="query-box-container">
        <input
          type="text"
          className="query-input"
          placeholder={`Describe what you need (e.g. "Recommend a ${selectedCategory?.toLowerCase() || 'laptop'} under ₹${maxBudget ? maxBudget.toLocaleString('en-IN') : '60,000'} for...")`}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button
          className="search-btn"
          onClick={onSearch}
          disabled={isLoading}
          type="button"
        >
          {isLoading ? (
            <span>Searching...</span>
          ) : (
            <>
              <Search size={18} />
              <span>Ask Agent</span>
            </>
          )}
        </button>
      </div>

      {/* Filters Row: Budget & Brands/Features */}
      <div className="filter-row">
        {/* Budget Slider */}
        <div className="filter-group">
          <div className="filter-header">
            <span className="filter-label">Maximum Budget (INR)</span>
            <span className="budget-val-badge">₹{Number(maxBudget).toLocaleString('en-IN')}</span>
          </div>
          <input
            type="range"
            className="budget-slider"
            min={1000}
            max={selectedCategory === 'Laptops' ? 150000 : selectedCategory === 'Smartphones' ? 100000 : 35000}
            step={1000}
            value={maxBudget}
            onChange={(e) => setMaxBudget(Number(e.target.value))}
          />
          <div className="budget-limits">
            <span>₹1,000</span>
            <span>Target Ceiling</span>
            <span>₹{selectedCategory === 'Laptops' ? '1,50,000+' : '35,000+'}</span>
          </div>
        </div>

        {/* Brand Preferences Chips */}
        <div className="filter-group">
          <div className="filter-header">
            <span className="filter-label">Brand Preference (Optional)</span>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>Click to toggle</span>
          </div>
          <div className="quick-tags">
            {popularBrands.map((brand) => {
              const isSelected = selectedBrands.includes(brand);
              return (
                <button
                  key={brand}
                  type="button"
                  className={`tag-chip ${isSelected ? 'selected' : ''}`}
                  onClick={() => onToggleBrand(brand)}
                >
                  {isSelected ? `✓ ${brand}` : `+ ${brand}`}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Desired Feature Chips */}
      <div style={{ marginBottom: '20px' }}>
        <div className="filter-header">
          <span className="filter-label" style={{ fontSize: '0.85rem' }}>Desired Features & Specifications:</span>
        </div>
        <div className="quick-tags">
          {popularFeatures.map((feat) => {
            const isSelected = selectedFeatures.includes(feat);
            return (
              <button
                key={feat}
                type="button"
                className={`tag-chip ${isSelected ? 'selected' : ''}`}
                onClick={() => onToggleFeature(feat)}
              >
                {isSelected ? `★ ${feat}` : feat}
              </button>
            );
          })}
        </div>
      </div>

      {/* Example Prompts */}
      <div className="example-prompts">
        <span style={{ fontWeight: 600 }}>Try asking:</span>
        {examplePrompts.map((p, idx) => (
          <button
            key={idx}
            type="button"
            className="example-btn"
            onClick={() => {
              setQuery(p);
              if (p.toLowerCase().includes("laptop")) onSelectCategory("Laptops");
              else if (p.toLowerCase().includes("smartphone")) onSelectCategory("Smartphones");
              else if (p.toLowerCase().includes("headphone")) onSelectCategory("Headphones");
            }}
          >
            "{p}"
          </button>
        ))}
      </div>
    </div>
  );
}
