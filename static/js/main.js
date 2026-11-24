// Agro Sur Latino S.A.C. — Diccionario bilingüe
// Única fuente: landing/i18n.json. Django lo usa para enviar las páginas /en/ ya traducidas
// (landing/middleware.py) y lo inserta en cada página como <script id="i18n-data"> para este archivo.
const _i18n = (() => {
  try { return JSON.parse(document.getElementById('i18n-data').textContent); }
  catch (e) { return { translations: { es: {}, en: {} }, phraseEN: {} }; }
})();
const translations = _i18n.translations;
const phraseEN = _i18n.phraseEN;

const _origText = new WeakMap();
const _origAttrs = new WeakMap();
const _normText = (t) => t.replace(/\s+/g, ' ').trim();

function applyStaticTranslations(lang) {
  const en = lang === 'en';
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(n => {
    const tag = n.parentElement && n.parentElement.tagName;
    if (!tag || tag === 'SCRIPT' || tag === 'STYLE') return;
    if (!_origText.has(n)) {
      if (!phraseEN[_normText(n.textContent)]) return;
      _origText.set(n, n.textContent);
    }
    const orig = _origText.get(n);
    n.textContent = en ? orig.replace(_normText(orig), phraseEN[_normText(orig)]) : orig;
  });

  document.querySelectorAll('[placeholder],[aria-label],[title],[alt]').forEach(el => {
    ['placeholder', 'aria-label', 'title', 'alt'].forEach(attr => {
      const cur = el.getAttribute(attr);
      if (cur === null) return;
      let store = _origAttrs.get(el);
      if (!store) { store = {}; _origAttrs.set(el, store); }
      if (!(attr in store)) {
        if (!phraseEN[_normText(cur)]) return;
        store[attr] = cur;
      }
      el.setAttribute(attr, en ? phraseEN[_normText(store[attr])] : store[attr]);
    });
  });

  // Elementos con texto alternativo en el HTML (p. ej. opciones de producto)
  document.querySelectorAll('[data-en-text]').forEach(el => {
    if (!el.hasAttribute('data-es-text')) el.setAttribute('data-es-text', el.textContent);
    el.textContent = en ? el.getAttribute('data-en-text') : el.getAttribute('data-es-text');
  });

  // El <title> y la meta descripción ya llegan en el idioma de la URL desde el servidor
  document.documentElement.lang = lang;
}

// El idioma lo fija la URL (/ = inglés, /es/ = español): lo lee del <html lang> que renderiza Django
let currentLanguage = (document.documentElement.lang || 'es').slice(0, 2) === 'en' ? 'en' : 'es';
const tr = (es, en) => (currentLanguage === 'en' ? en : es);

function setLanguage(lang) {
  currentLanguage = lang;
  document.body.setAttribute('data-lang', lang);

  document.querySelectorAll('.lang-btn').forEach(btn => {
    if (btn.getAttribute('data-set-lang') === lang) {
      btn.className = 'lang-btn inline-block px-1.5 py-0.5 transition-colors text-agro-950 font-bold underline decoration-agro-600 underline-offset-4';
    } else {
      btn.className = 'lang-btn inline-block px-1.5 py-0.5 transition-colors text-agro-600 hover:text-agro-950';
    }
  });

  const t = translations[lang] || translations.es;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (t[key]) {
      if (t[key].includes('<')) el.innerHTML = t[key]; else el.innerText = t[key];
    }
  });

  document.querySelectorAll('.bilingual-name').forEach(el => {
    const val = lang === 'en' ? el.getAttribute('data-en') : el.getAttribute('data-es');
    if (val) el.innerText = val;
  });

  // Nombre accesible de las tarjetas de producto en el idioma activo
  document.querySelectorAll('[data-product][role="button"]').forEach(card => {
    const name = card.querySelector('.bilingual-name')?.textContent.trim();
    if (name) card.setAttribute('aria-label', (lang === 'en' ? 'View details of ' : 'Ver detalles de ') + name);
  });

  document.querySelectorAll('a[aria-label][href*="?cat="]').forEach(link => {
    const name = link.querySelector('.bilingual-name')?.textContent.trim();
    if (name) link.setAttribute('aria-label', name);
  });

  document.querySelectorAll('img[data-alt-en]').forEach(img => {
    img.alt = lang === 'en' ? img.getAttribute('data-alt-en') : img.getAttribute('data-alt-es');
  });

  document.querySelectorAll('.bilingual-origin').forEach(el => {
    const val = lang === 'en' ? el.getAttribute('data-en') : el.getAttribute('data-es');
    if (val) el.innerText = val;
  });

  applyStaticTranslations(lang);
  updateClientTypeHints();
  updatePriceLabels();
  applyQuoteMode();
}

