<?php
/**
 * verify-subscriber.php
 * Handles the confirmation link click from the subscription email.
 * Verifies the token, saves subscriber to subscribers.csv, shows result page.
 * Supports ?format=json for AJAX calls from verify.html.
 */

ob_start(); // capture any accidental output (incl. BOM from editors)

define('PENDING_FILE',    __DIR__ . '/pending-subscribers.json');
define('SUBSCRIBERS_CSV', __DIR__ . '/subscribers.csv');
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
define('SITE_NAME',       'Vedtam Tech Solutions');
define('FROM_EMAIL',      'certin-advisories@vedtam.io');
define('FROM_NAME',       'Vedtam CERT-In Alerts');

$token  = trim($_GET['token'] ?? '');
$status = 'error';
$msg    = 'Invalid or expired confirmation link.';
$name   = '';

if ($token && preg_match('/^[a-f0-9]{64}$/', $token)) {
    $pending = [];
    if (file_exists(PENDING_FILE)) {
        $raw     = file_get_contents(PENDING_FILE);
        $pending = json_decode($raw, true) ?: [];
    }

    if (isset($pending[$token])) {
        $record  = $pending[$token];
        $expired = ($record['expires'] ?? 0) < time();

        if ($expired) {
            $status = 'expired';
            $msg    = 'Your confirmation link has expired. Please subscribe again.';
        } else {
            $name  = $record['name'];
            $email = $record['email'];
            $phone = $record['phone'];
            $org   = $record['org'] ?? '';

            // Check for duplicate
            $alreadyExists = false;
            if (file_exists(SUBSCRIBERS_CSV)) {
                $h = fopen(SUBSCRIBERS_CSV, 'r');
                if ($h) {
                    $header    = fgetcsv($h) ?: [];
                    $emailIdx  = array_search('email', $header);
                    $statusIdx = array_search('status', $header);

                    if ($emailIdx === false) {
                        $emailIdx = 3;
                    }
                    if ($statusIdx === false) {
                        $statusIdx = 4;
                    }

                    while (($row = fgetcsv($h)) !== false) {
                        if (
                            isset($row[$emailIdx], $row[$statusIdx]) &&
                            strtolower(trim($row[$emailIdx])) === strtolower($email) &&
                            trim($row[$statusIdx]) === 'confirmed'
                        ) {
                            $alreadyExists = true;
                            break;
                        }
                    }
                    fclose($h);
                }
            }

            if ($alreadyExists) {
                $status = 'duplicate';
                $msg    = 'This email is already confirmed.';
            } else {
                $writeHeader = !file_exists(SUBSCRIBERS_CSV) || filesize(SUBSCRIBERS_CSV) === 0;
                $h = fopen(SUBSCRIBERS_CSV, 'a');
                if ($h) {
                    if ($writeHeader) {
                        fputcsv($h, ['name', 'phone', 'organisation', 'email', 'status', 'subscribed_at']);
                    }
                    fputcsv($h, [
                        $name,
                        $phone,
                        $org,
                        $email,
                        'confirmed',
                        date('Y-m-d H:i:s')
                    ]);
                    fclose($h);
                    $status = 'success';
                    $msg    = 'You will now receive email alerts whenever CERT-In publishes new security advisories on ' . SITE_NAME . '.';
                } else {
                    $status = 'error';
                    $msg    = 'Could not save your subscription. Please contact us at info@vedtam.com.';
                }
            }

            // Remove token whether success or duplicate
            unset($pending[$token]);
            file_put_contents(PENDING_FILE, json_encode($pending, JSON_PRETTY_PRINT), LOCK_EX);

            // Send welcome email on fresh confirm
            if ($status === 'success') {
                sendWelcomeEmail($name, $email);
            }
        }
    }
}

