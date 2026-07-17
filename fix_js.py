import sys

def main():
    filename = 'assets/js/vedtam.js'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Keep up to line 1377 (index 0 to 1376)
        new_lines = lines[:1377]
        
        closing_code = """
      resetAutoRotate();
    }, 150); // Debounce scroll event
  });

  viewport.addEventListener('mouseenter', stopAutoRotate);
  viewport.addEventListener('mouseleave', startAutoRotate);
  viewport.addEventListener('touchstart', stopAutoRotate, { passive: true });
  viewport.addEventListener('touchend', resetAutoRotate, { passive: true });

  window.addEventListener('resize', () => {
    // On resize, re-center the current slide
    goToSlide(currentIndex);
  });

  // Initial update
  setTimeout(() => {
    // Ensure slides are rendered before calculating positions
    goToSlide(currentIndex);
    startAutoRotate();
  }, 100);
})();

// Prevent zoom on laptop/desktop (Ctrl+Scroll and Ctrl+/-)
document.addEventListener('keydown', function(e) {
  if (e.ctrlKey && (e.key === '+' || e.key === '-' || e.key === '=')) {
    e.preventDefault();
  }
});

document.addEventListener('wheel', function(e) {
  if (e.ctrlKey) {
    e.preventDefault();
  }
}, { passive: false });

// ==========================================================================
// Delayed Popup Modal (Triggers after 15 seconds on home page)
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
  const delayedModal = document.getElementById('delayedPopupModal');
  const closeDelayedBtn = document.getElementById('closeDelayedPopup');
  
  if (delayedModal) {
    // 15,000 milliseconds = 15 seconds
    const popupDelay = 15000; 

    setTimeout(() => {
      if (!sessionStorage.getItem('vedtamPopupShown')) {
        delayedModal.classList.add('active');
        document.body.classList.add('body-no-scroll');
        sessionStorage.setItem('vedtamPopupShown', 'true');
      }
    }, popupDelay);

    const closeDelayedModal = () => {
      delayedModal.classList.remove('active');
      document.body.classList.remove('body-no-scroll');
    };

    if (closeDelayedBtn) {
      closeDelayedBtn.addEventListener('click', closeDelayedModal);
    }

    delayedModal.addEventListener('click', (e) => {
      if (e.target === delayedModal) {
        closeDelayedModal();
      }
    });
  }
});
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
            if new_lines and not new_lines[-1].endswith('\n'):
                f.write('\n')
            f.write(closing_code)
            
        print("Fixed vedtam.js successfully! The syntax errors have been resolved.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
