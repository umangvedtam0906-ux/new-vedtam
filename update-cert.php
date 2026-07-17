<?php
/**
 * update-cert.php
 * Scrapes CERT-In advisories, updates cert-data.json,
 * and emails confirmed subscribers when new advisories are found.
 *
 * Run via Hostinger Cron Job every 12 hours:
 *   php /home/your_username/public_html/update-cert.php
 */

@set_time_limit(240);

// ── Configuration ───────────────────────────────────────────────────────────
define('SITE_NAME',        'Vedtam Tech Solutions');
// Detect protocol and host dynamically for staging/production compatibility (fallback to production domain when run via CLI cron)
$host = $_SERVER['HTTP_HOST'] ?? '';
if ($host) {
    $protocol = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off' 
                 || ($_SERVER['SERVER_PORT'] ?? 80) == 443 
                 || (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https')) 
                 ? 'https' : 'http';
    define('SITE_URL', $protocol . '://' . $host);
} else {
    define('SITE_URL', 'https://vedtam.com');
}
define('FROM_EMAIL',       'certin-advisories@vedtam.io');
define('FROM_NAME',        'Vedtam CERT-In Alerts');
define('CERT_JSON',        __DIR__ . '/cert-data.json');
define('SUBSCRIBERS_CSV',  __DIR__ . '/subscribers.csv');
define('LOG_FILE',         __DIR__ . '/cert-update-log.txt');
define('MAX_ENTRIES',      500);
define('YEAR_FILTER',      date('Y'));
define('LOCK_FILE',        __DIR__ . '/cert-update.lock');

// ── Prevent concurrent runs ───────────────────────────────────────────────────
$lockHandle = fopen(LOCK_FILE, 'c');
if (!$lockHandle || !flock($lockHandle, LOCK_EX | LOCK_NB)) {
    echo '[' . date('Y-m-d H:i:s') . '] Already running — skipping.' . PHP_EOL;
    exit(0);
}

// ── Helpers ──────────────────────────────────────────────────────────────────
function logMsg(string $msg): void {
    $line = '[' . date('Y-m-d H:i:s') . '] ' . $msg . PHP_EOL;
    file_put_contents(LOG_FILE, $line, FILE_APPEND | LOCK_EX);
    echo $line;
}

$sessionCookies = []; // Keyed by host (in-memory cookie jar)

function fetchUrl(string $url, int $timeout = 20, int $depth = 0): ?string {
    if ($depth > 3) return null;

    $parsedUrl = parse_url($url);
    $host = $parsedUrl['host'] ?? 'www.cert-in.org.in';

    global $sessionCookies;
    $ch = curl_init($url);
    
    $httpHeaders = [
        'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language: en-US,en;q=0.5',
        'Referer: https://' . $host . '/',
    ];

    if (!empty($sessionCookies[$host])) {
        $httpHeaders[] = 'Cookie: ' . $sessionCookies[$host];
    }

    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_MAXREDIRS      => 5,
        CURLOPT_TIMEOUT        => $timeout,
        CURLOPT_SSL_VERIFYPEER => false,
        CURLOPT_SSL_VERIFYHOST => false,
        CURLOPT_USERAGENT      => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        CURLOPT_HTTPHEADER     => $httpHeaders,
        CURLOPT_ENCODING       => 'gzip, deflate',
    ]);

    // Parse header to extract JSESSIONID
    curl_setopt($ch, CURLOPT_HEADERFUNCTION, function($curl, $headerLine) use ($host, &$sessionCookies) {
        if (stripos($headerLine, 'Set-Cookie:') === 0) {
            if (preg_match('/JSESSIONID=([^;]+)/i', $headerLine, $matches)) {
                $sessionCookies[$host] = 'JSESSIONID=' . $matches[1];
            }
        }
        return strlen($headerLine);
    });

    $html = curl_exec($ch);
    $err  = curl_error($ch);
    curl_close($ch);

    if ($html === false || $html === '') {
        if ($err) logMsg("  cURL error for $url: $err");
        return null;
    }

    // Handle frameset — follow the main content frame
    if (stripos($html, '<frameset') !== false) {
        if (preg_match('/<frame[^>]+src=["\']([^"\']+)["\'][^>]*>/i', $html, $fm)) {
            $frameUrl = strpos($fm[1], 'http') === 0
                ? $fm[1]
                : 'https://' . $host . '/' . ltrim($fm[1], '/');
            return fetchUrl($frameUrl, $timeout, $depth + 1);
        }
    }

    return $html;
}

