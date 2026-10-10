import "./globals.css";
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Providers from "./providers";

const geistSans = Geist({
  subsets: ["latin"],
  variable: "--font-geist-sans",
});

const geistMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-geist-mono",
});

export const metadata: Metadata = {
  title: "OFS Live Bid Tracker",
  description: "Real-time demand analysis for Offer For Sale bids across NSE and BSE. Track bid ladders, confirmed quantities, and cumulative demand.",
  openGraph: {
    title: "OFS Live Bid Tracker",
    description: "Real-time demand analysis for Offer For Sale bids across NSE and BSE.",
    type: "website",
    url: "https://ofs-tracker.onrender.com",
  },
  twitter: {
    card: "summary",
    title: "OFS Live Bid Tracker",
    description: "Real-time demand analysis for Offer For Sale bids across NSE and BSE.",
  },
  icons: {
    icon: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable}`}>
      <body className="bg-[#0c0c0c] text-[#f2f2f2] antialiased min-h-dvh font-sans">
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