// Precio por kg en cada producto del cotizador: US$ FOB (exportación) o S/ con IGV (Perú)
function updatePriceLabels() {
  const labels = document.querySelectorAll('.quote-price');
  if (!labels.length) return;
  const type = document.querySelector('input[name="client_type"]:checked')?.value || 'JURIDICA_RUC';
  const peru = type !== 'EXTRANJERO';
  const en = currentLanguage === 'en';
  labels.forEach(el => {
    const value = el.getAttribute(peru ? 'data-pen' : 'data-usd');
    const suffix = peru ? (en ? ' / kg (incl. VAT)' : ' / kg (incl. IGV)') : (en ? ' / kg FOB' : ' / kg FOB');
    el.textContent = value + suffix;
  });
}

// Cotización en Perú (RUC 20, RUC 10, DNI): sin Incoterm ni puerto de destino; el total incluye IGV, no es FOB
function applyQuoteMode() {
  const peru = (document.querySelector('input[name="client_type"]:checked')?.value || 'JURIDICA_RUC') !== 'EXTRANJERO';
  ['incoterm-field', 'port-field'].forEach(id => document.getElementById(id)?.classList.toggle('hidden', peru));
  const label = document.getElementById('quote-total-label');
  if (label) {
    const en = currentLanguage === 'en';
    label.textContent = peru ? (en ? 'Estimated total (incl. VAT):' : 'Total estimado (incl. IGV):') : (en ? 'Estimated FOB Total:' : 'Total FOB Estimado:');
  }
}

