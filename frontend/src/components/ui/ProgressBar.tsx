import React from 'react';
import { cn } from '../../utils/cn';

interface ProgressBarProps {
  label: string;
  value: number;
  max?: number;
  color?: 'blue' | 'green' | 'amber' | 'red';
  className?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  label,
  value,
  max = 100,
  color = 'blue',
  className,
}) => {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));

  const barColors = {
    blue: 'bg-blue-600',
    green: 'bg-emerald-500',
    amber: 'bg-amber-500',
    red: 'bg-rose-500',
  };

  // Auto-color if not provided or default
  const resolvedColor =
    color !== 'blue'
      ? barColors[color]
      : percentage >= 85
      ? 'bg-emerald-500'
      : percentage >= 70
      ? 'bg-blue-600'
      : percentage >= 55
      ? 'bg-amber-500'
      : 'bg-rose-500';

  return (
    <div className={cn('w-full', className)}>
      <div className="flex justify-between items-center mb-1.5 text-xs font-medium">
        <span className="text-slate-700">{label}</span>
        <span className="font-bold text-slate-900">{Math.round(value)}%</span>
      </div>
      <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
        <div
          className={cn('h-full rounded-full transition-all duration-700 ease-out', resolvedColor)}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
