// Agrosur Interactive Engine & Bilingual Dictionary

const translations = {
  es: {
    nav_home: "Inicio",
    nav_products: "Nuestros Frutos",
    nav_quote: "Cotizador Online",
    nav_origin: "Origen & Campos",
    nav_quality: "Certificaciones",
    nav_cta: "Cotizar Despacho",
    nav_tagline: "Agroexportación de Origen",
    floating_quote_btn: "Cotizador B2B / RUC Activo",
    hero_badge: "Temporada de Exportación 2026 en Marcha • Origen Perú",
    hero_title: "La Excelencia de los Frutos del Perú al Mundo.",
    hero_subtitle: "Cultivamos, cosechamos y exportamos los mejores superfoods y frutas frescas del país con trazabilidad garantizada y certificación internacional.",
    hero_btn_explore: "Ver Frutos de Exportación",
    hero_btn_quote: "Cotizador RUC & Internacional",
    catalog_tag: "Catálogo de Cosecha",
    catalog_title: "Nuestros Frutos de Exportación",
    catalog_desc: "Seleccionados a mano en punto óptimo de maduración, con cadena de frío continua desde el empaque hasta destino.",
    card_spec_btn: "Ver Ficha Técnica",
    quote_section_tag: "Mesa de Cotizaciones Inteligente",
    quote_section_title: "Cotizador de Exportación Agrosur",
    quote_section_desc: "Configura tu pedido según la normativa tributaria del Perú (RUC 20 / RUC 10 / DNI) o como Importador Extranjero.",
    step1_title: "1. Tipo de Cliente & Datos Fiscales",
    step2_title: "2. Selecciona los Frutos y Volúmenes",
    step3_title: "3. Términos de Entrega & Despacho",
    opt_juridica: "Empresa / Persona Jurídica (RUC 20)",
    opt_juridica_sub: "Ley del RUC Perú (SUNAT)",
    opt_natural_ruc: "Persona Natural con Negocio (RUC 10)",
    opt_natural_ruc_sub: "Ley del RUC Perú (SUNAT)",
    opt_natural_dni: "Persona Natural (DNI 8 dígitos)",
    opt_natural_dni_sub: "Documento Nacional Perú",
    opt_extranjero: "Cliente Internacional / Empresa Extranjera",
    opt_extranjero_sub: "Tax ID / VAT / Importador Global",
    lbl_legal_name: "Razón Social o Nombre Legal *",
    lbl_doc_num: "N° de Documento (RUC / DNI / Tax ID) *",
    lbl_contact_name: "Persona o Encargado de Compras *",
    lbl_country: "País de Destino / Residencia *",
    lbl_email: "Correo Electrónico Corporativo *",
    lbl_phone: "Teléfono / WhatsApp *",
    lbl_incoterm: "Incoterm Deseado",
    lbl_port: "Puerto o Aeropuerto de Arribo",
    lbl_notes: "Notas adicionales, calibres específicos o semanas de arribo",
    btn_submit_quote: "Generar y Enviar Cotización Formal",
    trace_tag: "Trazabilidad Integral",
    trace_title: "El Estándar Agrosur",
    trace_desc: "De los fértiles valles de Ica, Piura y Olmos hasta las mesas de Europa, Asia y América.",
    step_01_title: "Campos Propios & Riego Tecnificado",
    step_01_desc: "Gestión hídrica de precisión en valles desérticos con microclimas privilegiados que otorgan dulzura, firmeza y color natural excepcional.",
    step_02_title: "Planta de Empaque & Cadena de Frío",
    step_02_desc: "Líneas de selección óptica de última generación, calibrado por peso y cámaras frigoríficas de pre-enfriado rápido en túneles automáticos.",
    step_03_title: "Logística Global Directa",
    step_03_desc: "Despachos multimodales vía contenedores reefer marítimos y carga aérea express con monitoreo térmico satelital en tiempo real.",
    cert_tag: "Garantía Sanitaria Global",
    cert_title: "Homologados para Supermercados de Alta Gama",
    cert_desc: "Nuestros campos e instalaciones cuentan con auditorías continuas que acreditan inocuidad alimentaria, comercio ético y sostenibilidad ambiental.",
    footer_desc: "Agroexportadora peruana dedicada a llevar frutos frescos de alta gama a los mercados más competitivos del mundo.",
    footer_fruits_title: "Frutos Principales",
    footer_links_title: "Enlaces",
    modal_quote_btn: "Cotizar este fruto",
  },
  en: {
    nav_home: "Home",
    nav_products: "Our Fruits",
    nav_quote: "Online Quote Builder",
    nav_origin: "Origin & Fields",
    nav_quality: "Certifications",
    nav_cta: "Quote Shipment",
    nav_tagline: "Peruvian Origin Agro-Export",
    floating_quote_btn: "B2B & Tax ID Quote Tool",
    hero_badge: "Export Harvest Season 2026 Underway • Origin Peru",
    hero_title: "Excellence of Peruvian Fruits to the World.",
    hero_subtitle: "We grow, pack, and export the finest superfoods and fresh produce with guaranteed cold chain traceability and international certifications.",
    hero_btn_explore: "Explore Fresh Fruits",
    hero_btn_quote: "Interactive Quote Tool",
    catalog_tag: "Harvest Catalog",
    catalog_title: "Export Produce & Superfoods",
    catalog_desc: "Hand-picked at peak ripeness, featuring uninterrupted cold-chain assurance from packing facility to destination port.",
    card_spec_btn: "View Technical Specs",
    quote_section_tag: "Intelligent Quotation Engine",
    quote_section_title: "Agrosur Export Quote Builder",
    quote_section_desc: "Configure your order based on Peruvian tax law (RUC 20 / RUC 10 / DNI) or as an International Importer.",
    step1_title: "1. Client Type & Tax Identity",
    step2_title: "2. Select Produce and Volumes",
    step3_title: "3. Delivery Terms & Destination",
    opt_juridica: "Corporation / Legal Entity (RUC 20)",
    opt_juridica_sub: "Peru Tax Law (SUNAT)",
    opt_natural_ruc: "Sole Proprietor / Business Person (RUC 10)",
    opt_natural_ruc_sub: "Peru Tax Law (SUNAT)",
    opt_natural_dni: "Individual Citizen (DNI 8 digits)",
    opt_natural_dni_sub: "Peru National ID",
    opt_extranjero: "International Buyer / Foreign Importer",
    opt_extranjero_sub: "Tax ID / VAT / Global Importer",
    lbl_legal_name: "Company Legal Name / Full Name *",
    lbl_doc_num: "Tax ID / RUC / DNI / VAT Number *",
    lbl_contact_name: "Procurement Officer / Contact Person *",
    lbl_country: "Destination Country *",
    lbl_email: "Corporate Email Address *",
    lbl_phone: "Phone / WhatsApp *",
    lbl_incoterm: "Required Incoterm",
    lbl_port: "Destination Port or Airport",
    lbl_notes: "Additional notes, calibers, or target arrival weeks",
    btn_submit_quote: "Generate and Send Commercial Offer",
    trace_tag: "Comprehensive Traceability",
    trace_title: "The Agrosur Standard",
    trace_desc: "From the fertile valleys of Ica, Piura, and Olmos straight to tables across Europe, Asia, and the Americas.",
    step_01_title: "Owned Orchards & High-Tech Drip Irrigation",
    step_01_desc: "Precision water management in sunny coastal valleys providing superior fruit sweetness, firmness, and natural color.",
    step_02_title: "Automated Packing & Continuous Cold Chain",
    step_02_desc: "Optical sorting lines, high-speed weight grading, and automated forced-air cooling tunnels operating under HACCP standards.",
    step_03_title: "Direct Multimodal Global Logistics",
    step_03_desc: "Controlled-atmosphere reefer sea containers and express air-cargo shipments with satellite temperature tracking.",
    cert_tag: "Global Food Safety Assurance",
    cert_title: "Approved for Premium Supermarket Chains",
    cert_desc: "Our orchards and packing houses undergo rigorous continuous third-party audits certifying food safety, ethical trade, and sustainable agriculture.",
    footer_desc: "Peruvian agro-exporter delivering top-tier fresh produce to demanding international markets.",
    footer_fruits_title: "Key Fresh Produce",
    footer_links_title: "Quick Links",
    modal_quote_btn: "Quote this produce",
  }
};

