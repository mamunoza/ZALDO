export default function TermsPage() {
  return (
    <div className="mx-auto max-w-3xl px-6 py-16">
      <h1 className="text-3xl font-bold text-slate-900">Términos y Condiciones</h1>
      <p className="mt-4 text-slate-600">
        Al usar Zaldo aceptas utilizar la beta de forma responsable, no compartir acceso sin autorización y reportar bugs críticos.
        El servicio puede cambiar o detenerse en cualquier momento durante la beta.
      </p>
      <ul className="mt-6 list-disc space-y-2 pl-6 text-slate-600">
        <li>El acceso se habilita mediante invitaciones o aprobación manual.</li>
        <li>Los datos importados siguen siendo tuyos y puedes descargarlos cuando quieras.</li>
        <li>Aplican leyes chilenas y la zona horaria America/Santiago.</li>
      </ul>
    </div>
  );
}
