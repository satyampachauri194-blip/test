'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useRouter, useSearchParams } from 'next/navigation';
import { motion } from 'framer-motion';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { tenderApi } from '@/lib/api';
import type { Tender, SearchParams } from '@/types';
import { Search, Filter, MapPin, Rupee, Calendar, Clock, FileText, Bookmark } from 'lucide-react';
import Link from 'next/link';
import { format } from 'date-fns';

const indianStates = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
  'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
  'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
  'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
  'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
  'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Delhi'
];

const tenderTypes = ['goods', 'services', 'works', 'consultancy'];
const procurementTypes = ['open', 'limited', 'single_source', 'gem'];

export default function SearchPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [searchQuery, setSearchQuery] = useState(searchParams.get('query') || '');
  const [filters, setFilters] = useState<Partial<SearchParams>>({
    states: searchParams.getAll('state'),
    tenderTypes: searchParams.getAll('tenderType'),
    procurementTypes: searchParams.getAll('procurementType'),
    status: searchParams.getAll('status') || ['active'],
  });

  const { data, isLoading, error } = useQuery({
    queryKey: ['tenders-search', searchQuery, filters],
    queryFn: async () => {
      const params: Record<string, unknown> = {
        query: searchQuery,
        ...filters,
        page: 1,
        limit: 20,
      };
      const response = await tenderApi.search(params);
      return response.data;
    },
  });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const params = new URLSearchParams();
    if (searchQuery) params.set('query', searchQuery);
    
    filters.states?.forEach(state => params.append('state', state));
    filters.tenderTypes?.forEach(type => params.append('tenderType', type));
    filters.procurementTypes?.forEach(type => params.append('procurementType', type));
    filters.status?.forEach(status => params.append('status', status));
    
    router.push(`/search?${params.toString()}`);
  };

  const toggleFilter = (type: string, value: string) => {
    setFilters(prev => {
      const key = type as keyof SearchParams;
      const current = (prev[key] as string[]) || [];
      const updated = current.includes(value)
        ? current.filter(v => v !== value)
        : [...current, value];
      return { ...prev, [key]: updated };
    });
  };

  return (
    <div className="space-y-6">
      {/* Search Header */}
      <div className="sticky top-16 z-40 bg-background border-b py-4">
        <form onSubmit={handleSearch} className="container flex gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Search by keyword, tender number, department..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
          <Button type="submit">Search</Button>
        </form>
      </div>

      <div className="container grid lg:grid-cols-4 gap-6">
        {/* Filters Sidebar */}
        <div className="lg:col-span-1 space-y-6">
          <Card>
            <CardContent className="p-4 space-y-4">
              <div className="flex items-center gap-2 font-semibold">
                <Filter className="h-4 w-4" />
                Filters
              </div>

              {/* Status Filter */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Status</label>
                <div className="flex flex-wrap gap-2">
                  {['active', 'closed', 'cancelled', 'awarded'].map((status) => (
                    <Badge
                      key={status}
                      variant={filters.status?.includes(status) ? 'default' : 'outline'}
                      className="cursor-pointer capitalize"
                      onClick={() => toggleFilter('status', status)}
                    >
                      {status}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* States Filter */}
              <div className="space-y-2">
                <label className="text-sm font-medium">States</label>
                <div className="flex flex-wrap gap-2 max-h-48 overflow-y-auto">
                  {indianStates.map((state) => (
                    <Badge
                      key={state}
                      variant={filters.states?.includes(state) ? 'default' : 'outline'}
                      className="cursor-pointer text-xs"
                      onClick={() => toggleFilter('states', state)}
                    >
                      {state}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Tender Type Filter */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Tender Type</label>
                <div className="flex flex-wrap gap-2">
                  {tenderTypes.map((type) => (
                    <Badge
                      key={type}
                      variant={filters.tenderTypes?.includes(type) ? 'default' : 'outline'}
                      className="cursor-pointer capitalize"
                      onClick={() => toggleFilter('tenderTypes', type)}
                    >
                      {type}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Procurement Type Filter */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Procurement Type</label>
                <div className="flex flex-wrap gap-2">
                  {procurementTypes.map((type) => (
                    <Badge
                      key={type}
                      variant={filters.procurementTypes?.includes(type) ? 'default' : 'outline'}
                      className="cursor-pointer capitalize"
                      onClick={() => toggleFilter('procurementTypes', type)}
                    >
                      {type === 'gem' ? 'GeM' : type.replace('_', ' ')}
                    </Badge>
                  ))}
                </div>
              </div>

              <Button 
                variant="outline" 
                size="sm" 
                className="w-full"
                onClick={() => setFilters({ status: ['active'] })}
              >
                Clear All Filters
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Results */}
        <div className="lg:col-span-3 space-y-4">
          {isLoading ? (
            <div className="space-y-4">
              {[...Array(5)].map((_, i) => (
                <Card key={i}>
                  <CardContent className="p-6 animate-pulse">
                    <div className="h-4 bg-muted rounded w-3/4 mb-4"></div>
                    <div className="h-3 bg-muted rounded w-1/2 mb-2"></div>
                    <div className="h-3 bg-muted rounded w-1/4"></div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : error ? (
            <Card>
              <CardContent className="p-6 text-center text-destructive">
                Error loading tenders. Please try again.
              </CardContent>
            </Card>
          ) : !data || data.tenders.length === 0 ? (
            <Card>
              <CardContent className="p-12 text-center">
                <Search className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="font-semibold text-lg mb-2">No tenders found</h3>
                <p className="text-muted-foreground">Try adjusting your search or filters</p>
              </CardContent>
            </Card>
          ) : (
            <>
              <div className="flex items-center justify-between">
                <p className="text-sm text-muted-foreground">
                  Showing {data.tenders.length} of {data.total} results
                </p>
              </div>

              <div className="space-y-4">
                {data.tenders.map((tender: Tender, index: number) => (
                  <motion.div
                    key={tender.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                  >
                    <Link href={`/tenders/${tender.id}`}>
                      <Card className="hover:shadow-md transition-shadow cursor-pointer">
                        <CardContent className="p-6">
                          <div className="flex items-start justify-between gap-4">
                            <div className="flex-1 space-y-3">
                              <div className="flex items-start gap-3">
                                <div className="space-y-1 flex-1">
                                  <h3 className="font-semibold text-lg line-clamp-2">
                                    {tender.title}
                                  </h3>
                                  <div className="flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
                                    <span className="flex items-center gap-1">
                                      <MapPin className="h-3 w-3" />
                                      {tender.state}, {tender.city || tender.district}
                                    </span>
                                    <span className="flex items-center gap-1">
                                      <Rupee className="h-3 w-3" />
                                      {tender.bidValue ? `₹${tender.bidValue.toLocaleString('en-IN')}` : 'N/A'}
                                    </span>
                                    <span className="flex items-center gap-1">
                                      <Calendar className="h-3 w-3" />
                                      Published: {format(new Date(tender.publishedDate), 'dd MMM yyyy')}
                                    </span>
                                  </div>
                                </div>
                              </div>

                              <div className="flex flex-wrap items-center gap-2">
                                <Badge variant="secondary" className="capitalize">
                                  {tender.tenderType}
                                </Badge>
                                <Badge variant="outline" className="capitalize">
                                  {tender.procurementType === 'gem' ? 'GeM' : tender.procurementType}
                                </Badge>
                                <Badge variant={tender.status === 'active' ? 'success' : 'secondary'}>
                                  {tender.status}
                                </Badge>
                                {tender.emdAmount && (
                                  <Badge variant="outline">
                                    EMD: ₹{tender.emdAmount.toLocaleString('en-IN')}
                                  </Badge>
                                )}
                              </div>

                              <div className="flex items-center gap-4 text-sm text-muted-foreground pt-2 border-t">
                                <span className="flex items-center gap-1">
                                  <FileText className="h-3 w-3" />
                                  {tender.documents?.length || 0} documents
                                </span>
                                <span className={`flex items-center gap-1 ${getDaysUntil(tender.closingDate) <= 3 ? 'text-destructive font-medium' : ''}`}>
                                  <Clock className="h-3 w-3" />
                                  Closes: {formatDistanceToDeadline(tender.closingDate)}
                                </span>
                              </div>
                            </div>

                            <Button variant="ghost" size="icon" className="shrink-0">
                              <Bookmark className="h-4 w-4" />
                            </Button>
                          </div>
                        </CardContent>
                      </Card>
                    </Link>
                  </motion.div>
                ))}
              </div>

              {/* Pagination */}
              {data.totalPages > 1 && (
                <div className="flex justify-center gap-2 pt-4">
                  <Button variant="outline" size="sm" disabled>Previous</Button>
                  <Button variant="outline" size="sm">1</Button>
                  {data.totalPages > 2 && <span className="px-2">...</span>}
                  {data.totalPages > 1 && (
                    <Button variant="outline" size="sm">{data.totalPages}</Button>
                  )}
                  <Button variant="outline" size="sm">Next</Button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

function getDaysUntil(dateString: string): number {
  const deadline = new Date(dateString);
  const now = new Date();
  const diff = deadline.getTime() - now.getTime();
  return Math.ceil(diff / (1000 * 60 * 60 * 24));
}

function formatDistanceToDeadline(dateString: string): string {
  const days = getDaysUntil(dateString);
  
  if (days < 0) return 'Closed';
  if (days === 0) return 'Today';
  if (days === 1) return 'Tomorrow';
  if (days <= 7) return `${days} days`;
  
  return format(new Date(dateString), 'dd MMM yyyy');
}
