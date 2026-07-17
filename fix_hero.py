import re

with open('vedtam.css', 'r', encoding='utf-8') as f:
    css = f.read()

# We want to change align-items: center to align-items: flex-start inside any hero-shell rule
# and increase gap.

# Instead of complex regex, let's just do a global replace for these specific known blocks
# found from grep

css = css.replace(
    '.hero-shell {\n    align-items: center !important;',
    '.hero-shell {\n    align-items: flex-start !important;'
)

css = css.replace(
    '.hero-shell,\n[class*="-hero"] .hero-shell {\n    grid-template-columns: minmax(0, 1.08fr) minmax(300px, 0.92fr) !important;\n    align-items: center !important;',
    '.hero-shell,\n[class*="-hero"] .hero-shell {\n    grid-template-columns: minmax(0, 1.08fr) minmax(300px, 0.92fr) !important;\n    align-items: flex-start !important;\n    gap: 4rem !important;'
)

css = css.replace(
    '.ot-hero .hero-shell {\n    grid-template-columns: minmax(0, 1.06fr) minmax(320px, 0.94fr) !important;\n    align-items: center !important;',
    '.ot-hero .hero-shell {\n    grid-template-columns: minmax(0, 1.06fr) minmax(320px, 0.94fr) !important;\n    align-items: flex-start !important;'
)

css = css.replace(
    '.cert-hero .hero-shell {\n    grid-template-columns: 1fr 1fr !important;\n    gap: 5rem !important;\n    align-items: center !important;',
    '.cert-hero .hero-shell {\n    grid-template-columns: 1fr 1fr !important;\n    gap: 5rem !important;\n    align-items: flex-start !important;'
)

css = css.replace(
    'align-items: start !important;',
    'align-items: flex-start !important;'
)

css = css.replace(
    'gap: 2rem !important;\n    align-items: flex-start !important;\n    width: 100% !important;',
    'gap: 4rem !important;\n    align-items: flex-start !important;\n    width: 100% !important;'
)

with open('vedtam.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated vedtam.css hero-shell alignments and gaps.")
