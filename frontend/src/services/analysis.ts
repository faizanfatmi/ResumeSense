import api from './api';
import { Analysis, UploadedFile } from '../types';

export const analysisService = {
  async uploadFile(file: File, analysisType: 'resume' | 'ppt' = 'resume'): Promise<{ file: UploadedFile; analysis_id: number }> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('analysis_type', analysisType);

    const res = await api.post('/files/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },

  async getAnalysis(id: number): Promise<Analysis> {
    const res = await api.get<Analysis>(`/analysis/${id}/`);
    return res.data;
  },

  async getFeedback(id: number, severity?: string) {
    const params = severity ? { severity } : {};
    const res = await api.get(`/analysis/${id}/feedback/`, { params });
    return res.data;
  },

  async getText(id: number) {
    const res = await api.get(`/analysis/${id}/text/`);
    return res.data;
  },

  async loadSampleAnalysis(): Promise<{ analysis_id: number }> {
    const res = await api.post('/analysis/sample/');
    return res.data;
  },

  getReportDownloadUrl(analysisId: number): string {
    return `/api/analysis/${analysisId}/report/`;
  },

  async getFiles(): Promise<UploadedFile[]> {
    const res = await api.get<UploadedFile[]>('/files/');
    return res.data;
  },

  async deleteFile(id: number): Promise<void> {
    await api.delete(`/files/${id}/`);
  },

  async getDashboardStats() {
    const res = await api.get('/dashboard/stats/');
    return res.data;
  }
};
