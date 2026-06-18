import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, AuthTokens, Subscription } from '@/types';

interface AuthState {
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (tokens: AuthTokens, user: User) => void;
  logout: () => void;
  updateUser: (user: Partial<User>) => void;
  setTokens: (tokens: AuthTokens) => void;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      tokens: null,
      isAuthenticated: false,
      isLoading: true,
      login: (tokens, user) => set({ 
        tokens, 
        user, 
        isAuthenticated: true,
        isLoading: false 
      }),
      logout: () => set({ 
        user: null, 
        tokens: null, 
        isAuthenticated: false,
        isLoading: false 
      }),
      updateUser: (userData) => set((state) => ({
        user: state.user ? { ...state.user, ...userData } : null
      })),
      setTokens: (tokens) => set({ tokens }),
      setLoading: (loading) => set({ isLoading: loading }),
    }),
    {
      name: 'auth-storage',
    }
  )
);

interface UIState {
  isDarkMode: boolean;
  sidebarOpen: boolean;
  toggleDarkMode: () => void;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  isDarkMode: false,
  sidebarOpen: true,
  toggleDarkMode: () => set((state) => ({ isDarkMode: !state.isDarkMode })),
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
}));

interface SearchState {
  recentSearches: string[];
  savedFilters: SavedFilter[];
  addRecentSearch: (query: string) => void;
  saveFilter: (filter: SavedFilter) => void;
  removeSavedFilter: (id: string) => void;
  clearRecentSearches: () => void;
}

interface SavedFilter {
  id: string;
  name: string;
  params: Record<string, unknown>;
  createdAt: string;
}

export const useSearchStore = create<SearchState>((set) => ({
  recentSearches: [],
  savedFilters: [],
  addRecentSearch: (query) => set((state) => ({
    recentSearches: [query, ...state.recentSearches.filter(s => s !== query)].slice(0, 10)
  })),
  saveFilter: (filter) => set((state) => ({
    savedFilters: [...state.savedFilters, filter]
  })),
  removeSavedFilter: (id) => set((state) => ({
    savedFilters: state.savedFilters.filter(f => f.id !== id)
  })),
  clearRecentSearches: () => set({ recentSearches: [] }),
}));

interface NotificationState {
  notifications: Notification[];
  unreadCount: number;
  addNotification: (notification: Notification) => void;
  markAsRead: (id: string) => void;
  markAllAsRead: () => void;
  clearNotifications: () => void;
}

interface Notification {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message: string;
  read: boolean;
  createdAt: string;
  actionUrl?: string;
}

export const useNotificationStore = create<NotificationState>((set) => ({
  notifications: [],
  unreadCount: 0,
  addNotification: (notification) => set((state) => ({
    notifications: [notification, ...state.notifications],
    unreadCount: state.unreadCount + 1
  })),
  markAsRead: (id) => set((state) => ({
    notifications: state.notifications.map(n => 
      n.id === id ? { ...n, read: true } : n
    ),
    unreadCount: Math.max(0, state.unreadCount - 1)
  })),
  markAllAsRead: () => set((state) => ({
    notifications: state.notifications.map(n => ({ ...n, read: true })),
    unreadCount: 0
  })),
  clearNotifications: () => set({ notifications: [], unreadCount: 0 }),
}));
