/**
 * update-cert-data.mjs
 * ─────────────────────────────────────────────────────────────────────────────
 * Fetches 2026 vulnerability notes & advisories from the official CERT-In
 * portal and saves full detail data to cert-data.json.
 *
 * Fields captured per advisory:
 *   title, severity, date, link, code, summary,
 *   softwareAffected (HTML string), targetAudience, riskAssessment,
 *   impactAssessment, cves[], solutionLinks[]
 *
 * Runs silently via Windows Task Scheduler (wscript.exe + vbs launcher).
 * No CMD window / no popup ever shown to the user.
 * ─────────────────────────────────────────────────────────────────────────────
 */

import { writeFile, readFile } from "node:fs/promises";
import { existsSync } from "node:fs";

const HOME_URL = "https://www.cert-in.org.in/";
const PORTAL_URL = "https://www.cert-in.org.in/s2cMainServlet?pageid=PUBWEL01";
const ADV_LIST_URL = "https://www.cert-in.org.in/s2cMainServlet?pageid=PUBADVLIST";
const BHARAT_PORTAL_URL = "https://xn----1td4etbxb9bwj.xn--h2brj9c/s2cMainServlet?pageid=PUBWEL01";
const DEFAULT_OUTPUT_FILE = "cert-data.json";
const DEFAULT_MAX_ENTRIES = 1000;
const DEFAULT_YEAR = String(new Date().getFullYear());

const OUTPUT_FILE = process.env.CERT_OUTPUT_FILE || DEFAULT_OUTPUT_FILE;
const YEAR_FILTER = process.env.CERT_YEAR || DEFAULT_YEAR;
const MAX_ENTRIES = Number(process.env.CERT_MAX_ENTRIES || DEFAULT_MAX_ENTRIES);
const ARCHIVE_URL = `https://www.cert-in.org.in/s2cMainServlet?pageid=VLNLIST02&year=${YEAR_FILTER}`;
const ADV_ARCHIVE_URL = `https://www.cert-in.org.in/s2cMainServlet?pageid=PUBADVLIST02&year=${YEAR_FILTER}`;
const BHARAT_ARCHIVE_URL = `https://xn----1td4etbxb9bwj.xn--h2brj9c/s2cMainServlet?pageid=VLNLIST02&year=${YEAR_FILTER}`;

// ─── HTML utility ─────────────────────────────────────────────────────────────

function cleanHtmlToText(html) {
  let clean = html
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<\/?(?:div|p|br|h[1-6]|tr)[\s\S]*?>/gi, "\n")
    .replace(/<\/?li[\s\S]*?>/gi, "\n• ")
    .replace(/<[^>]+>/g, "")
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/gi, "'")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">")
    .replace(/\r\n/g, "\n")
    .replace(/\n{2,}/g, "\n")
    .trim();
  return clean;
}

function normalizeUrl(raw, base = HOME_URL) {
  try { return new URL(raw, base).toString(); }
  catch { return null; }
}

// ─── Field parsers ─────────────────────────────────────────────────────────────

function parseCode(url) {
  const m = url.match(/(?:VLCODE|CACODE)=([A-Z0-9-]+)/i);
  return m ? m[1] : null;
}

function parseSeverity(text) {
  const m1 = text.match(/Severity\s+Rating\s*:\s*(Critical|High|Medium|Low)/i);
  if (m1) return m1[1].toLowerCase();
  const m2 = text.match(/Risk\s+Assessment\s*:\s*(?:High|Critical)\s+risk/i);
  if (m2) return m2[0].toLowerCase().includes("critical") ? "critical" : "high";
  if (/CICA-\d{4}-/i.test(text)) return "high";
  return "high";
}

function parseDate(text) {
  // Try Primary format
  const m = text.match(/Original\s+Issue\s+Date\s*:?\s*([A-Za-z]+\s+\d{1,2},?\s+\d{4})/i);
  if (m) {
    const cleaned = m[1].replace(/\s*,\s*/, ", ");
    const parsed = new Date(cleaned);
    if (!Number.isNaN(parsed.getTime())) {
      const y = parsed.getFullYear();
      const mo = String(parsed.getMonth() + 1).padStart(2, '0');
      const d = String(parsed.getDate()).padStart(2, '0');
      return `${y}-${mo}-${d}`;
    }
  }
  // Fallback: Just look for a date-like string near the top
  const m2 = text.match(/([A-Za-z]+\s+\d{1,2},?\s+\d{4})/i);
  if (m2) {
    const parsed = new Date(m2[1]);
    if (!Number.isNaN(parsed.getTime())) {
      const y = parsed.getFullYear();
      const mo = String(parsed.getMonth() + 1).padStart(2, '0');
      const d = String(parsed.getDate()).padStart(2, '0');
      return `${y}-${mo}-${d}`;
    }
  }
  return null;
}

