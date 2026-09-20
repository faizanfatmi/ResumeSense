import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  ArrowLeft,
  Download,
  Share2,
  Lightbulb,
  AlertCircle,
  AlertTriangle,
  Info,
  CheckCircle2,
  Copy,
  Search,
  FileText,
  Presentation,
  Check,
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { CircularScore } from '../components/ui/CircularScore';
import { ProgressBar } from '../components/ui/ProgressBar';
import { analysisService } from '../services/analysis';
import { Analysis, Finding } from '../types';
import { cn } from '../utils/cn';

export const AnalysisResultsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Active Tab: Overview, Detailed Feedback, Extracted Text, Suggestions
  const [activeTab, setActiveTab] = useState<'overview' | 'feedback' | 'text' | 'suggestions'>('overview');

  // Filter in Detailed Feedback tab: 'all' | 'critical' | 'important' | 'suggestion'
  const [feedbackFilter, setFeedbackFilter] = useState<'all' | 'critical' | 'important' | 'suggestion'>('all');

  // Text search in Extracted Text tab
  const [textSearch, setTextSearch] = useState('');
  const [copied, setCopied] = useState(false);
  const [shareCopied, setShareCopied] = useState(false);

  useEffect(() => {
    if (id) {
      loadAnalysisData(parseInt(id, 10));
    }
  }, [id]);

  const loadAnalysisData = async (analysisId: number) => {
    try {
      setLoading(true);
      const data = await analysisService.getAnalysis(analysisId);
      setAnalysis(data);
    } catch (err: any) {
      console.error('Failed to load analysis:', err);
      setError('Could not load analysis results. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = () => {
    if (analysis) {
      window.open(analysisService.getReportDownloadUrl(analysis.id), '_blank');
    }
  };

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href);
    setShareCopied(true);
    setTimeout(() => setShareCopied(false), 2000);
  };

  const handleCopyText = () => {
    if (analysis?.extracted_text) {
      navigator.clipboard.writeText(analysis.extracted_text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] space-y-4">
        <div className="w-10 h-10 border-3 border-blue-600 border-t-transparent rounded-full animate-spin" />
        <p className="text-xs text-slate-500 font-medium">Loading analysis results...</p>
      </div>
    );
  }

  if (error || !analysis) {
    return (
      <div className="p-8 max-w-lg mx-auto text-center space-y-4">
        <div className="w-12 h-12 rounded-full bg-rose-50 text-rose-600 flex items-center justify-center mx-auto">
          <AlertCircle className="w-6 h-6" />
        </div>
        <h2 className="text-lg font-bold text-slate-900">Analysis Not Found</h2>
        <p className="text-xs text-slate-500">{error || 'The requested analysis record does not exist.'}</p>
        <Link to="/analyze">
          <Button size="sm">Upload Document</Button>
        </Link>
      </div>
    );
  }

  const fileName = analysis.file?.original_name || 'Document';
  const analyzedDate = new Date(analysis.created_at).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
  const analyzedTime = new Date(analysis.created_at).toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
  });

  // Filter findings for Detailed Feedback tab
  const filteredFindings = analysis.findings.filter((f) => {
    if (feedbackFilter === 'all') return true;
    return f.severity === feedbackFilter;
  });

  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-12">
      {/* Back to Files link from Screenshot 3 */}
      <Link
        to="/files"
        className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-900 transition-colors"
      >
        <ArrowLeft className="w-3.5 h-3.5" />
        <span>Back to Files</span>
      </Link>

      {/* Header with Title and Action buttons */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200/80 pb-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Analysis Results
          </h1>
          <div className="flex items-center gap-2 mt-1">
            <span className="text-sm font-semibold text-slate-700">{fileName}</span>
            <span className="text-slate-300">•</span>
            <span className="text-xs text-slate-400">
              Analyzed on {analyzedDate}, {analyzedTime}
            </span>
          </div>
        </div>

        {/* Download & Share Actions */}
        <div className="flex items-center gap-2.5">
          <Button
            variant="outline"
            size="sm"
            onClick={handleDownloadReport}
            className="flex items-center gap-1.5 text-xs font-semibold"
          >
            <Download className="w-3.5 h-3.5 text-slate-600" />
            <span>Download Report</span>
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={handleShare}
            className="flex items-center gap-1.5 text-xs font-semibold"
          >
            {shareCopied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Share2 className="w-3.5 h-3.5 text-slate-600" />}
            <span>{shareCopied ? 'Link Copied' : 'Share'}</span>
          </Button>
        </div>
      </div>

      {/* Navigation Tabs from Screenshot 3 */}
      <div className="flex border-b border-slate-200 gap-8 text-sm font-medium">
        <button
          onClick={() => setActiveTab('overview')}
          className={cn(
            'pb-3 relative transition-colors cursor-pointer',
            activeTab === 'overview'
              ? 'text-blue-600 font-bold border-b-2 border-blue-600 -mb-[1px]'
              : 'text-slate-500 hover:text-slate-900'
          )}
        >
          Overview
        </button>

        <button
          onClick={() => setActiveTab('feedback')}
          className={cn(
            'pb-3 relative transition-colors cursor-pointer',
            activeTab === 'feedback'
              ? 'text-blue-600 font-bold border-b-2 border-blue-600 -mb-[1px]'
              : 'text-slate-500 hover:text-slate-900'
          )}
        >
          Detailed Feedback
          {analysis.counts.critical > 0 && (
            <span className="ml-1.5 px-1.5 py-0.2 bg-rose-100 text-rose-700 rounded-full text-[10px] font-bold">
              {analysis.counts.critical}
            </span>
          )}
        </button>

        <button
          onClick={() => setActiveTab('text')}
          className={cn(
            'pb-3 relative transition-colors cursor-pointer',
            activeTab === 'text'
              ? 'text-blue-600 font-bold border-b-2 border-blue-600 -mb-[1px]'
              : 'text-slate-500 hover:text-slate-900'
          )}
        >
          Extracted Text
        </button>

        <button
          onClick={() => setActiveTab('suggestions')}
          className={cn(
            'pb-3 relative transition-colors cursor-pointer',
            activeTab === 'suggestions'
              ? 'text-blue-600 font-bold border-b-2 border-blue-600 -mb-[1px]'
              : 'text-slate-500 hover:text-slate-900'
          )}
        >
          Suggestions
        </button>
      </div>

      {/* TAB 1: OVERVIEW (Screenshot 3) */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <div className="grid md:grid-cols-12 gap-6">
            {/* Left Card: ATS Compatibility Score Gauge */}
            <Card className="md:col-span-5 p-6 flex flex-col items-center justify-center text-center">
              <h3 className="text-sm font-bold text-slate-900 self-start mb-6">
                ATS Compatibility Score
              </h3>

              <div className="py-2">
                <CircularScore
                  score={analysis.score}
                  size={160}
                  strokeWidth={12}
                  label="/100"
                />
              </div>

              <p className="text-xs font-semibold text-slate-700 mt-4 max-w-xs">
                {analysis.score >= 80
                  ? 'Great! Your resume is mostly ATS-friendly.'
                  : analysis.score >= 65
                  ? 'Fair compatibility. Several key elements require improvement.'
                  : 'Major improvements recommended for automated parsing.'}
              </p>

              <p className="text-[10px] text-slate-400 mt-2 italic">
                ResumeSense-generated compatibility score
              </p>
            </Card>

            {/* Right Card: Score Breakdown (from Screenshot 3) */}
            <Card className="md:col-span-7 p-6 flex flex-col justify-between">
              <h3 className="text-sm font-bold text-slate-900 mb-4">
                Score Breakdown
              </h3>

              <div className="space-y-4">
                <ProgressBar
                  label="Text Readability"
                  value={analysis.text_score}
                  color="green"
                />
                <ProgressBar
                  label="Section Structure"
                  value={analysis.structure_score}
                  color="blue"
                />
                <ProgressBar
                  label="Keyword Match"
                  value={analysis.keyword_score}
                  color="amber"
                />
                <ProgressBar
                  label="Formatting"
                  value={analysis.formatting_score}
                  color="green"
                />
                <ProgressBar
                  label="Contact Information"
                  value={analysis.contact_score}
                  color="green"
                />
              </div>

              <div className="pt-4 mt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                <span>Total Words: {analysis.word_count}</span>
                <span>Pages: {analysis.page_count}</span>
                <span>Analysis time: {analysis.processing_time}s</span>
              </div>
            </Card>
          </div>

          {/* Bottom Card: Quick Summary (from Screenshot 3) */}
          <div className="rounded-xl bg-blue-50/70 border border-blue-200/80 p-5 flex items-start gap-4 text-blue-950">
            <div className="w-9 h-9 rounded-lg bg-blue-600 text-white flex items-center justify-center shrink-0 shadow-2xs">
              <Lightbulb className="w-5 h-5" />
            </div>
            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-blue-900 mb-1">
                Quick Summary
              </h4>
              <p className="text-xs text-slate-700 leading-relaxed">
                {analysis.summary ||
                  'Your resume is well-structured and mostly ATS-friendly. A few improvements can make it even stronger. Check the detailed feedback for suggestions.'}
              </p>
            </div>
          </div>

          {/* PPT Slides View (if Presentation) */}
          {analysis.analysis_type === 'ppt' && analysis.slides && analysis.slides.length > 0 && (
            <Card className="p-6">
              <h3 className="text-sm font-bold text-slate-900 mb-4 flex items-center gap-2">
                <Presentation className="w-4 h-4 text-orange-600" />
                <span>Slide-by-Slide Analysis</span>
              </h3>

              <div className="grid sm:grid-cols-2 gap-4">
                {analysis.slides.map((s) => (
                  <div
                    key={s.id}
                    className="p-4 rounded-lg border border-slate-200 bg-slate-50/50 space-y-2 text-xs"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-slate-900">Slide {String(s.slide_number).padStart(2, '0')}</span>
                      <Badge
                        variant={
                          s.text_quality === 'good'
                            ? 'success'
                            : s.text_quality === 'warning'
                            ? 'warning'
                            : 'danger'
                        }
                        size="sm"
                      >
                        {s.text_quality.toUpperCase()}
                      </Badge>
                    </div>

                    <p className="text-slate-600 text-[11px] line-clamp-2 italic">
                      "{s.extracted_text || 'No extractable text'}"
                    </p>

                    {s.warnings.length > 0 ? (
                      <div className="space-y-1 pt-1">
                        {s.warnings.map((w, i) => (
                          <div key={i} className="flex items-center gap-1.5 text-amber-700 text-[11px]">
                            <AlertTriangle className="w-3 h-3 shrink-0" />
                            <span>{w}</span>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="flex items-center gap-1.5 text-emerald-700 text-[11px] pt-1">
                        <CheckCircle2 className="w-3 h-3 shrink-0" />
                        <span>Text readable • Standard fonts</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Quick Keywords Chips */}
          {analysis.keyword_groups && analysis.keyword_groups.length > 0 && (
            <Card className="p-6">
              <h3 className="text-sm font-bold text-slate-900 mb-3">Extracted Skills & Competencies</h3>
              <div className="space-y-3">
                {analysis.keyword_groups.map((group) => (
                  <div key={group.id}>
                    <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">
                      {group.group_name}
                    </p>
                    <div className="flex flex-wrap gap-1.5">
                      {group.keywords.map((kw, i) => (
                        <span
                          key={i}
                          className="px-2.5 py-1 bg-slate-100 border border-slate-200 text-slate-700 rounded-md text-xs font-medium"
                        >
                          {kw}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </div>
      )}

      {/* TAB 2: DETAILED FEEDBACK (Screenshot 4) */}
      {activeTab === 'feedback' && (
        <div className="space-y-6">
          <div>
            <h2 className="text-xl font-bold text-slate-900">Detailed Feedback</h2>
            <p className="text-xs text-slate-500 mt-1">
              Here's a detailed analysis of your document structure, keywords, and typography.
            </p>
          </div>

          {/* Filter Chips from Screenshot 4 */}
          <div className="flex flex-wrap gap-2 pt-1">
            <button
              onClick={() => setFeedbackFilter('all')}
              className={cn(
                'px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer',
                feedbackFilter === 'all'
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              )}
            >
              All ({analysis.counts.total})
            </button>

            <button
              onClick={() => setFeedbackFilter('critical')}
              className={cn(
                'px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer',
                feedbackFilter === 'critical'
                  ? 'bg-rose-600 text-white'
                  : 'bg-rose-50 text-rose-700 hover:bg-rose-100'
              )}
            >
              Critical ({analysis.counts.critical})
            </button>

            <button
              onClick={() => setFeedbackFilter('important')}
              className={cn(
                'px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer',
                feedbackFilter === 'important'
                  ? 'bg-amber-600 text-white'
                  : 'bg-amber-50 text-amber-800 hover:bg-amber-100'
              )}
            >
              Important ({analysis.counts.important})
            </button>

            <button
              onClick={() => setFeedbackFilter('suggestion')}
              className={cn(
                'px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer',
                feedbackFilter === 'suggestion'
                  ? 'bg-blue-600 text-white'
                  : 'bg-blue-50 text-blue-700 hover:bg-blue-100'
              )}
            >
              Suggestions ({analysis.counts.suggestion})
            </button>
          </div>

          {/* Feedback Items List from Screenshot 4 */}
          <div className="space-y-3">
            {filteredFindings.map((f) => {
              const isCrit = f.severity === 'critical';
              const isImp = f.severity === 'important';
              const isSugg = f.severity === 'suggestion';
              const isGood = f.severity === 'good';

              return (
                <Card
                  key={f.id}
                  className={cn(
                    'p-4 border transition-all flex items-start justify-between gap-4',
                    isCrit && 'border-rose-200/80 bg-rose-50/20',
                    isImp && 'border-amber-200/80 bg-amber-50/20',
                    isSugg && 'border-blue-200/80 bg-blue-50/10',
                    isGood && 'border-emerald-200/80 bg-emerald-50/10'
                  )}
                >
                  <div className="flex items-start gap-3.5 min-w-0">
                    {/* Severity Icon */}
                    <div className="shrink-0 mt-0.5">
                      {isCrit && (
                        <div className="w-7 h-7 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center">
                          <AlertCircle className="w-4 h-4" />
                        </div>
                      )}
                      {isImp && (
                        <div className="w-7 h-7 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center">
                          <AlertTriangle className="w-4 h-4" />
                        </div>
                      )}
                      {isSugg && (
                        <div className="w-7 h-7 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center">
                          <Info className="w-4 h-4" />
                        </div>
                      )}
                      {isGood && (
                        <div className="w-7 h-7 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center">
                          <CheckCircle2 className="w-4 h-4" />
                        </div>
                      )}
                    </div>

                    {/* Title & Description */}
                    <div className="space-y-1">
                      <h4 className="text-sm font-bold text-slate-900 leading-snug">
                        {f.title}
                      </h4>
                      <p className="text-xs text-slate-600 leading-relaxed">
                        {f.description}
                      </p>
                      {f.recommendation && (
                        <p className="text-xs text-blue-700 bg-blue-50/60 p-2 rounded-md font-medium mt-2">
                          <span className="font-bold">Recommendation:</span> {f.recommendation}
                        </p>
                      )}
                    </div>
                  </div>

                  {/* Badge */}
                  <div className="shrink-0">
                    <Badge
                      variant={
                        isCrit
                          ? 'danger'
                          : isImp
                          ? 'warning'
                          : isSugg
                          ? 'suggestion'
                          : 'success'
                      }
                      size="sm"
                    >
                      {f.severity.charAt(0).toUpperCase() + f.severity.slice(1)}
                    </Badge>
                  </div>
                </Card>
              );
            })}
          </div>
        </div>
      )}

      {/* TAB 3: EXTRACTED TEXT (Document Parser Transparency) */}
      {activeTab === 'text' && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 className="text-lg font-bold text-slate-900">Extracted Document Text</h2>
              <p className="text-xs text-slate-500">
                This is approximately what automated Applicant Tracking Systems parse from your file.
              </p>
            </div>

            <div className="flex items-center gap-2">
              <div className="relative">
                <Search className="w-3.5 h-3.5 absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search in text..."
                  value={textSearch}
                  onChange={(e) => setTextSearch(e.target.value)}
                  className="pl-8 pr-3 py-1 text-xs border border-slate-200 rounded-lg bg-white"
                />
              </div>

              <Button
                variant="outline"
                size="sm"
                onClick={handleCopyText}
                className="flex items-center gap-1.5 text-xs font-semibold"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5 text-slate-600" />}
                <span>{copied ? 'Copied' : 'Copy Text'}</span>
              </Button>
            </div>
          </div>

          <Card className="p-4 bg-slate-900 text-slate-200 font-mono text-xs overflow-x-auto max-h-[500px] leading-relaxed select-text">
            <pre className="whitespace-pre-wrap font-sans">
              {analysis.extracted_text || 'No extractable text was found in this document.'}
            </pre>
          </Card>
        </div>
      )}

      {/* TAB 4: ACTIONABLE SUGGESTIONS */}
      {activeTab === 'suggestions' && (
        <div className="space-y-4">
          <div>
            <h2 className="text-lg font-bold text-slate-900">Actionable Improvement Checklist</h2>
            <p className="text-xs text-slate-500">
              Prioritized checklist of changes to maximize parser compatibility.
            </p>
          </div>

          <div className="space-y-3">
            {analysis.findings
              .filter((f) => f.severity !== 'good')
              .map((f, idx) => (
                <Card key={f.id} className="p-4 flex items-start gap-3">
                  <span className="w-6 h-6 rounded-full bg-blue-50 text-blue-700 font-bold text-xs flex items-center justify-center shrink-0">
                    {idx + 1}
                  </span>
                  <div>
                    <h4 className="text-xs font-bold text-slate-900">{f.title}</h4>
                    <p className="text-xs text-slate-600 mt-0.5">{f.recommendation || f.description}</p>
                  </div>
                </Card>
              ))}
          </div>
        </div>
      )}
    </div>
  );
};
