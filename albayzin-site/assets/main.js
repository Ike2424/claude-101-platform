// Casas del Albayzín — interacciones compartidas
document.addEventListener('DOMContentLoaded', () => {
  // Menú móvil
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      const open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
  }

  // Año en el footer
  document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });

  // Filtro de reseñas
  const chips = document.querySelectorAll('.chip[data-filter]');
  const reviews = document.querySelectorAll('.review[data-apto]');
  chips.forEach(chip => chip.addEventListener('click', () => {
    chips.forEach(c => c.setAttribute('aria-pressed', 'false'));
    chip.setAttribute('aria-pressed', 'true');
    const f = chip.dataset.filter;
    reviews.forEach(r => { r.hidden = !(f === 'todos' || r.dataset.apto === f); });
  }));

  // Buscador de FAQ
  const search = document.querySelector('.faq-search');
  if (search) {
    search.addEventListener('input', () => {
      const q = search.value.trim().toLowerCase();
      document.querySelectorAll('.faq-group').forEach(group => {
        let visibles = 0;
        group.querySelectorAll('details').forEach(d => {
          const match = !q || d.textContent.toLowerCase().includes(q);
          d.hidden = !match;
          if (match) visibles++;
          if (q && match) d.open = true;
        });
        group.hidden = visibles === 0;
      });
    });
  }

  // Preseleccionar apartamento desde ?apto=
  const params = new URLSearchParams(location.search);
  const aptoSelect = document.getElementById('apartamento');
  if (aptoSelect && params.get('apto')) aptoSelect.value = params.get('apto');

  // Formulario de contacto (validación en cliente)
  const form = document.getElementById('contact-form');
  if (form) {
    const llegada = form.querySelector('#llegada');
    const salida = form.querySelector('#salida');
    const hoy = new Date().toISOString().split('T')[0];
    llegada.min = hoy; salida.min = hoy;
    llegada.addEventListener('change', () => { salida.min = llegada.value || hoy; });

    form.addEventListener('submit', e => {
      e.preventDefault();
      let ok = true;
      const setErr = (id, msg) => {
        const el = form.querySelector(`[data-error-for="${id}"]`);
        if (el) el.textContent = msg || '';
        if (msg) ok = false;
      };
      const v = id => form.querySelector('#' + id).value.trim();

      setErr('nombre', v('nombre').length < 2 ? 'Indica tu nombre.' : '');
      setErr('email', /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v('email')) ? '' : 'Introduce un email válido.');
      setErr('salida', v('llegada') && v('salida') && v('salida') <= v('llegada') ? 'La salida debe ser posterior a la llegada.' : '');
      setErr('mensaje', v('mensaje').length < 10 ? 'Cuéntanos un poco más (mín. 10 caracteres).' : '');
      setErr('privacidad', form.querySelector('#privacidad').checked ? '' : 'Debes aceptar la política de privacidad.');

      if (ok) {
        form.hidden = true;
        const msg = document.querySelector('.form-ok');
        msg.querySelector('[data-nombre]').textContent = v('nombre').split(' ')[0];
        msg.classList.add('show');
        msg.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  }
});
