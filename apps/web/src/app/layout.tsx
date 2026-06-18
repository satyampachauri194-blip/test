import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/layout/theme-provider";
import { Toaster } from "@/components/ui/toaster";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Tender Intelligence AI - India's Smartest Tender Discovery Platform",
  description: "Discover, analyze, and track Indian government tenders with AI-powered insights. Get real-time alerts for GeM, CPPP, state eProcurement, PSU, railways, and 1000+ procurement sources.",
  keywords: [
    "tenders",
    "government tenders",
    "India tenders",
    "GeM tenders",
    "CPPP",
    "eProcurement",
    "PSU tenders",
    "railway tenders",
    "bid opportunities",
    "tender alerts",
    "procurement",
    "government contracts"
  ],
  authors: [{ name: "Tender Intelligence AI" }],
  creator: "Tender Intelligence AI",
  publisher: "Tender Intelligence AI",
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  openGraph: {
    type: "website",
    locale: "en_IN",
    url: "https://tenderintelligence.ai",
    siteName: "Tender Intelligence AI",
    title: "Tender Intelligence AI - India's Smartest Tender Discovery Platform",
    description: "Discover, analyze, and track Indian government tenders with AI-powered insights.",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Tender Intelligence AI",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Tender Intelligence AI",
    description: "India's Smartest Tender Discovery Platform",
    images: ["/og-image.png"],
    creator: "@tenderintelai",
  },
  viewport: {
    width: "device-width",
    initialScale: 1,
    maximumScale: 1,
  },
  icons: {
    icon: "/favicon.ico",
    shortcut: "/favicon-16x16.png",
    apple: "/apple-touch-icon.png",
  },
  manifest: "/site.webmanifest",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}
