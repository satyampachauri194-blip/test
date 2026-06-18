import axios from 'axios';
import type { ApiResponse, Tender, SearchResult, User, Subscription, Alert, Invoice, TeamMember, DashboardStats } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const tokens = localStorage.getItem('auth-storage');
    if (tokens) {
      try {
        const parsed = JSON.parse(tokens);
        if (parsed.state?.tokens?.accessToken) {
          config.headers.Authorization = `Bearer ${parsed.state.tokens.accessToken}`;
        }
      } catch {
        // Ignore parsing errors
      }
    }
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth-storage');
        window.location.href = '/auth/login';
      }
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  login: async (email: string, password: string) => {
    const response = await apiClient.post<ApiResponse<{ user: User; tokens: { accessToken: string; refreshToken: string; expiresIn: number } }>>('/auth/login', { email, password });
    return response.data;
  },
  
  register: async (email: string, password: string, name: string, company?: string, phone?: string) => {
    const response = await apiClient.post<ApiResponse<{ user: User; tokens: { accessToken: string; refreshToken: string; expiresIn: number } }>>('/auth/register', { email, password, name, company, phone });
    return response.data;
  },
  
  logout: async () => {
    const response = await apiClient.post<ApiResponse<void>>('/auth/logout');
    return response.data;
  },
  
  refreshToken: async (refreshToken: string) => {
    const response = await apiClient.post<ApiResponse<{ accessToken: string; refreshToken: string; expiresIn: number }>>('/auth/refresh', { refreshToken });
    return response.data;
  },
  
  forgotPassword: async (email: string) => {
    const response = await apiClient.post<ApiResponse<void>>('/auth/forgot-password', { email });
    return response.data;
  },
  
  resetPassword: async (token: string, newPassword: string) => {
    const response = await apiClient.post<ApiResponse<void>>('/auth/reset-password', { token, newPassword });
    return response.data;
  },
  
  getCurrentUser: async () => {
    const response = await apiClient.get<ApiResponse<User>>('/auth/me');
    return response.data;
  },
  
  updateProfile: async (data: Partial<User>) => {
    const response = await apiClient.put<ApiResponse<User>>('/auth/profile', data);
    return response.data;
  },
  
  changePassword: async (currentPassword: string, newPassword: string) => {
    const response = await apiClient.post<ApiResponse<void>>('/auth/change-password', { currentPassword, newPassword });
    return response.data;
  },
};

export const tenderApi = {
  search: async (params: Record<string, unknown>) => {
    const response = await apiClient.get<ApiResponse<SearchResult>>('/tenders/search', { params });
    return response.data;
  },
  
  getById: async (id: string) => {
    const response = await apiClient.get<ApiResponse<Tender>>(`/tenders/${id}`);
    return response.data;
  },
  
  getSimilar: async (id: string, limit = 5) => {
    const response = await apiClient.get<ApiResponse<Tender[]>>(`/tenders/${id}/similar`, { params: { limit } });
    return response.data;
  },
  
  getTrending: async (limit = 10) => {
    const response = await apiClient.get<ApiResponse<Tender[]>>(`/tenders/trending`, { params: { limit } });
    return response.data;
  },
  
  getRecent: async (limit = 10) => {
    const response = await apiClient.get<ApiResponse<Tender[]>>(`/tenders/recent`, { params: { limit } });
    return response.data;
  },
  
  saveTender: async (id: string) => {
    const response = await apiClient.post<ApiResponse<void>>(`/tenders/${id}/save`);
    return response.data;
  },
  
  unsaveTender: async (id: string) => {
    const response = await apiClient.delete<ApiResponse<void>>(`/tenders/${id}/save`);
    return response.data;
  },
  
  getSavedTenders: async (page = 1, limit = 20) => {
    const response = await apiClient.get<ApiResponse<{ tenders: Tender[]; total: number }>>('/tenders/saved', { params: { page, limit } });
    return response.data;
  },
  
  downloadDocument: async (tenderId: string, documentId: string) => {
    const response = await apiClient.get(`/tenders/${tenderId}/documents/${documentId}/download`, { responseType: 'blob' });
    return response.data;
  },
  
  getAIAnalysis: async (id: string) => {
    const response = await apiClient.get<ApiResponse<Tender['aiSummary']>>(`/tenders/${id}/ai-analysis`);
    return response.data;
  },
};

export const alertApi = {
  getAll: async () => {
    const response = await apiClient.get<ApiResponse<Alert[]>>('/alerts');
    return response.data;
  },
  
  create: async (data: { keywords: string[]; filters: Record<string, unknown>; frequency: string; channels: string[] }) => {
    const response = await apiClient.post<ApiResponse<Alert>>('/alerts', data);
    return response.data;
  },
  
  update: async (id: string, data: Partial<Alert>) => {
    const response = await apiClient.put<ApiResponse<Alert>>(`/alerts/${id}`, data);
    return response.data;
  },
  
  delete: async (id: string) => {
    const response = await apiClient.delete<ApiResponse<void>>(`/alerts/${id}`);
    return response.data;
  },
  
  toggle: async (id: string) => {
    const response = await apiClient.post<ApiResponse<Alert>>(`/alerts/${id}/toggle`);
    return response.data;
  },
  
  test: async (id: string) => {
    const response = await apiClient.post<ApiResponse<void>>(`/alerts/${id}/test`);
    return response.data;
  },
};

