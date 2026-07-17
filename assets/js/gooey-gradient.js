document.addEventListener("DOMContentLoaded", () => {
  const wrapper = document.querySelector('.gooey-wrapper');
  const interactive = document.querySelector('.gooey-wrapper .interactive');
  
  if (!interactive || !wrapper) return;

  let curX = 0;
  let curY = 0;
  let tgX = 0;
  let tgY = 0;

  const handleMouseMove = (event) => {
    const rect = wrapper.getBoundingClientRect();
    tgX = event.clientX - rect.left;
    tgY = event.clientY - rect.top;
  };

  const animate = () => {
    curX += (tgX - curX) / 20;
    curY += (tgY - curY) / 20;
    
    interactive.style.transform = `translate(${Math.round(curX)}px, ${Math.round(curY)}px)`;
    requestAnimationFrame(animate);
  };

  window.addEventListener('mousemove', handleMouseMove);
  animate();
});
