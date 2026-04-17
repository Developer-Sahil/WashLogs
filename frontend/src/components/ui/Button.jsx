import React from 'react';
import './ui.css';

export function Button({ children, className = '', variant = 'primary', ...props }) {
  const baseClasses = 'ui-button convex';
  const variantClass = `ui-button-${variant}`;

  return (
    <button 
      className={`${baseClasses} ${variantClass} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
