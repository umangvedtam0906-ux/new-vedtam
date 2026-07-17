<?php
/**
 * otp-handler.php
 * Handles OTP Generation, Email sending, and Verification.
 * Saves pending OTPs securely to pending-otps.json.
 */

// Enable output buffering to avoid any trailing whitespaces/BOM issues
ob_start();

header('Content-Type: application/json');

// CORS setup
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

$action = trim($input['action'] ?? '');
$email  = trim($input['email'] ?? '');
$name   = trim($input['name'] ?? 'Subscriber');

if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo json_encode(['success' => false, 'message' => 'Please enter a valid email address.']);
    exit;
}

// Restriction check for personal domains
$personalDomains = [
    'aol.com','rediffmail.com','protonmail.com','proton.me','tutanota.com','gmx.com','gmx.net',
    'mailinator.com','guerrillamail.com','10minutemail.com','tempmail.com','throwam.com','yopmail.com',
    'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com'
];
$emailDomain = strtolower(substr(strrchr($email, '@'), 1));
if (in_array($emailDomain, $personalDomains, true)) {
    echo json_encode(['success' => false, 'message' => 'Please use your company email address. Personal email IDs are not accepted.']);
    exit;
}

define('OTP_FILE', __DIR__ . '/pending-otps.json');
define('OTP_EXPIRY', 600); // 10 minutes (600 seconds)

function load_otps() {
    if (!file_exists(OTP_FILE)) return [];
    $raw = file_get_contents(OTP_FILE);
    return json_decode($raw, true) ?: [];
}

function save_otps(array $otps) {
    file_put_contents(OTP_FILE, json_encode($otps, JSON_PRETTY_PRINT), LOCK_EX);
}

$otps = load_otps();
$now  = time();

// Clean expired OTPs
$otps = array_filter($otps, function($item) use ($now) {
    return ($item['expires'] ?? 0) > $now;
});

if ($action === 'send') {
    // Generate 6-digit numeric OTP
    $otpCode = sprintf('%06d', random_int(100000, 999999));
    
    // Store hashed OTP in database
    $otps[strtolower($email)] = [
        'otp'      => password_hash($otpCode, PASSWORD_BCRYPT),
        'expires'  => $now + OTP_EXPIRY,
        'attempts' => 0,
        'verified' => false
    ];
    save_otps($otps);
    
    // Send email
    $subject  = 'Your Verification Code — Vedtam Tech Solutions';
    $year     = date('Y');
    $safeName = htmlspecialchars($name, ENT_QUOTES);
    
    $body = <<<HTML
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background:#0f172a;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0f172a;">
    <tr>
      <td align="center" style="padding:40px 16px;">
        <table width="560" cellpadding="0" cellspacing="0" style="background:#1e293b;border-radius:16px;overflow:hidden;max-width:560px;width:100%;">
          <tr>
            <td style="background:linear-gradient(135deg,#3d3561,#2d2545);padding:28px 32px;text-align:center;">
              <p style="margin:0 0 4px 0;font-size:12px;color:rgba(255,255,255,0.5);letter-spacing:2px;text-transform:uppercase;">Vedtam Tech Solutions</p>
              <h1 style="margin:0;font-size:20px;font-weight:700;color:#f8fafc;">Verify Your Email</h1>
            </td>
          </tr>
          <tr>
            <td style="padding:28px 32px 8px;">
              <p style="margin:0;color:#e2e8f0;font-size:15px;">Hi <strong>{$safeName}</strong>,</p>
              <p style="margin:14px 0 0 0;color:#94a3b8;font-size:14px;line-height:1.7;">
                You are setting up email verification on Vedtam. Use the One-Time Password (OTP) below to verify your email address.
              </p>
              <p style="margin:12px 0 0 0;color:#94a3b8;font-size:14px;line-height:1.7;">
                This code is valid for <strong style="color:#f8fafc;">10 minutes</strong>.
              </p>
            </td>
          </tr>
          <tr>
            <td style="padding:24px 32px;text-align:center;">
              <div style="display:inline-block;background:#0f172a;border:1px solid rgba(0, 163, 217, 0.3);letter-spacing:6px;padding:16px 36px;border-radius:12px;font-weight:800;font-size:32px;color:#00a3d9;font-family:monospace;">
                {$otpCode}
              </div>
              <p style="margin:16px 0 0 0;color:#475569;font-size:11px;">
                For security, please do not share this code with anyone.
              </p>
            </td>
          </tr>
          <tr>
            <td style="background:#0f172a;padding:18px 32px;text-align:center;border-top:1px solid #1e293b;">
              <p style="margin:0;color:#475569;font-size:12px;line-height:1.6;">
                If you did not request this, please ignore this email.<br>
                &copy; {$year} Vedtam Tech Solutions &middot;
                <a href="https://vedtam.com/privacy-policy" style="color:#fb923c;text-decoration:none;">Privacy Policy</a>
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
HTML;

    $headers  = "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/html; charset=UTF-8\r\n";
    $headers .= "From: Vedtam CERT-In Alerts <certin-advisories@vedtam.io>\r\n";
    $headers .= "Reply-To: certin-advisories@vedtam.io\r\n";
    
    ob_end_clean();
    if (@mail($email, $subject, $body, $headers)) {
        echo json_encode(['success' => true, 'message' => 'A verification code has been sent to ' . $email]);
    } else {
        echo json_encode(['success' => false, 'message' => 'Could not send verification email. Please try again.']);
    }
    exit;
}

if ($action === 'verify') {
    $userOtp = trim($input['otp'] ?? '');
    
    if (empty($userOtp) || strlen($userOtp) !== 6) {
        ob_end_clean();
        echo json_encode(['success' => false, 'message' => 'Please enter a valid 6-digit OTP code.']);
        exit;
    }
    
    $emailKey = strtolower($email);
    if (!isset($otps[$emailKey])) {
        ob_end_clean();
        echo json_encode(['success' => false, 'message' => 'OTP expired or not found. Please request a new code.']);
        exit;
    }
    
    $record = $otps[$emailKey];
    
    // Check limit attempts
    if (($record['attempts'] ?? 0) >= 3) {
        unset($otps[$emailKey]);
        save_otps($otps);
        ob_end_clean();
        echo json_encode(['success' => false, 'message' => 'Too many failed verification attempts. Please request a new code.']);
        exit;
    }
    
    // Verify OTP hash
    if (password_verify($userOtp, $record['otp'])) {
        // Mark as verified
        $otps[$emailKey]['verified'] = true;
        $otps[$emailKey]['expires']  = $now + 300; // Extend valid verification for 5 mins to allow form submission
        save_otps($otps);
        
        ob_end_clean();
        echo json_encode(['success' => true, 'message' => 'Email verified successfully.']);
    } else {
        $otps[$emailKey]['attempts'] = ($record['attempts'] ?? 0) + 1;
        save_otps($otps);
        ob_end_clean();
        echo json_encode(['success' => false, 'message' => 'Invalid verification code. Please try again.']);
    }
    exit;
}

ob_end_clean();
echo json_encode(['success' => false, 'message' => 'Invalid action.']);
exit;
