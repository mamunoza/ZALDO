'use client';

import { useEffect, useMemo, useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

type FlowRow = {
  month: string;
  ingresos: number;
  egresos: number;
  ahorro: number;
  porcentaje_ahorro: number;
  saldo_acumulado: number;
};

type FlowResponse = {
  rows: FlowRow[];
  totals: Record<string, number>;
};

type CategoryBreakdown = {
  categoria: string;
  monto: number;
};

type CategoryResponse = {
  month: string;
  breakdown: CategoryBreakdown[];
};

export default function DashboardPage() {
  const [flow, setFlow] = useState<FlowResponse | null>(null);
  const [categories, setCategories] = useState<CategoryResponse | null>(null);
  const [range, setRange] = useState<'3M' | '12M' | 'YTD'>('3M');
  const [currency, setCurrency] = useState<'CLP' | 'UF'>('CLP');

  useEffect(() => {
    const now = new Date();
    const currentMonth = now.toISOString().slice(0, 7);
    const start = new Date(now);
    if (range === '3M') start.setMonth(start.getMonth() - 2);
    if (range === '12M') start.setMonth(start.getMonth() - 11);
    if (range === 'YTD') start.setMonth(0);
    const startMonth = start.toISOString().slice(0, 7);

    const params = new URLSearchParams({ from: startMonth, to: currentMonth, normalize: currency });
    fetch(`${API_URL}/analytics/flow?${params}`, { credentials: 'include' })
      .then((res) => res.json())
      .then(setFlow)
      .catch(() => setFlow(null));

    fetch(`${API_URL}/analytics/categories?month=${currentMonth}`, { credentials: 'include' })
      .then((res) => res.json())
      .then(setCategories)
      .catch(() => setCategories(null));
  }, [range, currency]);

  const kpis = useMemo(() => {
    if (!flow) return [];
    const latest = flow.rows[flow.rows.length - 1];
    const sumIngresos = latest?.ingresos ?? 0;
    const sumEgresos = latest?.egresos ?? 0;
    const ahorro = latest?.ahorro ?? 0;
    const ahorroPct = latest?.porcentaje_ahorro ?? 0;
    return [
      { label: 'Ingresos del mes', value: sumIngresos },
      { label: 'Egresos del mes', value: sumEgresos },
      { label: 'Ahorro', value: ahorro },
      { label: '% Ahorro YTD', value: Math.round(ahorroPct * 100) / 100 }
    ];
  }, [flow]);

  return (
    <div className="mx-auto max-w-6xl px-6 py-12">
      <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Dashboard</h1>
          <p className="text-slate-600">Resumen de tus finanzas. Zona horaria America/Santiago.</p>
        </div>
        <div className="flex items-center gap-3">
          <select value={range} onChange={(e) => setRange(e.target.value as any)} className="rounded-lg border border-slate-300 px-3 py-2">
            <option value="3M">Últimos 3 meses</option>
            <option value="12M">12 meses</option>
            <option value="YTD">YTD</option>
          </select>
          <select value={currency} onChange={(e) => setCurrency(e.target.value as any)} className="rounded-lg border border-slate-300 px-3 py-2">
            <option value="CLP">CLP</option>
            <option value="UF">UF</option>
          </select>
        </div>
      </div>

      <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {kpis.map((kpi) => (
          <div key={kpi.label} className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
            <p className="text-sm text-slate-500">{kpi.label}</p>
            <p className="mt-2 text-2xl font-semibold text-slate-900">
              {currency === 'CLP' ? `$${kpi.value.toLocaleString('es-CL')}` : `${kpi.value.toFixed(2)} UF`}
            </p>
          </div>
        ))}
      </div>

      <div className="mt-10 grid gap-6 lg:grid-cols-3">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-2">
          <h2 className="text-lg font-semibold text-slate-900">Ingresos vs Egresos</h2>
          <div className="mt-6 flex h-64 items-end gap-2">
            {flow?.rows.map((row) => (
              <div key={row.month} className="flex-1">
                <div className="flex items-end justify-center gap-1">
                  <div className="w-4 rounded-t bg-emerald-500" style={{ height: `${Math.max(row.ingresos, 1)}px` }}></div>
                  <div className="w-4 rounded-t bg-rose-500" style={{ height: `${Math.max(row.egresos, 1)}px` }}></div>
                </div>
                <p className="mt-2 text-center text-xs text-slate-500">{row.month}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900">Gastos por categoría</h2>
          <ul className="mt-4 space-y-3">
            {categories?.breakdown.map((item) => (
              <li key={item.categoria} className="flex items-center justify-between text-sm text-slate-600">
                <span>{item.categoria}</span>
                <span>{currency === 'CLP' ? `$${item.monto.toLocaleString('es-CL')}` : `${item.monto.toFixed(2)} UF`}</span>
              </li>
            )) || <li className="text-sm text-slate-500">Importa movimientos para ver tus categorías.</li>}
          </ul>
        </div>
      </div>

      <div className="mt-10 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-900">Flujo mensual</h2>
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200 text-sm">
            <thead className="bg-slate-50 text-left text-xs uppercase text-slate-500">
              <tr>
                <th className="px-4 py-2">Mes</th>
                <th className="px-4 py-2">Ingresos</th>
                <th className="px-4 py-2">Egresos</th>
                <th className="px-4 py-2">Ahorro</th>
                <th className="px-4 py-2">% Ahorro</th>
                <th className="px-4 py-2">Saldo acumulado</th>
              </tr>
            </thead>
            <tbody>
              {flow?.rows.map((row) => (
                <tr key={row.month} className="odd:bg-white even:bg-slate-50">
                  <td className="px-4 py-2 font-medium text-slate-700">{row.month}</td>
                  <td className="px-4 py-2">{currency === 'CLP' ? `$${row.ingresos.toLocaleString('es-CL')}` : `${row.ingresos.toFixed(2)} UF`}</td>
                  <td className="px-4 py-2">{currency === 'CLP' ? `$${row.egresos.toLocaleString('es-CL')}` : `${row.egresos.toFixed(2)} UF`}</td>
                  <td className="px-4 py-2">{currency === 'CLP' ? `$${row.ahorro.toLocaleString('es-CL')}` : `${row.ahorro.toFixed(2)} UF`}</td>
                  <td className="px-4 py-2">{(row.porcentaje_ahorro * 100).toFixed(1)}%</td>
                  <td className="px-4 py-2">{currency === 'CLP' ? `$${row.saldo_acumulado.toLocaleString('es-CL')}` : `${row.saldo_acumulado.toFixed(2)} UF`}</td>
                </tr>
              )) || (
                <tr>
                  <td colSpan={6} className="px-4 py-6 text-center text-slate-500">
                    Importa tus movimientos para calcular el flujo mensual.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
