import React from 'react';
import { Award, PiggyBank, ExternalLink, Check, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function SpotlightRecommendations({ bestMatch, budgetMatch }) {
  if (!bestMatch && !budgetMatch) return null;

  return (
    <div className="spotlight-grid">
      {/* Best Overall Match Card */}
      {bestMatch && (
        <div className="spotlight-card best-overall glass-panel">
          <div>
            <div className="spotlight-badge best-badge">
              <Award size={16} />
              <span>Recommended Best Overall Match</span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <span style={{ fontSize: '0.85rem', color: 'var(--emerald-400)', fontWeight: 600 }}>
                {bestMatch.brand} • {bestMatch.category}
              </span>
              <span style={{ 
                background: 'var(--emerald-glass)', 
                color: 'var(--emerald-400)', 
                padding: '2px 8px', 
                borderRadius: '6px', 
                fontSize: '0.8rem',
                fontWeight: 700 
              }}>
                Match Score: {bestMatch.match_score}/100
              </span>
            </div>

            <h3 className="card-title">{bestMatch.name}</h3>

            <div className="price-container">
              <span className="current-price">₹{Number(bestMatch.price_inr).toLocaleString('en-IN')}</span>
              {bestMatch.original_price_inr && (
                <span className="original-price">₹{Number(bestMatch.original_price_inr).toLocaleString('en-IN')}</span>
              )}
              {bestMatch.original_price_inr && (
                <span className="savings-tag">
                  Save ₹{(bestMatch.original_price_inr - bestMatch.price_inr).toLocaleString('en-IN')}
                </span>
              )}
            </div>

            {/* Specifications Grid */}
            {bestMatch.specifications && Object.keys(bestMatch.specifications).length > 0 && (
              <div className="spec-grid">
                {Object.entries(bestMatch.specifications).slice(0, 6).map(([key, val]) => (
                  <div key={key} className="spec-item">
                    <span className="spec-key">{key}</span>
                    <span className="spec-val">{val}</span>
                  </div>
                ))}
              </div>
            )}

            {/* Match Reason */}
            {bestMatch.match_reason && (
              <div style={{ 
                background: 'rgba(16, 185, 129, 0.08)', 
                borderLeft: '3px solid var(--emerald-500)', 
                padding: '10px 14px', 
                borderRadius: '4px',
                fontSize: '0.85rem',
                color: 'var(--text-secondary)',
                marginBottom: '16px'
              }}>
                <strong>Why it fits: </strong> {bestMatch.match_reason}
              </div>
            )}

            {/* Strengths */}
            {bestMatch.strengths && bestMatch.strengths.length > 0 && (
              <div className="reasons-box">
                <div className="reasons-title">Key Strengths</div>
                {bestMatch.strengths.map((str, idx) => (
                  <div key={idx} className="reason-bullet">
                    <Check size={16} color="var(--emerald-400)" style={{ flexShrink: 0, marginTop: '3px' }} />
                    <span>{str}</span>
                  </div>
                ))}
              </div>
            )}

            {/* Limitations */}
            {bestMatch.limitations && bestMatch.limitations.length > 0 && (
              <div className="limitations-box">
                <div className="reasons-title">Considerations & Limitations</div>
                {bestMatch.limitations.map((lim, idx) => (
                  <div key={idx} className="limitation-bullet">
                    <AlertTriangle size={15} color="var(--rose-400)" style={{ flexShrink: 0, marginTop: '3px' }} />
                    <span>{lim}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="action-bar">
            <div className="retailer-info">
              <span className="retailer-name">
                <ShieldCheck size={14} style={{ display: 'inline', marginRight: '4px', verticalAlign: 'middle', color: 'var(--emerald-400)' }} />
                {bestMatch.retailer}
              </span>
              <span className="stock-status">{bestMatch.availability}</span>
            </div>

            <a
              href={bestMatch.retailer_url}
              target="_blank"
              rel="noopener noreferrer"
              className="buy-button"
            >
              <span>View Product</span>
              <ExternalLink size={16} />
            </a>
          </div>
        </div>
      )}

      {/* Budget-Friendly Alternative Card */}
      {budgetMatch && (
        <div className="spotlight-card budget-friendly glass-panel">
          <div>
            <div className="spotlight-badge budget-badge">
              <PiggyBank size={16} />
              <span>Budget-Friendly Alternative</span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <span style={{ fontSize: '0.85rem', color: 'var(--amber-400)', fontWeight: 600 }}>
                {budgetMatch.brand} • {budgetMatch.category}
              </span>
              <span style={{ 
                background: 'rgba(245, 158, 11, 0.15)', 
                color: 'var(--amber-400)', 
                padding: '2px 8px', 
                borderRadius: '6px', 
                fontSize: '0.8rem',
                fontWeight: 700 
              }}>
                Match Score: {budgetMatch.match_score}/100
              </span>
            </div>

            <h3 className="card-title">{budgetMatch.name}</h3>

            <div className="price-container">
              <span className="current-price">₹{Number(budgetMatch.price_inr).toLocaleString('en-IN')}</span>
              {bestMatch && bestMatch.price_inr > budgetMatch.price_inr && (
                <span className="savings-tag" style={{ background: 'rgba(245, 158, 11, 0.2)', color: 'var(--amber-400)' }}>
                  Saves ₹{(bestMatch.price_inr - budgetMatch.price_inr).toLocaleString('en-IN')} vs Top Match
                </span>
              )}
            </div>

            {/* Specifications Grid */}
            {budgetMatch.specifications && Object.keys(budgetMatch.specifications).length > 0 && (
              <div className="spec-grid">
                {Object.entries(budgetMatch.specifications).slice(0, 6).map(([key, val]) => (
                  <div key={key} className="spec-item">
                    <span className="spec-key">{key}</span>
                    <span className="spec-val">{val}</span>
                  </div>
                ))}
              </div>
            )}

            {/* Match Reason */}
            {budgetMatch.match_reason && (
              <div style={{ 
                background: 'rgba(245, 158, 11, 0.08)', 
                borderLeft: '3px solid var(--amber-500)', 
                padding: '10px 14px', 
                borderRadius: '4px',
                fontSize: '0.85rem',
                color: 'var(--text-secondary)',
                marginBottom: '16px'
              }}>
                <strong>Value Proposition: </strong> {budgetMatch.match_reason}
              </div>
            )}

            {/* Strengths */}
            {budgetMatch.strengths && budgetMatch.strengths.length > 0 && (
              <div className="reasons-box">
                <div className="reasons-title">Key Strengths</div>
                {budgetMatch.strengths.map((str, idx) => (
                  <div key={idx} className="reason-bullet">
                    <Check size={16} color="var(--amber-400)" style={{ flexShrink: 0, marginTop: '3px' }} />
                    <span>{str}</span>
                  </div>
                ))}
              </div>
            )}

            {/* Limitations */}
            {budgetMatch.limitations && budgetMatch.limitations.length > 0 && (
              <div className="limitations-box">
                <div className="reasons-title">Trade-offs & Differences</div>
                {budgetMatch.limitations.map((lim, idx) => (
                  <div key={idx} className="limitation-bullet">
                    <AlertTriangle size={15} color="var(--rose-400)" style={{ flexShrink: 0, marginTop: '3px' }} />
                    <span>{lim}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="action-bar">
            <div className="retailer-info">
              <span className="retailer-name">
                <ShieldCheck size={14} style={{ display: 'inline', marginRight: '4px', verticalAlign: 'middle', color: 'var(--amber-400)' }} />
                {budgetMatch.retailer}
              </span>
              <span className="stock-status" style={{ color: 'var(--amber-400)' }}>{budgetMatch.availability}</span>
            </div>

            <a
              href={budgetMatch.retailer_url}
              target="_blank"
              rel="noopener noreferrer"
              className="buy-button"
              style={{ background: 'var(--amber-400)', color: '#0b0f17' }}
            >
              <span>View Product</span>
              <ExternalLink size={16} />
            </a>
          </div>
        </div>
      )}
    </div>
  );
}
