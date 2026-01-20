'use client';

import { getToken } from '@/lib/auth-utils';
import { redirect } from 'next/navigation';
import { ReactNode } from 'react';

interface ProtectedLayoutProps {
  children: ReactNode;
}

export default function ProtectedLayout({ children }: ProtectedLayoutProps) {
  const token = getToken();

  if (!token) {
    // Redirect to login if no token exists
    redirect('/login');
  }

  return <>{children}</>;
}