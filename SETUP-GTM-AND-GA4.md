# Complete Google Tag Manager & Google Analytics 4 Setup Guide

---

## Your Current Setup

| Item | Value |
|------|-------|
| **GTM Container ID** | GTM-TH898GVT |
| **GA4 Measurement ID** | G-E6BP31TD57 |
| **Search Console ID** | google6d4aaa76f30c4585 |
| **Website** | vedtam.com |

---

# PART 1: Google Tag Manager Configuration

## Step 1: Access Your GTM Container

### Go to Google Tag Manager
1. Open https://tagmanager.google.com
2. Sign in with your Google account
3. Click on your account -> Select Vedtam Tech Solutions workspace
4. Click on the GTM-TH898GVT container

Note: If you don't see your container, it may need to be created. Go to Step 2 below.

---

## Step 2: Create GTM Container (If Not Exists)

### Create New Container
1. Go to https://tagmanager.google.com
2. Click Create Account
3. Fill in:
   - Account Name: Vedtam Tech Solutions
   - Container Name: vedtam.com
   - Target Platform: Web
4. Click Create
5. Accept the Terms of Service
6. You'll get a Container ID like GTM-XXXXXX

Important: Your container ID in the code is GTM-TH898GVT - make sure it matches!

---

## Step 3: Verify GTM is Installed

### Check if GTM is Working
1. Open your website: https://vedtam.com (or localhost)
2. Press F12 (Open Developer Tools)
3. Go to Console tab
4. Type this command and press Enter:
```javascript
console.log(window.dataLayer)
```

Expected Output:
```javascript
[
  {event: 'gtm.js', 'gtm.start': 1717448400000},
  {
    event: 'consent_update',
    consent: {
      necessary: true,
      functionality: false,
      experience: false,
      measurement: false,
      marketing: false
    },
    timestamp: "2026-06-04T10:30:00Z"
  }
]
```

[OK] If you see this -> GTM is working!

---

## Step 4: Set Up Google Analytics 4 in GTM

### Create GA4 Tag

1. Go to your GTM container: https://tagmanager.google.com
2. Click on Tags (left sidebar)
3. Click New
4. Name: GA4 - Page View
5. Tag Configuration:
   - Click Tag Configuration box
   - Choose Google Analytics: GA4 Configuration
6. Measurement ID: Enter G-E6BP31TD57
7. Triggering:
   - Click in the Triggering section
   - Choose All Pages (this will create a trigger)
8. Click Save

Result: Now every page view sends data to Google Analytics

---

## Step 5: Add Consent Restriction to GA4

This ensures GA4 only fires when user accepts analytics cookies:

1. In your GA4 tag (from Step 4), scroll down
2. Find Advanced Settings -> User Consent Mode
3. Click Add Consent Requirement
4. For Consent Type: Select analytics or measurement
5. Value Required: yes
6. Click Save

What this does:
- [OK] GA4 only fires if user gave consent for measurement
- [OK] If user rejects -> GA4 won't load
- [OK] If user accepts later -> GA4 starts tracking

---

## Step 6: Create Consent Tag (Optional but Recommended)

This tells GTM about user consent choices:

1. Click Tags -> New
2. Name: Consent - Update GTM
3. Tag Configuration:
   - Choose Consent Mode
   - Configure these Consent Types:
     - analytics: denied (default)
     - ad_user_data: denied (default)
     - ad_personalization: denied (default)
4. Triggering:
   - Create a new trigger called "consent_update"
   - Trigger Type: Custom Event
   - Event Name: consent_update (this matches our code!)
5. Click Save

---

## Step 7: Preview & Debug

### Test Your GTM Setup

1. In GTM, click Preview (top right)
2. You'll see a banner: "Container in preview mode"
3. In a new tab, open your website: https://vedtam.com
4. You'll see Tag Assistant panel at bottom showing:
   - [OK] GTM-TH898GVT loaded
   - [OK] GA4 Configuration tag fired
   - [OK] Page View sent to GA4

