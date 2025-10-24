'use client';

import { useEffect, useState } from 'react';

export function AnalyticsConsent() {
  const [accepted, setAccepted] = useState<boolean | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem('analytics-consent');
    setAccepted(stored === 'accepted');
  }, []);

  const accept = () => {
    localStorage.setItem('analytics-consent', 'accepted');
    setAccepted(true);
  };

  const reject = () => {
    localStorage.setItem('analytics-consent', 'rejected');
    setAccepted(false);
  };

  if (accepted !== null) return null;

  return (
    <div className="fixed bottom-4 right-4 max-w-sm rounded-xl border border-slate-200 bg-white p-4 shadow-lg">
      <p className="text-sm text-slate-700">Usamos PostHog con datos anónimos para entender eventos clave. ¿Nos das permiso?</p>
      <div className="mt-3 flex gap-2">
        <button onClick={accept} className="rounded bg-primary px-3 py-1 text-sm font-semibold text-white">Aceptar</button>
        <button onClick={reject} className="rounded border border-slate-200 px-3 py-1 text-sm text-slate-600">Rechazar</button>
      </div>
    </div>
  );
}
