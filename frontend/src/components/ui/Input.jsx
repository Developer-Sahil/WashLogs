import React from 'react';
import './ui.css';

export function Input({ label, className = '', error, ...props }) {
  return (
    <div className="ui-input-wrapper">
      {label && <label className="ui-label">{label}</label>}
      <input 
        className={`ui-input concave ${className}`} 
        {...props} 
      />
      {error && <span style={{ color: 'var(--error)', fontSize: '0.8rem', marginTop: '-4px' }}>{error}</span>}
    </div>
  );
}
