// Google Integrations - Analytics, Tag Manager, and Consent Management
(function() {
  const GA_ID = 'G-E6BP31TD57';
  const GTM_ID = 'GTM-TH898GVT';
  const CONSENT_KEY = 'vedtam_cookie_consent';
  let gtmLoadPromise = null;
  let gaLoadPromise = null;

  function getConsent() {
    const stored = localStorage.getItem(CONSENT_KEY);
    return stored ? JSON.parse(stored) : null;
  }

  function shouldLoadTagManager(consent) {
    return !!(consent && (consent.functionality || consent.experience || consent.measurement || consent.marketing));
  }

  function ensureTagManagerLoaded() {
    if (gtmLoadPromise) return gtmLoadPromise;

    gtmLoadPromise = new Promise((resolve) => {
      const existing = document.querySelector(`script[src*="googletagmanager.com/gtm.js?id=${GTM_ID}"]`);
      if (existing) {
        resolve(true);
        return;
      }

      const script = document.createElement('script');
      script.async = true;
      script.src = `https://www.googletagmanager.com/gtm.js?id=${GTM_ID}`;
      script.onload = () => resolve(true);
      script.onerror = () => resolve(false);
      document.head.appendChild(script);
    });

    return gtmLoadPromise;
  }

  function initializeGoogleAnalytics() {
    const consent = getConsent();
    if (!consent || !consent.measurement) return Promise.resolve(false);
    if (window.gtag) return Promise.resolve(true);
    if (gaLoadPromise) return gaLoadPromise;

    gaLoadPromise = new Promise((resolve) => {
      const existing = document.querySelector(`script[src*="googletagmanager.com/gtag/js?id=${GA_ID}"]`);
      const finalize = () => {
        window.dataLayer = window.dataLayer || [];
        function gtag() {
          window.dataLayer.push(arguments);
        }
        gtag('js', new Date());
        gtag('config', GA_ID, {
          anonymize_ip: true,
          allow_google_signals: consent.marketing || false,
          allow_ad_personalization_signals: consent.marketing || false
        });
        window.gtag = gtag;
        resolve(true);
      };

      if (existing) {
        finalize();
        return;
      }

      const script = document.createElement('script');
      script.async = true;
      script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
      script.onload = finalize;
      script.onerror = () => resolve(false);
      document.head.appendChild(script);
    });

    return gaLoadPromise;
  }

  function updateGTMDataLayer(consent = getConsent()) {
    window.dataLayer = window.dataLayer || [];

    window.dataLayer.push({
      event: 'consent_update',
      consent: {
        necessary: consent ? consent.necessary : false,
        functionality: consent ? consent.functionality : false,
        experience: consent ? consent.experience : false,
        measurement: consent ? consent.measurement : false,
        marketing: consent ? consent.marketing : false
      },
      timestamp: consent ? consent.accepted_at : null
    });
  }

  function init() {
    window.dataLayer = window.dataLayer || [];
    const consent = getConsent();
    updateGTMDataLayer(consent);

    if (shouldLoadTagManager(consent)) {
      ensureTagManagerLoaded();
    }

    if (consent && consent.measurement) {
      initializeGoogleAnalytics();
    }
  }

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.vedtamUpdateGoogleConsent = function(consentData) {
    updateGTMDataLayer(consentData);

    if (shouldLoadTagManager(consentData)) {
      ensureTagManagerLoaded();
    }

    if (consentData.measurement && !window.gtag) {
      initializeGoogleAnalytics();
    }
  };
})();
