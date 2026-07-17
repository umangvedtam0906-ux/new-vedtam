<?php
/**
 * save-subscriber.php
 * GET  ?token=TOKEN  → email verification (renders HTML result page)
 * POST               → new subscription (returns JSON)
 */

// ── Shared config ─────────────────────────────────────────────────────────────
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
define('PENDING_FILE',    __DIR__ . '/pending-subscribers.json');
define('SUBSCRIBERS_CSV', __DIR__ . '/subscribers.csv');
define('TOKEN_EXPIRY',    3600 * 24);
define('RECAPTCHA_SECRET_KEY', '6Lfw7B8tAAAAAAu80dzMmNglhD-5XsVRdwsRZFUK'); // Google reCAPTCHA v2 Secret Key

// ── GET: email verification ───────────────────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $token  = trim($_GET['token'] ?? '');
    $status = 'error';
    $msg    = 'Invalid or expired confirmation link.';
    $name   = '';

    if ($token && preg_match('/^[a-f0-9]{64}$/', $token)) {
        $pending = [];
        if (file_exists(PENDING_FILE)) {
            $pending = json_decode(file_get_contents(PENDING_FILE), true) ?: [];
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

                $alreadyExists = false;
                if (file_exists(SUBSCRIBERS_CSV)) {
                    $h = fopen(SUBSCRIBERS_CSV, 'r');
                    if ($h) {
                        fgetcsv($h);
                        while (($row = fgetcsv($h)) !== false) {
                            if (isset($row[3]) && strtolower(trim($row[3])) === strtolower($email) && trim($row[4]) === 'confirmed') {
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
                    $org = $record['org'] ?? '';
                    $writeHeader = !file_exists(SUBSCRIBERS_CSV) || filesize(SUBSCRIBERS_CSV) === 0;
                    $h = fopen(SUBSCRIBERS_CSV, 'a');
                    if ($h) {
                        if ($writeHeader) fputcsv($h, ['name','phone','organisation','email','status','subscribed_at']);
                        fputcsv($h, [$name, $phone, $org, $email, 'confirmed', date('Y-m-d H:i:s')]);
                        fclose($h);
                        $status = 'success';
                        $msg    = 'You will now receive email alerts whenever CERT-In publishes new security advisories.';
                    } else {
                        $msg = 'Could not save your subscription. Please contact info@vedtam.com.';
                    }
                }

                unset($pending[$token]);
                file_put_contents(PENDING_FILE, json_encode($pending, JSON_PRETTY_PRINT), LOCK_EX);

                if ($status === 'success') {
                    $safeName_ = htmlspecialchars($name, ENT_QUOTES);
                    $year_     = date('Y');
                    $welcomeBody = <<<HTML
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#0f172a;font-family:sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#0f172a;"><tr><td align="center" style="padding:40px 16px;">
<table width="560" cellpadding="0" cellspacing="0" style="background:#1e293b;border-radius:12px;overflow:hidden;max-width:560px;width:100%;">
<tr><td style="background:linear-gradient(135deg,#3d3561,#2d2545);padding:28px 32px;text-align:center;">
<h1 style="margin:0;font-size:20px;font-weight:700;color:#f8fafc;">You're Subscribed!</h1></td></tr>
<tr><td style="padding:28px 32px 24px;">
<p style="color:#e2e8f0;font-size:15px;">Hi <strong>{$safeName_}</strong>,</p>
<p style="margin-top:12px;color:#94a3b8;font-size:14px;line-height:1.7;">You are now subscribed to <strong style="color:#f8fafc;">CERT-In Security Advisories</strong> from Vedtam Tech Solutions.</p>
</td></tr>
<tr><td style="padding:0 32px 28px;text-align:center;">
<a href="https://vedtam.com/cert-advisory" style="display:inline-block;background:linear-gradient(135deg,#fb923c,#f97316);color:#fff;text-decoration:none;padding:12px 28px;border-radius:8px;font-weight:700;font-size:14px;">View Current Advisories →</a>
</td></tr>
<tr><td style="background:#0f172a;padding:18px 32px;text-align:center;">
<p style="color:#475569;font-size:12px;">© {$year_} Vedtam Tech Solutions · <a href="https://vedtam.com/privacy-policy" style="color:#fb923c;text-decoration:none;">Privacy Policy</a></p>
</td></tr>
</table></td></tr></table></body></html>
HTML;
                    $wHeaders  = "MIME-Version: 1.0\r\nContent-Type: text/html; charset=UTF-8\r\n";
                    $wHeaders .= "From: " . FROM_NAME . " <" . FROM_EMAIL . ">\r\nReply-To: " . FROM_EMAIL . "\r\n";
                    @mail($email, 'Welcome to CERT-In Alerts — ' . SITE_NAME, $welcomeBody, $wHeaders);
                }
            }
        }
    }

    $isSuccess   = $status === 'success';
    $isDuplicate = $status === 'duplicate';
    $iconColor   = ($isSuccess || $isDuplicate) ? '#06d6a0' : ($status === 'expired' ? '#f9c74f' : '#e63946');
    $icon        = ($isSuccess || $isDuplicate) ? '&#10003;' : ($status === 'expired' ? '&#9201;' : '&#10007;');
    $headline    = $isSuccess    ? 'Subscription Confirmed!'
                 : ($isDuplicate ? 'Already Subscribed'
                 : ($status === 'expired' ? 'Link Expired' : 'Confirmation Failed'));
    ?><!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title><?= htmlspecialchars($headline) ?> — Vedtam Tech Solutions</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#0f172a;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}
    .card{background:#1e293b;border-radius:16px;padding:48px 40px;max-width:480px;width:100%;text-align:center}
    .icon{width:72px;height:72px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:32px;margin:0 auto 24px}
    h1{color:#f8fafc;font-size:1.6rem;margin-bottom:12px}
    p{color:#94a3b8;font-size:.95rem;line-height:1.7;margin-bottom:28px}
    .btn{display:inline-block;background:linear-gradient(135deg,#fb923c,#f97316);color:#fff;text-decoration:none;padding:12px 28px;border-radius:8px;font-weight:700;font-size:.95rem}
    .sec{display:block;margin-top:14px;color:#64748b;font-size:.85rem;text-decoration:none}
    .sec:hover{color:#94a3b8}
  </style>
</head>
<body>
  <div class="card">
    <div class="icon" style="background:<?= $iconColor ?>22;color:<?= $iconColor ?>"><?= $icon ?></div>
    <h1><?= htmlspecialchars($headline) ?></h1>
    <p>
      <?= htmlspecialchars($msg) ?>
      <?php if ($isSuccess && $name): ?>
        <br><strong style="color:#f8fafc"><?= htmlspecialchars($name) ?></strong>, check your inbox for a welcome email.
      <?php endif; ?>
    </p>
    <a href="<?= SITE_URL ?>/cert-advisory" class="btn">View CERT-In Advisories &rarr;</a>
    <a href="<?= SITE_URL ?>" class="sec">&larr; Back to Vedtam Home</a>
  </div>
</body>
</html>
    <?php
    exit;
}

// ── POST: new subscription ────────────────────────────────────────────────────
header('Content-Type: application/json');
$allowed_origins = [
    'https://vedtam.com',
    'https://vedtam.io',
    'http://vedtam.io',
    'http://localhost:8000',
    'http://127.0.0.1:8000'
];
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if (in_array($origin, $allowed_origins, true)) {
    header('Access-Control-Allow-Origin: ' . $origin);
} else {
    header('Access-Control-Allow-Origin: https://vedtam.com');
}
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed.']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
if (!$input) $input = $_POST;

$name  = trim($input['name']  ?? '');
$phone = trim($input['phone'] ?? '');
$org   = trim($input['org']   ?? '');
$email = trim($input['email'] ?? '');
$recaptchaToken = trim($input['recaptcha'] ?? '');

// Verify reCAPTCHA token using Enterprise API or fallback
if (empty($recaptchaToken)) {
    echo json_encode(['success' => false, 'message' => 'reCAPTCHA verification token is missing. Please complete the captcha challenge.']);
    exit;
}

function verify_recaptcha_enterprise(string $token, string $action): bool {
    // 1. Try Google Cloud SDK if available (Composer autoloader)
    if (file_exists(__DIR__ . '/vendor/autoload.php')) {
        try {
            require_once __DIR__ . '/vendor/autoload.php';
            if (class_exists('Google\Cloud\RecaptchaEnterprise\V1\Client\RecaptchaEnterpriseServiceClient')) {
                $client = new \Google\Cloud\RecaptchaEnterprise\V1\Client\RecaptchaEnterpriseServiceClient();
                $projectName = $client->projectName('robotic-tract-469911-b0');

                $event = (new \Google\Cloud\RecaptchaEnterprise\V1\Event())
                    ->setSiteKey('6Lfw7B8tAAAAAF8msWjJqvABoC0B48s0lktM7_L2')
                    ->setToken($token);

                $assessment = (new \Google\Cloud\RecaptchaEnterprise\V1\Assessment())
                    ->setEvent($event);

                $request = (new \Google\Cloud\RecaptchaEnterprise\V1\CreateAssessmentRequest())
                    ->setParent($projectName)
                    ->setAssessment($assessment);

                $response = $client->createAssessment($request);

                if ($response->getTokenProperties()->getValid() && $response->getTokenProperties()->getAction() === $action) {
                    $riskAnalysis = $response->getRiskAnalysis();
                    if ($riskAnalysis) {
                        $score = $riskAnalysis->getScore();
                        if ($score !== null && $score < 0.5) {
                            return false;
                        }
                    }
                    return true;
                }
                return false;
            }
        } catch (\Exception $e) {
            // Fallback on SDK exceptions
        }
    }

    // 2. Fallback: Verify via the standard siteverify API (fully supported by Enterprise keys for legacy integration)
    $verifyUrl = 'https://www.google.com/recaptcha/api/siteverify';
    $verifyData = [
        'secret'   => RECAPTCHA_SECRET_KEY,
        'response' => $token,
        'remoteip' => $_SERVER['REMOTE_ADDR'] ?? ''
    ];

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $verifyUrl);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($verifyData));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);

    $verifyResponse = curl_exec($ch);
    curl_close($ch);

    $verifyResult = json_decode($verifyResponse, true);
    if ($verifyResult && !empty($verifyResult['success'])) {
        if (isset($verifyResult['score']) && $verifyResult['score'] < 0.5) {
            return false;
        }
        return true;
    }
    return false;
}

if (!verify_recaptcha_enterprise($recaptchaToken, 'subscribe')) {
    echo json_encode(['success' => false, 'message' => 'reCAPTCHA security check failed. Please try again.']);
    exit;
}

if (strlen($name) < 2 || strlen($name) > 100) {
    echo json_encode(['success' => false, 'message' => 'Please enter your full name (2–100 characters).']);
    exit;
}
if (!preg_match('/^[a-zA-Z\s.\'-]+$/', $name)) {
    echo json_encode(['success' => false, 'message' => 'Name can only contain letters, spaces, and basic punctuation.']);
    exit;
}

$phoneDigits = preg_replace('/[^0-9]/', '', $phone);
if (substr($phoneDigits, 0, 2) === '91' && strlen($phoneDigits) === 12) {
    $phoneDigits = substr($phoneDigits, 2);
}
if (strlen($phoneDigits) !== 10) {
    echo json_encode(['success' => false, 'message' => 'Please enter a valid 10-digit Indian mobile number.']);
    exit;
}
if (!preg_match('/^[6-9][0-9]{9}$/', $phoneDigits)) {
    echo json_encode(['success' => false, 'message' => 'Mobile number must start with 6, 7, 8, or 9.']);
    exit;
}

if (strlen($org) < 2 || strlen($org) > 150) {
    echo json_encode(['success' => false, 'message' => 'Please enter your organisation name (2–150 characters).']);
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo json_encode(['success' => false, 'message' => 'Please enter a valid email address.']);
    exit;
}
$personalDomains = [
    'aol.com','rediffmail.com','protonmail.com','proton.me','tutanota.com','gmx.com','gmx.net',
    'mailinator.com','guerrillamail.com','10minutemail.com','tempmail.com','throwam.com','yopmail.com',
];
$emailDomain = strtolower(substr(strrchr($email, '@'), 1));
if (in_array($emailDomain, $personalDomains, true)) {
    echo json_encode(['success' => false, 'message' => 'Please use your company email address. Personal email IDs are not accepted.']);
    exit;
}

if (file_exists(SUBSCRIBERS_CSV)) {
    $handle = fopen(SUBSCRIBERS_CSV, 'r');
    if ($handle) {
        fgetcsv($handle);
        while (($row = fgetcsv($handle)) !== false) {
            if (isset($row[3]) && strtolower(trim($row[3])) === strtolower($email) && trim($row[4]) === 'confirmed') {
                fclose($handle);
                echo json_encode(['success' => false, 'message' => 'This email is already subscribed.']);
                exit;
            }
        }
        fclose($handle);
    }
}

// Check if the email was successfully verified via OTP first in pending-otps.json
$otpFile = __DIR__ . '/pending-otps.json';
$emailKey = strtolower($email);
$isVerified = false;

if (file_exists($otpFile)) {
    $otps = json_decode(file_get_contents($otpFile), true) ?: [];
    if (isset($otps[$emailKey])) {
        $record = $otps[$emailKey];
        $isExpired = ($record['expires'] ?? 0) < time();
        if (!$isExpired && !empty($record['verified'])) {
            $isVerified = true;
            // Clean up the verified OTP entry so it cannot be reused
            unset($otps[$emailKey]);
            file_put_contents($otpFile, json_encode($otps, JSON_PRETTY_PRINT), LOCK_EX);
        }
    }
}

if (!$isVerified) {
    echo json_encode(['success' => false, 'message' => 'Email verification is required. Please verify the OTP sent to your email first.']);
    exit;
}

// Since the email is verified, save to subscribers.csv immediately as 'confirmed'
$writeHeader = !file_exists(SUBSCRIBERS_CSV) || filesize(SUBSCRIBERS_CSV) === 0;
$h = fopen(SUBSCRIBERS_CSV, 'a');
if ($h) {
    if ($writeHeader) {
        fputcsv($h, ['name','phone','organisation','email','status','subscribed_at']);
    }
    $saved = fputcsv($h, [$name, $phoneDigits, $org, $email, 'confirmed', date('Y-m-d H:i:s')]);
    fclose($h);
} else {
    $saved = false;
}

if ($saved) {
    // Send welcome email immediately
    $safeName_ = htmlspecialchars($name, ENT_QUOTES);
    $year_     = date('Y');
    $welcomeBody = <<<HTML
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#0f172a;font-family:sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#0f172a;"><tr><td align="center" style="padding:40px 16px;">
<table width="560" cellpadding="0" cellspacing="0" style="background:#1e293b;border-radius:12px;overflow:hidden;max-width:560px;width:100%;">
<tr><td style="background:linear-gradient(135deg,#3d3561,#2d2545);padding:28px 32px;text-align:center;">
<h1 style="margin:0;font-size:20px;font-weight:700;color:#f8fafc;">You're Subscribed!</h1></td></tr>
<tr><td style="padding:28px 32px 24px;">
<p style="color:#e2e8f0;font-size:15px;">Hi <strong>{$safeName_}</strong>,</p>
<p style="margin-top:12px;color:#94a3b8;font-size:14px;line-height:1.7;">You are now subscribed to <strong style="color:#f8fafc;">CERT-In Security Advisories</strong> from Vedtam Tech Solutions.</p>
</td></tr>
<tr><td style="padding:0 32px 28px;text-align:center;">
<a href="https://vedtam.com/cert-advisory" style="display:inline-block;background:linear-gradient(135deg,#fb923c,#f97316);color:#fff;text-decoration:none;padding:12px 28px;border-radius:8px;font-weight:700;font-size:14px;">View Current Advisories →</a>
</td></tr>
<tr><td style="background:#0f172a;padding:18px 32px;text-align:center;">
<p style="color:#475569;font-size:12px;">© {$year_} Vedtam Tech Solutions · <a href="https://vedtam.com/privacy-policy" style="color:#fb923c;text-decoration:none;">Privacy Policy</a></p>
</td></tr>
</table></td></tr></table></body></html>
HTML;
    $wHeaders  = "MIME-Version: 1.0\r\nContent-Type: text/html; charset=UTF-8\r\n";
    $wHeaders .= "From: " . FROM_NAME . " <" . FROM_EMAIL . ">\r\nReply-To: " . FROM_EMAIL . "\r\n";
    @mail($email, 'Welcome to CERT-In Alerts — ' . SITE_NAME, $welcomeBody, $wHeaders);

    echo json_encode(['success' => true, 'message' => 'Subscription confirmed successfully! Check your inbox for a welcome email.']);
} else {
    echo json_encode(['success' => false, 'message' => 'Could not save your subscription. Please contact info@vedtam.com.']);
}