export const subscriptionApi = {
  getPlans: async () => {
    const response = await apiClient.get<ApiResponse<Array<{ id: string; name: string; price: number; currency: string; features: Record<string, unknown>; popular?: boolean }>>>('/subscription/plans');
    return response.data;
  },
  
  getCurrent: async () => {
    const response = await apiClient.get<ApiResponse<Subscription>>('/subscription/current');
    return response.data;
  },
  
  upgrade: async (planId: string) => {
    const response = await apiClient.post<ApiResponse<{ checkoutUrl: string }>>('/subscription/upgrade', { planId });
    return response.data;
  },
  
  cancel: async () => {
    const response = await apiClient.post<ApiResponse<void>>('/subscription/cancel');
    return response.data;
  },
  
  resume: async () => {
    const response = await apiClient.post<ApiResponse<void>>('/subscription/resume');
    return response.data;
  },
  
  getInvoices: async () => {
    const response = await apiClient.get<ApiResponse<Invoice[]>>('/subscription/invoices');
    return response.data;
  },
  
  downloadInvoice: async (invoiceId: string) => {
    const response = await apiClient.get(`/subscription/invoices/${invoiceId}/download`, { responseType: 'blob' });
    return response.data;
  },
  
  getUsage: async () => {
    const response = await apiClient.get<ApiResponse<{ searchesUsed: number; searchesLimit: number; downloadsUsed: number; downloadsLimit: number }>>('/subscription/usage');
    return response.data;
  },
};

export const teamApi = {
  getMembers: async () => {
    const response = await apiClient.get<ApiResponse<TeamMember[]>>('/team/members');
    return response.data;
  },
  
  inviteMember: async (email: string, role: 'admin' | 'member' | 'viewer') => {
    const response = await apiClient.post<ApiResponse<TeamMember>>('/team/invite', { email, role });
    return response.data;
  },
  
  removeMember: async (memberId: string) => {
    const response = await apiClient.delete<ApiResponse<void>>(`/team/members/${memberId}`);
    return response.data;
  },
  
  updateRole: async (memberId: string, role: 'admin' | 'member' | 'viewer') => {
    const response = await apiClient.put<ApiResponse<TeamMember>>(`/team/members/${memberId}/role`, { role });
    return response.data;
  },
  
  resendInvite: async (memberId: string) => {
    const response = await apiClient.post<ApiResponse<void>>(`/team/members/${memberId}/resend`);
    return response.data;
  },
};

export const dashboardApi = {
  getStats: async () => {
    const response = await apiClient.get<ApiResponse<DashboardStats>>('/dashboard/stats');
    return response.data;
  },
  
  getActivity: async (limit = 10) => {
    const response = await apiClient.get<ApiResponse<Array<{ id: string; action: string; description: string; createdAt: string }>>>('/dashboard/activity', { params: { limit } });
    return response.data;
  },
  
  getUpcomingDeadlines: async (limit = 10) => {
    const response = await apiClient.get<ApiResponse<Tender[]>>(`/dashboard/deadlines`, { params: { limit } });
    return response.data;
  },
};

export const adminApi = {
  getUsers: async (page = 1, limit = 20, filters?: Record<string, unknown>) => {
    const response = await apiClient.get<ApiResponse<{ users: User[]; total: number }>>('/admin/users', { params: { page, limit, ...filters } });
    return response.data;
  },
  
  getUser: async (userId: string) => {
    const response = await apiClient.get<ApiResponse<User>>(`/admin/users/${userId}`);
    return response.data;
  },
  
  updateUser: async (userId: string, data: Partial<User>) => {
    const response = await apiClient.put<ApiResponse<User>>(`/admin/users/${userId}`, data);
    return response.data;
  },
  
  deleteUser: async (userId: string) => {
    const response = await apiClient.delete<ApiResponse<void>>(`/admin/users/${userId}`);
    return response.data;
  },
  
  getScraperStatus: async () => {
    const response = await apiClient.get<ApiResponse<{ status: string; lastRun: string; nextRun: string; stats: Record<string, number> }>>('/admin/scraper/status');
    return response.data;
  },
  
  triggerScraper: async (source?: string) => {
    const response = await apiClient.post<ApiResponse<void>>('/admin/scraper/trigger', { source });
    return response.data;
  },
  
  getAnalytics: async (startDate: string, endDate: string) => {
    const response = await apiClient.get<ApiResponse<Record<string, unknown>>>('/admin/analytics', { params: { startDate, endDate } });
    return response.data;
  },
  
  getLogs: async (level?: string, limit = 100) => {
    const response = await apiClient.get<ApiResponse<Array<{ level: string; message: string; timestamp: string; context: Record<string, unknown> }>>>('/admin/logs', { params: { level, limit } });
    return response.data;
  },
};

export default apiClient;
