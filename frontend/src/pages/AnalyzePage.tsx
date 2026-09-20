import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  UploadCloud,
  FileText,
  File,
  Presentation,
  ShieldCheck,
  Zap,
  CheckCircle2,
  AlertCircle,
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { analysisService } from '../services/analysis';
import { useAuth } from '../context/AuthContext';

export const AnalyzePage: React.FC = () => {
  const navigate = useNavigate();
  const { ensureDemoSession } = useAuth();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [dragOver, setDragOver] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [processingStep, setProcessingStep] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileSelected(e.target.files[0]);
    }
  };

  const handleFileSelected = (selectedFile: File) => {
    setError(null);

    // Validate size (max 10MB)
    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('File size exceeds the 10MB limit. Please upload a smaller file.');
      return;
    }

    // Validate extension
    const ext = selectedFile.name.split('.').pop()?.toLowerCase();
    if (!ext || !['pdf', 'docx', 'pptx', 'ppt'].includes(ext)) {
      setError('Unsupported format. Please upload a PDF, DOCX, PPT, or PPTX file.');
      return;
    }

    setFile(selectedFile);
    startUploadAndAnalysis(selectedFile);
  };

  const startUploadAndAnalysis = async (targetFile: File) => {
    setUploading(true);
    setError(null);

    try {
      await ensureDemoSession();

      setProcessingStep('Uploading document...');
      await new Promise((r) => setTimeout(r, 400));

      setProcessingStep('Extracting document text & structures...');
      const ext = targetFile.name.split('.').pop()?.toLowerCase();
      const analysisType = ['ppt', 'pptx'].includes(ext || '') ? 'ppt' : 'resume';

      const res = await analysisService.uploadFile(targetFile, analysisType);

      setProcessingStep('Analyzing section structure and keywords...');
      await new Promise((r) => setTimeout(r, 400));

      setProcessingStep('Calculating ATS compatibility score...');
      await new Promise((r) => setTimeout(r, 300));

      setProcessingStep('Complete!');
      navigate(`/analysis/${res.analysis_id}`);
    } catch (err: any) {
      console.error('Upload failed:', err);
      setError(
        err.response?.data?.error ||
        err.response?.data?.detail ||
        'Failed to process and analyze the uploaded file. Please try again.'
      );
      setUploading(false);
      setProcessingStep('');
    }
  };

  const handleTrySample = async () => {
    setUploading(true);
    setProcessingStep('Loading sample analysis...');
    setError(null);

    try {
      await ensureDemoSession();
      const res = await analysisService.loadSampleAnalysis();
      navigate(`/analysis/${res.analysis_id}`);
    } catch (err: any) {
      setError('Could not load sample analysis. Please try again.');
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Analyze Your File
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Upload your resume or presentation to get started.
          </p>
        </div>

        {/* Try Sample Button from Screenshot 2 */}
        <Button
          variant="outline"
          size="sm"
          onClick={handleTrySample}
          disabled={uploading}
          className="flex items-center gap-1.5 self-start sm:self-auto border-blue-200 text-blue-700 hover:bg-blue-50/50"
        >
          <Zap className="w-3.5 h-3.5 text-blue-600 fill-blue-600" />
          <span>Try Sample</span>
        </Button>
      </div>

      {/* Error Alert */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 flex items-start gap-3 text-rose-800 text-xs">
          <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold">Analysis Failed</p>
            <p className="mt-0.5">{error}</p>
          </div>
        </div>
      )}

      {/* Main Drag & Drop Card from Screenshot 2 */}
      <Card
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`p-12 border-2 border-dashed transition-all text-center flex flex-col items-center justify-center min-h-[320px] ${
          dragOver
            ? 'border-blue-500 bg-blue-50/50'
            : 'border-slate-200 hover:border-slate-300 bg-white'
        }`}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".pdf,.docx,.pptx,.ppt"
          className="hidden"
        />

        {uploading ? (
          <div className="flex flex-col items-center space-y-4 max-w-sm">
            <div className="w-14 h-14 rounded-full bg-blue-50 border border-blue-200 flex items-center justify-center text-blue-600">
              <svg className="animate-spin h-7 w-7 text-blue-600" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
              </svg>
            </div>
            <div>
              <p className="text-sm font-bold text-slate-800">{processingStep}</p>
              <p className="text-xs text-slate-400 mt-1">
                {file ? file.name : 'Running analysis pipeline...'}
              </p>
            </div>
          </div>
        ) : (
          <>
            {/* Center Upload Icon */}
            <div className="w-16 h-16 rounded-full bg-blue-50/80 border border-blue-100 flex items-center justify-center text-blue-600 mb-4 shadow-2xs">
              <UploadCloud className="w-8 h-8 text-blue-600" />
            </div>

            {/* Title & Instructions */}
            <h3 className="text-base font-bold text-slate-900 mb-1">
              Drag & drop your file here or click to upload
            </h3>
            <p className="text-xs text-slate-400 mb-6 font-medium">
              Supports PDF, DOCX, PPT, PPTX (Max 10MB)
            </p>

            {/* Blue CTA Button */}
            <Button
              size="md"
              onClick={() => fileInputRef.current?.click()}
              className="px-6 shadow-xs font-semibold"
            >
              Choose File
            </Button>
          </>
        )}
      </Card>

      {/* 4 Format Cards from Screenshot 2 */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {/* PDF */}
        <Card className="p-4 flex items-center gap-3 border-slate-200/80 bg-white shadow-2xs">
          <div className="w-10 h-10 rounded-lg bg-rose-50 text-rose-600 flex items-center justify-center shrink-0">
            <FileText className="w-5 h-5" />
          </div>
          <div className="min-w-0">
            <h4 className="text-xs font-bold text-slate-900 uppercase">PDF</h4>
            <p className="text-[11px] text-slate-500 truncate">Resume, CV</p>
          </div>
        </Card>

        {/* DOCX */}
        <Card className="p-4 flex items-center gap-3 border-slate-200/80 bg-white shadow-2xs">
          <div className="w-10 h-10 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
            <File className="w-5 h-5" />
          </div>
          <div className="min-w-0">
            <h4 className="text-xs font-bold text-slate-900 uppercase">DOCX</h4>
            <p className="text-[11px] text-slate-500 truncate">Resume, Cover Letter</p>
          </div>
        </Card>

        {/* PPT */}
        <Card className="p-4 flex items-center gap-3 border-slate-200/80 bg-white shadow-2xs">
          <div className="w-10 h-10 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center shrink-0">
            <Presentation className="w-5 h-5" />
          </div>
          <div className="min-w-0">
            <h4 className="text-xs font-bold text-slate-900 uppercase">PPT</h4>
            <p className="text-[11px] text-slate-500 truncate">Presentation</p>
          </div>
        </Card>

        {/* PPTX */}
        <Card className="p-4 flex items-center gap-3 border-slate-200/80 bg-white shadow-2xs">
          <div className="w-10 h-10 rounded-lg bg-orange-50 text-orange-600 flex items-center justify-center shrink-0">
            <Presentation className="w-5 h-5" />
          </div>
          <div className="min-w-0">
            <h4 className="text-xs font-bold text-slate-900 uppercase">PPTX</h4>
            <p className="text-[11px] text-slate-500 truncate">Presentation</p>
          </div>
        </Card>
      </div>

      {/* Security notice at bottom */}
      <div className="flex items-center justify-center gap-1.5 text-xs text-slate-500 pt-2">
        <ShieldCheck className="w-4 h-4 text-slate-400" />
        <span>Your files are secure and confidential.</span>
      </div>
    </div>
  );
};
