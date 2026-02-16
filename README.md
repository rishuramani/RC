# RC Investment Properties - Website

A professional investor-facing website for RC Investment Properties, showcasing multifamily investment capabilities, portfolio, and market insights.

## Quick Start

### Option 1: Python (Recommended)

If you have Python installed, open a terminal in this directory and run:

```bash
# Python 3
python -m http.server 8000

# Or Python 2
python -m SimpleHTTPServer 8000
```

Then open your browser to: **http://localhost:8000**

### Option 2: Node.js

If you have Node.js installed:

```bash
# Install a simple server globally (one time)
npm install -g serve

# Run the server
serve .
```

### Option 3: VS Code Live Server

1. Install the "Live Server" extension in VS Code
2. Right-click `index.html` and select "Open with Live Server"

### Option 4: Direct File Access

Simply double-click `index.html` to open in your browser. Note: Some features may not work correctly due to browser security restrictions on local files.

## Project Structure

```
website/
├── index.html              # Main homepage
├── blog.html               # Blog listing page
├── post-houston-2025.html  # Sample blog post
├── css/
│   └── style.css           # Main stylesheet
├── js/
│   └── main.js             # JavaScript functionality
└── README.md               # This file
```

## Pages

- **Homepage** (`index.html`) - Company overview, investment thesis, portfolio, team, and contact form
- **Blog** (`blog.html`) - Market insights and analysis articles
- **Blog Post** (`post-houston-2025.html`) - Sample article on Houston market

## Features

- Fully responsive design (desktop, tablet, mobile)
- Smooth scroll navigation
- Mobile hamburger menu
- Contact form (frontend only - requires backend integration for production)
- Brand-compliant styling (RC Green #0A4E44, Georgia/Open Sans typography)
- Professional, non-promotional tone

## Customization

### Colors

Edit the CSS variables in `css/style.css`:

```css
:root {
    --rc-green: #0A4E44;
    --rc-green-dark: #083d36;
    --sage: #8FB3A9;
    --sage-light: #c5d9d4;
    --light-bg: #F5F7F6;
    --text: #2D2D2D;
    --muted: #6B7B75;
}
```

### Fonts

The site uses Google Fonts (Libre Baskerville for headings, Open Sans for body). To change fonts, update the `<link>` tag in the HTML files and the CSS variables.

### Content

- Edit `index.html` to update company information, portfolio, and team details
- Add new blog posts by duplicating `post-houston-2025.html` and updating content
- Update `blog.html` to add links to new posts

## Production Deployment

For production deployment, consider:

1. **Static Hosting**: Netlify, Vercel, GitHub Pages, AWS S3 + CloudFront
2. **Form Backend**: Formspree, Netlify Forms, or custom API
3. **Images**: Add actual property photos to an `images/` directory
4. **Analytics**: Add Google Analytics or similar tracking
5. **SSL**: Ensure HTTPS is enabled

### Netlify Deployment

1. Push code to GitHub
2. Connect repository to Netlify
3. Deploy automatically on push

### Manual Upload

1. Upload all files to your web server
2. Ensure `index.html` is served as the default document

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome for Android)

## Contact

RC Investment Properties
Houston, Texas

---

*This website is for informational purposes only and does not constitute an offer to sell or a solicitation of an offer to buy any securities.*
