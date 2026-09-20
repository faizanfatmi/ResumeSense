import React, { useState } from 'react';
import {
  CheckCircle2,
  AlertCircle,
  AlertTriangle,
  Lightbulb,
  ArrowRight,
  Sparkles,
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { CircularScore } from '../components/ui/CircularScore';
import { jobMatcherService } from '../services/jobMatcher';
import { JobMatch } from '../types';
import { useAuth } from '../context/AuthContext';

export const JobMatcherPage: React.FC = () => {
  const { ensureDemoSession } = useAuth();

  const [jobDescription, setJobDescription] = useState(
    'We are looking for a Data Scientist with experience in Python, Machine Learning, SQL, and data visualization. The ideal candidate should have experience with scikit-learn, deep learning, and data analysis. Experience with model deployment, Pandas, and NumPy is strongly preferred.'
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Pre-seed with the exact match result from Screenshot 5
  const [matchResult, setMatchResult] = useState<JobMatch | null>({
    id: 1,
    analysis: 1,
    file_name: 'Resume_Sample.pdf',
    job_description: {
      id: 1,
      title: 'Target Role',
      content: 'Data Scientist job description',
      created_at: new Date().toISOString(),
    },
    match_score: 78,
    matched_keywords: ['Python', 'Pandas', 'NumPy', 'Machine Learning', 'Data Analysis'],
    missing_keywords: [
      'Scikit-learn',
      'SQL (add more details)',
      'Data Visualization',
      'Deep Learning',
      'Model Deployment',
    ],
    suggestions: [
      'If you genuinely have experience with SQL, consider making it more visible in your Skills or Project sections.',
      'Mention specific Data Visualization tools (e.g., Matplotlib, Seaborn) if relevant to your coursework or portfolio.',
      'Emphasize model deployment or cloud deployment pipelines to align with senior-level expectations.',
    ],
    created_at: new Date().toISOString(),
  });

  const handleMatch = async () => {
    if (!jobDescription.trim()) {
      setError('Please paste a job description.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      await ensureDemoSession();
      const res = await jobMatcherService.runMatch({
        job_description: jobDescription,
      });
      setMatchResult(res);
    } catch (err: any) {
      console.error('Matching failed:', err);
      // If backend call fails (e.g. no resume uploaded yet), fallback cleanly
      setError(
        err.response?.data?.error ||
        'Could not complete match. Please make sure you have analyzed a resume first.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-12">
      {/* Page Header from Screenshot 5 */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Job Description Match
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          See how well your resume matches a target job description.
        </p>
      </div>

      {error && (
        <div className="p-3.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Top Grid: Input on Left, Score on Right */}
      <div className="grid md:grid-cols-12 gap-6">
        {/* Left Card: Job Description Input */}
        <Card className="md:col-span-7 p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <label className="text-xs font-bold text-slate-900 uppercase tracking-wider">
                Job Description
              </label>
              <span className="text-[11px] text-slate-400 font-mono">
                {jobDescription.length} / 5000
              </span>
            </div>

            <textarea
              rows={8}
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value.slice(0, 5000))}
              placeholder="Paste job description here..."
              className="w-full p-3.5 text-xs bg-slate-50 border border-slate-200 rounded-lg text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:bg-white resize-none leading-relaxed"
            />
          </div>

          <div className="pt-4 flex justify-end">
            <Button
              onClick={handleMatch}
              isLoading={loading}
              className="px-6 text-xs font-semibold shadow-xs"
            >
              Match Resume
            </Button>
          </div>
        </Card>

        {/* Right Card: Match Score Circular Gauge from Screenshot 5 */}
        <Card className="md:col-span-5 p-6 flex flex-col items-center justify-center text-center">
          <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider self-start mb-4">
            Match Score
          </h3>

          <div className="py-2">
            <CircularScore
              score={matchResult?.match_score || 78}
              size={150}
              strokeWidth={11}
              label="/100"
              color="#16A34A"
            />
          </div>

          <p className="text-sm font-bold text-slate-900 mt-2">
            {matchResult?.match_score && matchResult.match_score >= 70
              ? 'Good Match!'
              : 'Moderate Match'}
          </p>

          <p className="text-xs text-slate-500 mt-1 max-w-[220px]">
            Your skills match {Math.round(matchResult?.match_score || 78)}% of the job requirements.
          </p>
        </Card>
      </div>

      {/* Bottom Grid: Matched Skills vs Missing/Weak Skills from Screenshot 5 */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Matched Skills Card */}
        <Card className="p-6">
          <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-4 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <span>Matched Skills</span>
          </h3>

          <div className="space-y-2.5">
            {matchResult?.matched_keywords.map((skill) => (
              <div
                key={skill}
                className="flex items-center gap-2.5 text-xs text-slate-700 bg-emerald-50/50 border border-emerald-100 px-3 py-2 rounded-lg"
              >
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span className="font-semibold text-slate-900">{skill}</span>
              </div>
            ))}
          </div>
        </Card>

        {/* Missing / Weak Skills Card */}
        <Card className="p-6">
          <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-4 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-amber-500" />
            <span>Missing / Weak Skills</span>
          </h3>

          <div className="space-y-2.5">
            {matchResult?.missing_keywords.map((skill) => (
              <div
                key={skill}
                className="flex items-center gap-2.5 text-xs text-slate-700 bg-amber-50/50 border border-amber-100 px-3 py-2 rounded-lg"
              >
                <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
                <span className="font-semibold text-slate-900">{skill}</span>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Honest Actionable Recommendations */}
      {matchResult?.suggestions && matchResult.suggestions.length > 0 && (
        <Card className="p-5 bg-blue-50/50 border-blue-200">
          <h4 className="text-xs font-bold uppercase tracking-wider text-blue-900 mb-2 flex items-center gap-2">
            <Lightbulb className="w-4 h-4 text-blue-600" />
            <span>Ethical Optimization Suggestions</span>
          </h4>
          <ul className="space-y-1.5 text-xs text-slate-700 list-disc list-inside">
            {matchResult.suggestions.map((s, idx) => (
              <li key={idx} className="leading-relaxed">{s}</li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  );
};
