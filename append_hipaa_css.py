import sys
css_to_append = """
/* HIPAA Shield Hologram */
.hipaa-shield-hologram {
  position: relative;
  width: 100%;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  perspective: 1000px;
}
@media (min-width: 992px) {
  .hipaa-shield-hologram { height: 500px; }
}
.medical-cross-core {
  position: relative;
  width: 80px;
  height: 80px;
  z-index: 5;
  filter: drop-shadow(0 0 15px var(--primary));
  animation: float 4s ease-in-out infinite;
}
.cross-vert, .cross-horiz {
  position: absolute;
  background: var(--primary);
  border-radius: 4px;
}
.cross-vert {
  width: 24px;
  height: 80px;
  left: 50%;
  top: 0;
  transform: translateX(-50%);
}
.cross-horiz {
  width: 80px;
  height: 24px;
  top: 50%;
  left: 0;
  transform: translateY(-50%);
}

.shield-ring {
  position: absolute;
  width: 240px;
  height: 240px;
  border: 2px dashed var(--primary);
  opacity: 0.5;
  border-radius: 50%;
  animation: spin 15s linear infinite;
}
.shield-scanner {
  position: absolute;
  width: 100%;
  height: 2px;
  background: var(--primary);
  top: 50%;
  box-shadow: 0 0 15px var(--primary);
  animation: scan-vertical 4s ease-in-out infinite alternate;
}

.outer-orbit-medical {
  position: absolute;
  width: 340px;
  height: 340px;
  border: 1px solid transparent;
  border-radius: 50%;
  border-top: 1px solid var(--primary);
  border-bottom: 1px solid var(--primary);
  opacity: 0.3;
  animation: spin 20s linear infinite reverse;
}

@keyframes scan-vertical {
  0% { transform: translateY(-110px); }
  100% { transform: translateY(110px); }
}
"""

with open(r"c:\Users\Manu\Desktop\vedtam website\vedtam.css", "a", encoding="utf-8") as f:
    f.write(css_to_append)

print("HIPAA CSS appended.")
