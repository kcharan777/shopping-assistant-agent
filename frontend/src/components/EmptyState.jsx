import React from 'react';
import { SearchX, RotateCcw } from 'lucide-react';

export default function EmptyState({ onReset, maxBudget }) {
  return (
    <div className="empty-state glass-panel">
      <div className="empty-icon">
        <SearchX size={56} style={{ margin: '0 auto', color: 'var(--text-dim)' }} />
      </div>
      <h3 className="empty-title">No Matching Products Found</h3>
      <p className="empty-desc">
        We couldn't find verified products strictly within ₹{Number(maxBudget || 0).toLocaleString('en-IN')} matching all your selected brand and feature filters.
      </p>
      <div style={{ marginTop: '20px' }}>
        <button
          type="button"
          onClick={onReset}
          className="search-btn"
          style={{ margin: '0 auto', position: 'static' }}
        >
          <RotateCcw size={16} />
          <span>Reset Filters or Broaden Budget</span>
        </button>
      </div>
    </div>
  );
}
