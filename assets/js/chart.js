const ctx = document.getElementById('chart');

new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ['High', 'Medium', 'Low'],
    datasets: [{
      data: [high, medium, low]
    }]
  }
});