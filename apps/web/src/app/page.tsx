import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, Search, Bell, Shield, Zap, TrendingUp } from "lucide-react";

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <Shield className="h-8 w-8 text-primary" />
            <span className="text-xl font-bold">Tender Intelligence AI</span>
          </div>
          <div className="hidden md:flex items-center gap-6">
            <Link href="/search" className="text-sm font-medium hover:text-primary">
              Search Tenders
            </Link>
            <Link href="/pricing" className="text-sm font-medium hover:text-primary">
              Pricing
            </Link>
            <Link href="/about" className="text-sm font-medium hover:text-primary">
              About
            </Link>
            <Link href="/contact" className="text-sm font-medium hover:text-primary">
              Contact
            </Link>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link href="/register">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container py-24 space-y-8">
        <div className="text-center space-y-4 max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight">
            India&apos;s Smartest{" "}
            <span className="text-primary">Tender Discovery</span> Platform
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Discover, analyze, and track government tenders from GeM, CPPP, state
            eProcurement portals, PSUs, railways, and 1000+ sources with AI-powered
            insights and real-time alerts.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-8">
            <Link href="/search">
              <Button size="lg" className="gap-2">
                <Search className="h-5 w-5" />
                Search Tenders
              </Button>
            </Link>
            <Link href="/register">
              <Button size="lg" variant="outline" className="gap-2">
                Start Free Trial
                <ArrowRight className="h-5 w-5" />
              </Button>
            </Link>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 pt-16">
          {[
            { label: "Active Tenders", value: "50,000+" },
            { label: "Government Sources", value: "1,000+" },
            { label: "Daily Updates", value: "5,000+" },
            { label: "Happy Customers", value: "10,000+" },
          ].map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-primary">
                {stat.value}
              </div>
              <div className="text-sm text-muted-foreground mt-1">
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="bg-muted/50 py-24">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Why Choose Tender Intelligence AI?
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Advanced AI-powered features to help you win more government contracts
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: Search,
                title: "Advanced Search",
                description:
                  "Semantic search with filters for location, category, value, deadlines, and more.",
              },
              {
                icon: Bell,
                title: "Smart Alerts",
                description:
                  "Real-time notifications via email, WhatsApp, SMS for matching tenders.",
              },
              {
                icon: Zap,
                title: "AI Analysis",
                description:
                  "Automatic extraction of eligibility criteria, EMD, turnover requirements, and risk scoring.",
              },
              {
                icon: Shield,
                title: "Document Processing",
                description:
                  "OCR and NLP-powered PDF analysis to extract关键 clauses and requirements.",
              },
              {
                icon: TrendingUp,
                title: "Bid Analytics",
                description:
                  "Historical data on awarded bidders, pricing trends, and competitor insights.",
              },
              {
                icon: ArrowRight,
                title: "Team Collaboration",
                description:
                  "Multi-user access with role-based permissions for your organization.",
              },
            ].map((feature) => (
              <div
                key={feature.title}
                className="bg-background p-6 rounded-lg border shadow-sm"
              >
                <feature.icon className="h-12 w-12 text-primary mb-4" />
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-muted-foreground">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="container py-24">
        <div className="bg-primary text-primary-foreground rounded-2xl p-12 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to Win More Tenders?
          </h2>
          <p className="text-lg opacity-90 mb-8 max-w-2xl mx-auto">
            Join thousands of businesses using Tender Intelligence AI to discover
            and analyze government procurement opportunities.
          </p>
          <Link href="/register">
            <Button size="lg" variant="secondary" className="gap-2">
              Start Your Free Trial
              <ArrowRight className="h-5 w-5" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-12">
        <div className="container">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <Shield className="h-6 w-6 text-primary" />
                <span className="font-bold">Tender Intelligence AI</span>
              </div>
              <p className="text-sm text-muted-foreground">
                India&apos;s most advanced tender discovery and analysis platform.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>
                  <Link href="/search" className="hover:text-primary">
                    Search
                  </Link>
                </li>
                <li>
                  <Link href="/pricing" className="hover:text-primary">
                    Pricing
                  </Link>
                </li>
                <li>
                  <Link href="/features" className="hover:text-primary">
                    Features
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>
                  <Link href="/about" className="hover:text-primary">
                    About
                  </Link>
                </li>
                <li>
                  <Link href="/contact" className="hover:text-primary">
                    Contact
                  </Link>
                </li>
                <li>
                  <Link href="/blog" className="hover:text-primary">
                    Blog
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>
                  <Link href="/privacy" className="hover:text-primary">
                    Privacy
                  </Link>
                </li>
                <li>
                  <Link href="/terms" className="hover:text-primary">
                    Terms
                  </Link>
                </li>
                <li>
                  <Link href="/refund" className="hover:text-primary">
                    Refund Policy
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t mt-12 pt-8 text-center text-sm text-muted-foreground">
            © {new Date().getFullYear()} Tender Intelligence AI. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
