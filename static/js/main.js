// Agro Sur Latino S.A.C. — Green Botanical Identity & Bilingual Dictionary

const translations = {
  es: {
    nav_home: "INICIO",
    nav_origin: "SOBRE NOSOTROS",
    nav_products: "PRODUCTOS",
    nav_quality: "CERTIFICACIONES",
    nav_contact: "CONTACTO",
    nav_quote: "COTIZADOR",
    nav_cta: "¿DESEAS UN TRATO?",
    floating_quote_btn: "Cotizador B2B",
    hero_btn_explore: "PRODUCTOS",
    hero_btn_quote: "COTIZAR",
    panel_secondary_label: "Variedades",
    catalog_title: "Nuestros Productos",
    filter_all: "Todos",
    b3_tag: "DESDE 2007",
    b3_headline: "Agro Sur Latino se fundó en 2007 bajo nuestro principio: “de los productores hacia el mundo”",
    b3_btn_about: "SOBRE NOSOTROS",
    b4_headline: "Nuestro principal objetivo es lograr una mejora continua y garantizar stock todo el año",
    b4_card1_title: "Orgánico",
    b4_card2_title: "Planta Propia",
    b4_card3_title: "Stock 365 Días",
    b4_img_title: "Almacenes en Huachipa • Lima",
    b15_title: "Trabajamos y producimos bajo estándares y certificados",
    cert_view_all: "Ver todos →",
    contact_box_title: "¿Deseas un trato?",
    btn_open_quoter: "Cotizador Proforma PDF",
    c_btn_send: "Enviar",
    about_tag: "SOBRE NOSOTROS • ABOUT US",
    trace_title: "De los productores hacia el mundo",
    mission_title: "Nuestra Misión",
    vision_title: "Nuestra Visión",
    cert_tag: "CALIDAD INTERNACIONAL",
    cert_title: "Garantía Sanitaria & Certificaciones",
    quote_section_title: "¿Deseas un trato? Cotiza en línea",
    step1_title: "Datos Fiscales y Despacho",
    step2_title: "Selecciona tus Productos y Volúmenes",
    opt_juridica: "Empresa (RUC 20)",
    opt_natural_ruc: "Negocio (RUC 10)",
    opt_natural_dni: "Persona (DNI)",
    opt_extranjero: "Internacional",
    lbl_legal_name: "Razón Social / Nombre *",
    lbl_contact_name: "Contacto *",
    lbl_country: "País *",
    lbl_email: "Correo *",
    lbl_phone: "Teléfono / WhatsApp *",
    lbl_incoterm: "Incoterm",
    lbl_port: "Puerto / Ciudad Destino",
    lbl_notes: "Presentación requerida (Orgánico / Convencional / Sacos)",
    btn_submit_quote: "Generar Cotización & PDF",
    modal_quote_btn: "Cotizar este producto",
  },
  en: {
    nav_home: "HOME",
    nav_origin: "ABOUT US",
    nav_products: "PRODUCTS",
    nav_quality: "CERTIFICATIONS",
    nav_contact: "CONTACT",
    nav_quote: "B2B QUOTER",
    nav_cta: "WANT A DEAL?",
    floating_quote_btn: "B2B Quote",
    hero_btn_explore: "PRODUCTS",
    hero_btn_quote: "GET QUOTE",
    panel_secondary_label: "Varieties",
    catalog_title: "Our Products",
    filter_all: "All",
    b3_tag: "SINCE 2007",
    b3_headline: "Agro Sur Latino was founded in 2007 under our principle: “from producers to the world”",
    b3_btn_about: "ABOUT US",
    b4_headline: "Our main objective is to achieve continuous improvement and guarantee year-round stock",
    b4_card1_title: "Organic",
    b4_card2_title: "Owned Plant",
    b4_card3_title: "365-Day Stock",
    b4_img_title: "Huachipa Warehouses • Lima",
    b15_title: "We work and produce under international standards and certificates",
    cert_view_all: "View all →",
    contact_box_title: "Want a deal?",
    btn_open_quoter: "PDF Proforma Builder",
    c_btn_send: "Send",
    about_tag: "ABOUT US • AGRO SUR LATINO",
    trace_title: "From producers to the world",
    mission_title: "Our Mission",
    vision_title: "Our Vision",
    cert_tag: "INTERNATIONAL QUALITY",
    cert_title: "Food Safety & Global Certifications",
    quote_section_title: "Want a deal? Quote online",
    step1_title: "Tax Identity & Shipping",
    step2_title: "Select Products and Volumes",
    opt_juridica: "Corporation (RUC 20)",
    opt_natural_ruc: "Business (RUC 10)",
    opt_natural_dni: "Individual (DNI)",
    opt_extranjero: "International Buyer",
    lbl_legal_name: "Company Legal Name *",
    lbl_contact_name: "Contact Person *",
    lbl_country: "Country *",
    lbl_email: "Corporate Email *",
    lbl_phone: "Phone / WhatsApp *",
    lbl_incoterm: "Incoterm",
    lbl_port: "Destination Port / City",
    lbl_notes: "Required presentation (Organic / Conventional / Bags)",
    btn_submit_quote: "Generate Quote & PDF",
    modal_quote_btn: "Quote this product",
  }
};

