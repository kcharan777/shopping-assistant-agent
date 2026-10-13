import React from 'react';
import { Columns3, Trophy } from 'lucide-react';

export default function ComparisonTable({ comparisonAspects, products }) {
  if (!comparisonAspects || comparisonAspects.length === 0 || !products || products.length === 0) {
    return null;
  }

  const shortlistedProducts = products.slice(0, 4);

  return (
    <div className="comparison-section glass-panel">
      <div className="section-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--emerald-400)', marginBottom: '4px' }}>
          <Columns3 size={18} />
          <span style={{ fontWeight: 700, fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Specification Breakdown
          </span>
        </div>
        <h3 className="section-title">Side-by-Side Product Comparison</h3>
        <p className="section-sub">
          Detailed hardware and pricing matrix comparing shortlisted options within your budget constraints.
        </p>
      </div>

      <div className="table-responsive">
        <table className="compare-table">
          <thead>
            <tr>
              <th style={{ width: '22%' }}>Evaluation Aspect</th>
              {shortlistedProducts.map((p) => (
                <th key={p.id}>
                  <div style={{ fontWeight: 700, color: '#ffffff', fontSize: '0.9rem' }}>
                    {p.name.length > 36 ? p.name.substring(0, 36) + '...' : p.name}
                  </div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--emerald-400)', marginTop: '2px' }}>
                    ₹{Number(p.price_inr).toLocaleString('en-IN')}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {comparisonAspects.map((aspect, idx) => (
              <tr key={idx}>
                <td className="feature-header">
                  <div>{aspect.feature_name}</div>
                  {aspect.note && (
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginTop: '3px', fontWeight: 400 }}>
                      {aspect.note}
                    </div>
                  )}
                </td>
                {shortlistedProducts.map((p) => {
                  const val = aspect.product_values[p.id] || "Standard";
                  const isWinner = aspect.winner_product_id === p.id;
                  return (
                    <td key={p.id} className={isWinner ? "winner-cell" : ""}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                        {isWinner && <Trophy size={14} color="var(--emerald-400)" />}
                        <span>{val}</span>
                      </div>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