let currentLanguage = localStorage.getItem('agrosur_lang') || 'es';

function setLanguage(lang) {
  currentLanguage = lang;
  localStorage.setItem('agrosur_lang', lang);
  document.body.setAttribute('data-lang', lang);

  // Update switcher button styles
  document.querySelectorAll('.lang-btn').forEach(btn => {
    if (btn.getAttribute('data-set-lang') === lang) {
      btn.className = 'lang-btn px-2.5 py-1 rounded-full transition-all bg-agro-600 text-white font-medium';
    } else {
      btn.className = 'lang-btn px-2.5 py-1 rounded-full transition-all text-stone-300 hover:text-white font-medium';
    }
  });

  // Apply translations to all data-i18n elements
  const t = translations[lang] || translations.es;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (t[key]) {
      el.innerText = t[key];
    }
  });

  // Update dynamic bilingual text in products cards and hero
  document.querySelectorAll('.bilingual-name').forEach(el => {
    el.innerText = lang === 'en' ? el.getAttribute('data-en') : el.getAttribute('data-es');
  });

  document.querySelectorAll('.bilingual-origin').forEach(el => {
    el.innerText = lang === 'en' ? el.getAttribute('data-en') : el.getAttribute('data-es');
  });

  document.querySelectorAll('.bilingual-season').forEach(el => {
    el.innerText = (lang === 'en' ? 'Season: ' : 'Temporada: ') + (lang === 'en' ? el.getAttribute('data-en') : el.getAttribute('data-es'));
  });

  document.querySelectorAll('.bilingual-hero-title').forEach(el => {
    el.innerText = lang === 'en' && el.getAttribute('data-en') ? el.getAttribute('data-en') : el.getAttribute('data-es');
  });

  document.querySelectorAll('.bilingual-hero-tagline').forEach(el => {
    el.innerText = lang === 'en' && el.getAttribute('data-en') ? el.getAttribute('data-en') : el.getAttribute('data-es');
  });

  // Update client type document hints
  updateClientTypeHints();
}

