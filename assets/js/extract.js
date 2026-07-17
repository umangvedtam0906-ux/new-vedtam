const fs = require('fs');
const html = fs.readFileSync('C:\\Users\\Manu\\.gemini\\antigravity-ide\\brain\\c51cc468-df70-481b-afd3-cc5ca5b5639d\\.system_generated\\steps\\5\\content.md', 'utf8');

// simple regex to strip tags
const text = html.replace(/<style[^>]*>.*?<\/style>/gi, '')
    .replace(/<script[^>]*>.*?<\/script>/gi, '')
    .replace(/<[^>]+>/g, '\n')
    .replace(/\n\s*\n/g, '\n')
    .trim();

fs.writeFileSync('C:\\Users\\Manu\\Desktop\\vedtam website\\extracted_text.txt', text, 'utf8');
console.log('done');
