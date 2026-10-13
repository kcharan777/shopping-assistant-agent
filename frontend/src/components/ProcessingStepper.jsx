import React, { useEffect, useState } from 'react';
import { Globe, Cpu, CheckCircle, Sparkles } from 'lucide-react';

export default function ProcessingStepper() {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const timer1 = setTimeout(() => setCurrentStep(1), 800);
    const timer2 = setTimeout(() => setCurrentStep(2), 1800);
    const timer3 = setTimeout(() => setCurrentStep(3), 2800);
    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
      clearTimeout(timer3);
    };
  }, []);

  const steps = [
    { label: "Querying Live Web", desc: "Searching Amazon.in & Flipkart", icon: Globe },
    { label: "Extracting Specs", desc: "Parsing INR prices & hardware", icon: Cpu },
    { label: "Deterministic Ranking", desc: "Filtering budget & scoring", icon: CheckCircle },
    { label: "Gemini Synthesis", desc: "Generating expert verdict", icon: Sparkles }
  ];

  return (
    <div className="stepper-card glass-panel">
      <h3 style={{ fontSize: '1.1rem', marginBottom: '4px' }}>Agent Workflow in Progress</h3>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
        Gathering live market listings and comparing specifications...
      </p>

      <div className="stepper-steps">
        {steps.map((step, idx) => {
          const IconComp = step.icon;
          const isActive = idx <= currentStep;
          return (
            <div key={idx} className="step-item">
              <div className={`step-circle ${isActive ? 'active' : ''}`}>
                <IconComp size={18} />
              </div>
              <span className="step-title" style={{ color: isActive ? 'var(--text-main)' : 'var(--text-dim)' }}>
                {step.label}
              </span>
              <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>
                {step.desc}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
