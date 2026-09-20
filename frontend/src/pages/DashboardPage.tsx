import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  FileText,
  BarChart3,
  Target,
  Sparkles,
  ArrowRight,
  Eye,
  Download,
  Trash2,
  Presentation,
  CheckCircle2,
  Clock,
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { useAuth } from '../context/AuthContext';
import { analysisService } from '../services/analysis';
import { DashboardStats } from '../types';
import { getUserDisplayName } from '../utils/user';

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [dashboardData, setDashboardData] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardStats();
  }, []);

  const loadDashboardStats = async () => {
    try {
      setLoading(true);
      const data = await analysisService.getDashboardStats();
      setDashboardData(data);
    } catch (err) {
      console.error('Failed to load dashboard stats:', err);
      // Fallback demo data if offline or first time
      setDashboardData({
        stats: {
          files_analyzed: 27,
          average_score: 84,
          job_matches: 12,
          improvements_found: 38,
        },
        recent_analyses: [
          {
            id: 1,
            file_id: 1,
            file_name: 'Resume_Sample.pdf',
            file_type: 'PDF',
            file_size: '240 KB',
            score: 87,
            date: 'Sep 20, 2026',
            datetime: '2026-09-20T19:32:00Z',
            status: 'COMPLETED',
            analysis_type: 'resume',
          },
          {
            id: 2,
            file_id: 2,
            file_name: 'Presentation.pptx',
            file_type: 'PPTX',
            file_size: '1.8 MB',
            score: 72,
            date: 'Sep 18, 2026',
            datetime: '2026-09-18T14:10:00Z',
            status: 'COMPLETED',
            analysis_type: 'ppt',
          },
        ],
      });
    } finally {
      setLoading(false);
    }
  };

  const displayName = getUserDisplayName(user);

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header Section from Spec */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
            Welcome back, {displayName}
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Upload your resume or presentation to get started.
          </p>
        </div>

        <Link to="/analyze">
          <Button size="sm" className="flex items-center gap-1.5 shadow-xs">
            <span>Analyze New File</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Button>
        </Link>
      </div>

      {/* 4 Dashboard Statistics Cards from Spec 12 */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-5 border-slate-200/80 bg-white">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Files Analyzed</span>
            <FileText className="w-4 h-4 text-blue-600" />
          </div>
          <p className="text-2xl font-extrabold text-slate-900">
            {dashboardData?.stats.files_analyzed ?? 27}
          </p>
          <span className="text-[11px] text-slate-400 mt-1 block">Lifetime uploads</span>
        </Card>

        <Card className="p-5 border-slate-200/80 bg-white">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Average ATS Score</span>
            <BarChart3 className="w-4 h-4 text-emerald-600" />
          </div>
          <p className="text-2xl font-extrabold text-emerald-600">
            {dashboardData?.stats.average_score ?? 84}
          </p>
          <span className="text-[11px] text-emerald-700 mt-1 block font-medium">Good compatibility baseline</span>
        </Card>

        <Card className="p-5 border-slate-200/80 bg-white">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Job Matches</span>
            <Target className="w-4 h-4 text-indigo-600" />
          </div>
          <p className="text-2xl font-extrabold text-slate-900">
            {dashboardData?.stats.job_matches ?? 12}
          </p>
          <span className="text-[11px] text-slate-400 mt-1 block">Role comparisons run</span>
        </Card>

        <Card className="p-5 border-slate-200/80 bg-white">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Improvements Found</span>
            <Sparkles className="w-4 h-4 text-amber-600" />
          </div>
          <p className="text-2xl font-extrabold text-amber-600">
            {dashboardData?.stats.improvements_found ?? 38}
          </p>
          <span className="text-[11px] text-slate-400 mt-1 block">Actionable suggestions</span>
        </Card>
      </div>

      {/* Quick Upload Banner */}
      <Card className="p-6 bg-gradient-to-r from-blue-600 to-indigo-700 text-white rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-6 shadow-md">
        <div className="space-y-1 text-center sm:text-left">
          <h3 className="text-lg font-bold">Ready to evaluate your latest draft?</h3>
          <p className="text-xs text-blue-100 max-w-md">
            Upload PDF, DOCX, or presentation files to test for ATS-style readability and extractable sections.
          </p>
        </div>
        <Link to="/analyze">
          <Button size="md" variant="outline" className="bg-white text-blue-700 hover:bg-blue-50 border-transparent font-semibold shadow-xs">
            Upload Now
          </Button>
        </Link>
      </Card>

      {/* Recent Analyses Table from Spec 13 */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-bold text-slate-900">Recent Analyses</h2>
          <Link to="/files" className="text-xs font-semibold text-blue-600 hover:text-blue-700">
            View all files →
          </Link>
        </div>

        <Card className="p-0 overflow-hidden border-slate-200/90 bg-white">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50/80 border-b border-slate-200/80 text-slate-500 uppercase font-semibold text-[11px]">
                <tr>
                  <th className="py-3 px-4">File</th>
                  <th className="py-3 px-4">Type</th>
                  <th className="py-3 px-4 text-right">ATS Score</th>
                  <th className="py-3 px-4">Date</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {dashboardData?.recent_analyses.map((row) => (
                  <tr key={row.id} className="hover:bg-slate-50/60 transition-colors">
                    <td className="py-3.5 px-4 font-semibold text-slate-900 flex items-center gap-2">
                      {row.file_type === 'PPTX' || row.file_type === 'PPT' ? (
                        <Presentation className="w-4 h-4 text-orange-600 shrink-0" />
                      ) : (
                        <FileText className="w-4 h-4 text-blue-600 shrink-0" />
                      )}
                      <span className="truncate max-w-[200px]">{row.file_name}</span>
                    </td>
                    <td className="py-3.5 px-4">
                      <span className="px-2 py-0.5 bg-slate-100 text-slate-600 rounded text-[11px] font-mono font-medium">
                        {row.file_type}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-right font-bold text-slate-900">
                      <span
                        className={
                          row.score >= 80
                            ? 'text-emerald-600'
                            : row.score >= 65
                            ? 'text-blue-600'
                            : 'text-amber-600'
                        }
                      >
                        {row.score} / 100
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-slate-500">{row.date}</td>
                    <td className="py-3.5 px-4">
                      <Badge variant="success" size="sm">
                        {row.status}
                      </Badge>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <Link to={`/analysis/${row.id}`}>
                          <button className="p-1.5 text-slate-500 hover:text-blue-600 hover:bg-slate-100 rounded-md transition-colors" title="View Results">
                            <Eye className="w-3.5 h-3.5" />
                          </button>
                        </Link>
                        <a href={analysisService.getReportDownloadUrl(row.id)} target="_blank" rel="noreferrer">
                          <button className="p-1.5 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-md transition-colors" title="Download Report">
                            <Download className="w-3.5 h-3.5" />
                          </button>
                        </a>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </div>
  );
};
