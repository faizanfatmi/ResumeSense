import React from 'react';
import { Card } from '../components/ui/Card';
import { Compass, BookOpen, ExternalLink, HelpCircle, CheckCircle } from 'lucide-react';

export const ResourcesPage: React.FC = () => {
  const guides = [
    {
      title: 'The Modern ATS Parsing Guide (2026 Edition)',
      desc: 'How contemporary applicant tracking platforms parse resumes, why columns fail, and how fonts distort text.',
      tag: 'Guide',
    },
    {
      title: 'Ethical Keyword Optimization',
      desc: 'Learn how to incorporate target competencies naturally without stuffing keywords or falsifying experience.',
      tag: 'Strategy',
    },
    {
      title: 'PowerPoint & Presentation Best Practices for Technical Reviews',
      desc: 'Avoiding image-trapped text, tiny fonts, and complex shapes in recruitment portfolios.',
      tag: 'Presentation',
    },
  ];

  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-12">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Career Resources & ATS Guides</h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Evidence-backed articles and technical breakdowns for job seekers and career professionals.
        </p>
      </div>

      <div className="space-y-4">
        {guides.map((g, i) => (
          <Card key={i} className="p-5 flex items-start justify-between gap-4 hover:border-blue-200 transition-colors">
            <div className="space-y-1">
              <span className="px-2 py-0.5 bg-blue-50 text-blue-700 text-[10px] font-bold uppercase rounded">
                {g.tag}
              </span>
              <h3 className="text-sm font-bold text-slate-900 mt-1">{g.title}</h3>
              <p className="text-xs text-slate-500 leading-relaxed max-w-2xl">{g.desc}</p>
            </div>
            <button className="p-2 text-slate-400 hover:text-blue-600 rounded-lg hover:bg-slate-50">
              <ExternalLink className="w-4 h-4" />
            </button>
          </Card>
        ))}
      </div>
    </div>
  );
};
