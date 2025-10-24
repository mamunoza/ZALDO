export default function PrivacyPage() {
  return (
    <div className="mx-auto max-w-3xl px-6 py-16">
      <h1 className="text-3xl font-bold text-slate-900">Política de Privacidad</h1>
      <p className="mt-4 text-slate-600">
        Respetamos tu privacidad. Esta beta almacena datos mínimos necesarios para operar la plataforma.
        Puedes solicitar la eliminación escribiendo a hola@zaldo.cl.
      </p>
      <ul className="mt-6 list-disc space-y-2 pl-6 text-slate-600">
        <li>Datos de contacto solo para enviarte magic links y notificaciones relevantes.</li>
        <li>Transacciones y reglas se almacenan cifradas y solo se usan para tu panel.</li>
        <li>La telemetría con PostHog usa IDs anónimos y puedes desactivarla desde la app.</li>
      </ul>
    </div>
  );
}
