// Force Field Background - Vanilla JS implementation
// Ported from React component for vanilla HTML/JS integration

function initForceField(containerId, options = {}) {
  const container = document.getElementById(containerId);
  if (!container) return null;

  // Make sure container has relative positioning so canvas can fill it
  if (getComputedStyle(container).position === 'static') {
    container.style.position = 'relative';
  }

  const config = {
    imageUrl: options.imageUrl || 'services_images/service_cyber_security_1774586735180.png',
    hue: options.hue !== undefined ? options.hue : 210,
    saturation: options.saturation !== undefined ? options.saturation : 100,
    threshold: options.threshold !== undefined ? options.threshold : 255,
    minStroke: options.minStroke !== undefined ? options.minStroke : 2,
    maxStroke: options.maxStroke !== undefined ? options.maxStroke : 6,
    spacing: options.spacing !== undefined ? options.spacing : 10,
    noiseScale: options.noiseScale !== undefined ? options.noiseScale : 0,
    density: options.density !== undefined ? options.density : 2.0,
    invertImage: options.invertImage !== undefined ? options.invertImage : true,
    invertWireframe: options.invertWireframe !== undefined ? options.invertWireframe : true,
    magnifierEnabled: options.magnifierEnabled !== undefined ? options.magnifierEnabled : true,
    magnifierRadius: options.magnifierRadius !== undefined ? options.magnifierRadius : 150,
    forceStrength: options.forceStrength !== undefined ? options.forceStrength : 15,
    friction: options.friction !== undefined ? options.friction : 0.9,
    restoreSpeed: options.restoreSpeed !== undefined ? options.restoreSpeed : 0.05
  };

  const sketch = (p) => {
    let originalImg;
    let img;
    let palette = [];
    let points = [];
    let magnifierX = 0;
    let magnifierY = 0;
    let magnifierInertia = 0.1;

    p.preload = () => {
      originalImg = p.loadImage(config.imageUrl);
    };

    p.setup = () => {
      const rect = container.getBoundingClientRect();
      let canvas = p.createCanvas(rect.width || window.innerWidth, rect.height || window.innerHeight);
      canvas.style('position', 'absolute');
      canvas.style('inset', '0');
      canvas.style('z-index', '-1');
      magnifierX = p.width / 2;
      magnifierY = p.height / 2;

      processImage();
      generatePalette(config.hue, config.saturation);
      generatePoints();
    };

    p.windowResized = () => {
      const rect = container.getBoundingClientRect();
      p.resizeCanvas(rect.width || window.innerWidth, rect.height || window.innerHeight);
      processImage();
      generatePoints();
    };

    function processImage() {
      if (!originalImg) return;
      img = originalImg.get();
      if (p.width > 0 && p.height > 0) {
        img.resize(p.width, p.height);
      }
      img.filter(p.GRAY);

      if (config.invertImage) {
        img.loadPixels();
        for (let i = 0; i < img.pixels.length; i += 4) {
          img.pixels[i] = 255 - img.pixels[i];
          img.pixels[i + 1] = 255 - img.pixels[i + 1];
          img.pixels[i + 2] = 255 - img.pixels[i + 2];
        }
        img.updatePixels();
      }
    }

    function generatePalette(h, s) {
      palette = [];
      p.push();
      p.colorMode(p.HSL);
      for (let i = 0; i < 12; i++) {
        let lightness = p.map(i, 0, 11, 95, 5);
        palette.push(p.color(h, s, lightness));
      }
      p.pop();
    }

    function generatePoints() {
      if (!img) return;
      points = [];
      const safeSpacing = Math.max(2, config.spacing); 

      for (let y = 0; y < img.height; y += safeSpacing) {
        for (let x = 0; x < img.width; x += safeSpacing) {
          if (p.random() > config.density) continue;
          
          let nx = p.noise(x * config.noiseScale, y * config.noiseScale) - 0.5;
          let ny = p.noise((x + 500) * config.noiseScale, (y + 500) * config.noiseScale) - 0.5;
          let px = x + nx * safeSpacing;
          let py = y + ny * safeSpacing;
          
          points.push({
            pos: p.createVector(px, py),
            originalPos: p.createVector(px, py),
            vel: p.createVector(0, 0)
          });
        }
      }
    }

    function applyForceField(mx, my) {
      if (!config.magnifierEnabled) return;

      for (let pt of points) {
        let dir = p5.Vector.sub(pt.pos, p.createVector(mx, my));
        let d = dir.mag();
        
        if (d < config.magnifierRadius) {
          dir.normalize();
          let force = dir.mult(config.forceStrength / Math.max(1, d));
          pt.vel.add(force);
        }
        
        pt.vel.mult(config.friction);
        
        let restore = p5.Vector.sub(pt.pos, pt.originalPos).mult(-config.restoreSpeed);
        pt.vel.add(restore);
        
        pt.pos.add(pt.vel);
      }
    }

    p.draw = () => {
      if (!img) return;
      p.clear();

      magnifierX = p.lerp(magnifierX, p.mouseX, magnifierInertia);
      magnifierY = p.lerp(magnifierY, p.mouseY, magnifierInertia);

      applyForceField(magnifierX, magnifierY);

      img.loadPixels();
      p.noFill();

      for (let pt of points) {
        let x = pt.pos.x;
        let y = pt.pos.y;
        let d = p.dist(x, y, magnifierX, magnifierY);
        
        let px = p.constrain(p.floor(x), 0, img.width - 1);
        let py = p.constrain(p.floor(y), 0, img.height - 1);
        
        let index = (px + py * img.width) * 4;
        let brightness = img.pixels[index]; 
        
        if (brightness === undefined) continue;

        let condition = config.invertWireframe
          ? brightness < config.threshold
          : brightness > config.threshold;

        if (condition) {
          let shadeIndex = Math.floor(p.map(brightness, 0, 255, 0, palette.length - 1));
          shadeIndex = p.constrain(shadeIndex, 0, palette.length - 1);
          
          let strokeSize = p.map(brightness, 0, 255, config.minStroke, config.maxStroke);
          
          if (config.magnifierEnabled && d < config.magnifierRadius) {
            let factor = p.map(d, 0, config.magnifierRadius, 2, 1);
            strokeSize *= factor;
          }
          
          if (palette[shadeIndex]) {
            p.stroke(palette[shadeIndex]);
            p.strokeWeight(strokeSize);
            p.point(x, y);
          }
        }
      }
    };
  };

  return new p5(sketch, container);
}

// Auto-initialize if #force-field-bg exists
document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("force-field-bg")) {
    initForceField("force-field-bg");
  }
});
