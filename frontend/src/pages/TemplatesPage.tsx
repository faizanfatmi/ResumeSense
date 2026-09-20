import React from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { LayoutTemplate, Download, Check, Sparkles } from 'lucide-react';

export const TemplatesPage: React.FC = () => {
  const templates = [
    {
      title: 'Modern Software Engineer',
      format: 'DOCX / LaTeX',
      rating: '98% ATS Compatibility',
      desc: 'Optimized single-column layout prioritizing technical stack, production project bullets, and education.',
    },
    {
      title: 'Data Science & ML Specialist',
      format: 'DOCX / PDF',
      rating: '96% ATS Compatibility',
      desc: 'Structured with explicit sections for ML modeling, data pipelines, statistical tools, and research papers.',
    },
    {
      title: 'Executive Product Manager',
      format: 'DOCX',
      rating: '94% ATS Compatibility',
      desc: 'Emphasizes business impact metrics, cross-functional leadership, and feature delivery milestones.',
    },
  ];

  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-12">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          ATS-Optimized Templates
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Pre-tested resume layouts guaranteed to parse cleanly into major enterprise Applicant Tracking Systems.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {templates.map((tpl, i) => (
          <Card key={i} className="p-6 flex flex-col justify-between hover:shadow-md transition-all">
            <div className="space-y-3">
              <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
                <LayoutTemplate className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-bold text-slate-900">{tpl.title}</h3>
              <p className="text-xs text-slate-500 leading-relaxed">{tpl.desc}</p>
              <div className="inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">
                <Check className="w-3 h-3" /> {tpl.rating}
              </div>
            </div>

            <div className="pt-6">
              <Button
                variant="outline"
                size="sm"
                className="w-full flex items-center justify-center gap-1.5 text-xs font-semibold"
                onClick={() => alert(`Downloading ${tpl.title} template...`)}
              >
                <Download className="w-3.5 h-3.5 text-slate-600" />
                <span>Download {tpl.format}</span>
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
