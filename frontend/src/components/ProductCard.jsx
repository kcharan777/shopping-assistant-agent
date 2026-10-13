import React from 'react';
import { ExternalLink, ShieldCheck, Star } from 'lucide-react';

export default function ProductCard({ product }) {
  return (
    <div className="mini-card glass-panel">
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>
            {product.brand}
          </span>
          <span style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '4px', 
            fontSize: '0.8rem', 
            color: 'var(--amber-400)',
            fontWeight: 700 
          }}>
            <Star size={13} fill="var(--amber-400)" />
            <span>{product.rating || 4.2}</span>
          </span>
        </div>

        <h4 style={{ fontSize: '1.05rem', marginBottom: '10px', lineHeight: 1.35, color: '#ffffff' }}>
          {product.name}
        </h4>

        <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', marginBottom: '14px' }}>
          <span style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--emerald-400)', fontFamily: 'var(--font-heading)' }}>
            ₹{Number(product.price_inr).toLocaleString('en-IN')}
          </span>
          {product.original_price_inr && (
            <span style={{ fontSize: '0.85rem', color: 'var(--text-dim)', textDecoration: 'line-through' }}>
              ₹{Number(product.original_price_inr).toLocaleString('en-IN')}
            </span>
          )}
        </div>

        {/* Specs badges */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '16px' }}>
          {product.specifications && Object.entries(product.specifications).slice(0, 4).map(([k, v]) => (
            <span key={k} style={{ 
              fontSize: '0.75rem', 
              background: 'rgba(255, 255, 255, 0.05)', 
              border: '1px solid var(--border-subtle)', 
              padding: '3px 8px', 
              borderRadius: '4px',
              color: 'var(--text-secondary)'
            }}>
              <strong>{k}:</strong> {v}
            </span>
          ))}
        </div>

        {product.match_reason && (
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '16px', lineHeight: 1.5 }}>
            {product.match_reason}
          </p>
        )}
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--border-subtle)', paddingTop: '12px' }}>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>
          <ShieldCheck size={14} style={{ display: 'inline', marginRight: '4px', verticalAlign: 'middle', color: 'var(--emerald-400)' }} />
          {product.retailer}
        </span>

        <a
          href={product.retailer_url}
          target="_blank"
          rel="noopener noreferrer"
          style={{ 
            display: 'inline-flex', 
            alignItems: 'center', 
            gap: '4px', 
            fontSize: '0.85rem', 
            color: 'var(--emerald-400)', 
            textDecoration: 'none',
            fontWeight: 600
          }}
        >
          <span>View</span>
          <ExternalLink size={14} />
        </a>
      </div>
    </div>
  );
}
