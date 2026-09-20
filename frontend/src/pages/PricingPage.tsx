import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Check, Sparkles } from 'lucide-react';
import { PublicNavbar } from '../components/navbar/PublicNavbar';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { cn } from '../utils/cn';

export const PricingPage: React.FC = () => {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly');

  return (
    <div className="min-h-screen bg-slate-50/50 flex flex-col selection:bg-blue-100">
      <PublicNavbar />

      <main className="flex-1 py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
        {/* Header Section from Screenshot 6 */}
        <div className="text-center max-w-2xl mx-auto mb-12">
          <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
            Simple, Transparent Pricing
          </h1>
          <p className="text-sm text-slate-500 mt-2">
            Choose a plan that works for you.
          </p>

          {/* Monthly / Yearly Toggle */}
          <div className="mt-8 inline-flex items-center p-1 bg-slate-100 rounded-full border border-slate-200">
            <button
              onClick={() => setBillingCycle('monthly')}
              className={cn(
                'px-5 py-1.5 rounded-full text-xs font-semibold transition-all cursor-pointer',
                billingCycle === 'monthly'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              )}
            >
              Monthly
            </button>
            <button
              onClick={() => setBillingCycle('yearly')}
              className={cn(
                'px-5 py-1.5 rounded-full text-xs font-semibold transition-all flex items-center gap-2 cursor-pointer',
                billingCycle === 'yearly'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              )}
            >
              <span>Yearly</span>
              <span className="px-1.5 py-0.2 bg-blue-100 text-blue-700 text-[10px] rounded-full font-bold">
                Save 20%
              </span>
            </button>
          </div>
        </div>

        {/* 3 Pricing Cards from Screenshot 6 */}
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto items-stretch">
          {/* FREE PLAN */}
          <Card className="p-8 flex flex-col justify-between border-slate-200 bg-white shadow-xs hover:shadow-md transition-all">
            <div>
              <h3 className="text-lg font-bold text-slate-900">Free</h3>
              <p className="text-xs text-slate-500 mt-1">Get started with basic analysis</p>

              <div className="mt-6 mb-6">
                <span className="text-4xl font-extrabold text-slate-900">₹0</span>
                <span className="text-xs text-slate-500 ml-1 font-medium">/ month</span>
              </div>

              <div className="space-y-3 border-t border-slate-100 pt-6 text-xs text-slate-700">
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>1 file analysis per day</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>Basic ATS score</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>Limited feedback</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>Standard support</span>
                </div>
              </div>
            </div>

            <div className="pt-8">
              <Link to="/analyze">
                <Button variant="outline" className="w-full text-xs font-semibold py-2.5">
                  Get Started
                </Button>
              </Link>
            </div>
          </Card>

          {/* PRO PLAN (MOST POPULAR) */}
          <Card className="p-8 flex flex-col justify-between border-2 border-blue-600 bg-white shadow-lg relative hover:shadow-xl transition-all">
            {/* Most Popular Badge */}
            <div className="absolute -top-3.5 right-6 px-3 py-0.5 rounded-full bg-blue-600 text-white text-[11px] font-bold shadow-xs">
              Most Popular
            </div>

            <div>
              <h3 className="text-lg font-bold text-slate-900">Pro</h3>
              <p className="text-xs text-slate-500 mt-1">For students and professionals</p>

              <div className="mt-6 mb-6">
                <span className="text-4xl font-extrabold text-slate-900">
                  {billingCycle === 'yearly' ? '₹399' : '₹499'}
                </span>
                <span className="text-xs text-slate-500 ml-1 font-medium">/ month</span>
              </div>

              <div className="space-y-3 border-t border-slate-100 pt-6 text-xs text-slate-700">
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-blue-600 shrink-0" />
                  <span className="font-semibold text-slate-900">Unlimited file analysis</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-blue-600 shrink-0" />
                  <span>Detailed ATS report</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-blue-600 shrink-0" />
                  <span>Job description matching</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-blue-600 shrink-0" />
                  <span>Priority support</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-blue-600 shrink-0" />
                  <span>Access to resume templates</span>
                </div>
              </div>
            </div>

            <div className="pt-8">
              <Link to="/analyze">
                <Button variant="primary" className="w-full text-xs font-semibold py-2.5 shadow-sm">
                  Upgrade to Pro
                </Button>
              </Link>
            </div>
          </Card>

          {/* TEAM PLAN */}
          <Card className="p-8 flex flex-col justify-between border-slate-200 bg-white shadow-xs hover:shadow-md transition-all">
            <div>
              <h3 className="text-lg font-bold text-slate-900">Team</h3>
              <p className="text-xs text-slate-500 mt-1">For teams and organizations</p>

              <div className="mt-6 mb-6">
                <span className="text-4xl font-extrabold text-slate-900">
                  {billingCycle === 'yearly' ? '₹1,199' : '₹1,499'}
                </span>
                <span className="text-xs text-slate-500 ml-1 font-medium">/ month</span>
              </div>

              <div className="space-y-3 border-t border-slate-100 pt-6 text-xs text-slate-700">
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span className="font-semibold text-slate-900">Everything in Pro</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>Team collaboration</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>Bulk document analysis</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>API access (coming soon)</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>Dedicated support</span>
                </div>
              </div>
            </div>

            <div className="pt-8">
              <Button
                variant="outline"
                className="w-full text-xs font-semibold py-2.5"
                onClick={() => alert('Our team will contact you shortly regarding enterprise onboarding.')}
              >
                Contact Sales
              </Button>
            </div>
          </Card>
        </div>

        {/* Tagline footer quote from Screenshot 6 */}
        <p className="text-center text-xs text-slate-400 italic mt-16">
          "Better resumes. Brighter careers."
        </p>
      </main>
    </div>
  );
};
