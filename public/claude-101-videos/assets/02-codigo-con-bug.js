// Asset · Código con bug para demo de debugging
// Usar en: M6 · Escena 3 (Programación y análisis técnico)
//
// El bug: dentro del bucle, cuando `users[i]` es null/undefined,
// el acceso a `.name` y `.email` lanza TypeError. Además, el filtro
// de `active` no maneja el caso en que la propiedad falta.
//
// Mensaje de error que sale en producción:
// TypeError: Cannot read properties of null (reading 'name')

function sendWelcomeEmails(users, emailService) {
  const sent = [];
  const failed = [];

  for (let i = 0; i < users.length; i++) {
    const user = users[i];

    // Bug aquí: no comprobamos si user existe
    if (user.active === true) {
      const payload = {
        to: user.email,
        subject: `¡Bienvenido, ${user.name}!`,
        body: buildWelcomeBody(user.name, user.plan)
      };

      try {
        emailService.send(payload);
        sent.push(user.email);
      } catch (err) {
        failed.push({ email: user.email, error: err.message });
      }
    }
  }

  return { sent, failed };
}

function buildWelcomeBody(name, plan) {
  return `Hola ${name},\n\nGracias por unirte al plan ${plan.toUpperCase()}.`;
}

// Llamada que dispara el error en producción
const users = [
  { name: 'Laura', email: 'laura@example.com', active: true, plan: 'pro' },
  null, // <-- usuario borrado de la BBDD pero el array no se limpió
  { name: 'Diego', email: 'diego@example.com', active: true, plan: 'free' },
  { email: 'sofia@example.com', active: true, plan: 'pro' } // <-- falta name
];

sendWelcomeEmails(users, mockEmailService);