What to look for:
```
GTM-TH898GVT loaded [OK]
GA4 Configuration (G-E6BP31TD57) [OK]
Google Analytics: GA4 Configuration fired [OK]
```

---

## Step 8: Publish Your Container

### Go Live

1. Click Submit (top right)
2. Add Version Name: "Initial GA4 Setup"
3. Add Version Description: "Configure GA4 and consent tracking"
4. Click Publish

Important: After publishing, it takes 5-15 minutes for changes to be live

---

# PART 2: Google Analytics 4 Configuration

## Step 1: Access Google Analytics 4

### Open GA4 Dashboard
1. Go to https://analytics.google.com
2. Sign in with your Google account
3. Select Vedtam Tech Solutions property
4. You'll see your GA4 dashboard

---

## Step 2: Verify Data is Coming In

### Check Real-Time Data

1. Click Reports (left sidebar)
2. Click Real-Time -> Overview
3. Open your website in a new tab: https://vedtam.com
4. In GA4, you should see:
   - [OK] 1 active user
   - [OK] Recent event: page_view
   - [OK] Event count increases as you browse

If no data appears:
- Wait 5-10 minutes (GA4 takes time to process)
- Check that user accepted "measurement" cookies
- Verify GTM container ID matches

---

## Step 3: Set Up Conversion Tracking

### Create Your First Conversion

