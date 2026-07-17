# Google Integration Setup - Complete Documentation

## Overview
Your website now has a complete Google integration system that respects user cookie consent:
- **Google Tag Manager (GTM)** - Central tag management system
- **Google Analytics (GA4)** - Visitor tracking and analytics
- **Google Search Console** - Site verification and SEO monitoring

---

## How It Works

### 1. Cookie Consent Flow
```
User arrives -> Cookie Popup Shows -> User selects preferences
                                  |
         User clicks "Accept All" -> Cookies set -> Google scripts load
              OR
         User clicks "Reject All" -> Only necessary cookies -> GA/GTM disabled
```

### 2. Cookie Types Set
The following cookies are set on the visitor's system:
- vedtam_necessary - Always enabled (required for site function)
- vedtam_functionality - User preference (for enhanced features)
- vedtam_experience - User preference (for user experience)
- vedtam_measurement - User preference (enables Google Analytics)
- vedtam_marketing - User preference (enables marketing tracking)

### 3. Google Scripts
All 34 pages have:
- **GTM Head Script** - Loads in <head> (runs before page content)
- **GTM Noscript** - Fallback for users with JavaScript disabled
- **Google Integrations JS** - Conditionally loads GA based on consent
- **Search Console Verification** - Meta tag for site verification

---

## What Gets Tracked

### If User Accepts Everything:
- [YES] Google Analytics (GA4) tracks all visitor behavior
- [YES] GTM can track custom events and conversions
- [YES] Marketing pixels can track user actions
- [YES] Full user ID tracking enabled

### If User Only Accepts Necessary:
- [YES] Site functionality works (no impact)
- [NO] Google Analytics disabled
- [NO] Marketing tracking disabled
- [NO] Advanced personalization disabled

---

## Configuration IDs

| Service | ID | Location |
|---------|----|----|
| Google Analytics | G-E6BP31TD57 | google-integrations.js |
| Google Tag Manager | GTM-TH898GVT | All HTML pages |
| Search Console | google6d4aaa76f30c4585 | All HTML pages |

---

## File Structure

```
assets/
  js/
    ├── cookie-banner.js          <- Cookie consent popup
    └── google-integrations.js     <- GA4 + consent management
```

### cookie-banner.js
- Displays the consent popup
- Sets actual browser cookies (vedtam_*)
- Stores consent in localStorage
- Calls google-integrations.js when consent changes

### google-integrations.js
- Loads Google Analytics IF measurement consent given
- Updates GTM's dataLayer with consent status
- Handles consent updates dynamically
- Respects user privacy choices

---

## On All Pages (34 total)

### In <head>:
```
<!-- Google Tag Manager -->
<script>...GTM script...</script>
<!-- End Google Tag Manager -->

<!-- Search Console Verification -->
<meta name="google-site-verification" content="google6d4aaa76f30c4585.html" />

<!-- Google Integrations (GA4 + Consent) -->
<script src="assets/js/google-integrations.js"></script>
```

### In <body> (right after opening tag):
```
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="..."></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
```

---

## How GTM Works

1. **GTM loads on every page** (regardless of consent)
2. **Inside GTM container**, you can set up rules like:
   - "Only fire Google Analytics if vedtam_measurement cookie = 1"
   - "Only track purchases if vedtam_marketing cookie = 1"
   - "Always track page views (necessary cookies)"

3. **Consent data passed to GTM via dataLayer:**
```javascript
{
  necessary: true/false,
  functionality: true/false,
  experience: true/false,
  measurement: true/false,
  marketing: true/false,
  timestamp: "2026-06-04T..."
}
```

---

## Testing

### Test 1: Fresh Visit (Should Show Popup)
1. Clear browser localStorage + cookies
2. Open any page
3. Cookie popup should appear

### Test 2: Accept All
1. Click "Accept Everything"
2. Refresh page -> Popup should NOT appear
3. In DevTools -> Application -> Cookies -> Check vedtam_* cookies exist
4. Google Analytics should load (check Network tab for GA requests)

### Test 3: Reject All
1. Clear cookies again
2. Click "Reject Everything"
3. Check cookies -> only vedtam_necessary=0 should be set
4. Google Analytics should NOT load

### Test 4: Google Search Console
1. Go to https://search.google.com/search-console
2. Add your domain
3. Google should recognize the meta tag verification

---

## How User Consent Flows Through System

```
Cookie Popup Shown
    |
User Clicks "Accept All"
    |
cookie-banner.js sets cookies + localStorage
    |
Calls: window.vedtamUpdateGoogleConsent(consentData)
    |
google-integrations.js receives consent
    |
Updates GTM's dataLayer with consent status
    |
Loads Google Analytics (GA4)
    |
GTM can now use consent status for tag firing rules
```

---

## Important Notes

1. **Consent expires after 365 days** - Users will see popup again after 1 year
2. **Cookies are HttpOnly Safe** - Set with SameSite=Lax for security
3. **All scripts are async** - Won't block page loading
4. **GDPR Compliant** - Users can reject, preferences are respected
5. **Search Console meta tag** - Helps Google find your site

---

## Next Steps (Optional)

If you want to customize further:

1. **In GTM Dashboard:**
   - Set up custom events (button clicks, form submissions, etc.)
   - Create conversion tracking
   - Add custom dimensions/metrics

2. **In Google Analytics 4:**
   - Set up goals/conversions
   - View user behavior reports
   - Export data to Google Ads

3. **Modify Consent:**
   - Change cookie expiration in cookie-banner.js
   - Add more cookie types if needed

---

## Support

If GA4/GTM don't show data after 24 hours:
1. Check that user actually accepted tracking
2. Verify GA ID is correct: G-E6BP31TD57
3. Check GTM ID is correct: GTM-TH898GVT
4. Use Google Analytics Debugger Chrome extension to verify events
