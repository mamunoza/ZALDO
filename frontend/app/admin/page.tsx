'use client';

import { useEffect, useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

type UserRow = {
  email: string;
  verificado: boolean;
  activo: boolean;
  ultima_sesion: string | null;
  flags: Record<string, unknown>;
};

type InviteRow = {
  code: string;
  uses: number;
  max_uses: number;
  created_at: string;
};

export default function AdminPage() {
  const [users, setUsers] = useState<UserRow[]>([]);
  const [code, setCode] = useState<string | null>(null);
  const [metrics, setMetrics] = useState<Record<string, number>>({});
  const [maxUses, setMaxUses] = useState(5);

  const refresh = () => {
    fetch(`${API_URL}/admin/users`, { credentials: 'include' }).then((res) => res.json()).then(setUsers);
    fetch(`${API_URL}/admin/metrics`, { credentials: 'include' }).then((res) => res.json()).then(setMetrics);
  };

  useEffect(() => {
    refresh();
  }, []);

  const createInvite = async () => {
    const res = await fetch(`${API_URL}/admin/invites`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ max_uses: maxUses })
    });
    if (res.ok) {
      const data = await res.json();
      setCode(data.code);
    }
  };

  return (
    <div className="mx-auto max-w-5xl px-6 py-12">
      <h1 className="text-3xl font-bold text-slate-900">Admin</h1>
      <p className="mt-2 text-slate-600">Gestiona invitaciones y revisa actividad básica.</p>

      <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-900">Invitaciones</h2>
        <div className="mt-4 flex flex-col gap-3 sm:flex-row">
          <input
            type="number"
            value={maxUses}
            onChange={(event) => setMaxUses(Number(event.target.value))}
            min={1}
            className="w-32 rounded-lg border border-slate-300 px-3 py-2"
          />
          <button onClick={createInvite} className="rounded-lg bg-primary px-4 py-2 font-semibold text-white">Generar código</button>
          {code && <span className="rounded bg-slate-900 px-3 py-2 text-white">{code}</span>}
        </div>
      </section>

      <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-900">Usuarios</h2>
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead className="bg-slate-50 text-slate-500">
              <tr>
                <th className="px-4 py-2 text-left">Email</th>
                <th className="px-4 py-2 text-left">Verificado</th>
                <th className="px-4 py-2 text-left">Activo</th>
                <th className="px-4 py-2 text-left">Última sesión</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.email} className="odd:bg-white even:bg-slate-50">
                  <td className="px-4 py-2 font-medium text-slate-700">{user.email}</td>
                  <td className="px-4 py-2">{user.verificado ? 'Sí' : 'No'}</td>
                  <td className="px-4 py-2">{user.activo ? 'Sí' : 'No'}</td>
                  <td className="px-4 py-2">{user.ultima_sesion ? new Date(user.ultima_sesion).toLocaleString('es-CL') : '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-900">Métricas</h2>
        <div className="mt-4 grid gap-4 sm:grid-cols-2">
          {Object.entries(metrics).map(([key, value]) => (
            <div key={key} className="rounded-lg border border-slate-200 bg-slate-50 px-4 py-3">
              <p className="text-sm uppercase text-slate-500">{key}</p>
              <p className="text-2xl font-semibold text-slate-900">{value}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
