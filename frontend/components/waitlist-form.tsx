'use client';

import { useState } from 'react';

export function WaitlistForm() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/waitlist`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });
      const data = await res.json();
      setMessage(data.message || 'Te avisaremos pronto.');
      setSubmitted(true);
    } catch (error) {
      setMessage('Ocurrió un error. Inténtalo nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mt-6 flex w-full max-w-md flex-col gap-3 sm:flex-row">
      <input
        type="email"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
        required
        placeholder="tu@email.cl"
        className="flex-1 rounded-lg border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-sm focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary"
      />
      <button
        type="submit"
        disabled={loading}
        className="rounded-lg bg-primary px-6 py-3 font-semibold text-white shadow hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-70"
      >
        {loading ? 'Enviando…' : 'Únete' }
      </button>
      {submitted && (
        <p className="text-sm text-slate-200 sm:ml-4 sm:mt-0">{message}</p>
      )}
    </form>
  );
}
