import os

css_path = r"c:\Users\Manu\Downloads\vedtam-main (2) (1)\vedtam-main (9)\vedtam-main\assets\css\vedtam.css"
css_content = """
/* Creative Testimonials UI Enhancements */
#testimonials .tm-card-premium {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(15px) !important;
  -webkit-backdrop-filter: blur(15px) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease !important;
  position: relative !important;
  overflow: hidden !important;
}

#testimonials .tm-card-premium::before {
  content: '' !important;
  position: absolute !important;
  top: 0 !important;
  left: -100% !important;
  width: 50% !important;
  height: 100% !important;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent) !important;
  transform: skewX(-20deg) !important;
  transition: left 0.7s ease !important;
}

#testimonials .tm-card-premium:hover::before {
  left: 200% !important;
}

#testimonials .tm-card-premium:hover {
  transform: translateY(-10px) scale(1.02) !important;
  box-shadow: 0 15px 40px rgba(0, 195, 255, 0.2), 0 0 20px rgba(0, 195, 255, 0.1) inset !important;
  border: 1px solid rgba(0, 195, 255, 0.3) !important;
}

#testimonials .tm-text {
  color: #ffffff !important;
  font-weight: 400 !important;
  line-height: 1.6 !important;
  text-shadow: 0 1px 2px rgba(0,0,0,0.5) !important;
  position: relative !important;
  z-index: 1 !important;
}

#testimonials .tm-name {
  color: #00c3ff !important;
  font-weight: 700 !important;
  letter-spacing: 1px !important;
  text-transform: uppercase !important;
  margin-top: 15px !important;
  position: relative !important;
  z-index: 1 !important;
}

#testimonials .tm-quote-left, #testimonials .tm-quote-right {
  color: rgba(255, 255, 255, 0.15) !important;
  font-size: 4rem !important;
  line-height: 0.8 !important;
}
"""

with open(css_path, "a", encoding="utf-8") as f:
    f.write(css_content)

print("Testimonial CSS appended successfully!")
