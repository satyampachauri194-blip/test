'use client';

import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { dashboardApi, tenderApi } from '@/lib/api';
import type { Tender } from '@/types';
import { 
  FileText, 
  Clock, 
  TrendingUp, 
  Bell, 
  Save, 
  AlertCircle,
  Calendar,
  ArrowRight
} from 'lucide-react';
import Link from 'next/link';
import { format } from 'date-fns';

const statCards = [
  { title: 'Active Tenders', icon: FileText, valueKey: 'activeTenders', color: 'text-blue-500' },
  { title: 'Saved Tenders', icon: Save, valueKey: 'savedTenders', color: 'text-green-500' },
  { title: 'Active Alerts', icon: Bell, valueKey: 'alertsCount', color: 'text-yellow-500' },
  { title: 'Searches Today', icon: TrendingUp, valueKey: 'recentSearches', color: 'text-purple-500' },
];

export default function DashboardOverviewPage() {
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      const response = await dashboardApi.getStats();
      return response.data;
    },
  });

  const { data: deadlines, isLoading: deadlinesLoading } = useQuery({
    queryKey: ['dashboard-deadlines'],
    queryFn: async () => {
      const response = await dashboardApi.getUpcomingDeadlines(5);
      return response.data;
    },
  });

  const { data: trending, isLoading: trendingLoading } = useQuery({
    queryKey: ['tenders-trending'],
    queryFn: async () => {
      const response = await tenderApi.getTrending(5);
      return response.data;
    },
  });

  if (statsLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard Overview</h1>
        <p className="text-muted-foreground">Welcome back! Here's what's happening with your tenders.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                <stat.icon className={`h-4 w-4 ${stat.color}`} />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {stats ? stats[stat.valueKey as keyof typeof stats] : '-'}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Upcoming Deadlines */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5" />
              Upcoming Deadlines
            </CardTitle>
            <CardDescription>Tenders closing soon</CardDescription>
          </CardHeader>
          <CardContent>
            {deadlinesLoading ? (
              <div className="flex justify-center py-8">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
              </div>
            ) : deadlines && deadlines.length > 0 ? (
              <div className="space-y-4">
                {deadlines.map((tender: Tender) => (
                  <Link key={tender.id} href={`/tenders/${tender.id}`}>
                    <div className="flex items-start justify-between p-3 rounded-lg border hover:bg-muted/50 transition-colors cursor-pointer">
                      <div className="space-y-1 flex-1">
                        <p className="font-medium text-sm line-clamp-1">{tender.title}</p>
                        <p className="text-xs text-muted-foreground">{tender.buyerName}</p>
                      </div>
                      <Badge variant={getDaysUntil(tender.closingDate) <= 3 ? 'destructive' : 'secondary'}>
                        {formatDistanceToDeadline(tender.closingDate)}
                      </Badge>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <p className="text-center text-muted-foreground py-8">No upcoming deadlines</p>
            )}
            <div className="mt-4 pt-4 border-t">
              <Link href="/dashboard/saved-tenders" className="text-sm text-primary hover:underline flex items-center gap-1">
                View all saved tenders <ArrowRight className="h-3 w-3" />
              </Link>
            </div>
          </CardContent>
        </Card>

        {/* Trending Tenders */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              Trending Tenders
            </CardTitle>
            <CardDescription>Popular opportunities right now</CardDescription>
          </CardHeader>
          <CardContent>
            {trendingLoading ? (
              <div className="flex justify-center py-8">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
              </div>
            ) : trending && trending.length > 0 ? (
              <div className="space-y-4">
                {trending.map((tender: Tender) => (
                  <Link key={tender.id} href={`/tenders/${tender.id}`}>
                    <div className="flex items-start justify-between p-3 rounded-lg border hover:bg-muted/50 transition-colors cursor-pointer">
                      <div className="space-y-1 flex-1">
                        <p className="font-medium text-sm line-clamp-1">{tender.title}</p>
                        <div className="flex items-center gap-2 text-xs text-muted-foreground">
                          <span>{tender.state}</span>
                          <span>•</span>
                          <span>₹{tender.bidValue?.toLocaleString('en-IN') || 'N/A'}</span>
                        </div>
                      </div>
                      <Badge variant="outline">{tender.procurementType}</Badge>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <p className="text-center text-muted-foreground py-8">No trending tenders</p>
            )}
            <div className="mt-4 pt-4 border-t">
              <Link href="/search" className="text-sm text-primary hover:underline flex items-center gap-1">
                Search all tenders <ArrowRight className="h-3 w-3" />
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>Common tasks and shortcuts</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Link href="/search">
              <Button variant="outline" className="w-full h-auto py-4 flex flex-col gap-2">
                <FileText className="h-5 w-5" />
                <span className="text-xs">Search Tenders</span>
              </Button>
            </Link>
            <Link href="/dashboard/alerts">
              <Button variant="outline" className="w-full h-auto py-4 flex flex-col gap-2">
                <Bell className="h-5 w-5" />
                <span className="text-xs">Manage Alerts</span>
              </Button>
            </Link>
            <Link href="/dashboard/saved-tenders">
              <Button variant="outline" className="w-full h-auto py-4 flex flex-col gap-2">
                <Save className="h-5 w-5" />
                <span className="text-xs">Saved Tenders</span>
              </Button>
            </Link>
            <Link href="/dashboard/subscriptions">
              <Button variant="outline" className="w-full h-auto py-4 flex flex-col gap-2">
                <Calendar className="h-5 w-5" />
                <span className="text-xs">Subscription</span>
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>
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
  
  const weeks = Math.floor(days / 7);
  return `${weeks} week${weeks > 1 ? 's' : ''}`;
}
