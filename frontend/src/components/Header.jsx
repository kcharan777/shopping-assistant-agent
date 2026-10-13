import React from 'react';
import { ShoppingBag, Sparkles, CheckCircle2, AlertCircle } from 'lucide-react';

export default function Header({ backendStatus }) {
  const isHealthy = backendStatus?.status === 'healthy';

  return (
    <header className="app-header">
      <div className="logo-area">
        <div className="logo-badge">
          <ShoppingBag size={24} />
        </div>
        <div className="brand-text">
          <h1>ShopAgent AI</h1>
          <span className="brand-tagline">Real-Time Indian Market E-Commerce Intelligence</span>
        </div>
      </div>

      <div className="header-status">
        <div className="live-indicator">
          <span className="pulse-dot"></span>
          <span>Live Web Search Active</span>
        </div>

        {backendStatus && (
          <div 
            style={{ 
              display: 'inline-flex', 
              alignItems: 'center', 
              gap: '6px', 
              fontSize: '0.8rem',
              color: isHealthy ? 'var(--emerald-400)' : 'var(--amber-400)'
            }}
            title={backendStatus.gemini_configured ? "Google Gemini API connected" : "Local heuristic intelligence active"}
          >
            {isHealthy ? <CheckCircle2 size={16} /> : <AlertCircle size={16} />}
            <span>{isHealthy ? (backendStatus.gemini_configured ? "Gemini 2.5 Active" : "Backend Connected") : "Connecting..."}</span>
          </div>
        )}
      </div>
    </header>
  );
}
