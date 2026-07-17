import os
import re

print("Updating logo rotation logic globally...")

# 1. Append CSS to assets/css/vedtam.css
css_file = os.path.join('assets', 'css', 'vedtam.css')
css_animation = """
/* Logo Switcher Animation Global */
@keyframes fadeLogo1 {
  0%, 45% { opacity: 1 !important; visibility: visible !important; }
  50%, 95% { opacity: 0 !important; visibility: hidden !important; }
  100% { opacity: 1 !important; visibility: visible !important; }
}
@keyframes fadeLogo2 {
  0%, 45% { opacity: 0 !important; visibility: hidden !important; }
  50%, 95% { opacity: 1 !important; visibility: visible !important; }
  100% { opacity: 0 !important; visibility: hidden !important; }
}
.logo-en {
  animation: fadeLogo1 6s infinite !important;
  transition: none !important;
}
.logo-hi {
  animation: fadeLogo2 6s infinite !important;
  transition: none !important;
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  width: 100% !important;
  height: 100% !important;
  object-fit: contain !important;
}
"""

if os.path.exists(css_file):
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'fadeLogo1' not in content:
        with open(css_file, 'a', encoding='utf-8') as f:
            f.write(css_animation)
        print("Added animation to vedtam.css")
else:
    print(f"Error: {css_file} not found")

# 2. Remove conflicting JavaScript from assets/js/vedtam.js
js_file = os.path.join('assets', 'js', 'vedtam.js')

if os.path.exists(js_file):
    with open(js_file, 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # We want to remove the block that starts with const logoEns = ... and ends at the interval
    # Let's use a regex to match the block
    pattern = r"//  Reveal on scroll \nconst logoEns.*?\n\}\n"
    
    # Actually, let's just do string replacement for safety
    block_to_remove = """const logoEns = document.querySelectorAll('.logo-en');
const logoHis = document.querySelectorAll('.logo-hi');

if (logoEns.length > 0 && logoHis.length > 0) {
  logoEns.forEach(el => {
    el.style.transition = 'opacity 0.8s ease-in-out';
    if(el.parentElement) {
      el.parentElement.style.position = 'relative';
    }
  });
  
  logoHis.forEach(el => {
    el.style.transition = 'opacity 0.8s ease-in-out';
    el.style.position = 'absolute';
    el.style.top = '0';
    el.style.left = '0';
    el.style.width = '100%';
    el.style.height = '100%';
    el.style.objectFit = 'contain';
  });
  
  let showEnglish = true;
  setInterval(() => {
    showEnglish = !showEnglish;
    if (showEnglish) {
      logoEns.forEach(el => el.style.opacity = '1');
      logoHis.forEach(el => el.style.opacity = '0');
    } else {
      logoEns.forEach(el => el.style.opacity = '0');
      logoHis.forEach(el => el.style.opacity = '1');
    }
  }, 3000); // Switch every 3 seconds
}"""

    if block_to_remove in js_content:
        js_content = js_content.replace(block_to_remove, "")
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print("Removed conflicting JS from vedtam.js")
    else:
        print("JS block not found in vedtam.js (already removed?)")

print("\\nDone updating global logo switch!")
