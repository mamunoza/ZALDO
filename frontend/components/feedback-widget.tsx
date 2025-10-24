'use client';

import { useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export function FeedbackWidget() {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [status, setStatus] = useState<string | null>(null);

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    const res = await fetch(`${API_URL}/feedback`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mensaje: message })
    });
    if (res.ok) {
      setStatus('Gracias por tu feedback ✨');
      setMessage('');
      setOpen(false);
    } else {
      setStatus('No pudimos enviar tu feedback. Inténtalo más tarde.');
    }
  };

  return (
    <div className="fixed bottom-6 left-6">
      <button onClick={() => setOpen((value) => !value)} className="rounded-full bg-primary px-4 py-2 font-semibold text-white shadow-lg">
        Enviar feedback
      </button>
      {open && (
        <form onSubmit={submit} className="mt-3 w-72 rounded-2xl border border-slate-200 bg-white p-4 shadow-xl">
          <textarea
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            required
            placeholder="Cuéntanos qué mejorar…"
            className="h-28 w-full rounded-lg border border-slate-300 px-3 py-2"
          />
          <button type="submit" className="mt-3 w-full rounded-lg bg-primary px-4 py-2 font-semibold text-white">Enviar</button>
        </form>
      )}
      {status && <p className="mt-2 text-sm text-white">{status}</p>}
    </div>
  );
}
