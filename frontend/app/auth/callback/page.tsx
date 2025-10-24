'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

export default function CallbackPage() {
  const params = useSearchParams();
  const router = useRouter();
  const [message, setMessage] = useState('Validando enlace…');

  useEffect(() => {
    const token = params.get('token');
    const invite = params.get('invite');
    if (!token) {
      setMessage('Token inválido');
      return;
    }

    const verify = async () => {
      const url = new URL(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/auth/callback`);
      url.searchParams.set('token', token);
      if (invite) url.searchParams.set('invite', invite);
      const res = await fetch(url, { credentials: 'include' });
      if (!res.ok) {
        setMessage('El enlace expiró o ya fue utilizado. Solicita uno nuevo.');
        return;
      }
      const data = await res.json();
      setMessage(data.is_new_user ? '¡Bienvenido! Configura tu cuenta inicial.' : 'Listo, estás dentro.');
      setTimeout(() => router.push('/onboarding'), 2000);
    };
    void verify();
  }, [params, router]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-900">
      <div className="rounded-2xl bg-white px-8 py-10 text-center shadow-xl">
        <h1 className="text-2xl font-semibold text-slate-900">{message}</h1>
        <p className="mt-4 text-sm text-slate-600">Si no se redirige automáticamente, vuelve al inicio.</p>
      </div>
    </div>
  );
}
