import React from 'react';
import { cn } from '../../utils/cn';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  hover?: boolean;
}

export const Card: React.FC<CardProps> = ({ children, className, hover = false, ...props }) => {
  return (
    <div
      className={cn(
        'bg-white rounded-xl border border-slate-200/80 shadow-xs p-5 transition-all',
        hover && 'hover:shadow-md hover:border-blue-200',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};
