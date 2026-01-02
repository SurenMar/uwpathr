import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import ReduxProvider from "@/store/ReduxProvider";
import Setup from "@/components/utils/Setup";
import "@/styles/globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "UWPathr",
  description: "Plan your CS degree.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <ReduxProvider>
          <Setup />
          { children }
        </ReduxProvider>
      </body>
    </html>
  );
}
