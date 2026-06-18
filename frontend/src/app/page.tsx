'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Search, 
  Bell, 
  FileText, 
  Shield, 
  TrendingUp, 
  Clock, 
  CheckCircle2, 
  ArrowRight,
  Zap,
  Target,
  BarChart3,
  Users
} from 'lucide-react';

const features = [
  {
    icon: Search,
    title: 'Advanced Search',
    description: 'AI-powered semantic search across millions of Indian government tenders with smart filters and typo tolerance.'
  },
  {
    icon: Bell,
    title: 'Smart Alerts',
    description: 'Real-time notifications via Email, WhatsApp, Telegram, and SMS for tenders matching your criteria.'
  },
  {
    icon: FileText,
    title: 'AI Document Analysis',
    description: 'Automatic extraction of ATC, BOQ, eligibility criteria, and risk assessment from tender PDFs.'
  },
  {
    icon: Shield,
    title: 'Risk Detection',
    description: 'Identify red flags, hidden clauses, and compliance requirements before you bid.'
  },
  {
    icon: TrendingUp,
    title: 'Competitor Intelligence',
    description: 'Track historical bids, L1/L2/L3 winners, and buyer patterns to optimize your strategy.'
  },
  {
    icon: Clock,
    title: 'Deadline Management',
    description: 'Never miss a bid deadline with intelligent reminders and calendar integration.'
  }
];

const sources = [
  'GeM', 'CPPP', 'Railways', 'PSU Portals', 'State eProcurement',
  'Municipal Corporations', 'Smart Cities', 'Hospitals', 'Universities',
  'Defense', 'PWD', 'Electricity Boards', 'Jal Nigam', 'NIC Portals'
];

const pricingPlans = [
  {
    name: 'Free',
    price: '₹0',
    period: '/month',
    description: 'Perfect for exploring the platform',
    features: [
      '10 daily searches',
      'Basic tender details',
      '5 saved tenders',
      'Email alerts (daily)',
      'Limited document access'
    ],
    cta: 'Get Started',
    popular: false
  },
  {
    name: 'Professional',
    price: '₹2,499',
    period: '/month',
    description: 'For serious bidders and small businesses',
    features: [
      'Unlimited searches',
      'AI document analysis (50/month)',
      '100 saved tenders',
      'Instant alerts (all channels)',
      'Full document access',
      'Risk scoring',
      'Competitor insights',
      'Export functionality'
    ],
    cta: 'Start Free Trial',
    popular: true
  },
  {
    name: 'Business',
    price: '₹7,999',
    period: '/month',
    description: 'For growing teams and agencies',
    features: [
      'Everything in Professional',
      'AI analysis (unlimited)',
      'Unlimited saved tenders',
      '5 team members',
      'API access',
      'Historical data (2 years)',
      'Bid analytics dashboard',
      'Priority support',
      'Custom integrations'
    ],
    cta: 'Contact Sales',
    popular: false
  },
  {
    name: 'Enterprise',
    price: 'Custom',
    period: '',
    description: 'For large organizations',
    features: [
      'Everything in Business',
      'Unlimited team members',
      'Dedicated account manager',
      'Custom AI models',
      'On-premise deployment',
      'SLA guarantee',
      'White-label options',
      'Advanced analytics'
    ],
    cta: 'Contact Sales',
    popular: false
  }
];

