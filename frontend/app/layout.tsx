import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Neon Tasks',
  description: 'A modern todo application with neon theme and glassmorphism design',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 min-h-screen`}>
        {children}
      </body>
    </html>
  );
}