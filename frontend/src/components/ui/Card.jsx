import React from 'react';
import './ui.css';

export function Card({ children, className = '', ...props }) {
  return (
    <div className={`ui-card convex ${className}`} {...props}>
      {children}
    </div>
  );
}
