import sys

css_to_append = """
/* Cyber Overview Section Styling */
.cyber-overview-section {
  padding: 5rem 0;
  position: relative;
}

.cyber-overview-grid {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 4rem;
  align-items: center;
}

.cyber-overview-copy {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.cyber-overview-copy .section-label {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  background: rgba(0, 163, 217, 0.1);
  color: var(--cyan);
  border: 1px solid rgba(0, 163, 217, 0.2);
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  width: max-content;
}

.cyber-overview-copy .section-heading {
  font-size: clamp(2rem, 3vw, 2.8rem);
  font-weight: 700;
  line-height: 1.2;
  margin: 0;
  color: var(--white);
}

.cyber-overview-copy .section-heading span {
  color: var(--accent-green);
  display: block;
}

.cyber-overview-copy .section-sub {
  font-size: 1.1rem;
  line-height: 1.7;
  color: var(--off);
  margin: 0;
}

/* Premium Card */
.cyber-overview-card {
  background: rgba(13, 21, 32, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.cyber-card-top {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--white);
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.cyber-stack-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.cyber-stack-item {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  padding-left: 1.5rem;
  position: relative;
}

.cyber-stack-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 8px;
  width: 8px;
  height: 8px;
  background: var(--accent-green);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--accent-green);
}

.cyber-stack-item strong {
  font-size: 1.1rem;
  color: var(--white);
}

.cyber-stack-item span {
  font-size: 0.95rem;
  color: var(--muted);
  line-height: 1.5;
}

@media (max-width: 992px) {
  .cyber-overview-grid {
    grid-template-columns: 1fr;
    gap: 3.5rem;
  }
}

@media (max-width: 576px) {
  .cyber-overview-section {
    padding: 3.5rem 0;
  }
  .cyber-overview-card {
    padding: 1.8rem;
  }
}
"""

with open(r"c:\Users\Manu\Desktop\vedtam website\vedtam.css", "a", encoding="utf-8") as f:
    f.write(css_to_append)

print("CSS appended.")
