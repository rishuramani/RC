'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

export default function Home() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const closeMenu = () => setIsMenuOpen(false);

  return (
    <>
      {/* Navigation */}
      <nav className="navbar" style={{
        boxShadow: scrollY > 50 ? '0 2px 20px rgba(0,0,0,0.1)' : '0 2px 4px rgba(0,0,0,0.05)'
      }}>
        <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <a href="/" className="logo">RC Investment Properties</a>
          <button 
            className={`mobile-menu-btn ${isMenuOpen ? 'active' : ''}`}
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            aria-label="Toggle menu"
          >
            <span></span>
            <span></span>
            <span></span>
          </button>
          <ul className={`nav-links ${isMenuOpen ? 'active' : ''}`}>
            <li><a href="#about" onClick={closeMenu}>About</a></li>
            <li><a href="#portfolio" onClick={closeMenu}>Portfolio</a></li>
            <li><a href="#approach" onClick={closeMenu}>Approach</a></li>
            <li><Link href="/blog" onClick={closeMenu}>Insights</Link></li>
            <li><a href="#contact" className="btn-nav" onClick={closeMenu}>Contact</a></li>
          </ul>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="hero">
        <div className="container">
          <div className="hero-content">
            <p className="hero-label">Houston & Phoenix Multifamily</p>
            <h1>Sub-institutional in size.<br />Institutional in execution.</h1>
            <p className="hero-subtitle">We partner with family offices and high net worth individuals to invest in workforce multifamily housing across high-growth Sunbelt markets.</p>
            <div className="hero-stats">
              <div className="stat">
                <span className="stat-value">128+</span>
                <span className="stat-label">Units Managed</span>
              </div>
              <div className="stat">
                <span className="stat-value">$20M+</span>
                <span className="stat-label">Transaction Volume</span>
              </div>
              <div className="stat">
                <span className="stat-value">18-25%</span>
                <span className="stat-label">Target IRR</span>
              </div>
              <div className="stat">
                <span className="stat-value">2.0x+</span>
                <span className="stat-label">Target Multiple</span>
              </div>
            </div>
            <a href="#contact" className="btn btn-primary">Partner With Us</a>
          </div>
        </div>
      </header>

      {/* About Section */}
      <section id="about" className="section">
        <div className="container">
          <div className="section-header">
            <p className="section-label">Who We Are</p>
            <h2>A Boutique Approach to Multifamily Investment</h2>
          </div>
          <div className="about-grid">
            <div className="about-text">
              <p className="lead">RC Investment Properties is a privately held real estate investment company focused exclusively on acquiring, repositioning, and managing multifamily properties across high-growth Sunbelt markets.</p>
              <p>Our strategy centers on well-located workforce housing in established metros, with an emphasis on durable cash flow, downside protection, and disciplined basis acquisition.</p>
              <p>Founded by Michael Rosen and Bradley Couch, we deploy equity into differentiated opportunities that are often overlooked by institutional buyers but demand institutional-quality execution.</p>
            </div>
            <div className="about-highlights">
              <div className="highlight-card">
                <h4>Investment Focus</h4>
                <p>Workforce multifamily housing in supply-constrained, high-growth markets</p>
              </div>
              <div className="highlight-card">
                <h4>Deal Size</h4>
                <p>$5 million to $20 million per transaction</p>
              </div>
              <div className="highlight-card">
                <h4>Hold Period</h4>
                <p>Typically 5-7 years with flexibility for early exit</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Investment Thesis */}
      <section className="section section-alt">
        <div className="container">
          <div className="section-header">
            <p className="section-label">Our Thesis</p>
            <h2>How We Create Value</h2>
          </div>
          <div className="thesis-grid">
            <div className="thesis-card">
              <div className="thesis-number">01</div>
              <h3>Strategic Market Selection</h3>
              <p>We target high-growth, supply-constrained metros where structural demand supports rental growth and appreciation. Our focus areas include Houston and Phoenix.</p>
            </div>
            <div className="thesis-card">
              <div className="thesis-number">02</div>
              <h3>Workforce Housing Focus</h3>
              <p>We concentrate on housing for essential workers, teachers, and professionals—demographics with reliable income streams and sustainable rental demand.</p>
            </div>
            <div className="thesis-card">
              <div className="thesis-number">03</div>
              <h3>Value-Add Execution</h3>
              <p>Our team identifies underperforming assets with operational, capital, or repositioning upside and executes disciplined value-creation plans.</p>
            </div>
            <div className="thesis-card">
              <div className="thesis-number">04</div>
              <h3>Downside Protection</h3>
              <p>We emphasize sustainable cash flow, conservative underwriting, and sufficient equity cushion to weather market cycles and provide investor security.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Portfolio Section */}
      <section id="portfolio" className="section">
        <div className="container">
          <div className="section-header">
            <p className="section-label">Track Record</p>
            <h2>Proven Results</h2>
          </div>
          <div className="portfolio-grid">
            <div className="portfolio-card">
              <h3>Ashton Multifamily</h3>
              <p className="card-meta">Houston, TX | 64 Units</p>
              <p>Strategic repositioning of workforce housing in established Houston submarket. Target IRR: 21%</p>
            </div>
            <div className="portfolio-card">
              <h3>Phoenix Heights</h3>
              <p className="card-meta">Phoenix, AZ | 64 Units</p>
              <p>Value-add acquisition in high-growth Phoenix market with significant operational upside. Target IRR: 22%</p>
            </div>
          </div>
        </div>
      </section>

      {/* Approach Section */}
      <section id="approach" className="section section-alt">
        <div className="container">
          <div className="section-header">
            <p className="section-label">Investment Details</p>
            <h2>Our Approach</h2>
          </div>
          
          <div style={{ marginBottom: '60px' }}>
            <h3 style={{ marginBottom: '30px', fontSize: '1.5rem' }}>Investment Terms</h3>
            <div className="terms-grid">
              <div className="term-card">
                <h4>Target Returns</h4>
                <p className="term-value">18-25% IRR</p>
              </div>
              <div className="term-card">
                <h4>Target Equity Multiple</h4>
                <p className="term-value">2.0x - 2.5x</p>
              </div>
              <div className="term-card">
                <h4>Typical Hold Period</h4>
                <p className="term-value">5-7 Years</p>
              </div>
              <div className="term-card">
                <h4>Preferred Capital Structure</h4>
                <p className="term-value">50% Equity / 50% Debt</p>
              </div>
              <div className="term-card">
                <h4>Minimum Investment</h4>
                <p className="term-value">$500K - $2M</p>
              </div>
              <div className="term-card">
                <h4>Management Fee</h4>
                <p className="term-value">0.5% - 1.0% Annually</p>
              </div>
            </div>
          </div>

          <div>
            <h3 style={{ marginBottom: '30px', fontSize: '1.5rem' }}>Our Competitive Advantages</h3>
            <div className="advantages-grid">
              <div className="advantage-card">
                <h4>Market Expertise</h4>
                <p>Deep relationships and market knowledge in Houston and Phoenix, built over years of active investing.</p>
              </div>
              <div className="advantage-card">
                <h4>Operational Excellence</h4>
                <p>In-house property management capabilities and established relationships with best-in-class operators.</p>
              </div>
              <div className="advantage-card">
                <h4>Capital Efficiency</h4>
                <p>Lean, scalable organization enables competitive fee structures and prioritization of investor returns.</p>
              </div>
              <div className="advantage-card">
                <h4>Strategic Partnerships</h4>
                <p>Established relationships with lenders, brokers, and service providers ensure deal access and execution quality.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="section">
        <div className="container">
          <div className="section-header">
            <p className="section-label">Get In Touch</p>
            <h2>Ready to Partner?</h2>
          </div>
          <div className="contact-content">
            <div className="contact-form">
              <form>
                <div className="form-group">
                  <label htmlFor="name">Full Name</label>
                  <input type="text" id="name" name="name" required />
                </div>
                <div className="form-group">
                  <label htmlFor="email">Email Address</label>
                  <input type="email" id="email" name="email" required />
                </div>
                <div className="form-group">
                  <label htmlFor="phone">Phone Number</label>
                  <input type="tel" id="phone" name="phone" />
                </div>
                <div className="form-group">
                  <label htmlFor="message">Message</label>
                  <textarea id="message" name="message" rows={6}></textarea>
                </div>
                <button type="submit" className="btn btn-primary">Send Message</button>
              </form>
            </div>
            <div className="contact-info">
              <div className="info-block">
                <h4>Contact Information</h4>
                <p><strong>Email:</strong> hello@rcinvestmentproperties.com</p>
                <p><strong>Phone:</strong> (713) 555-0123</p>
              </div>
              <div className="info-block">
                <h4>Based In</h4>
                <p>Houston, Texas<br />Phoenix, Arizona</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-section">
              <h4>RC Investment Properties</h4>
              <p>Sub-institutional in size. Institutional in execution.</p>
            </div>
            <div className="footer-section">
              <h4>Navigation</h4>
              <ul>
                <li><a href="#about">About</a></li>
                <li><a href="#portfolio">Portfolio</a></li>
                <li><a href="#approach">Approach</a></li>
                <li><Link href="/blog">Insights</Link></li>
                <li><a href="#contact">Contact</a></li>
              </ul>
            </div>
            <div className="footer-section">
              <h4>Connect</h4>
              <ul>
                <li><a href="mailto:hello@rcinvestmentproperties.com">Email Us</a></li>
                <li><a href="tel:+17135550123">Call Us</a></li>
              </ul>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2024 RC Investment Properties. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </>
  );
}