1. In GA4, go to Admin (settings icon, bottom left)
2. Under Property, click Conversions
3. Click Create Conversion
4. Conversion Name: Contact Form Submission
5. Conversion Category: Choose relevant category
6. Event Name: Match a GTM event (we'll create this next)
7. Click Save

Example Events to Track:
- contact_form_submit - When user submits contact form
- download_resource - When user downloads a file
- video_play - When user plays a video
- purchase - When user makes a purchase

---

## Step 4: Add Custom Events to GTM

### Create Event Tag (Example: Contact Form)

1. Go back to GTM: https://tagmanager.google.com
2. Click Tags -> New
3. Name: Event - Contact Form Submit
4. Tag Configuration:
   - Choose Google Analytics: GA4 Event
   - Measurement ID: G-E6BP31TD57
   - Event Name: contact_form_submit
   - User Properties:
     - Property Name: form_type
     - Value: contact
5. Triggering:
   - Create new trigger: "Contact Form Submit"
   - Trigger Type: Form Submission
   - This trigger fires on: Form ID = "contact-form" (match your form ID)
6. Click Save

---

## Step 5: Set Up Google Ads Conversion Tracking (Optional)

### Link GA4 to Google Ads

1. In GA4, go to Admin -> Google Ads Links
2. Click Link Google Ads Account
3. Select your Google Ads account
4. Choose conversions to sync (recommended: all)
5. Click Link

This allows you to see which ads drive conversions

---

## Step 6: Verify Search Console Integration

### Verify Domain Ownership

1. Go to https://search.google.com/search-console
2. Click +Add Property
3. Enter your domain: vedtam.com
4. Google will detect the meta tag on your pages
5. Click Verify

[OK] Your site is now verified and Google can see your pages

---

# PART 3: Test Consent Flow

## Test Scenario 1: User Accepts All

### Step-by-Step Test

1. Clear browser data:
   - Press F12
   - DevTools -> Application
   - Cookies -> Delete all cookies for vedtam.com
   - Local Storage -> Delete all entries
   - Session Storage -> Delete all entries

2. Refresh page
   - You should see the cookie popup

3. Click "Accept Everything"
   - Popup closes
   - Check cookies:
     - vedtam_necessary = 1 [OK]
     - vedtam_measurement = 1 [OK]
     - vedtam_marketing = 1 [OK]

4. Check GTM:
   - Open DevTools -> Network tab
   - Look for requests to:
     - google-analytics.com [OK]
     - googletagmanager.com [OK]
     - These mean tracking is active

5. Check GA4 Real-Time:
   - Open GA4: https://analytics.google.com
   - Go to Reports -> Real-Time
   - You should appear as an active user

---

## Test Scenario 2: User Rejects All

### Step-by-Step Test

1. Clear browser data again (same as above)
2. Refresh page
3. Click "Reject Everything"
   - Popup closes
   - Check cookies:
     - vedtam_necessary = 1 [OK]
     - vedtam_measurement = 0 [NO - tracking disabled]
     - vedtam_marketing = 0 [NO]

4. Check GTM Network:
   - DevTools -> Network
   - You should NOT see requests to google-analytics.com
   - GTM still loads, but GA4 doesn't fire

---

## Test Scenario 3: User Changes Mind

### Accept After Rejecting

1. After rejecting (from Test 2):
2. Open DevTools Console:
   ```javascript
   // Clear the stored consent
   localStorage.removeItem('vedtam_cookie_consent');
   // Refresh
   location.reload();
   ```

3. Click "Accept Everything" on new popup
4. Check GA4:
   - GA4 should now start tracking
   - May take 5-10 minutes to appear in reports

---

# PART 4: Monitor & Maintain

## Weekly Checklist

- [ ] Check GA4 Real-Time dashboard for active users
- [ ] Review conversion goals in GA4
- [ ] Check Search Console for crawl errors
- [ ] Monitor page views and bounce rates

## Monthly Checklist

- [ ] Review top pages and user flow
- [ ] Check conversion rates by source
- [ ] Analyze user demographics in GA4
- [ ] Check GTM for any tag errors

## Quarterly Review

- [ ] Export GA4 reports for analysis
- [ ] Optimize underperforming pages
- [ ] Update conversion goals
- [ ] Review marketing ROI

---

# PART 5: Troubleshooting

## Problem: GA4 Not Showing Data

### Solutions:
1. Wait 24 hours - GA4 can take 12-24 hours for initial data
2. Check cookie consent - User must accept "measurement" cookies
3. Verify GA4 ID - Should be G-E6BP31TD57 (check for typos)
4. Check GTM container - Go to GTM > Preview, browse site
5. Check browser console - Press F12, look for errors in Console tab

---

## Problem: GTM Not Loading

### Solutions:
1. Clear cache - Press Ctrl+Shift+Delete, clear cache
2. Check GTM ID - Should be GTM-TH898GVT in HTML code
3. Verify script placement - Should be in <head> tag (check in DevTools)
4. Check for errors - Press F12, go to Console, look for red errors

---

## Problem: Consent Not Working

### Solutions:
1. Check localStorage - DevTools > Application > Local Storage
2. Verify cookie names - Should be vedtam_* (check spelling)
3. Check cookie banner script - Should have loaded with page
4. Test in incognito - Open site in incognito mode (clears cookies)

---

# Quick Reference

## Important Links

- GTM Dashboard: https://tagmanager.google.com
- GA4 Dashboard: https://analytics.google.com
- Search Console: https://search.google.com/search-console
- Your Website: https://vedtam.com

## Key IDs (Save These!)

```
Container ID:      GTM-TH898GVT
GA4 Measurement:   G-E6BP31TD57
Search Console:    google6d4aaa76f30c4585
```

## File Locations

```
assets/js/cookie-banner.js          <- Consent popup
assets/js/google-integrations.js    <- GA4 loader
```

---

# Summary

You now have:
[OK] Google Tag Manager is installed on all pages
[OK] Google Analytics 4 is tracking visitors
[OK] Consent is respected (GA4 only loads if accepted)
[OK] Real-time data is flowing into your GA4 dashboard
[OK] Data will be fully processed in 24 hours

**Next Actions:**
1. Go to GTM and create GA4 tag (Step 4 above)
2. Publish the container
3. Test with cookie acceptance
4. Monitor GA4 for data after 24 hours

Need help with any specific step? Let me know!
