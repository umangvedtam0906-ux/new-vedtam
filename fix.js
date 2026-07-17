const fs = require('fs');
const path = require('path');

const baseDir = __dirname;
const faLink = '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />\n';

function walkSync(dir, callback) {
    fs.readdirSync(dir).forEach(file => {
        const dirPath = path.join(dir, file);
        if (fs.statSync(dirPath).isDirectory()) {
            walkSync(dirPath, callback);
        } else {
            callback(dirPath);
        }
    });
}

walkSync(baseDir, (filePath) => {
    if (!filePath.endsWith('.html')) return;
    
    let content = fs.readFileSync(filePath, 'utf-8');
    let modified = false;

    // Fix Font Awesome
    if (!content.includes('font-awesome') && !content.includes('all.min.css')) {
        if (content.includes('</head>')) {
            content = content.replace('</head>', faLink + '</head>');
            modified = true;
        }
    }

    // Fix Footer Icons
    const locPattern = /<span\s+class="fc-icon">✓<\/span>/g;
    if (locPattern.test(content)) {
        content = content.replace(locPattern, '<i class="fas fa-map-marker-alt fc-icon"></i>');
        modified = true;
    }

    const emailPattern = /<span\s+class="fc-icon">âœ‰<\/span>/g;
    if (emailPattern.test(content)) {
        content = content.replace(emailPattern, '<i class="fas fa-envelope fc-icon"></i>');
        modified = true;
    }

    const phonePattern = /<span\s+class="fc-icon">â˜Ž<\/span>/g;
    if (phonePattern.test(content)) {
        content = content.replace(phonePattern, '<i class="fas fa-phone fc-icon"></i>');
        modified = true;
    }

    if (modified) {
        fs.writeFileSync(filePath, content, 'utf-8');
        console.log(`Fixed: ${filePath}`);
    }
});