function updateClientTypeHints() {
  const selectedType = document.querySelector('input[name="client_type"]:checked')?.value || 'JURIDICA_RUC';
  const docLabel = document.getElementById('lbl-doc-number');
  const docInput = document.getElementById('input-doc-number');
  const countryInput = document.getElementById('input-country');
  const docHint = document.getElementById('doc-validation-hint');

  if (!docLabel || !docInput || !docHint) return;
  const isEn = currentLanguage === 'en';

  if (selectedType === 'JURIDICA_RUC') {
    docLabel.innerText = isEn ? "Company RUC (11 digits, starts with 20) *" : "RUC Empresa (11 dígitos, inicia con 20) *";
    docInput.placeholder = "20123456789";
    docInput.maxLength = 11;
    docHint.innerText = isEn ? "SUNAT Tax ID: 11 digits starting with 20" : "Ley del RUC (SUNAT): 11 dígitos numéricos que inician con 20";
    if (countryInput) countryInput.value = "Perú";
  } else if (selectedType === 'NATURAL_RUC') {
    docLabel.innerText = isEn ? "Personal RUC (11 digits, starts with 10) *" : "RUC Persona Natural (11 dígitos, inicia con 10) *";
    docInput.placeholder = "10456789012";
    docInput.maxLength = 11;
    docHint.innerText = isEn ? "SUNAT RUC: 11 digits starting with 10" : "Ley del RUC (SUNAT): 11 dígitos numéricos que inician con 10";
    if (countryInput) countryInput.value = "Perú";
  } else if (selectedType === 'NATURAL_DNI') {
    docLabel.innerText = isEn ? "National ID - DNI (8 digits) *" : "DNI Peruano (8 dígitos numéricos) *";
    docInput.placeholder = "45678901";
    docInput.maxLength = 8;
    docHint.innerText = isEn ? "National ID: 8 numeric digits" : "Documento Nacional de Identidad: 8 dígitos numéricos";
    if (countryInput) countryInput.value = "Perú";
  } else if (selectedType === 'EXTRANJERO') {
    docLabel.innerText = isEn ? "International Tax ID / VAT / EIN *" : "Tax ID / VAT / Registro Fiscal Extranjero *";
    docInput.placeholder = isEn ? "e.g. NL854621589B01" : "Ej: NL854621589B01 o EIN";
    docInput.maxLength = 30;
    docHint.innerText = isEn ? "Enter foreign tax ID and destination country" : "Ingrese Tax ID extranjero y país de destino";
    if (countryInput && (countryInput.value === 'Perú' || countryInput.value === 'Peru')) {
      countryInput.value = '';
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (typeof Lenis !== 'undefined') {
    const lenis = new Lenis({
      duration: 1.1,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
    });
    function raf(time) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);
    window.lenis = lenis;
  }

  if (window.lucide) {
    window.lucide.createIcons();
  }

  setLanguage(currentLanguage);

  // Animaciones de aparición al hacer scroll (estilo Xpodeka)
  (function initScrollReveal() {
    if (!('IntersectionObserver' in window)) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    const targets = document.querySelectorAll([
      'main section:not(.hero-photo) h1', 'main section:not(.hero-photo) h2', 'main section:not(.hero-photo) h3',
      'main section:not(.hero-photo) > div > p', 'main section:not(.hero-photo) .reveal-item',
      'main form',
      'main section:not(.hero-photo) .rounded-2xl', 'main section:not(.hero-photo) .rounded-3xl',
    ].join(','));

    const seen = new Set();
    const items = [];

    // Las cuadrículas de productos aparecen como UN solo bloque (no fila por fila)
    const productGrids = new Set([...document.querySelectorAll('main [data-product]')].map(e => e.parentElement));
    const quoteGrid = document.getElementById('quote-items-selection');
    if (quoteGrid) productGrids.add(quoteGrid);
    productGrids.forEach(g => { if (g && !seen.has(g)) { seen.add(g); items.push(g); } });

    targets.forEach(el => {
      if (seen.has(el) || el.closest('#product-modal, #video-modal, #notification-toast, header, footer')) return;
      // evita animar un elemento dentro de otro ya animado
      if (items.some(p => p.contains(el))) return;
      seen.add(el);
      items.push(el);
    });

    // retraso escalonado entre hermanos
    const counters = new Map();
    items.forEach(el => {
      const n = counters.get(el.parentElement) || 0;
      counters.set(el.parentElement, n + 1);
      el.style.setProperty('--reveal-delay', Math.min(n, 5) * 90 + 'ms');
      el.classList.add('reveal');
    });

    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        io.unobserve(el);
        el.classList.add('reveal-in');
        // al terminar, quitar las clases para no pisar los hover/transiciones propios del elemento
        setTimeout(() => {
          el.classList.remove('reveal', 'reveal-in');
          el.style.removeProperty('--reveal-delay');
        }, 1300);
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -6% 0px' });

    items.forEach(el => io.observe(el));
  })();

  // Menú: transparente sobre la foto del inicio, sólido al hacer scroll
  const navbar = document.getElementById('navbar');
  if (navbar) {
    const onScroll = () => navbar.classList.toggle('is-scrolled', window.scrollY > 40);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Client Type Radio Switcher
  document.querySelectorAll('input[name="client_type"]').forEach(radio => {
    radio.addEventListener('change', updateClientTypeHints);
  });

  // Cotizador Interactive Product Selector
  // Los montos los calcula el servidor (/api/quote/estimate/); aquí solo se muestran.
  const MAX_QTY = { CONTENEDOR_FCL: 50, TONELADAS: 1000, PALLET: 1000, SACOS_25KG: 10000, KILOS: 100000 };
  const selectedClientType = () => document.querySelector('input[name="client_type"]:checked')?.value || 'JURIDICA_RUC';
  const isPeruType = (t) => t !== 'EXTRANJERO';

  function collectQuoteItems() {
    const items = [];
    document.querySelectorAll('.quote-prod-checkbox:checked').forEach(cb => {
      const row = cb.closest('.quote-product-row');
      items.push({
        product_id: parseInt(cb.value, 10),
        name: cb.getAttribute('data-name'),
        quantity: row.querySelector('.quote-qty-input')?.value || '',
        unit: row.querySelector('.quote-unit-select')?.value || '',
        unitLabel: (() => { const sel = row.querySelector('.quote-unit-select'); return sel?.options[sel.selectedIndex]?.text || ''; })(),
      });
    });
    return items;
  }

  // Unidades disponibles según tipo de cliente (Perú: S/ con IGV, sacos o kilos)
  function applyClientTypeUnits() {
    const peru = isPeruType(selectedClientType());
    document.querySelectorAll('.quote-unit-select').forEach(sel => {
      Array.from(sel.options).forEach(opt => {
        const scope = opt.getAttribute('data-scope');
        const ok = scope === 'both' || (peru ? scope === 'peru' : scope === 'export');
        opt.hidden = !ok;
        opt.disabled = !ok;
      });
      if (sel.options[sel.selectedIndex]?.disabled) {
        sel.value = peru ? 'SACOS_25KG' : 'CONTENEDOR_FCL';
      }
      const qty = sel.closest('.quote-product-row')?.querySelector('.quote-qty-input');
      if (qty) qty.max = MAX_QTY[sel.value] || 50;
    });
  }

  let estimateTimer = null;
  let estimateSeq = 0;
  window.updateQuoteSummary = function() {
    clearTimeout(estimateTimer);
    estimateTimer = setTimeout(runEstimate, 200);
  };

  async function runEstimate() {
    const summaryList = document.getElementById('quote-summary-items');
    if (!summaryList) return;
    const items = collectQuoteItems();
    const countBadge = document.getElementById('quote-selected-count');
    if (countBadge) countBadge.innerText = items.length;
    const placeholder = document.getElementById('quote-empty-placeholder');
    if (placeholder) placeholder.classList.toggle('hidden', items.length > 0);
    const totalEl = document.getElementById('quote-total-est');

    summaryList.innerHTML = '';
    if (items.length === 0) {
      if (totalEl) totalEl.innerText = '—';
      return;
    }

    const seq = ++estimateSeq;
    let data = null;
    try {
      const res = await fetch('/api/quote/estimate/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || '' },
        body: JSON.stringify({ client_type: selectedClientType(), lang: currentLanguage, items: items.map(i => ({ product_id: i.product_id, quantity: i.quantity, unit: i.unit })) }),
      });
      data = await res.json();
    } catch (err) {
      data = null;
    }
    if (seq !== estimateSeq) return; // llegó una respuesta más nueva

    const subtotals = {};
    const served = {};
    if (data && data.success) data.items.forEach(i => { subtotals[i.product_id] = i.subtotal; served[i.product_id] = i; });
    items.forEach(i => {
      const li = document.createElement('div');
      li.className = 'flex items-center justify-between text-xs py-1.5 border-b border-stone-800';
      const left = document.createElement('span');
      left.className = 'font-normal text-stone-200';
      const s = served[i.product_id];
      left.textContent = s ? `${s.name} (${s.label})` : `${i.name} (${i.quantity} ${i.unitLabel})`;
      const right = document.createElement('span');
      right.className = 'font-mono font-medium text-agro-300';
      right.textContent = subtotals[i.product_id] ? `~${subtotals[i.product_id]}` : '—';
      li.append(left, right);
      summaryList.appendChild(li);
    });
    if (totalEl) totalEl.innerText = data && data.success ? data.total : (data?.message || '—');
  }

  document.querySelectorAll('input[name="client_type"]').forEach(r => {
    r.addEventListener('change', () => { applyClientTypeUnits(); updatePriceLabels(); applyQuoteMode(); updateQuoteSummary(); });
  });
  document.querySelectorAll('.quote-unit-select').forEach(sel => {
    sel.addEventListener('change', () => {
      const qty = sel.closest('.quote-product-row')?.querySelector('.quote-qty-input');
      if (qty) qty.max = MAX_QTY[sel.value] || 50;
    });
  });
  applyClientTypeUnits();

  document.querySelectorAll('.quote-prod-checkbox').forEach(cb => {
    cb.addEventListener('change', (e) => {
      const row = e.target.closest('.quote-product-row');
      const controls = row.querySelector('.quote-controls');
      if (e.target.checked) {
        row.classList.add('border-agro-600', 'bg-agro-50/40');
        row.classList.remove('border-stone-200', 'bg-white');
        if (controls) controls.classList.remove('opacity-40', 'pointer-events-none');
      } else {
        row.classList.remove('border-agro-600', 'bg-agro-50/40');
        row.classList.add('border-stone-200', 'bg-white');
        if (controls) controls.classList.add('opacity-40', 'pointer-events-none');
      }
      updateQuoteSummary();
    });
  });

  document.querySelectorAll('.quote-qty-input, .quote-unit-select').forEach(input => {
    input.addEventListener('input', updateQuoteSummary);
    input.addEventListener('change', updateQuoteSummary);
  });

  // Producto preseleccionado desde el catálogo (?producto=slug, ya marcado por el servidor); si no hay, el primero
  const preselected = document.querySelectorAll('.quote-prod-checkbox:checked');
  if (preselected.length) {
    preselected.forEach(cb => cb.dispatchEvent(new Event('change')));
    if (new URLSearchParams(window.location.search).has('producto')) {
      const row = preselected[0].closest('.quote-product-row');
      if (row) setTimeout(() => {
        const top = row.getBoundingClientRect().top + window.scrollY - Math.max(120, (window.innerHeight - row.offsetHeight) / 2);
        window.scrollTo({ top, behavior: 'instant' });
      }, 300);
    }
  } else {
    const firstCheckbox = document.querySelector('.quote-prod-checkbox');
    if (firstCheckbox) {
      firstCheckbox.checked = true;
      firstCheckbox.dispatchEvent(new Event('change'));
    }
  }

  // Quote Form Submission
  const quoteForm = document.getElementById('quote-form');
  if (quoteForm) {
    quoteForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const checkedItems = document.querySelectorAll('.quote-prod-checkbox:checked');
      if (checkedItems.length === 0) {
        showToast(tr('Por favor selecciona al menos un producto para cotizar.', 'Please select at least one product to quote.'), false);
        return;
      }

      const clientType = document.querySelector('input[name="client_type"]:checked').value;
      const docNum = document.getElementById('input-doc-number').value.trim();

      if (clientType === 'NATURAL_DNI' && !/^\d{8}$/.test(docNum)) {
        showToast(tr('El DNI debe contener exactamente 8 dígitos numéricos.', 'The DNI must contain exactly 8 digits.'), false);
        return;
      }
      if (clientType === 'NATURAL_RUC' && (!/^\d{11}$/.test(docNum) || !/^1[057]/.test(docNum))) {
        showToast(tr('El RUC de Persona Natural debe tener 11 dígitos e iniciar con 10, 15 o 17.', 'The personal RUC must have 11 digits and start with 10, 15 or 17.'), false);
        return;
      }
      if (clientType === 'JURIDICA_RUC' && (!/^\d{11}$/.test(docNum) || !docNum.startsWith('20'))) {
        showToast(tr('El RUC de Empresa debe tener 11 dígitos e iniciar con 20.', 'The company RUC must have 11 digits and start with 20.'), false);
        return;
      }

      const submitBtn = quoteForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;
      submitBtn.disabled = true;

      const items = collectQuoteItems().map(i => ({ product_id: i.product_id, quantity: i.quantity, unit: i.unit }));

      const payload = {
        client_type: clientType,
        document_number: docNum,
        legal_name: document.getElementById('input-legal-name').value.trim(),
        contact_name: document.getElementById('input-contact-name').value.trim(),
        country: document.getElementById('input-country').value.trim(),
        email: document.getElementById('input-email').value.trim(),
        phone: document.getElementById('input-phone').value.trim(),
        incoterm: clientType === 'EXTRANJERO' ? document.getElementById('input-incoterm').value : '',
        destination_port: clientType === 'EXTRANJERO' ? document.getElementById('input-destination-port').value.trim() : '',
        notes: document.getElementById('input-notes').value.trim(),
        items: items,
        website: document.getElementById('input-website')?.value || '',
        lang: currentLanguage,
      };

      try {
        const res = await fetch('/api/quote/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
          },
          body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (data.success) {
          showToast(data.message, true);
          const banner = document.getElementById('quote-success-banner');
          if (banner) {
            banner.classList.remove('hidden');
            const codeEl = document.getElementById('quote-success-code');
            if (codeEl) codeEl.innerText = data.quote_code;
            const pdfBtn = document.getElementById('quote-success-pdf-btn');
            if (pdfBtn && data.pdf_url) {
              pdfBtn.href = data.pdf_url;
            }
            banner.scrollIntoView({ behavior: 'smooth' });
          }
        } else {
          showToast(data.message || tr('Error al procesar la cotización.', 'Error processing the quotation.'), false);
        }
      } catch (err) {
        showToast(tr('Error de conexión con el servidor.', 'Connection error with the server.'), false);
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    });
  }

  // Direct Contact Form Submission
  const contactForm = document.getElementById('direct-contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;
      const formData = new FormData(contactForm);
      formData.set('lang', currentLanguage);
      try {
        const res = await fetch('/api/contact/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken') || ''
          },
          body: formData
        });
        const data = await res.json();
        if (data.success) {
          showToast(data.message, true);
          contactForm.reset();
        } else {
          showToast(data.message || tr('Complete los campos requeridos.', 'Please complete the required fields.'), false);
        }
      } catch (err) {
        showToast(tr('Error al enviar el mensaje.', 'Error sending the message.'), false);
      } finally {
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  }

  // Toast Notification
  const toast = document.getElementById('notification-toast');
  const toastMessage = document.getElementById('toast-message');

  function showToast(msg, isSuccess = true) {
    if (!toast) return;
    toastMessage.innerText = msg;
    toast.className = `fixed bottom-6 right-6 z-50 flex items-center gap-3 px-6 py-4 rounded-2xl shadow-xl transition-all duration-500 transform translate-y-0 opacity-100 ${
      isSuccess ? 'bg-[#143d1f] text-white border border-agro-500' : 'bg-red-900 text-white border border-red-700'
    }`;
    setTimeout(() => {
      toast.classList.add('translate-y-12', 'opacity-0');
    }, 6000);
  }

  // Product Visual Modal
  const modal = document.getElementById('product-modal');
  const modalImage = document.getElementById('modal-image');
  const modalTitle = document.getElementById('modal-title');
  const modalScientific = document.getElementById('modal-scientific');
  const modalVariety = document.getElementById('modal-variety');
  const modalOrigin = document.getElementById('modal-origin');
  const modalSeason = document.getElementById('modal-season');
  const modalSpecs = document.getElementById('modal-specs');
  const closeModalBtn = document.getElementById('modal-close');

  const modalQuoteBtn = document.getElementById('modal-quote-btn');
  let modalTrigger = null;

  window.openProductModal = function (btn) {
    if (!modal) return;
    const data = JSON.parse(btn.getAttribute('data-product'));
    const isEn = currentLanguage === 'en';
    modalTrigger = btn;
    modalImage.src = data.image;
    modalImage.alt = isEn && data.name_en ? data.name_en : data.name;
    if (modalQuoteBtn && data.slug) {
      // El cotizador llega con este producto ya seleccionado
      modalQuoteBtn.href = (modalQuoteBtn.getAttribute('data-quote-url') || '/cotizador/') + '?producto=' + encodeURIComponent(data.slug);
    }
    modalTitle.innerText = isEn && data.name_en ? data.name_en : data.name;
    modalScientific.innerText = (isEn ? data.modality_en : data.modality) || data.scientific_name || '';
    modalVariety.innerText = data.variety;
    modalOrigin.innerText = isEn && data.origin_en ? data.origin_en : data.origin;
    modalSeason.innerText = isEn && data.season_en ? data.season_en : data.season;
    modalSpecs.innerText = isEn && data.packing_specs_en ? data.packing_specs_en : data.packing_specs;

    modal.classList.remove('hidden');
    setTimeout(() => {
      modal.classList.remove('opacity-0');
      modal.querySelector('.modal-card').classList.remove('scale-95');
      modal.querySelector('.modal-card').classList.add('scale-100');
      if (closeModalBtn) closeModalBtn.focus();
    }, 10);
  };

  window.closeModal = function() {
    if (!modal) return;
    modal.classList.add('opacity-0');
    modal.querySelector('.modal-card').classList.add('scale-95');
    modal.querySelector('.modal-card').classList.remove('scale-100');
    setTimeout(() => {
      modal.classList.add('hidden');
    }, 300);
    if (modalTrigger) { modalTrigger.focus(); modalTrigger = null; }
  };

  // Teclado: las tarjetas de producto se abren con Enter / Espacio y el modal se cierra con Esc
  document.querySelectorAll('[data-product][role="button"]').forEach(card => {
    card.addEventListener('keydown', (e) => {
      if (e.target !== card) return;
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openProductModal(card);
      }
    });
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal && !modal.classList.contains('hidden')) closeModal();
  });

  if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });
  }

  // Mobile Menu
  const mobileToggle = document.getElementById('mobile-menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
    });
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => mobileMenu.classList.add('hidden'));
    });
  }
});
