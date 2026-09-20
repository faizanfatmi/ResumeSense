export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  display_name: string;
  avatar: string | null;
  date_joined: string;
}

export interface AuthResponse {
  user: User;
  tokens: {
    access: string;
    refresh: string;
  };
}

export interface UploadedFile {
  id: number;
  original_name: string;
  file_type: 'PDF' | 'DOCX' | 'PPT' | 'PPTX';
  file_size: number;
  size_display: string;
  mime_type: string;
  processing_status: 'UPLOADED' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
  error_message?: string;
  uploaded_at: string;
  updated_at: string;
  latest_score?: number | null;
}

export interface Finding {
  id: number;
  severity: 'critical' | 'important' | 'suggestion' | 'good';
  category: string;
  title: string;
  description: string;
  recommendation: string;
  metadata?: Record<string, any>;
}

export interface ExtractedSection {
  id: number;
  section_name: string;
  content: string;
  detected: boolean;
  confidence: number;
  order: number;
}

export interface KeywordGroup {
  id: number;
  group_name: string;
  keywords: string[];
}

export interface SlideAnalysis {
  id: number;
  slide_number: number;
  extracted_text: string;
  text_quality: 'good' | 'warning' | 'poor';
  has_images: boolean;
  has_tables: boolean;
  font_issues: string[];
  warnings: string[];
}

export interface Analysis {
  id: number;
  file: UploadedFile;
  analysis_type: 'resume' | 'ppt';
  score: number;
  text_score: number;
  structure_score: number;
  formatting_score: number;
  keyword_score: number;
  contact_score: number;
  extracted_text: string;
  summary: string;
  page_count: number;
  word_count: number;
  processing_time: number;
  created_at: string;
  findings: Finding[];
  sections: ExtractedSection[];
  keyword_groups: KeywordGroup[];
  slides?: SlideAnalysis[];
  counts: {
    total: number;
    critical: number;
    important: number;
    suggestion: number;
    good: number;
  };
}

export interface JobMatch {
  id: number;
  analysis: number;
  file_name: string;
  job_description: {
    id: number;
    title: string;
    content: string;
    created_at: string;
  };
  match_score: number;
  matched_keywords: string[];
  missing_keywords: string[];
  suggestions: string[];
  created_at: string;
}

export interface DashboardStats {
  stats: {
    files_analyzed: number;
    average_score: number;
    job_matches: number;
    improvements_found: number;
  };
  recent_analyses: Array<{
    id: number;
    file_id: number;
    file_name: string;
    file_type: string;
    file_size: string;
    score: number;
    date: string;
    datetime: string;
    status: string;
    analysis_type: string;
  }>;
}