function parseTitle(text) {
  const m1 = text.match(
    /CERT-In\s+(?:Vulnerability\s+Note|Advisory)\s+[A-Z0-9-]+\s+(.+?)(?=\s+Original\s+Issue\s+Date:)/i
  );
  if (m1) return m1[1].trim();
  const m2 = text.match(
    /(?:^|[\r\n])([A-Z][^.!?]{15,180})[\s\r\n]*Original\s+Issue\s+Date/i
  );
  if (m2) return m2[1].trim();
  return null;
}

function parseSummary(text) {
  const m = text.match(/Overview\s+(.{40,600}?)(?=\s+(?:Target Audience|Risk Assessment|Description|Solution|References|$))/i);
  return m ? m[1].trim() : null;
}

function parseSoftwareAffected(text) {
  const m = text.match(
    /Software Affected([\s\S]+?)(?=Overview|Target Audience|Description|Risk Assessment)/i
  );
  if (!m) return "";
  let block = m[1].trim();
  if (block.startsWith("• ")) block = block.substring(2);
  // Split on bullets, clean empty lines
  const items = block.split(/\n•/g).map(s => s.replace(/\n/g, ' ').replace(/\s+/g, ' ').trim()).filter(Boolean);
  return items;
}

function parseField(text, label) {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const pattern = new RegExp(
    `${escaped}\\s*:?\\s*([\\s\\S]+?)(?=\\s*(?:Target Audience|Risk Assessment|Impact Assessment|Description|Solution|Vendor Information|References|Software Affected|Overview|$))`,
    "i"
  );
  const m = text.match(pattern);
  return m ? m[1].replace(/\n/g, ' ').replace(/\s+/g, " ").trim() : null;
}

function parseCves(text) {
  const pattern = /CVE-\d{4}-\d{4,7}/gi;
  const found = text.match(pattern) || [];
  return [...new Set(found)];
}

function parseSolutionLinks(html) {
  const match = html.match(/(?:Vendor Information|References)([\s\S]*?)Disclaimer/i);
  if (!match) return [];
  const links = match[1].match(/(http|https):\/\/[^\s<"']+/gi) || [];
  const valid = links
    .map(normalizeUrl)
    .filter(l => l && !l.includes('cve.org') && !l.includes('cve.mitre.org'));
  return [...new Set(valid)].slice(0, 8);
}

// ─── Network ──────────────────────────────────────────────────────────────────

let sessionCookie = null;

async function initSession() {
  try {
    console.log(`[cert-updater] Initializing session with ${HOME_URL}`);
    const res = await fetch(HOME_URL, {
      headers: {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      },
      signal: AbortSignal.timeout(20_000)
    });
    if (res.ok) {
      const setCookie = res.headers.get("set-cookie");
      if (setCookie) {
        const match = setCookie.match(/JSESSIONID=([^;]+)/);
        if (match) {
          sessionCookie = `JSESSIONID=${match[1]}`;
          console.log(`[cert-updater] Session cookie established: ${sessionCookie}`);
        }
      }
    }
  } catch (e) {
    console.warn(`[cert-updater] Warning: could not initialize session: ${e.message}`);
  }
}

async function fetchText(url, retries = 2, depth = 0) {
  if (depth > 3) return { html: "" };
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const referer = depth === 0 ? HOME_URL : url;
      const headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "referer": referer
      };
      if (sessionCookie) {
        headers["cookie"] = sessionCookie;
      }
      const res = await fetch(url, {
        headers,
        signal: AbortSignal.timeout(20_000)
      });
      if (!res.ok) return { html: "" };
      let text = await res.text();
      
      if (text.includes("<frameset")) {
        const frames = [...text.matchAll(/<frame[^>]+src=["']([^"']+)["']/gi)];
        const mainFrame = frames.find(f => f[1] && !f[1].includes("about:blank"));
        if (mainFrame) {
          const frameUrl = new URL(mainFrame[1], url).toString();
          return await fetchText(frameUrl, retries, depth + 1);
        }
      }
      return { html: text, url };
    } catch (e) {
      if (attempt === retries) return { html: "" };
      await new Promise(r => setTimeout(r, 1000 * (attempt + 1)));
    }
  }
  return { html: "" };
}


// ─── URL collection ────────────────────────────────────────────────────────────

