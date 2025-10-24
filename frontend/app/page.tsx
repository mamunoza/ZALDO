import Link from 'next/link';
import { WaitlistForm } from '../components/waitlist-form';

const benefits = [
  'Importa CSV/XLSX de bancos y tarjetas sin drama.',
  'Aplica reglas inteligentes y deduplicación automática.',
  'Visualiza flujo mensual con CLP ⇆ UF.',
  'Dashboard con KPIs esenciales para tus decisiones.',
  'Feedback in-app y roadmap público.'
];

const faqs = [
  {
    question: '¿Necesito tarjeta de crédito para empezar?',
    answer: 'No. Estamos en beta cerrada con acceso por invitación o lista de espera.'
  },
  {
    question: '¿Qué bancos soportan?',
    answer: 'Puedes importar cualquier archivo CSV/XLSX. Pronto agregaremos conexiones automáticas.'
  },
  {
    question: '¿Cómo manejan mi información?',
    answer: 'Tus datos se almacenan cifrados y solo los usaremos para darte valor. Puedes solicitar su eliminación cuando quieras.'
  }
];

const steps = [
  {
    title: 'Regístrate con tu email',
    description: 'Recibe un magic link y entra sin contraseñas.'
  },
  {
    title: 'Importa tus movimientos',
    description: 'Sube un CSV/XLSX, mapea columnas y limpia totales en segundos.'
  },
  {
    title: 'Activa tus reglas',
    description: 'Clasifica automáticamente suscripciones, gastos fijos y transferencias.'
  }
];

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-900 to-slate-800 text-white">
      <nav className="mx-auto flex w-full max-w-5xl items-center justify-between px-6 py-6">
        <div className="text-2xl font-bold">Zaldo</div>
        <div className="flex items-center gap-4 text-sm font-medium">
          <Link href="#beneficios" className="hover:text-primary">Beneficios</Link>
          <Link href="#funciona" className="hover:text-primary">Cómo funciona</Link>
          <Link href="#faqs" className="hover:text-primary">FAQs</Link>
          <button className="rounded-lg border border-slate-500 px-4 py-2">Acceso beta</button>
        </div>
      </nav>

      <section className="mx-auto flex w-full max-w-5xl flex-col items-center px-6 pb-24 pt-16 text-center">
        <span className="rounded-full bg-primary/10 px-4 py-1 text-sm text-primary">Beta cerrada · Acceso por invitación</span>
        <h1 className="mt-6 text-4xl font-bold sm:text-6xl">Ordena tu plata, sin planillas</h1>
        <p className="mt-4 max-w-2xl text-lg text-slate-300">
          Una plataforma modular de finanzas personales para Chile. Importa, automatiza y entiende tu flujo mensual en minutos.
        </p>
        <WaitlistForm />
        <p className="mt-4 text-sm text-slate-400">¿Ya tienes código? <Link className="underline" href="/auth/invite">Solicita tu enlace</Link></p>
        <div className="mt-12 grid w-full gap-4 sm:grid-cols-2">
          <div className="rounded-2xl border border-slate-700 bg-slate-800/60 p-6 text-left">
            <h3 className="text-lg font-semibold text-white">Flujo mensual en tiempo real</h3>
            <p className="mt-2 text-sm text-slate-300">Ahorro, egresos y saldo acumulado. Con toggle CLP/UF y promedio móvil.</p>
          </div>
          <div className="rounded-2xl border border-slate-700 bg-slate-800/60 p-6 text-left">
            <h3 className="text-lg font-semibold text-white">Dashboard accionable</h3>
            <p className="mt-2 text-sm text-slate-300">KPIs inmediatos, gráficos 12M y categorías al día.</p>
          </div>
        </div>
      </section>

      <section id="beneficios" className="bg-white py-20 text-slate-900">
        <div className="mx-auto flex w-full max-w-5xl flex-col gap-12 px-6 md:flex-row">
          <div className="w-full md:w-1/2">
            <h2 className="text-3xl font-bold">Beneficios clave</h2>
            <p className="mt-4 text-slate-600">Diseñada para founders, freelancers y equipos que necesitan claridad financiera sin planillas eternas.</p>
          </div>
          <ul className="grid flex-1 gap-6">
            {benefits.map((benefit) => (
              <li key={benefit} className="rounded-2xl border border-slate-200 bg-slate-50 p-6 shadow-sm">
                <p className="text-lg font-semibold text-slate-900">{benefit}</p>
              </li>
            ))}
          </ul>
        </div>
      </section>

      <section id="funciona" className="bg-slate-100 py-20 text-slate-900">
        <div className="mx-auto w-full max-w-5xl px-6">
          <h2 className="text-3xl font-bold">Cómo funciona</h2>
          <div className="mt-10 grid gap-6 md:grid-cols-3">
            {steps.map((step) => (
              <div key={step.title} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <h3 className="text-xl font-semibold">{step.title}</h3>
                <p className="mt-2 text-slate-600">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="faqs" className="bg-white py-20 text-slate-900">
        <div className="mx-auto w-full max-w-5xl px-6">
          <h2 className="text-3xl font-bold">Preguntas frecuentes</h2>
          <div className="mt-8 space-y-6">
            {faqs.map((faq) => (
              <div key={faq.question} className="rounded-2xl border border-slate-200 bg-slate-50 p-6">
                <h3 className="text-xl font-semibold text-slate-900">{faq.question}</h3>
                <p className="mt-2 text-slate-600">{faq.answer}</p>
              </div>
            ))}
          </div>
          <div className="mt-10 text-sm text-slate-500">
            <p>Contacto: <a className="underline" href="mailto:hola@zaldo.cl">hola@zaldo.cl</a></p>
            <div className="mt-2 flex gap-4">
              <Link className="underline" href="/privacy">Privacidad</Link>
              <Link className="underline" href="/terms">Términos</Link>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
