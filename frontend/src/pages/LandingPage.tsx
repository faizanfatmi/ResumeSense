import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  FileCheck,
  Sparkles,
  ArrowRight,
  Play,
  CheckCircle2,
  FileText,
  BrainCircuit,
  Target,
  Lightbulb,
  ShieldCheck,
  Layers,
  BarChart3,
  Presentation,
} from 'lucide-react';
import { PublicNavbar } from '../components/navbar/PublicNavbar';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { useAuth } from '../context/AuthContext';
import { analysisService } from '../services/analysis';

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const { ensureDemoSession } = useAuth();

  const handleTrySample = async () => {
    try {
      await ensureDemoSession();
      const res = await analysisService.loadSampleAnalysis();
      navigate(`/analysis/${res.analysis_id}`);
    } catch (err) {
      navigate('/analyze');
    }
  };

  return (
    <div className="min-h-screen bg-white text-slate-900 flex flex-col selection:bg-blue-100">
      <PublicNavbar />

      {/* Hero Section */}
      <section className="relative pt-12 pb-20 overflow-hidden bg-gradient-to-b from-blue-50/40 via-white to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-12 gap-12 items-center">
            {/* Left Column: Headlines & Call to Actions */}
            <div className="lg:col-span-6 space-y-6 text-left">
              {/* Pill Badge */}
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-200/80 text-blue-700 text-xs font-semibold">
                <Sparkles className="w-3.5 h-3.5 text-blue-600" />
                <span>AI-Powered Resume & PPT Analyzer</span>
              </div>

              {/* Headline */}
              <h1 className="text-5xl sm:text-6xl font-extrabold tracking-tight text-slate-900 leading-[1.1]">
                Better Resumes. <br />
                <span className="text-blue-600">Bigger Opportunities.</span>
              </h1>

              {/* Subheading */}
              <p className="text-base sm:text-lg text-slate-600 leading-relaxed max-w-xl">
                Check if your resume or presentation is ATS-friendly, identify formatting and content issues, and get actionable recommendations.
              </p>

              {/* CTAs */}
              <div className="flex flex-wrap items-center gap-4 pt-2">
                <Link to="/analyze">
                  <Button size="lg" className="flex items-center gap-2 text-sm font-semibold shadow-sm">
                    <span>Analyze Your File</span>
                    <ArrowRight className="w-4 h-4" />
                  </Button>
                </Link>

                <Button
                  size="lg"
                  variant="outline"
                  onClick={handleTrySample}
                  className="flex items-center gap-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                >
                  <Play className="w-4 h-4 text-blue-600 fill-blue-600" />
                  <span>Watch Demo / Try Sample</span>
                </Button>
              </div>

              {/* Formats Supported */}
              <p className="text-xs text-slate-500 font-medium flex items-center gap-1.5 pt-1">
                <span className="text-blue-500 font-bold">✦</span>
                Supports PDF, DOCX, PPT, PPTX (Max 10MB)
              </p>
            </div>

            {/* Right Column: Hero Visual Mockup from Reference Screenshot 1 */}
            <div className="lg:col-span-6 relative flex justify-center items-center">
              {/* Background ambient glow */}
              <div className="absolute -inset-4 bg-gradient-to-tr from-blue-100 to-indigo-50 rounded-3xl -z-10 blur-xl opacity-80" />

              <div className="relative w-full max-w-lg">
                {/* Simulated Resume Preview Card */}
                <div className="bg-white rounded-2xl border border-slate-200/90 shadow-xl p-6 relative">
                  {/* Candidate header */}
                  <div className="flex items-center gap-4 pb-4 border-b border-slate-100">
                    <div className="w-12 h-12 rounded-full bg-slate-900 text-white font-bold text-base flex items-center justify-center shrink-0">
                      A
                    </div>
                    <div>
                      <h3 className="text-base font-bold text-slate-900">Alex Morgan</h3>
                      <p className="text-xs text-blue-600 font-medium">Software Engineer</p>
                      <p className="text-[11px] text-slate-400 mt-0.5">
                        alex.morgan@example.com • +1 (555) 019-2834 • San Francisco, CA
                      </p>
                    </div>
                  </div>

                  {/* Skills tags */}
                  <div className="py-4 border-b border-slate-100">
                    <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Skills</p>
                    <div className="flex flex-wrap gap-1.5">
                      {['Python', 'SQL', 'Machine Learning', 'Data Analysis', 'Django'].map((s) => (
                        <span
                          key={s}
                          className="px-2.5 py-0.5 bg-slate-100 text-slate-700 rounded-md text-xs font-medium"
                        >
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Experience excerpt */}
                  <div className="pt-3">
                    <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Experience</p>
                    <p className="text-xs font-medium text-slate-800">Machine Learning Intern • FinTech Analytics</p>
                    <p className="text-[11px] text-slate-500 line-clamp-2 mt-0.5">
                      Built predictive scoring pipelines with Pandas and Scikit-learn, optimizing classification accuracy by 14%.
                    </p>
                  </div>
                </div>

                {/* Floating ATS Score Card from Screenshot 1 */}
                <div className="absolute -bottom-6 -right-4 sm:-right-6 bg-white rounded-2xl border border-slate-200 shadow-2xl p-5 w-60 z-20 animate-in fade-in slide-in-from-bottom-3 duration-700">
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <span className="text-3xl font-extrabold text-emerald-600 leading-none">92</span>
                      <span className="text-xs text-slate-400 font-semibold block">/ 100</span>
                    </div>
                    <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">ATS Score</span>
                  </div>

                  {/* Positive checks list */}
                  <div className="space-y-1.5 text-xs text-slate-700 border-t border-slate-100 pt-3">
                    <div className="flex items-center gap-2 text-emerald-600 font-medium">
                      <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                      <span className="text-slate-700">ATS Friendly</span>
                    </div>
                    <div className="flex items-center gap-2 text-emerald-600 font-medium">
                      <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                      <span className="text-slate-700">Well Structured</span>
                    </div>
                    <div className="flex items-center gap-2 text-emerald-600 font-medium">
                      <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                      <span className="text-slate-700">Good Keywords</span>
                    </div>
                    <div className="flex items-center gap-2 text-emerald-600 font-medium">
                      <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                      <span className="text-slate-700">Readable Text</span>
                    </div>
                  </div>

                  <div className="mt-3.5 pt-2.5 border-t border-slate-100 text-[11px] text-emerald-700 font-semibold bg-emerald-50 px-2 py-1 rounded-md text-center">
                    Great job! Your resume is ATS-ready
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* 4 Feature Cards from Screenshot 1 */}
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 mt-20">
            <Card className="p-5 border-slate-200/90 hover:border-blue-300 hover:shadow-md transition-all text-left">
              <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center mb-3">
                <FileText className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-bold text-slate-900 mb-1">Multiple File Formats</h3>
              <p className="text-xs text-slate-500">PDF, DOCX, PPT and PPTX</p>
            </Card>

            <Card className="p-5 border-slate-200/90 hover:border-blue-300 hover:shadow-md transition-all text-left">
              <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-3">
                <BrainCircuit className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-bold text-slate-900 mb-1">AI-Powered Analysis</h3>
              <p className="text-xs text-slate-500">Detailed document structure and content analysis</p>
            </Card>

            <Card className="p-5 border-slate-200/90 hover:border-blue-300 hover:shadow-md transition-all text-left">
              <div className="w-10 h-10 rounded-xl bg-sky-50 text-sky-600 flex items-center justify-center mb-3">
                <Target className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-bold text-slate-900 mb-1">Job Description Match</h3>
              <p className="text-xs text-slate-500">Compare your resume against a target job description</p>
            </Card>

            <Card className="p-5 border-slate-200/90 hover:border-blue-300 hover:shadow-md transition-all text-left">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-3">
                <Lightbulb className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-bold text-slate-900 mb-1">Actionable Suggestions</h3>
              <p className="text-xs text-slate-500">Understand exactly what needs improvement</p>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 bg-slate-50 border-y border-slate-200/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">How It Works</h2>
          <p className="text-sm text-slate-600 mt-2 max-w-xl mx-auto">
            Three simple steps to test and optimize your career documents for automated parsers.
          </p>

          <div className="grid md:grid-cols-3 gap-8 mt-12 text-left">
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs">
              <span className="text-xs font-black text-blue-600 tracking-wider uppercase">Step 01</span>
              <h3 className="text-base font-bold text-slate-900 mt-1 mb-2">Upload</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Upload your resume (PDF/DOCX) or presentation (PPT/PPTX). Our parser securely inspects text, fonts, and layouts.
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs">
              <span className="text-xs font-black text-blue-600 tracking-wider uppercase">Step 02</span>
              <h3 className="text-base font-bold text-slate-900 mt-1 mb-2">Analyze</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                ResumeSense extracts text, verifies sections, computes keyword coverage, and generates a transparent compatibility score.
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs">
              <span className="text-xs font-black text-blue-600 tracking-wider uppercase">Step 03</span>
              <h3 className="text-base font-bold text-slate-900 mt-1 mb-2">Improve</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Review categorized findings, missing skills, and slide-by-slide checks. Download a comprehensive PDF report.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Product Features Deep Dive */}
      <section id="features" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">
              Enterprise Document Intelligence
            </h2>
            <p className="text-sm text-slate-600 mt-2">
              Engineered with deterministic parsing algorithms and NLP semantic analysis to ensure reliable evaluation.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <Card className="p-6">
              <FileCheck className="w-6 h-6 text-blue-600 mb-3" />
              <h3 className="text-base font-bold text-slate-900">Resume Analyzer</h3>
              <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
                Inspects contact details, standard headings, work experience dates, and education credentials.
              </p>
            </Card>

            <Card className="p-6">
              <Presentation className="w-6 h-6 text-orange-600 mb-3" />
              <h3 className="text-base font-bold text-slate-900">PPT & Presentation Analyzer</h3>
              <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
                Slide-by-slide analysis detecting text trapped inside screenshots, small fonts, and complex shapes.
              </p>
            </Card>

            <Card className="p-6">
              <BarChart3 className="w-6 h-6 text-emerald-600 mb-3" />
              <h3 className="text-base font-bold text-slate-900">ATS Compatibility Score</h3>
              <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
                Weighted scoring across text extraction, structure, formatting, keyword coverage, and contact info.
              </p>
            </Card>

            <Card className="p-6">
              <Target className="w-6 h-6 text-indigo-600 mb-3" />
              <h3 className="text-base font-bold text-slate-900">Job Description Matcher</h3>
              <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
                Paste any job posting to evaluate matched competencies, missing requirements, and relevance suggestions.
              </p>
            </Card>

            <Card className="p-6">
              <Layers className="w-6 h-6 text-purple-600 mb-3" />
              <h3 className="text-base font-bold text-slate-900">Keyword Taxonomy</h3>
              <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
                Categorizes technical skills, tools & platforms, and interpersonal competencies without fabricating claims.
              </p>
            </Card>

            <Card className="p-6">
              <ShieldCheck className="w-6 h-6 text-slate-700 mb-3" />
              <h3 className="text-base font-bold text-slate-900">Downloadable PDF Reports</h3>
              <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
                Export full professional PDF reports ready to share with career counselors, recruiters, or mentors.
              </p>
            </Card>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto bg-slate-900 text-slate-400 py-12 border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-lg bg-blue-600 flex items-center justify-center text-white">
              <FileCheck className="w-4 h-4" />
            </div>
            <span className="text-base font-bold text-white tracking-tight">ResumeSense</span>
          </div>

          <p className="text-xs text-slate-500">
            © {new Date().getFullYear()} ResumeSense. All rights reserved. ATS compatibility score is an internal heuristic and does not guarantee employer hiring decisions.
          </p>

          <div className="flex items-center gap-6 text-xs font-medium">
            <Link to="/pricing" className="hover:text-white transition-colors">Pricing</Link>
            <Link to="/login" className="hover:text-white transition-colors">Sign In</Link>
            <Link to="/register" className="hover:text-white transition-colors">Register</Link>
          </div>
        </div>
      </footer>
    </div>
  );
};