async function collectAdvisoryUrls() {
  const sources = [
    PORTAL_URL,
    ARCHIVE_URL,
    ADV_ARCHIVE_URL,
    ADV_LIST_URL,
    BHARAT_PORTAL_URL,
    BHARAT_ARCHIVE_URL
  ];
  const urls = [];

  // Combined pattern: specific servlet links + any link containing the code
  const urlPattern = new RegExp(
    `(?:href|HREF)\\s*=\\s*["']([^"']*(?:s2cMainServlet\\?[^"']*(?:CIVN|CIAD|CICA)-${YEAR_FILTER}-|(?:CIVN|CIAD|CICA)-${YEAR_FILTER}-)[^"']+)["']`,
    "gi"
  );
  const jsPattern = new RegExp(
    `callPage\\s*\\(\\s*['"](VulnerabilityNote|Advisory|CurrentActivities)['"]\\s*,\\s*['"]((?:CIVN|CIAD|CICA)-${YEAR_FILTER}-[^'"]+)['"]\\s*\\)`,
    "gi"
  );
  const codePattern = new RegExp(`(?:CIVN|CIAD|CICA)-${YEAR_FILTER}-\\d{4}`, "gi");

  for (const src of sources) {
    try {
      const { html } = await fetchText(src);
      console.log(`[cert-updater] Fetched ${src}: ${html.length} chars`);
      
      // 1. Match direct URLs
      let match;
      while ((match = urlPattern.exec(html)) !== null) {
        const norm = normalizeUrl(match[1], src);
        if (!norm || urls.includes(norm)) continue;
        urls.push(norm);
      }

      // 2. Match JS calls
      while ((match = jsPattern.exec(html)) !== null) {
        const type = match[1];
        const code = match[2];
        let pageId = "PUBVLNOTES01"; // Default
        if (type === "Advisory") pageId = "PUBADV01";
        if (type === "CurrentActivities") pageId = "PUBADV01";

        const constructed = `s2cMainServlet?pageid=${pageId}&VLCODE=${code}`;
        const norm = normalizeUrl(constructed, src);
        if (!norm || urls.includes(norm)) continue;
        urls.push(norm);
      }

      // 3. Fallback: detect raw advisory codes and synthesize servlet URLs
      const rawCodes = html.match(codePattern) || [];
      for (const code of new Set(rawCodes)) {
        const pageId = code.startsWith("CIAD") ? "PUBADV01" : "PUBVLNOTES01";
        const norm = normalizeUrl(`s2cMainServlet?pageid=${pageId}&VLCODE=${code}`, src);
        if (!norm || urls.includes(norm)) continue;
        urls.push(norm);
      }

      if (urls.length >= MAX_ENTRIES) break;
    } catch (err) {
      console.warn(`[cert-updater] Warning: could not fetch index ${src}`);
    }
  }
  console.log(`[cert-updater] Collected ${urls.length} raw URLs.`);
  return urls.slice(0, MAX_ENTRIES);
}

// ─── Entry builder ────────────────────────────────────────────────────────────

async function buildEntry(url) {
  const { html } = await fetchText(url);
  const text = cleanHtmlToText(html);
  const code = parseCode(url);
  const date = parseDate(text);

  if (!date) return null;

  const title = parseTitle(text) || (code ? `CERT-In Advisory ${code}` : "CERT-In Advisory");
  const severity = parseSeverity(text);
  const summary = parseSummary(text) || "Multiple vulnerabilities reported.";

  const softwareAffected = parseSoftwareAffected(text);
  const targetAudience = parseField(text, "Target Audience") || "";
  const riskAssessment = parseField(text, "Risk Assessment") || "";
  const impactAssessment = parseField(text, "Impact Assessment") || "";
  const description = parseField(text, "Description") || "";
  const cves = parseCves(text);
  const solutionLinks = parseSolutionLinks(html);

  return {
    title,
    severity,
    date,
    link: url,
    code: code || undefined,
    summary,
    description,
    softwareAffected,
    targetAudience,
    riskAssessment,
    impactAssessment,
    cves,
    solutionLinks
  };
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  console.log(`[cert-updater] Starting refresh for year ${YEAR_FILTER} -> ${OUTPUT_FILE}`);
  await initSession();
  const urls = await collectAdvisoryUrls();
  if (!urls.length) {
    process.exitCode = 0;
    return;
  }

  const settled = await Promise.allSettled(urls.map(buildEntry));

  const freshEntries = settled
    .filter(r => r.status === "fulfilled" && r.value)
    .map(r => r.value)
    .sort((a, b) => new Date(b.date) - new Date(a.date));

  // Merge: keep every existing entry that was not refreshed this run.
  // This prevents partial year-specific fetches from wiping older years or
  // previously captured same-year advisories when CERT-In blocks some pages.
  let existing = [];
  if (existsSync(OUTPUT_FILE)) {
    try { existing = JSON.parse(await readFile(OUTPUT_FILE, "utf8")); }
    catch { existing = []; }
  }

  const freshLinks = new Set(freshEntries.map(e => e.link));
  const kept = existing.filter(e => !freshLinks.has(e.link));

  const merged = [...freshEntries, ...kept]
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .slice(0, MAX_ENTRIES);

  if (!merged.length) {
    process.exitCode = 0;
    return;
  }

  await writeFile(OUTPUT_FILE, `${JSON.stringify(merged, null, 2)}\n`, "utf8");
  const logMsg = `[cert-updater] ${new Date().toISOString()} — Saved ${merged.length} advisories (${freshEntries.length} fresh).`;
  console.log(logMsg);
  try {
    await writeFile("cert-update-log.txt", `${logMsg}\n`, { flag: "a" });
  } catch (e) {}
}

main().catch(err => {
  console.error(`[cert-updater] ${new Date().toISOString()} — Error: ${err.message}`);
  process.exitCode = 1;
});
