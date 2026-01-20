import React, { HTMLAttributes } from 'react';

interface GlassCardProps extends HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
}

const GlassCard: React.FC<GlassCardProps> = ({ children, className = '', ...props }) => {
  return (
    <div
      className={`glass-card bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 shadow-lg ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export default GlassCard;