function cleanText(string $html): string {
    $html = preg_replace('/<script[\s\S]*?<\/script>/i', '', $html);
    $html = preg_replace('/<style[\s\S]*?<\/style>/i',   '', $html);
    $html = preg_replace('/<br\s*\/?>/i', "\n", $html);
    $html = preg_replace('/<\/?(p|div|tr|h[1-6])[^>]*>/i', "\n", $html);
    $html = preg_replace('/<\/?(li)[^>]*>/i', "\n• ", $html);
    $html = strip_tags($html);
    $html = html_entity_decode($html, ENT_QUOTES | ENT_HTML5, 'UTF-8');
    $html = preg_replace('/\n{2,}/', "\n", $html);
    return trim($html);
}

function parseSeverity(string $text): string {
    if (preg_match('/Severity\s+Rating\s*:\s*(Critical|High|Medium|Low)/i', $text, $m))
        return strtolower($m[1]);
    if (preg_match('/Risk\s+Assessment\s*:\s*(Critical|High)\s+risk/i', $text, $m))
        return strtolower($m[1]);
    if (stripos($text, 'Critical') !== false) return 'critical';
    if (stripos($text, 'High')     !== false) return 'high';
    if (stripos($text, 'Medium')   !== false) return 'medium';
    return 'low';
}

function parseDate(string $text): string {
    // Try "Month DD, YYYY" format (e.g., June 12, 2026)
    if (preg_match('/(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})/i', $text, $m)) {
        $ts = strtotime($m[1] . ' ' . $m[2] . ' ' . $m[3]);
        if ($ts) return date('Y-m-d', $ts);
    }
    // Try "DD Month YYYY" format (e.g., 12 June 2026)
    if (preg_match('/(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})/i', $text, $m)) {
        $ts = strtotime($m[1] . ' ' . $m[2] . ' ' . $m[3]);
        if ($ts) return date('Y-m-d', $ts);
    }
    // Try ISO date
    if (preg_match('/(\d{4}-\d{2}-\d{2})/', $text, $m)) return $m[1];
    return date('Y-m-d');
}

function parseTitle(string $text, string $code): string {
    if (preg_match('/CERT-In\s+(?:Vulnerability\s+Note|Advisory)\s+[A-Z0-9-]+\s+(.+?)(?=\s+Original\s+Issue\s+Date:)/is', $text, $m)) {
        return trim($m[1]);
    }
    if (preg_match('/(?:^|[\r\n])([A-Z][^.!?]{15,180})[\s\r\n]*Original\s+Issue\s+Date/is', $text, $m)) {
        return trim($m[1]);
    }
    return $code;
}

function parseSolutionLinks(string $html): array {
    if (preg_match('/(?:Vendor Information|References)([\s\S]*?)Disclaimer/i', $html, $m)) {
        if (preg_match_all('/(https?:\/\/[^\s<"\']+)/i', $m[1], $links)) {
            $valid = [];
            foreach (array_unique($links[1]) as $link) {
                if (stripos($link, 'cve.org') === false && stripos($link, 'cve.mitre.org') === false) {
                    $valid[] = $link;
                }
            }
            return array_slice($valid, 0, 8);
        }
    }
    return [];
}

// ── Load existing cert-data.json ──────────────────────────────────────────────
$existing = [];
if (file_exists(CERT_JSON)) {
    $raw = @file_get_contents(CERT_JSON);
    $existing = json_decode($raw, true) ?: [];
}
$existingCodes = array_column($existing, 'code');
logMsg('Loaded ' . count($existing) . ' existing advisories.');

// Initialize sessions by hitting domains
logMsg("Initializing sessions...");
fetchUrl('https://www.cert-in.org.in/');
fetchUrl('https://xn----1td4etbxb9bwj.xn--h2brj9c/');

// ── Fetch from multiple CERT-In sources and collect advisory URLs ─────────────
$sources = [
    'https://www.cert-in.org.in/s2cMainServlet?pageid=PUBWEL01',
    'https://www.cert-in.org.in/s2cMainServlet?pageid=VLNLIST02&year=' . YEAR_FILTER,
    'https://www.cert-in.org.in/s2cMainServlet?pageid=PUBADVLIST02&year=' . YEAR_FILTER,
    'https://www.cert-in.org.in/s2cMainServlet?pageid=PUBADVLIST',
    'https://xn----1td4etbxb9bwj.xn--h2brj9c/s2cMainServlet?pageid=PUBWEL01',
    'https://xn----1td4etbxb9bwj.xn--h2brj9c/s2cMainServlet?pageid=VLNLIST02&year=' . YEAR_FILTER,
    'https://xn----1td4etbxb9bwj.xn--h2brj9c/s2cMainServlet?pageid=PUBADVLIST02&year=' . YEAR_FILTER,
];

