import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Tender Intelligence AI - Win More Government Tenders with AI',
  description: 'India\'s most advanced tender intelligence platform. Aggregate, analyze, and act on lakhs of Indian government tenders from GeM, CPPP, state portals, PSUs, and more.',
  keywords: ['government tenders', 'tender search', 'GeM', 'CPPP', 'procurement', 'bid management', 'tender alerts', 'AI tender analysis'],
  authors: [{ name: 'Tender Intelligence AI' }],
  openGraph: {
    title: 'Tender Intelligence AI - Win More Government Tenders',
    description: 'AI-powered tender intelligence for Indian government procurement',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-background font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
