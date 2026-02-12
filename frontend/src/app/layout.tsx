'use client';

import './globals.css';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000,
        refetchOnWindowFocus: false,
      },
    },
  }));

  return (
    <html lang="en">
      <head>
        <title>DepositGuard AI - Security Deposit Protection</title>
        <meta name="description" content="AI-powered security deposit dispute resolution for Texas tenants" />
      </head>
      <body>
        <QueryClientProvider client={queryClient}>
          <div className="min-h-screen bg-gray-50">
            <nav className="bg-white border-b border-gray-200">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16 items-center">
                  <div className="flex items-center">
                    <h1 className="text-2xl font-bold text-primary-600">DepositGuard AI</h1>
                  </div>
                  <div className="flex items-center space-x-4">
                    <a href="/" className="text-gray-700 hover:text-primary-600 px-3 py-2">
                      Home
                    </a>
                    <a href="/cases" className="text-gray-700 hover:text-primary-600 px-3 py-2">
                      Cases
                    </a>
                    <a href="/new-case" className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
                      New Case
                    </a>
                  </div>
                </div>
              </div>
            </nav>
            <main>{children}</main>
          </div>
        </QueryClientProvider>
      </body>
    </html>
  );
}
