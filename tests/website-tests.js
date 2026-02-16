/**
 * RC Investment Properties Website Tests
 * Tests for link validation, HTML structure, and best practices
 */

const fs = require('fs');
const path = require('path');

const WEBSITE_DIR = path.join(__dirname, '..');
const RESULTS = {
    passed: [],
    failed: [],
    warnings: []
};

// Helper functions
function readFile(filename) {
    const filepath = path.join(WEBSITE_DIR, filename);
    if (fs.existsSync(filepath)) {
        return fs.readFileSync(filepath, 'utf8');
    }
    return null;
}

function fileExists(filename) {
    return fs.existsSync(path.join(WEBSITE_DIR, filename));
}

function extractLinks(html) {
    const linkRegex = /href=["']([^"']+)["']/g;
    const links = [];
    let match;
    while ((match = linkRegex.exec(html)) !== null) {
        links.push(match[1]);
    }
    return links;
}

function extractScripts(html) {
    const scriptRegex = /src=["']([^"']+)["']/g;
    const scripts = [];
    let match;
    while ((match = scriptRegex.exec(html)) !== null) {
        scripts.push(match[1]);
    }
    return scripts;
}

function test(name, condition, errorMsg = '') {
    if (condition) {
        RESULTS.passed.push(name);
        console.log(`  ✓ ${name}`);
    } else {
        RESULTS.failed.push({ name, error: errorMsg });
        console.log(`  ✗ ${name}${errorMsg ? ': ' + errorMsg : ''}`);
    }
}

function warn(name, msg) {
    RESULTS.warnings.push({ name, msg });
    console.log(`  ⚠ ${name}: ${msg}`);
}

// ============================================
// TEST SUITES
// ============================================

console.log('\n========================================');
console.log('RC INVESTMENT PROPERTIES WEBSITE TESTS');
console.log('========================================\n');

// 1. File Existence Tests
console.log('📁 FILE EXISTENCE TESTS');
console.log('------------------------');

const requiredFiles = [
    'index.html',
    'blog.html',
    'css/style.css',
    'js/main.js'
];

requiredFiles.forEach(file => {
    test(`${file} exists`, fileExists(file), `File not found: ${file}`);
});

// 2. Internal Link Tests
console.log('\n🔗 INTERNAL LINK TESTS');
console.log('------------------------');

const htmlFiles = ['index.html', 'blog.html', 'post-houston-2025.html', 'post-houston-q4-2025-market-update.html'];
const brokenLinks = [];
const placeholderLinks = [];

htmlFiles.forEach(htmlFile => {
    const content = readFile(htmlFile);
    if (!content) return;

    const links = extractLinks(content);

    links.forEach(link => {
        // Skip external links and anchors
        if (link.startsWith('http') || link.startsWith('mailto:') || link.startsWith('tel:')) {
            return;
        }

        // Check for placeholder links
        if (link === '#') {
            placeholderLinks.push({ file: htmlFile, link });
            return;
        }

        // Check anchor links (skip validation for these as they're internal)
        if (link.startsWith('#')) {
            return;
        }

        // Check internal file links
        let targetFile = link.split('#')[0]; // Remove anchor part
        if (targetFile && !fileExists(targetFile)) {
            brokenLinks.push({ file: htmlFile, link: targetFile });
        }
    });
});

// Report broken links
if (brokenLinks.length === 0) {
    test('All internal links are valid', true);
} else {
    brokenLinks.forEach(({ file, link }) => {
        test(`Link in ${file}`, false, `Broken link: ${link}`);
    });
}

// Report placeholder links
if (placeholderLinks.length > 0) {
    placeholderLinks.forEach(({ file, link }) => {
        warn(`Placeholder link in ${file}`, 'Link points to "#" (placeholder)');
    });
}

// 3. CSS/JS Resource Tests
console.log('\n📄 RESOURCE LOADING TESTS');
console.log('------------------------');

htmlFiles.forEach(htmlFile => {
    const content = readFile(htmlFile);
    if (!content) return;

    // Check CSS links
    const cssLinks = content.match(/href=["']([^"']*\.css)["']/g) || [];
    cssLinks.forEach(match => {
        const cssFile = match.match(/href=["']([^"']+)["']/)[1];
        if (!cssFile.startsWith('http')) {
            test(`CSS in ${htmlFile}: ${cssFile}`, fileExists(cssFile), `CSS file not found: ${cssFile}`);
        }
    });

    // Check JS scripts
    const scripts = extractScripts(content);
    scripts.forEach(script => {
        if (!script.startsWith('http')) {
            test(`JS in ${htmlFile}: ${script}`, fileExists(script), `JS file not found: ${script}`);
        }
    });
});