$foundLinks = []; // [code => url]

foreach ($sources as $src) {
    logMsg("Fetching: $src");
    $html = fetchUrl($src, 25);
    if (!$html) {
        logMsg("  WARNING: Could not fetch $src, skipping.");
        continue;
    }
    logMsg('  Got ' . strlen($html) . ' bytes.');

    $parsedSrc = parse_url($src);
    $srcBase = ($parsedSrc['scheme'] ?? 'https') . '://' . ($parsedSrc['host'] ?? 'www.cert-in.org.in') . '/';

    // Pattern 1 — direct href containing VLCODE (handles &amp; entities)
    preg_match_all('/href=["\']([^"\']*VLCODE=((?:CIVN|CIAD|CICA)-' . YEAR_FILTER . '-\d+))["\']/i', $html, $m1);
    foreach ($m1[1] as $i => $href) {
        $code = strtoupper($m1[2][$i]);
        $href = html_entity_decode($href, ENT_QUOTES | ENT_HTML5, 'UTF-8');
        $url  = strpos($href, 'http') === 0 ? $href : $srcBase . ltrim($href, '/');
        if (!isset($foundLinks[$code])) $foundLinks[$code] = $url;
    }

    // Pattern 2 — JavaScript callPage('VulnerabilityNote','CIVN-2026-XXXX')
    preg_match_all("/callPage\s*\(\s*['\"](\w+)['\"]\s*,\s*['\"]((?:CIVN|CIAD|CICA)-" . YEAR_FILTER . "-[^'\"]+)['\"]\s*\)/i", $html, $m2);
    foreach ($m2[2] as $i => $code) {
        $code   = strtoupper(trim($code));
        $type   = strtolower($m2[1][$i]);
        $pageId = (strpos($type, 'adv') !== false) ? 'PUBADV01' : 'PUBVLNOTES01';
        $url    = $srcBase . 's2cMainServlet?pageid=' . $pageId . '&VLCODE=' . $code;
        if (!isset($foundLinks[$code])) $foundLinks[$code] = $url;
    }

    // Pattern 3 — raw advisory codes anywhere in the HTML (fallback)
    preg_match_all('/((?:CIVN|CIAD|CICA)-' . YEAR_FILTER . '-\d{4,})/i', $html, $m3);
    foreach (array_unique($m3[1]) as $code) {
        $code   = strtoupper($code);
        $pageId = strpos($code, 'CIAD') === 0 ? 'PUBADV01' : 'PUBVLNOTES01';
        $url    = $srcBase . 's2cMainServlet?pageid=' . $pageId . '&VLCODE=' . $code;
        if (!isset($foundLinks[$code])) $foundLinks[$code] = $url;
    }
}

logMsg('Total unique advisory codes found across all sources: ' . count($foundLinks));

if (count($foundLinks) === 0) {
    logMsg('ERROR: No advisory links found from any source. Aborting.');
    flock($lockHandle, LOCK_UN);
    fclose($lockHandle);
    exit(1);
}

// ── Process new advisories ────────────────────────────────────────────────────
$newAdvisories = [];

foreach ($foundLinks as $code => $detailUrl) {
    if (in_array($code, $existingCodes, true)) continue; // already have it

    logMsg("  Fetching new advisory: $code");
    $detail = fetchUrl($detailUrl, 15);
    if (!$detail) {
        logMsg("  WARNING: Could not fetch detail for $code, skipping.");
        continue;
    }

    $plainText = cleanText($detail);

    $title = parseTitle($plainText, $code);
    $severity  = parseSeverity($plainText);
    $date      = parseDate($plainText);

    // Summary: first non-trivial paragraph
    $summary = '';
    if (preg_match('/(?:Description|Summary)\s*[:\-]?\s*\n([\s\S]{30,400}?)(?:\n[A-Z]|\z)/i', $plainText, $ms)) {
        $summary = trim(preg_replace('/\s+/', ' ', $ms[1]));
    }
    if (!$summary && strlen($plainText) > 50) {
        $summary = substr(preg_replace('/\s+/', ' ', $plainText), 0, 280) . '...';
    }

    // Software affected (parsed as array)
    $softwareAffected = [];
    if (preg_match('/(?:Software Affected|Affected\s+Software|Systems?\s+Affected)\s*[:\-]?\s*\n([\s\S]{10,500}?)(?:\n[A-Z][a-z]|\z)/i', $plainText, $msw)) {
        $block = trim($msw[1]);
        if (strpos($block, '• ') === 0) {
            $block = substr($block, 3);
        }
        $parts = preg_split('/\n•/u', $block);
        foreach ($parts as $part) {
            $partCleaned = trim(preg_replace('/\s+/', ' ', $part));
            if ($partCleaned !== '') {
                $softwareAffected[] = $partCleaned;
            }
        }
    }

    // CVEs
    preg_match_all('/CVE-\d{4}-\d{4,}/', $plainText, $cveMatches);
    $cves = array_unique($cveMatches[0]);

    // Solution links
    $solutionLinks = parseSolutionLinks($detail);

    $newAdvisories[] = [
        'id'               => strtolower(str_replace(['/', ' '], '-', $code)),
        'code'             => $code,
        'title'            => $title,
        'severity'         => $severity,
        'date'             => $date,
        'link'             => $detailUrl,
        'summary'          => $summary,
        'description'      => $summary,
        'softwareAffected' => $softwareAffected,
        'cves'             => $cves,
        'targetAudience'   => 'System administrators and users',
        'riskAssessment'   => ucfirst($severity) . ' risk',
        'impactAssessment' => '',
        'solutionLinks'    => $solutionLinks
    ];

    usleep(400000); // 0.4s polite delay between requests
    if (count($newAdvisories) >= 15) break; // cap per run to prevent server timeout
}

