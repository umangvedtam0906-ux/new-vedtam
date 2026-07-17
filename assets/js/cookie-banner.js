// Cookie Consent Popup - Premium Design with Toggle Switches
(function() {
  const COOKIE_CONSENT_KEY = 'vedtam_cookie_consent';

  function getCookieConsent() {
    const cookie = localStorage.getItem(COOKIE_CONSENT_KEY);
    return cookie ? JSON.parse(cookie) : null;
  }

  function setCookieConsent(consent) {
    const consentData = {
      ...consent,
      timestamp: new Date().getTime()
    };

    // Store in localStorage
    localStorage.setItem(COOKIE_CONSENT_KEY, JSON.stringify(consentData));

    // Set actual cookies
    setCookie('vedtam_necessary', consent.necessary ? '1' : '0', 365);
    setCookie('vedtam_functionality', consent.functionality ? '1' : '0', 365);
    setCookie('vedtam_experience', consent.experience ? '1' : '0', 365);
    setCookie('vedtam_measurement', consent.measurement ? '1' : '0', 365);
    setCookie('vedtam_marketing', consent.marketing ? '1' : '0', 365);

    // Update Google integrations
    if (window.vedtamUpdateGoogleConsent) {
      window.vedtamUpdateGoogleConsent(consentData);
    }
  }

  function setCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = 'expires=' + date.toUTCString();
    document.cookie = name + '=' + value + ';' + expires + ';path=/;SameSite=Lax';
  }

  function disableScroll() {
    document.documentElement.style.overflow = 'hidden';
    document.body.style.overflow = 'hidden';
  }

  function enableScroll() {
    document.documentElement.style.overflow = 'auto';
    document.body.style.overflow = 'auto';
  }

  function createPopup() {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.id = 'vedtam-cookie-overlay';

    // Create popup
    const popup = document.createElement('div');
    popup.id = 'vedtam-cookie-popup';
    popup.setAttribute('role', 'dialog');
    popup.setAttribute('aria-labelledby', 'cookie-popup-title');
    popup.setAttribute('aria-modal', 'true');
    popup.innerHTML = `
      <div class="cookie-popup-inner">
        <button id="cookie-close-btn" class="cookie-close-btn" aria-label="Close cookie preferences">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>

        <h2 id="cookie-popup-title" class="cookie-popup-title">Information</h2>

        <div class="cookie-popup-description">
          <p>We and selected third parties use cookies or similar technologies for technical purposes and, with your consent, also for the purposes of functionality, experience, measurement and marketing (with personalized ads) as specified in the <a href="/privacy-policy.html" class="cookie-policy-link">Cookie Policy</a>. Refusal of consent may render the relevant functions unavailable.</p>
          <p>You can freely give, refuse or withdraw your consent, at any time.<br>
          use the "Accept All" button to consent, use the "Reject All" button or close this policy to continue without accepting.</p>
        </div>

        <div class="cookie-toggles">
          <div class="cookie-toggle-item">
            <span class="cookie-toggle-text">Necessary</span>
            <label class="cookie-toggle-label">
              <input type="checkbox" id="cookie-necessary" class="cookie-toggle-input" checked disabled>
              <span class="cookie-toggle-switch">
                <span class="cookie-toggle-knob"></span>
              </span>
            </label>
          </div>

          <div class="cookie-toggle-item">
            <span class="cookie-toggle-text">Functionality</span>
            <label class="cookie-toggle-label">
              <input type="checkbox" id="cookie-functionality" class="cookie-toggle-input">
              <span class="cookie-toggle-switch">
                <span class="cookie-toggle-knob"></span>
              </span>
            </label>
          </div>

          <div class="cookie-toggle-item">
            <span class="cookie-toggle-text">Experience</span>
            <label class="cookie-toggle-label">
              <input type="checkbox" id="cookie-experience" class="cookie-toggle-input">
              <span class="cookie-toggle-switch">
                <span class="cookie-toggle-knob"></span>
              </span>
            </label>
          </div>

          <div class="cookie-toggle-item">
            <span class="cookie-toggle-text">Measurement</span>
            <label class="cookie-toggle-label">
              <input type="checkbox" id="cookie-measurement" class="cookie-toggle-input">
              <span class="cookie-toggle-switch">
                <span class="cookie-toggle-knob"></span>
              </span>
            </label>
          </div>

          <div class="cookie-toggle-item">
            <span class="cookie-toggle-text">Marketing</span>
            <label class="cookie-toggle-label">
              <input type="checkbox" id="cookie-marketing" class="cookie-toggle-input">
              <span class="cookie-toggle-switch">
                <span class="cookie-toggle-knob"></span>
              </span>
            </label>
          </div>
        </div>

        <div class="cookie-popup-actions">
          <button id="cookie-reject-all" class="cookie-action-btn cookie-action-btn-secondary" type="button">
            Reject Everything
          </button>
          <button id="cookie-accept-all" class="cookie-action-btn cookie-action-btn-primary" type="button">
            Accept Everything
          </button>
        </div>
      </div>
    `;

    return { overlay, popup };
  }

  function addStyles() {
    const style = document.createElement('style');
    style.textContent = `
      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }

      @keyframes popupSlideIn {
        from {
          opacity: 0;
          transform: translate(-50%, -50%) scale(0.95);
        }
        to {
          opacity: 1;
          transform: translate(-50%, -50%) scale(1);
        }
      }

      #vedtam-cookie-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.75);
        z-index: 9998;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: fadeIn 0.3s ease-out;
      }

      #vedtam-cookie-popup {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999;
        max-width: 650px;
        width: 90%;
        max-height: 90vh;
        overflow-y: auto;
        animation: popupSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
      }

      .cookie-popup-inner {
        background: linear-gradient(135deg, #3d3561 0%, #2d2545 100%);
        border-radius: 16px;
        padding: 32px;
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
        position: relative;
        border: 1px solid rgba(255, 255, 255, 0.1);
      }

      .cookie-close-btn {
        position: absolute;
        top: 20px;
        right: 20px;
        background: transparent;
        border: none;
        color: #cbd5e1;
        cursor: pointer;
        padding: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 6px;
        transition: all 0.2s ease;
      }

      .cookie-close-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        color: #f1f5f9;
      }

      .cookie-popup-title {
        margin: 0 0 20px 0;
        font-size: 1.5rem;
        font-weight: 700;
        color: #f8fafc;
      }

      .cookie-popup-description {
        margin-bottom: 24px;
        font-size: 0.9rem;
        line-height: 1.6;
        color: #cbd5e1;
      }

      .cookie-popup-description p {
        margin: 0 0 10px 0;
      }

      .cookie-popup-description p:last-child {
        margin-bottom: 0;
      }

      .cookie-policy-link {
        color: #fb923c;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.2s ease;
      }

      .cookie-policy-link:hover {
        color: #fdba74;
        text-decoration: underline;
      }

      .cookie-toggles {
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-bottom: 24px;
        padding: 16px 0;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      }

      .cookie-toggle-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .cookie-toggle-text {
        color: #e2e8f0;
        font-weight: 500;
        font-size: 0.95rem;
      }

      .cookie-toggle-label {
        display: flex;
        align-items: center;
        cursor: pointer;
      }

      .cookie-toggle-input {
        display: none;
      }

      .cookie-toggle-switch {
        position: relative;
        display: inline-block;
        width: 48px;
        height: 26px;
        background: #475569;
        border-radius: 999px;
        transition: background 0.3s ease;
        margin-left: 10px;
      }

      .cookie-toggle-knob {
        position: absolute;
        top: 3px;
        left: 3px;
        width: 20px;
        height: 20px;
        background: #fff;
        border-radius: 50%;
        transition: transform 0.3s ease;
      }

      .cookie-toggle-input:checked + .cookie-toggle-switch {
        background: #7c3aed;
      }

      .cookie-toggle-input:checked + .cookie-toggle-switch .cookie-toggle-knob {
        transform: translateX(22px);
      }

      .cookie-toggle-input:disabled + .cookie-toggle-switch {
        opacity: 1;
        cursor: not-allowed;
      }

      .cookie-popup-actions {
        display: flex;
        gap: 12px;
        justify-content: flex-end;
      }

      .cookie-action-btn {
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        text-decoration: none;
        display: inline-block;
        white-space: nowrap;
      }

      .cookie-action-btn:hover {
        transform: translateY(-2px);
      }

      .cookie-action-btn:active {
        transform: translateY(0);
      }

      .cookie-action-btn-primary {
        background: linear-gradient(135deg, #fb923c 0%, #f97316 100%);
        color: #fff;
        box-shadow: 0 6px 20px rgba(251, 146, 60, 0.3);
      }

      .cookie-action-btn-primary:hover {
        box-shadow: 0 8px 24px rgba(251, 146, 60, 0.4);
      }

      .cookie-action-btn-secondary {
        background: transparent;
        color: #cbd5e1;
        border: 2px solid #475569;
      }

      .cookie-action-btn-secondary:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: #64748b;
      }

      @media (max-width: 640px) {
        .cookie-popup-inner {
          padding: 24px 20px;
        }

        .cookie-popup-title {
          font-size: 1.3rem;
          margin-bottom: 16px;
        }

        .cookie-popup-description {
          font-size: 0.85rem;
          margin-bottom: 20px;
        }

        .cookie-toggles {
          margin-bottom: 20px;
          padding: 12px 0;
          gap: 10px;
        }

        .cookie-popup-actions {
          flex-direction: column;
          gap: 10px;
        }

        .cookie-action-btn {
          width: 100%;
          text-align: center;
        }
      }

      ::-webkit-scrollbar {
        width: 6px;
      }

      ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
      }

      ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 3px;
      }

      ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
      }
    `;
    document.head.appendChild(style);
  }

  function showPopup() {
    addStyles();

    const { overlay, popup } = createPopup();
    document.body.appendChild(overlay);
    document.body.appendChild(popup);

    // Disable page scroll
    disableScroll();

    // Get toggle elements
    const toggles = {
      necessary: document.getElementById('cookie-necessary'),
      functionality: document.getElementById('cookie-functionality'),
      experience: document.getElementById('cookie-experience'),
      measurement: document.getElementById('cookie-measurement'),
      marketing: document.getElementById('cookie-marketing')
    };

    // Handle Accept All
    document.getElementById('cookie-accept-all').addEventListener('click', function() {
      setCookieConsent({
        necessary: true,
        functionality: true,
        experience: true,
        measurement: true,
        marketing: true,
        accepted_at: new Date().toISOString()
      });
      overlay.remove();
      popup.remove();
      enableScroll();
    });

    // Handle Reject All
    document.getElementById('cookie-reject-all').addEventListener('click', function() {
      setCookieConsent({
        necessary: true,
        functionality: false,
        experience: false,
        measurement: false,
        marketing: false,
        accepted_at: new Date().toISOString()
      });
      overlay.remove();
      popup.remove();
      enableScroll();
    });

    // Handle Close Button
    document.getElementById('cookie-close-btn').addEventListener('click', function() {
      setCookieConsent({
        necessary: toggles.necessary.checked,
        functionality: toggles.functionality.checked,
        experience: toggles.experience.checked,
        measurement: toggles.measurement.checked,
        marketing: toggles.marketing.checked,
        accepted_at: new Date().toISOString()
      });
      overlay.remove();
      popup.remove();
      enableScroll();
    });

    // Prevent closing by clicking overlay
    overlay.addEventListener('click', function(e) {
      if (e.target === overlay) {
        e.preventDefault();
      }
    });

    // Prevent keyboard escape
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        e.preventDefault();
      }
    });
  }

  function init() {
    const consent = getCookieConsent();
    const schedulePopup = () => {
      if ('requestIdleCallback' in window) {
        window.requestIdleCallback(showPopup, { timeout: 1500 });
      } else {
        window.setTimeout(showPopup, 700);
      }
    };

    // Show popup only if user hasn't made a choice
    if (!consent) {
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', schedulePopup, { once: true });
      } else {
        schedulePopup();
      }
    }
  }

  // Initialize
  init();
})();
