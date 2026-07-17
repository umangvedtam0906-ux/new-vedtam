const https = require('https');
https.get('https://www.cert-in.org.in/s2cMainServlet?pageid=PUBVLNOTES01&VLCODE=CIVN-2026-0187', (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
      const match = data.match(/Vendor Information([\s\S]*?)Disclaimer/i);
      if (match) {
         const links = match[1].match(/(http|https):\/\/[^\s<"']+/gi);
         console.log(links);
      }
  });
});
