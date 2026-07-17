import { request } from 'node:https';

request('https://www.cert-in.org.in/s2cMainServlet?pageid=VLNLIST01&year=2026', (res) => {
  let html = '';
  res.on('data', (c) => html += c);
  res.on('end', () => {
    const urls = html.match(/(?:href|HREF)\s*=\s*['"]([^'"]+)['"]/gi) || [];
    console.log('CIVNs in VLNLIST02:', urls.filter(u => u.includes('CIVN-2026')).length);
  });
}).end();
