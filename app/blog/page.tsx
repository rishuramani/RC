import type { Metadata } from 'next';
import Link from 'next/link';
import BlogNavbar from '../components/BlogNavbar';
import BlogFooter from '../components/BlogFooter';

export const metadata: Metadata = {
  title: 'Market Insights | RC Investment Properties',
  description: 'Data-driven analysis of multifamily markets, investment trends, and operational strategies.',
};

export default function BlogPage() {
  return (
    <>
      <BlogNavbar />

      {/* Blog Hero */}
      <header className="blog-hero">
        <div className="container">
          <h1>Market Insights</h1>
          <p className="lead">Data-driven analysis of multifamily markets, investment trends, and operational strategies.</p>
        </div>
      </header>

      {/* Blog Content */}
      <main className="container">
        <div className="blog-grid">
          <div className="blog-posts">

            {/* Blog Post - Q4 2025 Market Update */}
            <article className="blog-card">
              <div className="blog-card-image">
                <span className="placeholder">Q4 2025 Data</span>
              </div>
              <div className="blog-card-content">
                <div className="blog-meta">
                  <span>January 2026</span>
                  <span>Market Analysis</span>
                </div>
                <h2><Link href="/blog/houston-q4-2025">Houston Q4 2025: Strong Absorption and Slowing Supply Signal Market Inflection</Link></h2>
                <p className="blog-excerpt">The latest Colliers data reveals a Houston multifamily market gaining momentum: occupancy up 200 basis points year-over-year to 90.4%, record annual absorption of 26,510 units, and a construction pipeline down 34%. The fundamentals are aligning for workforce housing investors.</p>
                <Link href="/blog/houston-q4-2025" className="read-more">{`Read More \u2192`}</Link>
              </div>
            </article>

            {/* Blog Post 1 */}
            <article className="blog-card">
              <div className="blog-card-image">
                <span className="placeholder">Houston Market</span>
              </div>
              <div className="blog-card-content">
                <div className="blog-meta">
                  <span>January 2025</span>
                  <span>Market Analysis</span>
                </div>
                <h2><Link href="/blog/houston-2025">Houston Multifamily: Why Workforce Housing Remains Resilient in 2025</Link></h2>
                <p className="blog-excerpt">{"Despite broader economic uncertainty, Houston's workforce housing segment continues to demonstrate strong fundamentals. We examine the factors driving rental demand and why sub-institutional assets offer compelling risk-adjusted returns."}</p>
                <Link href="/blog/houston-2025" className="read-more">{`Read More \u2192`}</Link>
              </div>
            </article>

          </div>

          {/* Sidebar */}
          <aside className="blog-sidebar">
            <div className="sidebar-widget">
              <h3>Categories</h3>
              <ul>
                <li><Link href="/blog">Market Analysis</Link></li>
                <li><Link href="/blog">Investment Strategy</Link></li>
                <li><Link href="/blog">Operations</Link></li>
              </ul>
            </div>

            <div className="sidebar-widget">
              <h3>Markets</h3>
              <ul>
                <li><Link href="/blog">Houston, TX</Link></li>
                <li><Link href="/blog">Phoenix, AZ</Link></li>
              </ul>
            </div>

            <div className="sidebar-widget">
              <h3>Key Metrics</h3>
              <ul>
                <li><strong>Target IRR:</strong> 18-25%</li>
                <li><strong>Equity Multiple:</strong> 2.0x+</li>
                <li><strong>Cash Return:</strong> 7-9%</li>
                <li><strong>Hold Period:</strong> 5-7 years</li>
              </ul>
            </div>

            <div className="sidebar-widget" style={{ background: 'var(--rc-green)', color: 'var(--white)' }}>
              <h3 style={{ color: 'var(--sage)', borderColor: 'var(--sage)' }}>Partner With Us</h3>
              <p style={{ fontSize: '14px', color: 'var(--sage-light)', marginBottom: '20px' }}>Interested in co-investing in our next opportunity?</p>
              <Link href="/#contact" className="btn btn-outline" style={{ color: 'var(--white)', borderColor: 'var(--white)', width: '100%', textAlign: 'center' }}>Get in Touch</Link>
            </div>
          </aside>
        </div>
      </main>

      <BlogFooter />
    </>
  );
}