let currentLanguage = localStorage.getItem('agrosur_lang') || 'es';

function setLanguage(lang) {
  currentLanguage = lang;
  localStorage.setItem('agrosur_lang', lang);
  document.body.setAttribute('data-lang', lang);

  document.querySelectorAll('.lang-btn').forEach(btn => {
    if (btn.getAttribute('data-set-lang') === lang) {
      btn.className = 'lang-btn px-1.5 py-0.5 transition-colors text-agro-950 font-bold underline decoration-agro-600 underline-offset-4';
    } else {
      btn.className = 'lang-btn px-1.5 py-0.5 transition-colors text-agro-600 hover:text-agro-950';
    }
  });

  const t = translations[lang] || translations.es;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (t[key]) {
      el.innerText = t[key];
    }
  });

  document.querySelectorAll('.bilingual-name').forEach(el => {
    const val = lang === 'en' ? el.getAttribute('data-en') : el.getAttribute('data-es');
    if (val) el.innerText = val;
  });

  document.querySelectorAll('.bilingual-origin').forEach(el => {
    const val = lang === 'en' ? el.getAttribute('data-en') : el.getAttribute('data-es');
    if (val) el.innerText = val;
  });

  document.querySelectorAll('.bilingual-hero-title').forEach(el => {
    const val = lang === 'en' && el.getAttribute('data-en') ? el.getAttribute('data-en') : el.getAttribute('data-es');
    if (val) el.innerText = val;
  });

  updateClientTypeHints();
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
    docInput.placeholder = "20517805662";
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

  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      setLanguage(e.currentTarget.getAttribute('data-set-lang'));
    });
  });

  setLanguage(currentLanguage);

  // Hero Visual Panels Slider
  const slides = document.querySelectorAll('.hero-slide');
  const indicators = document.querySelectorAll('.hero-indicator');
  const watermarkEl = document.getElementById('hero-watermark');
  let currentSlide = 0;
  let slideInterval = null;

  function showSlide(index) {
    if (slides.length === 0) return;
    slides.forEach((s, i) => {
      if (i === index) {
        s.classList.remove('opacity-0', 'pointer-events-none', 'z-0', 'hidden', 'absolute', 'inset-0');
        s.classList.add('opacity-100', 'relative', 'z-10', 'hero-slide-active');
        if (watermarkEl) {
          const wm = currentLanguage === 'en' ? s.getAttribute('data-watermark-en') : s.getAttribute('data-watermark-es');
          if (wm) watermarkEl.innerHTML = wm.replace(' ', '<br>');
        }
      } else {
        s.classList.add('opacity-0', 'pointer-events-none', 'z-0', 'hidden', 'absolute', 'inset-0');
        s.classList.remove('opacity-100', 'relative', 'z-10', 'hero-slide-active');
      }
    });

    indicators.forEach((ind, i) => {
      const bar = ind.querySelector('.indicator-bar');
      if (i === index) {
        if (bar) bar.style.width = '100%';
        ind.classList.add('opacity-100');
        ind.classList.remove('opacity-40');
      } else {
        if (bar) bar.style.width = '0%';
        ind.classList.remove('opacity-100');
        ind.classList.add('opacity-40');
      }
    });
    currentSlide = index;
  }

  function nextSlide() {
    showSlide((currentSlide + 1) % slides.length);
  }

  function prevSlide() {
    showSlide((currentSlide - 1 + slides.length) % slides.length);
  }

  function startSlideTimer() {
    if (slideInterval) clearInterval(slideInterval);
    slideInterval = setInterval(nextSlide, 6500);
  }

  if (slides.length > 0) {
    showSlide(0);
    startSlideTimer();
    document.getElementById('hero-next')?.addEventListener('click', () => { nextSlide(); startSlideTimer(); });
    document.getElementById('hero-prev')?.addEventListener('click', () => { prevSlide(); startSlideTimer(); });
    indicators.forEach((ind, i) => {
      ind.addEventListener('click', () => { showSlide(i); startSlideTimer(); });
    });
  }

  // Client Type Radio Switcher
  document.querySelectorAll('input[name="client_type"]').forEach(radio => {
    radio.addEventListener('change', updateClientTypeHints);
  });

  // Cotizador Interactive Product Selector
  window.updateQuoteSummary = function() {
    let selectedCount = 0;
    let totalEst = 0;
    const summaryList = document.getElementById('quote-summary-items');
    if (!summaryList) return;
    summaryList.innerHTML = '';

    document.querySelectorAll('.quote-prod-checkbox:checked').forEach(cb => {
      selectedCount++;
      const prodCard = cb.closest('.quote-product-row');
      const prodName = cb.getAttribute('data-name');
      const priceFob = parseFloat(cb.getAttribute('data-price') || 0);
      const qtyInput = prodCard.querySelector('.quote-qty-input');
      const unitSelect = prodCard.querySelector('.quote-unit-select');

      const qty = parseFloat(qtyInput?.value || 1);
      const unit = unitSelect?.value || 'CONTENEDOR_40';
      const unitLabel = unitSelect?.options[unitSelect.selectedIndex]?.text || unit;

      let subtotal = 0;
      if (unit === 'CONTENEDOR_40') {
        subtotal = qty * 20000 * priceFob;
      } else if (unit === 'TONELADAS') {
        subtotal = qty * 1000 * priceFob;
      } else if (unit === 'PALLET') {
        subtotal = qty * 1000 * priceFob;
      } else {
        subtotal = qty * 25 * priceFob;
      }

      totalEst += subtotal;

      const li = document.createElement('div');
      li.className = 'flex items-center justify-between text-xs py-1.5 border-b border-stone-800';
      li.innerHTML = `
        <span class="font-normal text-stone-200">${prodName} (${qty} ${unitLabel})</span>
        <span class="font-mono font-medium text-agro-300">~$${Math.round(subtotal).toLocaleString()} USD</span>
      `;
      summaryList.appendChild(li);
    });

    const countBadge = document.getElementById('quote-selected-count');
    if (countBadge) countBadge.innerText = selectedCount;

    const totalEl = document.getElementById('quote-total-est');
    if (totalEl) totalEl.innerText = `$${Math.round(totalEst).toLocaleString()} USD`;

    const placeholder = document.getElementById('quote-empty-placeholder');
    if (placeholder) {
      placeholder.classList.toggle('hidden', selectedCount > 0);
    }
  };

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

  const firstCheckbox = document.querySelector('.quote-prod-checkbox');
  if (firstCheckbox) {
    firstCheckbox.checked = true;
    firstCheckbox.dispatchEvent(new Event('change'));
  }

  // Quote Form Submission
  const quoteForm = document.getElementById('quote-form');
  if (quoteForm) {
    quoteForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const checkedItems = document.querySelectorAll('.quote-prod-checkbox:checked');
      if (checkedItems.length === 0) {
        showToast('Por favor selecciona al menos un producto para cotizar.', false);
        return;
      }

      const clientType = document.querySelector('input[name="client_type"]:checked').value;
      const docNum = document.getElementById('input-doc-number').value.trim();

      if (clientType === 'NATURAL_DNI' && !/^\d{8}$/.test(docNum)) {
        showToast('El DNI debe contener exactamente 8 dígitos numéricos.', false);
        return;
      }
      if (clientType === 'NATURAL_RUC' && (!/^\d{11}$/.test(docNum) || !docNum.startsWith('10'))) {
        showToast('El RUC de Persona Natural debe tener 11 dígitos e iniciar con 10.', false);
        return;
      }
      if (clientType === 'JURIDICA_RUC' && (!/^\d{11}$/.test(docNum) || !docNum.startsWith('20'))) {
        showToast('El RUC de Empresa debe tener 11 dígitos e iniciar con 20.', false);
        return;
      }

      const submitBtn = quoteForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;
      submitBtn.disabled = true;

      const items = [];
      checkedItems.forEach(cb => {
        const row = cb.closest('.quote-product-row');
        const qty = parseFloat(row.querySelector('.quote-qty-input')?.value || 1);
        const unit = row.querySelector('.quote-unit-select')?.value || 'CONTENEDOR_40';
        const priceFob = parseFloat(cb.getAttribute('data-price') || 0);
        let subtotal = 0;
        if (unit === 'CONTENEDOR_40') subtotal = qty * 20000 * priceFob;
        else if (unit === 'TONELADAS') subtotal = qty * 1000 * priceFob;
        else if (unit === 'PALLET') subtotal = qty * 1000 * priceFob;
        else subtotal = qty * 25 * priceFob;

        items.push({
          product_id: parseInt(cb.value),
          quantity: qty,
          unit: unit,
          subtotal: Math.round(subtotal)
        });
      });

      const payload = {
        client_type: clientType,
        document_number: docNum,
        legal_name: document.getElementById('input-legal-name').value.trim(),
        contact_name: document.getElementById('input-contact-name').value.trim(),
        country: document.getElementById('input-country').value.trim(),
        email: document.getElementById('input-email').value.trim(),
        phone: document.getElementById('input-phone').value.trim(),
        incoterm: document.getElementById('input-incoterm').value,
        destination_port: document.getElementById('input-destination-port').value.trim(),
        notes: document.getElementById('input-notes').value.trim(),
        items: items,
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
          showToast(data.message || 'Error al procesar la cotización.', false);
        }
      } catch (err) {
        showToast('Error de conexión con el servidor.', false);
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
      const formData = new FormData(contactForm);
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
          showToast(data.message || 'Complete los campos requeridos.', false);
        }
      } catch (err) {
        showToast('Error al enviar el mensaje.', false);
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

  window.openProductModal = function (btn) {
    if (!modal) return;
    const data = JSON.parse(btn.getAttribute('data-product'));
    const isEn = currentLanguage === 'en';
    modalImage.src = data.image;
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
  };

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
