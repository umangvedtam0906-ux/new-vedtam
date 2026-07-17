class NetworkNodeSystem {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.nodes = [];
    this.connections = [];
    this.width = window.innerWidth;
    this.height = window.innerHeight;
    this.mouse = { x: null, y: null, radius: 120 };
    
    this.init();
    this.animate();
    
    window.addEventListener('resize', () => {
      this.width = window.innerWidth;
      this.height = window.innerHeight;
      this.canvas.width = this.width;
      this.canvas.height = this.height;
      this.initNodes();
    });
    
    const container = this.canvas.closest('.netsec-hero') || this.canvas.parentElement;
    
    container.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      this.mouse.x = e.clientX - rect.left;
      this.mouse.y = e.clientY - rect.top;
    });
    
    container.addEventListener('mouseleave', () => {
      this.mouse.x = null;
      this.mouse.y = null;
    });
  }

  init() {
    this.canvas.width = this.width;
    this.canvas.height = this.height;
    this.initNodes();
  }

  initNodes() {
    this.nodes = [];
    let numNodes = (this.width * this.height) / 4000;
    for(let i=0; i<numNodes; i++) {
      let x = Math.random() * this.width;
      let y = Math.random() * this.height;
      let vx = (Math.random() - 0.5) * 1.5;
      let vy = (Math.random() - 0.5) * 1.5;
      let size = Math.random() * 2 + 1;
      this.nodes.push({x, y, vx, vy, size});
    }
  }

  draw() {
    this.ctx.clearRect(0, 0, this.width, this.height);
    
    // Update and draw nodes
    for(let i=0; i<this.nodes.length; i++) {
      let node = this.nodes[i];
      
      // Move
      node.x += node.vx;
      node.y += node.vy;
      
      // Bounce
      if(node.x < 0 || node.x > this.width) node.vx *= -1;
      if(node.y < 0 || node.y > this.height) node.vy *= -1;
      
      // Mouse interaction
      if(this.mouse.x != null) {
        let dx = this.mouse.x - node.x;
        let dy = this.mouse.y - node.y;
        let dist = Math.sqrt(dx*dx + dy*dy);
        
        if(dist < this.mouse.radius) {
          let forceDirectionX = dx / dist;
          let forceDirectionY = dy / dist;
          let force = (this.mouse.radius - dist) / this.mouse.radius;
          
          // If very close, repel to prevent clumping
          if (dist < 50) {
            node.vx -= forceDirectionX * force * 3.0;
            node.vy -= forceDirectionY * force * 3.0;
          } else {
            // Attract to mouse
            node.vx += forceDirectionX * force * 1.5;
            node.vy += forceDirectionY * force * 1.5;
          }
          
          // Draw connecting laser to mouse
          this.ctx.beginPath();
          this.ctx.strokeStyle = `rgba(14, 165, 233, ${0.9 - (dist/this.mouse.radius)*0.9})`;
          this.ctx.lineWidth = 2.0;
          this.ctx.moveTo(node.x, node.y);
          this.ctx.lineTo(this.mouse.x, this.mouse.y);
          this.ctx.stroke();
        }
      }
      
      // Dynamic Speed limit
      let maxSpeed = 1.5;
      if (this.mouse.x != null) {
         let dx = this.mouse.x - node.x;
         let dy = this.mouse.y - node.y;
         if (Math.sqrt(dx*dx + dy*dy) < this.mouse.radius) {
            maxSpeed = 5; // Allow fast swarming
         }
      }
      
      let speed = Math.sqrt(node.vx*node.vx + node.vy*node.vy);
      if(speed > maxSpeed) {
        node.vx = (node.vx/speed) * maxSpeed;
        node.vy = (node.vy/speed) * maxSpeed;
      }
      
      // Draw node
      this.ctx.beginPath();
      this.ctx.arc(node.x, node.y, node.size, 0, Math.PI * 2);
      this.ctx.fillStyle = 'rgba(56, 189, 248, 0.8)';
      this.ctx.fill();
    }
    
    // Draw connections
    for(let a=0; a<this.nodes.length; a++) {
      for(let b=a+1; b<this.nodes.length; b++) {
        let dx = this.nodes[a].x - this.nodes[b].x;
        let dy = this.nodes[a].y - this.nodes[b].y;
        let dist = Math.sqrt(dx*dx + dy*dy);
        
        if(dist < 150) {
          this.ctx.beginPath();
          this.ctx.strokeStyle = `rgba(14, 165, 233, ${1 - dist/150})`;
          this.ctx.lineWidth = 1;
          this.ctx.moveTo(this.nodes[a].x, this.nodes[a].y);
          this.ctx.lineTo(this.nodes[b].x, this.nodes[b].y);
          this.ctx.stroke();
        }
      }
    }
  }

  animate() {
    this.draw();
    requestAnimationFrame(() => this.animate());
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('netsecCanvas');
  if(canvas) {
    new NetworkNodeSystem(canvas);
  }
});
