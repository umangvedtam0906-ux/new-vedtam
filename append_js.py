import os

js_file = r"c:\Users\Manu\Downloads\new-vedtam-main (3)\new-vedtam-main\assets\js\vedtam.js"

logo_script = """

// Logo Alternation Script
(function() {
  const logosEn = document.querySelectorAll('.nav-logo .logo-en');
  const logosHi = document.querySelectorAll('.nav-logo .logo-hi');
  
  if (logosEn.length === 0 || logosHi.length === 0) return;
  
  let showEnglish = true;
  
  setInterval(() => {
    showEnglish = !showEnglish;
    
    logosEn.forEach(logo => {
      logo.style.opacity = showEnglish ? '1' : '0';
    });
    
    logosHi.forEach(logo => {
      logo.style.opacity = showEnglish ? '0' : '1';
    });
  }, 2000); // Toggle every 2 seconds
})();
"""

with open(js_file, 'a', encoding='utf-8') as f:
    f.write(logo_script)

print("Appended logo script to vedtam.js")