// 4. HTML Structure Tests
console.log('\n📐 HTML STRUCTURE TESTS');
console.log('------------------------');

htmlFiles.forEach(htmlFile => {
    const content = readFile(htmlFile);
    if (!content) return;

    // Check for DOCTYPE
    test(`${htmlFile} has DOCTYPE`, content.includes('<!DOCTYPE html>'));

    // Check for meta viewport
    test(`${htmlFile} has viewport meta`, content.includes('viewport'));

    // Check for title
    test(`${htmlFile} has title`, content.includes('<title>') && content.includes('</title>'));

    // Check for lang attribute
    test(`${htmlFile} has lang attribute`, content.includes('lang="en"'));
});

// 5. Accessibility Tests
console.log('\n♿ ACCESSIBILITY TESTS');
console.log('------------------------');

const indexHtml = readFile('index.html');
if (indexHtml) {
    // Check for alt on images (if any)
    const imgTags = indexHtml.match(/<img[^>]+>/g) || [];
    const imagesWithoutAlt = imgTags.filter(img => !img.includes('alt='));
    test('All images have alt attributes', imagesWithoutAlt.length === 0,
        imagesWithoutAlt.length > 0 ? `${imagesWithoutAlt.length} images missing alt` : '');

    // Check for form labels
    const formInputs = indexHtml.match(/<input[^>]+id=["']([^"']+)["']/g) || [];
    const inputIds = formInputs.map(input => {
        const match = input.match(/id=["']([^"']+)["']/);
        return match ? match[1] : null;
    }).filter(Boolean);

    let allLabelsPresent = true;
    inputIds.forEach(id => {
        if (!indexHtml.includes(`for="${id}"`)) {
            allLabelsPresent = false;
        }
    });
    test('All form inputs have labels', allLabelsPresent);

    // Check for aria-label on mobile menu button
    test('Mobile menu has aria-label', indexHtml.includes('aria-label="Toggle menu"'));
}

// 6. SEO Tests
console.log('\n🔍 SEO TESTS');
console.log('------------------------');

htmlFiles.forEach(htmlFile => {
    const content = readFile(htmlFile);
    if (!content) return;

    // Check for h1
    const h1Count = (content.match(/<h1/g) || []).length;
    test(`${htmlFile} has exactly one h1`, h1Count === 1, `Found ${h1Count} h1 tags`);

    // Check meta charset
    test(`${htmlFile} has charset meta`, content.includes('charset="UTF-8"') || content.includes("charset='UTF-8'"));
});

// 7. Performance Tests
console.log('\n⚡ PERFORMANCE TESTS');
console.log('------------------------');

// Check CSS file size
const cssContent = readFile('css/style.css');
if (cssContent) {
    const cssSize = Buffer.byteLength(cssContent, 'utf8');
    test('CSS file under 50KB', cssSize < 50000, `CSS is ${(cssSize/1024).toFixed(1)}KB`);
}

// Check JS file size
const jsContent = readFile('js/main.js');
if (jsContent) {
    const jsSize = Buffer.byteLength(jsContent, 'utf8');
    test('JS file under 20KB', jsSize < 20000, `JS is ${(jsSize/1024).toFixed(1)}KB`);
}

// 8. Content Quality Tests
console.log('\n📝 CONTENT QUALITY TESTS');
console.log('------------------------');

if (indexHtml) {
    // Check contact form exists
    test('Contact form exists', indexHtml.includes('id="contactForm"'));

    // Check for company name consistency
    test('Company name in title', indexHtml.includes('RC Investment Properties'));

    // Check for required contact fields
    test('Name field exists', indexHtml.includes('id="name"'));
    test('Email field exists', indexHtml.includes('id="email"'));

    // Check for footer
    test('Footer exists', indexHtml.includes('<footer'));

    // Check for navigation
    test('Navigation exists', indexHtml.includes('<nav'));
}

// ============================================
// SUMMARY
// ============================================

console.log('\n========================================');
console.log('TEST SUMMARY');
console.log('========================================');
console.log(`✓ Passed: ${RESULTS.passed.length}`);
console.log(`✗ Failed: ${RESULTS.failed.length}`);
console.log(`⚠ Warnings: ${RESULTS.warnings.length}`);

if (RESULTS.failed.length > 0) {
    console.log('\n❌ FAILED TESTS:');
    RESULTS.failed.forEach(({ name, error }) => {
        console.log(`   - ${name}: ${error}`);
    });
}

if (RESULTS.warnings.length > 0) {
    console.log('\n⚠️  WARNINGS:');
    RESULTS.warnings.forEach(({ name, msg }) => {
        console.log(`   - ${name}: ${msg}`);
    });
}

console.log('\n');

// Exit with error code if there are failures
process.exit(RESULTS.failed.length > 0 ? 1 : 0);
