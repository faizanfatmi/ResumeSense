import api from './api';
import { JobMatch } from '../types';

export const jobMatcherService = {
  async runMatch(data: { job_description: string; analysis_id?: number; title?: string }): Promise<JobMatch> {
    const res = await api.post<JobMatch>('/job-matcher/match/', data);
    return res.data;
  },

  async getHistory(): Promise<JobMatch[]> {
    const res = await api.get<JobMatch[]>('/job-matcher/history/');
    return res.data;
  },

  async getMatch(id: number): Promise<JobMatch> {
    const res = await api.get<JobMatch>(`/job-matcher/${id}/`);
    return res.data;
  }
};
