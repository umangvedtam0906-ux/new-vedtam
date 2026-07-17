const fs = require('fs');
const path = require('path');

const dirPath = "c:\\Users\\Manu\\Downloads\\new-vedtam-main (3)\\new-vedtam-main";

const pattern = /(<a[^>]*class="[^"]*nav-logo[^"]*"[^>]*>)\s*<img[^>]*class="logo-en"[^>]*src="([^"]*?)website-logo\/VEDTAM%20TECH%20SOLUTIONS%20en\.png"[^>]*>\s*<img[^>]*class="logo-hi"[^>]*src="([^"]*?)website-logo\/VEDTAM%20TECH%20SOLUTIONS%20hn\.png"[^>]*>\s*<\/a>/gi;

let count = 0;

function walkSync(currentDirPath) {
    fs.readdirSync(currentDirPath).forEach(function (name) {
        const filePath = path.join(currentDirPath, name);
        const stat = fs.statSync(filePath);
        if (stat.isFile() && filePath.endsWith('.html')) {
            let content = fs.readFileSync(filePath, 'utf8');
            let matched = false;
            let newContent = content.replace(pattern, (match, p1, p2, p3) => {
                matched = true;
                count++;
                return `${p1}
        <img alt="Vedtam Tech Solutions logo" decoding="async"
          src="${p2}website-logo/VEDTAM%20TECH%20SOLUTIONS%20en.png" 
          data-logo-switcher 
          data-logos="${p2}website-logo/VEDTAM%20TECH%20SOLUTIONS%20en.png, ${p2}website-logo/VEDTAM%20TECH%20SOLUTIONS%20hn.png" />
      </a>`;
            });
            if (matched) {
                fs.writeFileSync(filePath, newContent, 'utf8');
            }
        } else if (stat.isDirectory()) {
            walkSync(filePath);
        }
    });
}

walkSync(dirPath);
console.log(`Replaced ${count} instances of the old logo tags.`);