// ── Send welcome email ────────────────────────────────────────────────────────
function sendWelcomeEmail(string $name, string $email): void {
    $safeName = htmlspecialchars($name, ENT_QUOTES);
    $subject  = 'Welcome to CERT-In Alerts — ' . SITE_NAME;
    $year     = date('Y');

    $body = <<<HTML
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#0f172a;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0f172a;">
    <tr><td align="center" style="padding:40px 16px;">
      <table width="560" cellpadding="0" cellspacing="0" style="background:#1e293b;border-radius:12px;overflow:hidden;max-width:560px;width:100%;">
        <tr>
          <td style="background:linear-gradient(135deg,#3d3561,#2d2545);padding:28px 32px;text-align:center;">
            <p style="margin:0 0 4px 0;font-size:12px;color:rgba(255,255,255,0.5);letter-spacing:2px;text-transform:uppercase;">Vedtam Tech Solutions</p>
            <h1 style="margin:0;font-size:20px;font-weight:700;color:#f8fafc;">You're Subscribed!</h1>
          </td>
        </tr>
        <tr>
          <td style="padding:28px 32px 24px;">
            <p style="margin:0;color:#e2e8f0;font-size:15px;">Hi <strong>{$safeName}</strong>,</p>
            <p style="margin:14px 0 0 0;color:#94a3b8;font-size:14px;line-height:1.7;">
              You are now subscribed to <strong style="color:#f8fafc;">CERT-In Security Advisories</strong> from Vedtam Tech Solutions.
            </p>
            <p style="margin:12px 0 0 0;color:#94a3b8;font-size:14px;line-height:1.7;">
              Whenever CERT-In publishes new security advisories on our website, we will email you a summary directly to this address.
            </p>
          </td>
        </tr>
        <tr>
          <td style="padding:0 32px 28px;text-align:center;">
            <a href="https://vedtam.com/cert-advisory"
               style="display:inline-block;background:linear-gradient(135deg,#fb923c,#f97316);color:#fff;text-decoration:none;padding:12px 28px;border-radius:8px;font-weight:700;font-size:14px;">
              View Current Advisories →
            </a>
          </td>
        </tr>
        <tr>
          <td style="background:#0f172a;padding:18px 32px;text-align:center;border-top:1px solid #1e293b;">
            <p style="margin:0;color:#475569;font-size:12px;">
              © {$year} Vedtam Tech Solutions ·
              <a href="https://vedtam.com/privacy-policy" style="color:#fb923c;text-decoration:none;">Privacy Policy</a>
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
    @mail($email, $subject, $body, $headers);
}

// ── Build result variables ────────────────────────────────────────────────────
$isSuccess   = $status === 'success';
$isDuplicate = $status === 'duplicate';
$iconColor   = ($isSuccess || $isDuplicate) ? '#06d6a0' : ($status === 'expired' ? '#f9c74f' : '#e63946');
$icon        = ($isSuccess || $isDuplicate) ? '✓' : ($status === 'expired' ? '⏱' : '✕');
$headline    = $isSuccess    ? 'Subscription Confirmed!'
             : ($isDuplicate ? 'Already Subscribed'
             : ($status === 'expired' ? 'Link Expired' : 'Confirmation Failed'));

// ── JSON response for AJAX calls (from verify.html) ──────────────────────────
if (($_GET['format'] ?? '') === 'json') {
    ob_end_clean();
    header('Content-Type: application/json');
    echo json_encode([
        'status'   => $status,
        'headline' => $headline,
        'message'  => $msg,
        'name'     => $isSuccess ? $name : ''
    ]);
    exit;
}

ob_end_clean();
?><!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title><?= htmlspecialchars($headline) ?> — Vedtam Tech Solutions</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0f172a;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }
    .card {
      background: #1e293b;
      border-radius: 16px;
      padding: 48px 40px;
      max-width: 480px;
      width: 100%;
      text-align: center;
    }
    .icon {
      width: 72px;
      height: 72px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 32px;
      margin: 0 auto 24px;
    }
    h1 { color: #f8fafc; font-size: 1.6rem; margin-bottom: 12px; }
    p  { color: #94a3b8; font-size: 0.95rem; line-height: 1.7; margin-bottom: 28px; }
    .btn {
      display: inline-block;
      background: linear-gradient(135deg, #fb923c, #f97316);
      color: #fff;
      text-decoration: none;
      padding: 12px 28px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.95rem;
    }
    .secondary { display: block; margin-top: 14px; color: #64748b; font-size: 0.85rem; text-decoration: none; }
    .secondary:hover { color: #94a3b8; }
  </style>
</head>
<body>
  <div class="card">
    <div class="icon" style="background:<?= $iconColor ?>22; color:<?= $iconColor ?>;">
      <?= $icon ?>
    </div>
    <h1><?= htmlspecialchars($headline) ?></h1>
    <p>
      <?= htmlspecialchars($msg) ?>
      <?php if ($isSuccess && $name): ?>
        <br><strong style="color:#f8fafc;"><?= htmlspecialchars($name) ?></strong>, check your inbox for a welcome email.
      <?php endif; ?>
    </p>
    <a href="<?= SITE_URL ?>/cert-advisory" class="btn">View CERT-In Advisories →</a>
    <a href="<?= SITE_URL ?>" class="secondary">← Back to Vedtam Home</a>
  </div>
</body>
</html>
