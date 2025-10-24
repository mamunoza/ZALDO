import './globals.css';
import { ReactNode } from 'react';
import { Inter } from 'next/font/google';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Providers } from '../components/providers';
import { AnalyticsConsent } from '../components/analytics-consent';
import { FeedbackWidget } from '../components/feedback-widget';

const inter = Inter({ subsets: ['latin'] });

const queryClient = new QueryClient();

export const metadata = {
  title: 'Zaldo — Finanzas personales en serio',
  description: 'Importa tus movimientos, automatiza reglas y entiende tu flujo en minutos.'
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="es">
      <body className={`${inter.className} bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-50`}>
        <QueryClientProvider client={queryClient}>
          <Providers>
            {children}
            <AnalyticsConsent />
            <FeedbackWidget />
          </Providers>
        </QueryClientProvider>
      </body>
    </html>
  );
}
