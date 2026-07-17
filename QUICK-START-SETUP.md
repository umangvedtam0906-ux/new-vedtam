# QUICK START: Google Tag Manager & GA4 Setup

---

## YOUR IDs (Write These Down!)

```
GTM Container ID:    GTM-TH898GVT
GA4 Measurement ID:  G-E6BP31TD57
Search Console:      google6d4aaa76f30c4585
```

---

## STEP 1: GO TO GOOGLE TAG MANAGER

1. Open browser: Chrome
2. Go to: https://tagmanager.google.com
3. Sign in with your Google account
4. Click container: GTM-TH898GVT

---

## STEP 2: CREATE GA4 TAG

1. In left menu, click: **Tags**
2. Click blue **[New]** button (top right)
3. In "Tag Name" field, type: GA4 - Page View
4. Click "Tag Configuration" box
5. From dropdown, select: Google Analytics: GA4 Configuration
6. In "Measurement ID" field, enter: G-E6BP31TD57

---

## STEP 3: SET UP TRIGGERING

1. Scroll down to "Triggering" section
2. Click the Triggering box
3. From list, click: All Pages
4. Click **[Save]** button (bottom right)

---

## STEP 4: ADD CONSENT REQUIREMENT

1. Click **[Edit]** on the GA4 tag you just created
2. Scroll down to "Advanced Settings"
3. Expand "Advanced Settings" by clicking arrow
4. Find "User Consent Mode" section
5. Check box: "Add Consent Requirements"
6. Click **[+ Add Consent Requirement]**
7. Select: analytics
8. Set "Value Required" to: Yes
9. Click **[Save]** button

---

## STEP 5: PREVIEW YOUR SETUP

1. At top of GTM page, click: **[Preview]** button
2. Open new browser tab
3. Go to: https://vedtam.com (or localhost)
4. You should see cookie popup
5. Click **[Accept Everything]** button
6. Look at bottom right - you should see Tag Assistant showing:
   - GTM-TH898GVT [Loaded]
   - GA4 Configuration [Fired]

---

## STEP 6: PUBLISH

1. Go back to GTM tab
2. Click **[Submit]** button (top right)
3. For "Version Name" enter: Initial GA4 Setup v1
4. For "Version Description" enter: Configure GA4 and consent
5. Click **[Publish]** button
6. Wait for success message

---

## STEP 7: VERIFY IN GOOGLE ANALYTICS

1. Open new tab: https://analytics.google.com
2. Sign in with Google account
3. Click your property: Vedtam Website
4. In left menu, click: **Reports**
5. Click: **Real-Time** then **Overview**
6. Open your website in another tab
7. You should see "1" active user in GA4
8. Click around your website - you should see events increase

---

## WHAT TO LOOK FOR

SUCCESS SIGNS:
- Cookie popup appears when you first visit
- Tag Assistant shows green [Loaded] and [Fired] messages
- GA4 Real-Time dashboard shows you as active user
- Network tab (F12) shows requests to google-analytics.com

ISSUES TO FIX:
- No Tag Assistant? Wait 5-10 minutes, browser may need cache clear
- No GA data? Make sure you clicked "Accept Everything"
- No consent popup? Clear browser cookies and localStorage
- Wrong ID? Double-check: G-E6BP31TD57 (not G-XXXXX)

---

## TIMELINE

TODAY: Set up GTM and GA4 (30 minutes)
24 HOURS LATER: Check GA4 for full data and reports

---

## NEED HELP?

See these detailed guides:
- GOOGLE-INTEGRATION-SETUP.md - Overview of how system works
- SETUP-GTM-AND-GA4.md - Complete step-by-step instructions
- DETAILED-SETUP-GUIDE.md - Visual ASCII diagrams of each screen

---

## QUICK REFERENCE

GTM Dashboard:     https://tagmanager.google.com
GA4 Dashboard:     https://analytics.google.com
Your Website:      https://vedtam.com
Search Console:    https://search.google.com/search-console

---

## COMMON MISTAKES

1. Forgetting to click [Save] button - FIX: Always click Save after each step
2. Wrong Measurement ID - FIX: Use G-E6BP31TD57 (not G-XXXXX)
3. Not accepting cookies - FIX: Must click "Accept Everything" for GA4 to track
4. Not publishing changes - FIX: Always click [Submit] then [Publish]
5. Checking GA4 too soon - FIX: Wait 24 hours for full data

---

READY? Start with STEP 1 above!