const stats = [
  { value: '500K+', label: 'Active Tenders' },
  { value: '10K+', label: 'Daily Updates' },
  { value: '5K+', label: 'Happy Customers' },
  { value: '98%', label: 'Success Rate' }
];

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1">
        {/* Hero Section */}
        <section className="container py-24 md:py-32">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center max-w-4xl mx-auto"
          >
            <Badge variant="secondary" className="mb-4">
              🚀 India's Most Advanced Tender Intelligence Platform
            </Badge>
            <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
              Win More Government Tenders with{' '}
              <span className="text-primary">AI-Powered Intelligence</span>
            </h1>
            <p className="text-xl text-muted-foreground mb-8">
              Aggregate, analyze, and act on lakhs of Indian government tenders from GeM, CPPP, 
              state portals, PSUs, and more. Never miss an opportunity again.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/auth/register">
                <Button size="lg" className="gap-2">
                  Start Free Trial <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <Link href="/search">
                <Button size="lg" variant="outline">
                  Search Tenders
                </Button>
              </Link>
            </div>
          </motion.div>
        </section>

        {/* Stats Section */}
        <section className="bg-muted/50 py-12">
          <div className="container">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {stats.map((stat, index) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  className="text-center"
                >
                  <div className="text-3xl md:text-4xl font-bold text-primary mb-2">{stat.value}</div>
                  <div className="text-sm text-muted-foreground">{stat.label}</div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Sources Section */}
        <section className="container py-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Comprehensive Coverage</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              We aggregate tenders from all major government procurement sources across India
            </p>
          </div>
          <div className="flex flex-wrap justify-center gap-3">
            {sources.map((source) => (
              <Badge key={source} variant="outline" className="px-4 py-2 text-sm">
                {source}
              </Badge>
            ))}
          </div>
        </section>

        {/* Features Section */}
        <section className="container py-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Powerful Features</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Everything you need to discover, analyze, and win government tenders
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1, duration: 0.5 }}
              >
                <Card className="h-full">
                  <CardHeader>
                    <feature.icon className="h-12 w-12 text-primary mb-4" />
                    <CardTitle>{feature.title}</CardTitle>
                    <CardDescription>{feature.description}</CardDescription>
                  </CardHeader>
                </Card>
              </motion.div>
            ))}
          </div>
        </section>

        {/* How It Works */}
        <section className="bg-muted/50 py-16">
          <div className="container">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold mb-4">How It Works</h2>
              <p className="text-muted-foreground max-w-2xl mx-auto">
                Get started in minutes and start winning tenders
              </p>
            </div>
            <div className="grid md:grid-cols-3 gap-8">
              {[
                { icon: Target, title: '1. Search & Discover', description: 'Find relevant tenders using AI-powered search with smart filters' },
                { icon: Zap, title: '2. Analyze & Evaluate', description: 'Get AI insights, risk scores, and qualification probability' },
                { icon: CheckCircle2, title: '3. Bid & Win', description: 'Download documents, prepare bids, and submit with confidence' }
              ].map((step, index) => (
                <motion.div
                  key={step.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.2, duration: 0.5 }}
                  className="text-center"
                >
                  <div className="bg-primary/10 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                    <step.icon className="h-8 w-8 text-primary" />
                  </div>
                  <h3 className="font-semibold text-lg mb-2">{step.title}</h3>
                  <p className="text-muted-foreground">{step.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Pricing Section */}
        <section className="container py-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Simple, Transparent Pricing</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Choose the plan that fits your business needs
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {pricingPlans.map((plan, index) => (
              <motion.div
                key={plan.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1, duration: 0.5 }}
              >
                <Card className={`h-full relative ${plan.popular ? 'border-primary shadow-lg' : ''}`}>
                  {plan.popular && (
                    <Badge className="absolute -top-3 left-1/2 -translate-x-1/2">Most Popular</Badge>
                  )}
                  <CardHeader className="text-center pb-2">
                    <CardTitle className="text-2xl">{plan.name}</CardTitle>
                    <div className="mt-4">
                      <span className="text-4xl font-bold">{plan.price}</span>
                      <span className="text-muted-foreground">{plan.period}</span>
                    </div>
                    <CardDescription className="mt-2">{plan.description}</CardDescription>
                  </CardHeader>
                  <CardContent className="pt-6">
                    <ul className="space-y-3 mb-6">
                      {plan.features.map((feature) => (
                        <li key={feature} className="flex items-start gap-2 text-sm">
                          <CheckCircle2 className="h-5 w-5 text-green-500 shrink-0" />
                          <span className="text-muted-foreground">{feature}</span>
                        </li>
                      ))}
                    </ul>
                    <Button className="w-full" variant={plan.popular ? 'default' : 'outline'}>
                      {plan.cta}
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </section>

        {/* CTA Section */}
        <section className="container py-16">
          <Card className="bg-primary text-primary-foreground">
            <CardContent className="py-12 text-center">
              <h2 className="text-3xl font-bold mb-4">Ready to Start Winning Tenders?</h2>
              <p className="text-lg mb-8 opacity-90 max-w-2xl mx-auto">
                Join thousands of businesses using Tender Intelligence AI to discover and win government contracts
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/auth/register">
                  <Button size="lg" variant="secondary">
                    Start Your Free Trial
                  </Button>
                </Link>
                <Link href="/contact">
                  <Button size="lg" variant="outline" className="border-white text-white hover:bg-white/10">
                    Schedule Demo
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </section>
      </main>

      <Footer />
    </div>
  );
}
