'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function AuthPage() {
  const [email, setEmail] = useState('');
  const [invite, setInvite] = useState('');
  const [status, setStatus] = useState<string | null>(null);

  const requestLink = async (event: React.FormEvent) => {
    event.preventDefault();
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/auth/magic-link`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, invite_code: invite || undefined })
    });
    const data = await res.json();
    setStatus(data.status === 'waitlisted' ? 'Te sumamos a la lista de espera.' : 'Revisa tu correo para continuar.');
  };

  return (
    <div className="mx-auto flex min-h-screen max-w-lg flex-col justify-center gap-6 px-6 py-12">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Accede sin contraseña</h1>
        <p className="mt-2 text-slate-600">Ingresa tu email y te enviaremos un enlace mágico válido por 15 minutos.</p>
      </div>
      <form onSubmit={requestLink} className="space-y-4">
        <input
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
          placeholder="tu@email.cl"
          className="w-full rounded-lg border border-slate-300 px-4 py-3"
        />
        <input
          type="text"
          value={invite}
          onChange={(event) => setInvite(event.target.value)}
          placeholder="Código de invitación (opcional)"
          className="w-full rounded-lg border border-slate-300 px-4 py-3"
        />
        <button type="submit" className="w-full rounded-lg bg-primary px-4 py-3 font-semibold text-white">Enviar enlace</button>
      </form>
      {status && <p className="text-sm text-slate-600">{status}</p>}
      <p className="text-sm text-slate-500">¿Aún sin código? <Link className="underline" href="/">Únete a la lista de espera.</Link></p>
    </div>
  );
}
