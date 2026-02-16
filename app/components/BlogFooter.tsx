import Link from 'next/link';

export default function BlogFooter() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-brand">
            <span className="logo">RC Investment Properties</span>
            <p>Multifamily investment excellence in Houston and Phoenix.</p>
          </div>
          <div className="footer-links">
            <h4>Company</h4>
            <ul>
              <li><Link href="/#about">About</Link></li>
              <li><Link href="/#portfolio">Portfolio</Link></li>
              <li><Link href="/#approach">Approach</Link></li>
              <li><Link href="/#contact">Contact</Link></li>
            </ul>
          </div>
          <div className="footer-links">
            <h4>Resources</h4>
            <ul>
              <li><Link href="/blog">Market Insights</Link></li>
              <li><Link href="/#approach">Investment Criteria</Link></li>
              <li><Link href="/#contact">Contact Us</Link></li>
            </ul>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2025 RC Investment Properties. All rights reserved.</p>
          <p className="disclaimer">This website is for informational purposes only and does not constitute an offer to sell or a solicitation of an offer to buy any securities. Past performance is not indicative of future results.</p>
        </div>
      </div>
    </footer>
  );
}
