export interface User {
  id: string;
  email: string;
  name: string;
  role: 'free' | 'starter' | 'professional' | 'business' | 'enterprise' | 'admin';
  company?: string;
  phone?: string;
  avatar?: string;
  createdAt: string;
  subscription?: Subscription;
}

export interface Subscription {
  id: string;
  plan: 'free' | 'starter' | 'professional' | 'business' | 'enterprise';
  status: 'active' | 'cancelled' | 'past_due' | 'trialing';
  currentPeriodEnd: string;
  features: SubscriptionFeatures;
}

export interface SubscriptionFeatures {
  dailySearches: number;
  pdfDownloads: number;
  aiAnalysis: boolean;
  alerts: boolean;
  savedTenders: number;
  export: boolean;
  teamMembers: number;
  apiAccess: boolean;
  historicalData: boolean;
  bidAnalytics: boolean;
}

export interface Tender {
  id: string;
  tenderNumber: string;
  title: string;
  description: string;
  department: string;
  buyerName: string;
  buyerEmail?: string;
  buyerPhone?: string;
  state: string;
  district: string;
  city: string;
  location: string;
  tenderType: 'goods' | 'services' | 'works' | 'consultancy';
  procurementType: 'open' | 'limited' | 'single_source' | 'gem';
  category: string;
  subCategory?: string;
  publishedDate: string;
  closingDate: string;
  openingDate: string;
  bidValue?: number;
  emdAmount?: number;
  contractPeriod?: string;
  status: 'active' | 'closed' | 'cancelled' | 'awarded';
  source: string;
  sourceUrl: string;
  documents: TenderDocument[];
  corrigendum?: Corrigendum[];
  aiSummary?: AISummary;
  eligibilityCriteria?: EligibilityCriteria;
  technicalSpecs?: TechnicalSpecification[];
  createdAt: string;
  updatedAt: string;
}

export interface TenderDocument {
  id: string;
  name: string;
  type: 'tender_notice' | 'bid_document' | 'technical_spec' | 'commercial_bid' | 'corrigendum' | 'addendum';
  url: string;
  size?: number;
  uploadedAt: string;
}

export interface Corrigendum {
  id: string;
  date: string;
  description: string;
  documentUrl?: string;
}

export interface AISummary {
  summary: string;
  riskScore: number;
  complexityScore: number;
  qualificationProbability: number;
  redFlags: RedFlag[];
  complianceChecklist: ComplianceItem[];
  requiredDocuments: string[];
  keyDates: KeyDate[];
  extractedAt: string;
}

export interface RedFlag {
  severity: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  description: string;
  recommendation?: string;
}

export interface ComplianceItem {
  requirement: string;
  status: 'compliant' | 'non_compliant' | 'unknown';
  details?: string;
}

export interface KeyDate {
  event: string;
  date: string;
  description?: string;
}

export interface EligibilityCriteria {
  turnover?: number;
  experienceYears?: number;
  similarWorkCount?: number;
  oemAuthorization?: boolean;
  mseExemption?: boolean;
  startupExemption?: boolean;
  otherCriteria?: string[];
}

export interface TechnicalSpecification {
  parameter: string;
  requirement: string;
  unit?: string;
}

export interface Alert {
  id: string;
  userId: string;
  keywords: string[];
  filters: AlertFilters;
  frequency: 'instant' | 'daily' | 'weekly';
  channels: AlertChannel[];
  isActive: boolean;
  lastTriggered?: string;
  createdAt: string;
}

export interface AlertFilters {
  states?: string[];
  categories?: string[];
  tenderTypes?: string[];
  minBidValue?: number;
  maxBidValue?: number;
  departments?: string[];
}

export type AlertChannel = 'email' | 'whatsapp' | 'telegram' | 'sms' | 'push';

export interface SearchParams {
  query?: string;
  states?: string[];
  categories?: string[];
  tenderTypes?: string[];
  procurementTypes?: string[];
  minBidValue?: number;
  maxBidValue?: number;
  publishedFrom?: string;
  publishedTo?: string;
  closingFrom?: string;
  closingTo?: string;
  status?: string[];
  page?: number;
  limit?: number;
  sortBy?: 'relevance' | 'published_date' | 'closing_date' | 'bid_value';
  sortOrder?: 'asc' | 'desc';
}

export interface SearchResult {
  tenders: Tender[];
  total: number;
  page: number;
  totalPages: number;
  facets: SearchFacets;
}

export interface SearchFacets {
  states: FacetCount[];
  categories: FacetCount[];
  tenderTypes: FacetCount[];
  departments: FacetCount[];
  status: FacetCount[];
}

export interface FacetCount {
  value: string;
  count: number;
}

export interface DashboardStats {
  totalTenders: number;
  activeTenders: number;
  savedTenders: number;
  alertsCount: number;
  recentSearches: number;
  subscriptionUsage: SubscriptionUsage;
}

export interface SubscriptionUsage {
  searchesUsed: number;
  searchesLimit: number;
  downloadsUsed: number;
  downloadsLimit: number;
  teamMembersUsed: number;
  teamMembersLimit: number;
}

export interface Invoice {
  id: string;
  amount: number;
  currency: string;
  status: 'paid' | 'pending' | 'failed';
  date: string;
  description: string;
  gstNumber?: string;
  invoiceUrl: string;
}

export interface TeamMember {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'member' | 'viewer';
  invitedAt: string;
  joinedAt?: string;
  status: 'pending' | 'active' | 'inactive';
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name: string;
  company?: string;
  phone?: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
  success: boolean;
}

export interface PaginationParams {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
}
