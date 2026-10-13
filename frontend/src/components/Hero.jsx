import React from 'react';
import { Sparkles, ShieldCheck, Zap } from 'lucide-react';

export default function Hero() {
  return (
    <section className="hero-section">
      <div className="hero-pill">
        <Sparkles size={14} />
        <span>Autonomous Real-Time Shopping Agent</span>
      </div>

      <h2 className="hero-title">
        Find the exact product you need, <span>within your budget</span>.
      </h2>

      <p className="hero-subtitle">
        Tell the agent your requirements in natural language. We crawl live Indian e-commerce data (Amazon.in, Flipkart, Croma), 
        filter by strict budget in INR (₹), compare hardware specifications, and recommend the best overall option alongside a budget-friendly alternative.
      </p>
    </section>
  );
}
