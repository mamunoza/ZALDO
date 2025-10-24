'use client';

import { useState } from 'react';
import Link from 'next/link';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

type Step = 1 | 2 | 3;

export default function OnboardingPage() {
  const [step, setStep] = useState<Step>(1);
  const [accountId, setAccountId] = useState<string>('');
  const [status, setStatus] = useState<string>('');

  const createAccount = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const res = await fetch(`${API_URL}/accounts`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nombre: form.get('nombre'),
        tipo: form.get('tipo'),
        institucion: form.get('institucion'),
        moneda: form.get('moneda')
      })
    });
    if (res.ok) {
      const data = await res.json();
      setAccountId(data.id);
      setStatus('Cuenta creada. Vamos al siguiente paso.');
      setStep(2);
    } else {
      setStatus('No pudimos crear la cuenta. Revisa tus datos.');
    }
  };

  const createRule = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const res = await fetch(`${API_URL}/rules`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nombre: form.get('nombre'),
        prioridad: Number(form.get('prioridad') || 1),
        condiciones: { contiene: form.get('condicion') },
        acciones: { categoria: form.get('accion') },
        activo: true
      })
    });
    if (res.ok) {
      setStatus('Regla creada. ¡Listo!');
      setStep(3);
    } else {
      setStatus('No pudimos crear la regla.');
    }
  };

  return (
    <div className="mx-auto flex min-h-screen max-w-4xl flex-col gap-10 px-6 py-12">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Onboarding guiado</h1>
        <p className="mt-2 text-slate-600">Completa los pasos para ver tu tablero con datos reales.</p>
      </div>
      <div className="flex flex-col gap-6">
        <section className={`rounded-2xl border ${step >= 1 ? 'border-primary' : 'border-slate-200'} bg-white p-6 shadow-sm`}>
          <header className="flex items-center justify-between">
            <h2 className="text-xl font-semibold">1. Crea tu primera cuenta</h2>
            {accountId && <span className="text-sm text-primary">Cuenta lista</span>}
          </header>
          <p className="mt-2 text-slate-600">Banca, tarjeta, efectivo o inversión. Puedes editarla luego.</p>
          <form onSubmit={createAccount} className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
            <input required name="nombre" placeholder="Nombre" className="rounded-lg border border-slate-300 px-4 py-3" />
            <select name="tipo" className="rounded-lg border border-slate-300 px-4 py-3">
              <option value="bank_account">Cuenta corriente</option>
              <option value="credit_card">Tarjeta de crédito</option>
              <option value="cash">Efectivo</option>
              <option value="investment">Inversión</option>
            </select>
            <input name="institucion" placeholder="Institución" className="rounded-lg border border-slate-300 px-4 py-3" />
            <select name="moneda" className="rounded-lg border border-slate-300 px-4 py-3">
              <option value="CLP">CLP</option>
              <option value="USD">USD</option>
            </select>
            <div className="md:col-span-2">
              <button type="submit" className="rounded-lg bg-primary px-4 py-3 font-semibold text-white">Guardar cuenta</button>
            </div>
          </form>
        </section>

        <section className={`rounded-2xl border ${step >= 2 ? 'border-primary' : 'border-slate-200'} bg-white p-6 shadow-sm`}>
          <header className="flex items-center justify-between">
            <h2 className="text-xl font-semibold">2. Importa tu primer archivo</h2>
            {step > 2 && <span className="text-sm text-primary">Importado</span>}
          </header>
          <p className="mt-2 text-slate-600">Sube un CSV/XLSX, revisa la vista previa y confirma. Usa los samples desde la carpeta <code>samples/</code>.</p>
          <Link className="mt-4 inline-flex items-center text-sm font-semibold text-primary" href="/dashboard">Ir al importador</Link>
        </section>

        <section className={`rounded-2xl border ${step >= 3 ? 'border-primary' : 'border-slate-200'} bg-white p-6 shadow-sm`}>
          <header className="flex items-center justify-between">
            <h2 className="text-xl font-semibold">3. Crea tu primera regla</h2>
            {step >= 3 && <span className="text-sm text-primary">Regla lista</span>}
          </header>
          <p className="mt-2 text-slate-600">Ejemplo: si la descripción contiene "Spotify" => Categoría Suscripciones.</p>
          <form onSubmit={createRule} className="mt-4 grid gap-4 md:grid-cols-2">
            <input name="nombre" placeholder="Nombre" defaultValue="Spotify" className="rounded-lg border border-slate-300 px-4 py-3" />
            <input name="prioridad" placeholder="Prioridad" defaultValue="1" className="rounded-lg border border-slate-300 px-4 py-3" />
            <input name="condicion" placeholder="Texto a buscar" defaultValue="Spotify" className="rounded-lg border border-slate-300 px-4 py-3" />
            <input name="accion" placeholder="Categoría" defaultValue="Suscripciones" className="rounded-lg border border-slate-300 px-4 py-3" />
            <div className="md:col-span-2">
              <button type="submit" className="rounded-lg bg-primary px-4 py-3 font-semibold text-white">Crear regla</button>
            </div>
          </form>
        </section>
      </div>

      {status && <div className="rounded-lg bg-slate-900/90 px-4 py-3 text-sm text-white">{status}</div>}
      <div className="text-sm text-slate-500">
        ¿Listo? <Link className="underline" href="/dashboard">Ir al tablero</Link>
      </div>
    </div>
  );
}