function updateClientTypeHints() {
  const selectedType = document.querySelector('input[name="client_type"]:checked')?.value || 'JURIDICA_RUC';
  const docLabel = document.getElementById('lbl-doc-number');
  const docInput = document.getElementById('input-doc-number');
  const countryInput = document.getElementById('input-country');
  const countryContainer = document.getElementById('country-field-container');
  const docHint = document.getElementById('doc-validation-hint');

  const isEn = currentLanguage === 'en';

  if (selectedType === 'JURIDICA_RUC') {
    docLabel.innerText = isEn ? "Company RUC (11 digits, starts with 20) *" : "RUC Empresa (11 dígitos, inicia con 20) *";
    docInput.placeholder = "20601234567";
    docInput.maxLength = 11;
    docHint.innerText = isEn ? "Peruvian Corporate Tax ID: Exactly 11 digits starting with 20" : "Ley del RUC (SUNAT): Exactamente 11 dígitos numéricos que inician con 20";
    if (countryInput) countryInput.value = "Perú";
  } else if (selectedType === 'NATURAL_RUC') {
    docLabel.innerText = isEn ? "Personal Business RUC (11 digits, starts with 10) *" : "RUC Persona Natural (11 dígitos, inicia con 10) *";
    docInput.placeholder = "10456789012";
    docInput.maxLength = 11;
    docHint.innerText = isEn ? "Peruvian Sole Proprietor RUC: 11 digits starting with 10" : "Ley del RUC (SUNAT): 11 dígitos numéricos que inician con 10";
    if (countryInput) countryInput.value = "Perú";
  } else if (selectedType === 'NATURAL_DNI') {
    docLabel.innerText = isEn ? "National ID - DNI (8 digits) *" : "DNI Peruano (8 dígitos numéricos) *";
    docInput.placeholder = "45678901";
    docInput.maxLength = 8;
    docHint.innerText = isEn ? "National Identity Document: 8 digits" : "Documento Nacional de Identidad: 8 dígitos numéricos";
    if (countryInput) countryInput.value = "Perú";
  } else if (selectedType === 'EXTRANJERO') {
    docLabel.innerText = isEn ? "International Tax ID / VAT Number / EIN *" : "Tax ID / VAT / Registro Fiscal Extranjero *";
    docInput.placeholder = isEn ? "e.g. NL854621589B01 or EIN 12-3456789" : "Ej: NL854621589B01 o US EIN 12-3456789";
    docInput.maxLength = 30;
    docHint.innerText = isEn ? "Enter valid foreign tax identifier and specify your destination country" : "Ingrese su identificación tributaria extranjera y especifique país de destino";
    if (countryInput && (countryInput.value === 'Perú' || countryInput.value === 'Peru')) {
      countryInput.value = '';
      countryInput.focus();
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Lenis luxury smooth momentum scroll
  if (typeof Lenis !== 'undefined') {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
      touchMultiplier: 1.5,
    });
    function raf(time) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);
    window.lenis = lenis;
  }

  // Lucide Icons initialization
  if (window.lucide) {
    window.lucide.createIcons();
  }

  // Language buttons event
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const targetLang = e.currentTarget.getAttribute('data-set-lang');
      setLanguage(targetLang);
    });
  });

  // Initialize Language
  setLanguage(currentLanguage);

  // Sticky & Dynamic Navbar
  const navbar = document.getElementById('navbar');
  const logoLight = document.getElementById('nav-logo-light');
  const logoDark = document.getElementById('nav-logo-dark');
  const navLangContainer = document.getElementById('nav-lang-container');
  const navLangMobile = document.getElementById('nav-lang-container-mobile');

  function updateNavbar() {
    const isScrolled = window.scrollY > 20;
    if (isScrolled) {
      navbar.classList.add('navbar-scrolled', 'bg-white/95', 'shadow-sm', 'backdrop-blur-md', 'py-3', 'border-b', 'border-stone-200/80');
      navbar.classList.remove('bg-transparent', 'py-5');
      navbar.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('text-white/90');
        link.classList.add('text-stone-700', 'hover:text-stone-950');
      });
      if (logoLight) {
        logoLight.style.setProperty('display', 'none', 'important');
      }
      if (logoDark) {
        logoDark.style.setProperty('display', 'block', 'important');
      }
      if (navLangContainer) {
        navLangContainer.classList.remove('glass-dark', 'text-white', 'border-white/15');
        navLangContainer.classList.add('bg-stone-100', 'text-stone-700', 'border-stone-200');
      }
      if (navLangMobile) {
        navLangMobile.classList.remove('glass-dark', 'text-white', 'border-white/15');
        navLangMobile.classList.add('bg-stone-100', 'text-stone-700', 'border-stone-200');
      }
      const mobileToggle = document.getElementById('mobile-menu-toggle');
      if (mobileToggle) {
        mobileToggle.classList.remove('text-white');
        mobileToggle.classList.add('text-stone-800');
      }
    } else {
      navbar.classList.remove('navbar-scrolled', 'bg-white/95', 'shadow-sm', 'backdrop-blur-md', 'py-3', 'border-b', 'border-stone-200/80');
      navbar.classList.add('bg-transparent', 'py-5');
      navbar.querySelectorAll('.nav-link').forEach(link => {
        link.classList.add('text-white/90');
        link.classList.remove('text-stone-700', 'hover:text-stone-950');
      });
      if (logoLight) {
        logoLight.style.setProperty('display', 'block', 'important');
      }
      if (logoDark) {
        logoDark.style.setProperty('display', 'none', 'important');
      }
      if (navLangContainer) {
        navLangContainer.classList.add('glass-dark', 'text-white', 'border-white/15');
        navLangContainer.classList.remove('bg-stone-100', 'text-stone-700', 'border-stone-200');
      }
      if (navLangMobile) {
        navLangMobile.classList.add('glass-dark', 'text-white', 'border-white/15');
        navLangMobile.classList.remove('bg-stone-100', 'text-stone-700', 'border-stone-200');
      }
      const mobileToggle = document.getElementById('mobile-menu-toggle');
      if (mobileToggle) {
        mobileToggle.classList.add('text-white');
        mobileToggle.classList.remove('text-stone-800');
      }
    }
  }

  window.addEventListener('scroll', updateNavbar, { passive: true });
  window.addEventListener('resize', updateNavbar, { passive: true });
  updateNavbar();

  // Hero Slider
  const slides = document.querySelectorAll('.hero-slide');
  const indicators = document.querySelectorAll('.hero-indicator');
  let currentSlide = 0;
  let slideInterval = null;

  function showSlide(index) {
    if (slides.length === 0) return;
    slides.forEach((s, i) => {
      if (i === index) {
        s.classList.remove('opacity-0', 'pointer-events-none', 'z-0');
        s.classList.add('opacity-100', 'z-10', 'hero-slide-active');
      } else {
        s.classList.add('opacity-0', 'pointer-events-none', 'z-0');
        s.classList.remove('opacity-100', 'z-10', 'hero-slide-active');
      }
    });

    indicators.forEach((ind, i) => {
      const bar = ind.querySelector('.indicator-bar');
      if (i === index) {
        bar.style.width = '100%';
        ind.classList.add('opacity-100');
        ind.classList.remove('opacity-40');
      } else {
        bar.style.width = '0%';
        ind.classList.remove('opacity-100');
        ind.classList.add('opacity-40');
      }
    });
    currentSlide = index;
  }

  function nextSlide() {
    let next = (currentSlide + 1) % slides.length;
    showSlide(next);
  }

  function prevSlide() {
    let prev = (currentSlide - 1 + slides.length) % slides.length;
    showSlide(prev);
  }

  function startSlideTimer() {
    if (slideInterval) clearInterval(slideInterval);
    slideInterval = setInterval(nextSlide, 7000);
  }

  if (slides.length > 0) {
    showSlide(0);
    startSlideTimer();

    const nextBtn = document.getElementById('hero-next');
    const prevBtn = document.getElementById('hero-prev');
    if (nextBtn) nextBtn.addEventListener('click', () => { nextSlide(); startSlideTimer(); });
    if (prevBtn) prevBtn.addEventListener('click', () => { prevSlide(); startSlideTimer(); });

    indicators.forEach((ind, i) => {
      ind.addEventListener('click', () => {
        showSlide(i);
        startSlideTimer();
      });
    });
  }

  // Stats Counters
  const counters = document.querySelectorAll('.stat-counter');
  let counted = false;

  const countObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !counted) {
        counted = true;
        counters.forEach(counter => {
          const targetText = counter.getAttribute('data-target') || counter.innerText;
          const numericMatch = targetText.match(/\d+[\.,]?\d*/);
          if (numericMatch) {
            const num = parseFloat(numericMatch[0].replace(',', ''));
            let current = 0;
            const duration = 1800;
            const stepTime = 20;
            const steps = duration / stepTime;
            const increment = num / steps;

            const timer = setInterval(() => {
              current += increment;
              if (current >= num) {
                counter.innerText = targetText;
                clearInterval(timer);
              } else {
                const formatted = Math.floor(current).toLocaleString();
                counter.innerText = targetText.replace(numericMatch[0], formatted);
              }
            }, stepTime);
          }
        });
      }
    });
  }, { threshold: 0.3 });

  const statsSection = document.getElementById('stats-section');
  if (statsSection) countObserver.observe(statsSection);

  // Client Type Radio Switcher
  document.querySelectorAll('input[name="client_type"]').forEach(radio => {
    radio.addEventListener('change', updateClientTypeHints);
  });

  // Cotizador Interactive Product Selector
  const quoteItemsContainer = document.getElementById('quote-items-selection');
  window.updateQuoteSummary = function() {
    let selectedCount = 0;
    let totalEst = 0;
    const summaryList = document.getElementById('quote-summary-items');
    if (!summaryList) return;
    summaryList.innerHTML = '';

    document.querySelectorAll('.quote-prod-checkbox:checked').forEach(cb => {
      selectedCount++;
      const prodCard = cb.closest('.quote-product-row');
      const prodId = cb.value;
      const prodName = cb.getAttribute('data-name');
      const priceFob = parseFloat(cb.getAttribute('data-price') || 0);
      const qtyInput = prodCard.querySelector('.quote-qty-input');
      const unitSelect = prodCard.querySelector('.quote-unit-select');

      const qty = parseFloat(qtyInput?.value || 1);
      const unit = unitSelect?.value || 'CONTENEDOR_40';
      const unitLabel = unitSelect?.options[unitSelect.selectedIndex]?.text || unit;

      // Approximate metric tons per container: 21 TM = 21000 kg
      let subtotal = 0;
      if (unit === 'CONTENEDOR_40') {
        subtotal = qty * 21000 * priceFob;
      } else if (unit === 'TONELADAS') {
        subtotal = qty * 1000 * priceFob;
      } else if (unit === 'PALLET') {
        subtotal = qty * 1000 * priceFob;
      } else {
        subtotal = qty * priceFob;
      }

      totalEst += subtotal;

      const li = document.createElement('div');
      li.className = 'flex items-center justify-between text-xs py-1.5 border-b border-agro-900/70';
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
      if (selectedCount === 0) {
        placeholder.classList.remove('hidden');
      } else {
        placeholder.classList.add('hidden');
      }
    }
  };

  // Listen to changes in product checkboxes, quantities, units
  document.querySelectorAll('.quote-prod-checkbox').forEach(cb => {
    cb.addEventListener('change', (e) => {
      const row = e.target.closest('.quote-product-row');
      const controls = row.querySelector('.quote-controls');
      if (e.target.checked) {
        row.classList.add('border-agro-500', 'bg-agro-50/60');
        row.classList.remove('border-stone-200', 'bg-white');
        if (controls) controls.classList.remove('opacity-40', 'pointer-events-none');
      } else {
        row.classList.remove('border-agro-500', 'bg-agro-50/60');
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

  // Pre-select first product to feel alive and prompt immediate interaction
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
        const msg = currentLanguage === 'en' ? 'Please select at least one produce item to quote.' : 'Por favor seleccione al menos un fruto para cotizar.';
        showToast(msg, false);
        return;
      }

      const clientType = document.querySelector('input[name="client_type"]:checked').value;
      const docNum = document.getElementById('input-doc-number').value.trim();

      // Client-side quick Peruvian RUC / DNI verification
      if (clientType === 'NATURAL_DNI' && !/^\d{8}$/.test(docNum)) {
        showToast(currentLanguage === 'en' ? 'DNI must have exactly 8 numeric digits.' : 'El DNI debe contener exactamente 8 dígitos numéricos.', false);
        return;
      }
      if (clientType === 'NATURAL_RUC' && (!/^\d{11}$/.test(docNum) || !docNum.startsWith('10'))) {
        showToast(currentLanguage === 'en' ? 'Peruvian Sole Proprietor RUC must have 11 digits starting with 10.' : 'El RUC de Persona Natural (SUNAT) debe tener 11 dígitos e iniciar con 10.', false);
        return;
      }
      if (clientType === 'JURIDICA_RUC' && (!/^\d{11}$/.test(docNum) || !docNum.startsWith('20'))) {
        showToast(currentLanguage === 'en' ? 'Peruvian Corporate RUC must have 11 digits starting with 20.' : 'El RUC de Persona Jurídica / Empresa (SUNAT) debe tener 11 dígitos e iniciar con 20.', false);
        return;
      }

      const submitBtn = quoteForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = `
        <svg class="animate-spin h-5 w-5 text-agro-950 inline-block mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
        </svg> Procesando Cotización...
      `;

      // Build Items Array
      const items = [];
      checkedItems.forEach(cb => {
        const row = cb.closest('.quote-product-row');
        const qty = parseFloat(row.querySelector('.quote-qty-input')?.value || 1);
        const unit = row.querySelector('.quote-unit-select')?.value || 'CONTENEDOR_40';
        const priceFob = parseFloat(cb.getAttribute('data-price') || 0);
        let subtotal = 0;
        if (unit === 'CONTENEDOR_40') subtotal = qty * 21000 * priceFob;
        else if (unit === 'TONELADAS') subtotal = qty * 1000 * priceFob;
        else if (unit === 'PALLET') subtotal = qty * 1000 * priceFob;
        else subtotal = qty * priceFob;

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
          // Highlight success banner in modal or section
          const banner = document.getElementById('quote-success-banner');
          if (banner) {
            banner.classList.remove('hidden');
            const codeEl = document.getElementById('quote-success-code');
            if (codeEl) codeEl.innerText = data.quote_code;
            const pdfBtn = document.getElementById('quote-success-pdf-btn');
            if (pdfBtn && data.pdf_url) {
              pdfBtn.href = data.pdf_url;
              pdfBtn.classList.remove('hidden');
            }
            if (window.lenis) {
              window.lenis.scrollTo(banner, { offset: -120 });
            } else {
              banner.scrollIntoView({ behavior: 'smooth' });
            }
          }
          quoteForm.reset();
          document.querySelectorAll('.quote-prod-checkbox').forEach(cb => { cb.checked = false; });
          updateQuoteSummary();
        } else {
          showToast(data.message || 'Error al procesar la cotización.', false);
        }
      } catch (err) {
        showToast('Error de conexión con el servidor de Agrosur.', false);
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    });
  }

  // Toast Function
  const toast = document.getElementById('notification-toast');
  const toastMessage = document.getElementById('toast-message');

  function showToast(msg, isSuccess = true) {
    if (!toast) return;
    toastMessage.innerText = msg;
    toast.className = `fixed bottom-6 right-6 z-50 flex items-center gap-3 px-6 py-4 rounded-2xl shadow-lg transition-all duration-500 transform translate-y-0 opacity-100 ${
      isSuccess ? 'bg-agro-900 text-agro-100 border border-agro-700/60' : 'bg-stone-900 text-red-200 border border-red-800/60'
    }`;
    setTimeout(() => {
      toast.classList.add('translate-y-12', 'opacity-0');
    }, 6500);
  }

  // Product Inspection Modal
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
    const data = JSON.parse(btn.getAttribute('data-product'));
    const isEn = currentLanguage === 'en';
    modalImage.src = data.image;
    modalTitle.innerText = isEn && data.name_en ? data.name_en : data.name;
    modalScientific.innerText = data.scientific_name || 'Variedad selecta de exportación';
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
