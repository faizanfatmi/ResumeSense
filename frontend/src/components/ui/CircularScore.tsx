import React from 'react';

interface CircularScoreProps {
  score: number;
  maxScore?: number;
  size?: number;
  strokeWidth?: number;
  label?: string;
  sublabel?: string;
  color?: string;
}

export const CircularScore: React.FC<CircularScoreProps> = ({
  score,
  maxScore = 100,
  size = 150,
  strokeWidth = 10,
  label = '/100',
  sublabel,
  color,
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const percentage = Math.min(100, Math.max(0, (score / maxScore) * 100));
  const offset = circumference - (percentage / 100) * circumference;

  // Determine color if not explicitly provided
  const resolvedColor =
    color ||
    (score >= 85 ? '#16A34A' : score >= 70 ? '#2563EB' : score >= 55 ? '#F59E0B' : '#DC2626');

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="transform -rotate-90">
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#E2E8F0"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          {/* Progress circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={resolvedColor}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Center label */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className="text-4xl font-extrabold text-slate-900 tracking-tight leading-none">
            {Math.round(score)}
          </span>
          {label && (
            <span className="text-xs font-semibold text-slate-400 mt-1">
              {label}
            </span>
          )}
        </div>
      </div>

      {sublabel && (
        <p className="mt-3 text-xs font-semibold text-slate-600 text-center max-w-[200px]">
          {sublabel}
        </p>
      )}
    </div>
  );
};