logMsg('New advisories found: ' . count($newAdvisories));

// ── Merge, sort, trim, save ───────────────────────────────────────────────────
if (count($newAdvisories) > 0) {
    $merged = array_merge($newAdvisories, $existing);

    usort($merged, function($a, $b) {
        return strcmp($b['date'] ?? '0', $a['date'] ?? '0');
    });

    $merged = array_slice($merged, 0, MAX_ENTRIES);

    file_put_contents(CERT_JSON, json_encode($merged, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
    logMsg('cert-data.json updated. Total entries: ' . count($merged));

    // ── Email subscribers ─────────────────────────────────────────────────────
    emailSubscribers($newAdvisories);
} else {
    logMsg('No new advisories. cert-data.json unchanged.');
}

logMsg('Done.');
flock($lockHandle, LOCK_UN);
fclose($lockHandle);

// ── Email subscribers function ────────────────────────────────────────────────
function emailSubscribers(array $newAdvisories): void {
    if (!file_exists(SUBSCRIBERS_CSV)) {
        logMsg('No subscribers file found, skipping email.');
        return;
    }

    $subscribers = [];
    $handle = fopen(SUBSCRIBERS_CSV, 'r');
    if (!$handle) return;

    $header    = fgetcsv($handle) ?: [];
    $nameIdx   = array_search('name',   $header);
    $emailIdx  = array_search('email',  $header);
    $statusIdx = array_search('status', $header);

    // Fallback to old 5-column format if header is missing/unrecognised
    if ($emailIdx === false)  $emailIdx  = 2;
    if ($statusIdx === false) $statusIdx = 3;
    if ($nameIdx === false)   $nameIdx   = 0;

    while (($row = fgetcsv($handle)) !== false) {
        if (isset($row[$statusIdx]) && trim($row[$statusIdx]) === 'confirmed' && isset($row[$emailIdx])) {
            $subscribers[] = [
                'name'  => trim($row[$nameIdx]),
                'email' => trim($row[$emailIdx])
            ];
        }
    }
    fclose($handle);

    if (empty($subscribers)) {
        logMsg('No confirmed subscribers to email.');
        return;
    }

    logMsg('Emailing ' . count($subscribers) . ' subscribers...');

    // Build advisory rows for the email
    $advisoryRows = '';
    foreach (array_slice($newAdvisories, 0, 10) as $adv) {
        $sevColor = match(strtolower($adv['severity'] ?? '')) {
            'critical' => '#e63946',
            'high'     => '#f4842d',
            'medium'   => '#f9c74f',
            'low'      => '#06d6a0',
            default    => '#94a3b8'
        };
        $link     = SITE_URL . '/cert-advisory#' . ($adv['id'] ?? '');
        $title    = htmlspecialchars($adv['title'] ?? $adv['code'], ENT_QUOTES);
        $date     = htmlspecialchars($adv['date'] ?? '', ENT_QUOTES);
        $sev      = strtoupper($adv['severity'] ?? 'INFO');
        $advisoryRows .= "
        <tr>
          <td style='padding:10px 12px; border-bottom:1px solid #1e293b;'>
            <a href='{$link}' style='color:#fb923c; text-decoration:none; font-weight:600;'>{$title}</a>
          </td>
          <td style='padding:10px 12px; border-bottom:1px solid #1e293b; white-space:nowrap;'>
            <span style='background:{$sevColor}22; color:{$sevColor}; padding:2px 8px; border-radius:4px; font-size:12px; font-weight:700;'>{$sev}</span>
          </td>
          <td style='padding:10px 12px; border-bottom:1px solid #1e293b; color:#94a3b8; white-space:nowrap; font-size:13px;'>{$date}</td>
        </tr>";
    }

    $totalNew  = count($newAdvisories);
    $advWord   = $totalNew === 1 ? 'advisory' : 'advisories';
    $subject   = "CERT-In Alert: {$totalNew} New Security " . ($totalNew === 1 ? 'Advisory' : 'Advisories') . ' — Vedtam';
    $siteUrl   = SITE_URL;
    $siteName  = SITE_NAME;
    $year      = date('Y');

    foreach ($subscribers as $sub) {
        $to   = $sub['email'];
        $name = htmlspecialchars($sub['name'], ENT_QUOTES);

        $body = <<<HTML
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#0f172a;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0f172a;">
    <tr><td align="center" style="padding:32px 16px;">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#1e293b;border-radius:12px;overflow:hidden;max-width:600px;width:100%;">

        <!-- Header -->
        <tr>
          <td style="background:linear-gradient(135deg,#3d3561,#2d2545);padding:28px 32px;text-align:center;">
            <p style="margin:0 0 4px 0;font-size:13px;color:rgba(255,255,255,0.5);letter-spacing:2px;text-transform:uppercase;">Vedtam Tech Solutions</p>
            <h1 style="margin:0;font-size:22px;font-weight:700;color:#f8fafc;">CERT-In Security Alert</h1>
            <p style="margin:8px 0 0 0;font-size:13px;color:rgba(255,255,255,0.6);">{$totalNew} new {$advWord} published</p>
          </td>
        </tr>

        <!-- Greeting -->
        <tr>
          <td style="padding:24px 32px 8px;">
            <p style="margin:0;color:#e2e8f0;font-size:15px;">Hi <strong>{$name}</strong>,</p>
            <p style="margin:12px 0 0 0;color:#94a3b8;font-size:14px;line-height:1.6;">
              CERT-In has published <strong style="color:#fb923c;">{$totalNew} new security {$advWord}</strong>.
              Here is a summary of the latest updates:
            </p>
          </td>
        </tr>

        <!-- Advisories Table -->
        <tr>
          <td style="padding:16px 32px 24px;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background:#0f172a;border-radius:8px;overflow:hidden;font-size:14px;color:#e2e8f0;">
              <tr style="background:#1e293b;">
                <th style="padding:10px 12px;text-align:left;color:#64748b;font-size:12px;text-transform:uppercase;letter-spacing:1px;font-weight:600;">Advisory</th>
                <th style="padding:10px 12px;text-align:left;color:#64748b;font-size:12px;text-transform:uppercase;letter-spacing:1px;font-weight:600;">Severity</th>
                <th style="padding:10px 12px;text-align:left;color:#64748b;font-size:12px;text-transform:uppercase;letter-spacing:1px;font-weight:600;">Date</th>
              </tr>
              {$advisoryRows}
            </table>
          </td>
        </tr>

        <!-- CTA -->
        <tr>
          <td style="padding:0 32px 28px;text-align:center;">
            <a href="{$siteUrl}/cert-advisory" style="display:inline-block;background:linear-gradient(135deg,#fb923c,#f97316);color:#fff;text-decoration:none;padding:12px 28px;border-radius:8px;font-weight:600;font-size:15px;">
              View All Advisories &rarr;
            </a>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="background:#0f172a;padding:20px 32px;text-align:center;border-top:1px solid #1e293b;">
            <p style="margin:0;color:#475569;font-size:12px;">
              You are receiving this because you subscribed to CERT-In alerts on {$siteName}.<br>
              &copy; {$year} {$siteName} &middot; <a href="{$siteUrl}/privacy-policy" style="color:#fb923c;text-decoration:none;">Privacy Policy</a>
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
HTML;

        $headers  = "MIME-Version: 1.0\r\n";
        $headers .= "Content-Type: text/html; charset=UTF-8\r\n";
        $headers .= "From: " . FROM_NAME . " <" . FROM_EMAIL . ">\r\n";
        $headers .= "Reply-To: " . FROM_EMAIL . "\r\n";
        $headers .= "X-Mailer: VedtamCertAlert/1.0\r\n";

        $sent = @mail($to, $subject, $body, $headers);
        logMsg('  Email to ' . $to . ': ' . ($sent ? 'sent' : 'FAILED'));

        usleep(200000); // 0.2s between emails
    }
}
