import Link from 'next/link';
import ClientScripts from './components/ClientScripts';

export default function Home() {
  return (
    <>
      <ClientScripts />

      {/* Navigation */}
      <nav className="navbar">
        <div className="container">
          <Link href="/" className="logo">RC Investment Properties</Link>
          <ul className="nav-links">
            <li><a href="#about">About</a></li>
            <li><a href="#portfolio">Portfolio</a></li>
            <li><a href="#approach">Approach</a></li>
            <li><Link href="/blog">Insights</Link></li>
            <li><a href="#contact" className="btn-nav">Contact</a></li>
          </ul>
          <button className="mobile-menu-btn" aria-label="Toggle menu">
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="hero">
        <div className="container">
          <div className="hero-content">
            <p className="hero-label">Houston &amp; Phoenix Multifamily</p>
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
              <h3>Sub-Institutional Advantage</h3>
              <p>We target assets where institutional competition is limited and pricing inefficiencies exist. Deals between $5M-$20M are often too small for institutional buyers but too large for individual investors.</p>
            </div>
            <div className="thesis-card">
              <div className="thesis-number">02</div>
              <h3>Low Basis Acquisitions</h3>
              <p>Every acquisition targets a meaningful discount to replacement cost, creating an immediate equity cushion and enhancing downside protection for our investors.</p>
            </div>
            <div className="thesis-card">
              <div className="thesis-number">03</div>
              <h3>Hands-On Value Creation</h3>
              <p>We create value through active asset management, operational improvements, and strategic capital deployment rather than relying on market speculation or cap rate compression.</p>
            </div>
            <div className="thesis-card">
              <div className="thesis-number">04</div>
              <h3>Cash Flow First</h3>
              <p>Durable in-place cash flow reduces reliance on exit assumptions. We underwrite to conservative scenarios and target 7-9% average annual cash returns.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Track Record */}
      <section className="section">
        <div className="container">
          <div className="section-header">
            <p className="section-label">Track Record</p>
            <h2>Proven Performance</h2>
          </div>
          <div className="track-record-highlight">
            <div className="track-record-content">
              <div className="track-record-stat">
                <span className="big-number">43.4%</span>
                <span className="stat-description">Value Increase on Full-Cycle Exit</span>
              </div>
              <div className="track-record-details">
                <h3>8601 Meta Street | Houston, TX</h3>
                <p>24-unit property acquired at $55,000 per unit and sold at $79,000 per unit after an 18-month hold. Capital was recycled via 1031 exchange into Phoenix.</p>
                <div className="detail-stats">
                  <div className="detail-stat">
                    <span className="label">Acquired</span>
                    <span className="value">$1.325M</span>
                  </div>
                  <div className="detail-stat">
                    <span className="label">Sold</span>
                    <span className="value">$1.9M</span>
                  </div>
                  <div className="detail-stat">
                    <span className="label">Hold Period</span>
                    <span className="value">18 Months</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Portfolio Section */}
      <section id="portfolio" className="section section-alt">
        <div className="container">
          <div className="section-header">
            <p className="section-label">Current Holdings</p>
            <h2>Active Portfolio</h2>
          </div>
          <div className="portfolio-grid">
            <div className="portfolio-card">
              <div className="portfolio-header">
                <h3>101 Avondale Street</h3>
                <span className="location">Houston, TX</span>
              </div>
              <div className="portfolio-stats">
                <div className="portfolio-stat">
                  <span className="value">19</span>
                  <span className="label">Units</span>
                </div>
                <div className="portfolio-stat">
                  <span className="value">$92K</span>
                  <span className="label">Per Unit</span>
                </div>
                <div className="portfolio-stat highlight">
                  <span className="value">19.7%</span>
                  <span className="label">AAR</span>
                </div>
              </div>
              <p className="portfolio-description">Value-add repositioning acquired December 2023. Strong performance through first two years of ownership.</p>
            </div>

            <div className="portfolio-card">
              <div className="portfolio-header">
                <h3>414 Marshall Street</h3>
                <span className="location">Houston, TX</span>
              </div>
              <div className="portfolio-stats">
                <div className="portfolio-stat">
                  <span className="value">27</span>
                  <span className="label">Units</span>
                </div>
                <div className="portfolio-stat">
                  <span className="value">$85K</span>
                  <span className="label">Per Unit</span>
                </div>
                <div className="portfolio-stat highlight">
                  <span className="value">~40%</span>
                  <span className="label">Target IRR</span>
                </div>
              </div>
              <p className="portfolio-description">Fully off-market acquisition with 50% seller financing. Direct-to-seller sourcing. Targeting 2026 exit at ~$120,000/unit.</p>
            </div>

            <div className="portfolio-card">
              <div className="portfolio-header">
                <h3>1218 Jackson Boulevard</h3>
                <span className="location">Houston, TX</span>
              </div>
              <div className="portfolio-stats">
                <div className="portfolio-stat">
                  <span className="value">26</span>
                  <span className="label">Units</span>
                </div>
                <div className="portfolio-stat">
                  <span className="value">$125K</span>
                  <span className="label">Per Unit</span>
                </div>
                <div className="portfolio-stat highlight">
                  <span className="value">6.5%+</span>
                  <span className="label">CoC</span>
                </div>
              </div>
              <p className="portfolio-description">Loan distress acquisition with mission-driven financing. Year 1 cash-on-cash trending toward 7%+.</p>
            </div>

            <div className="portfolio-card">
              <div className="portfolio-header">
                <h3>1541 Moritz Drive</h3>
                <span className="location">Houston, TX</span>
              </div>
              <div className="portfolio-stats">
                <div className="portfolio-stat">
                  <span className="value">56</span>
                  <span className="label">Units</span>
                </div>
                <div className="portfolio-stat">
                  <span className="value">$87.5K</span>
                  <span className="label">Per Unit</span>
                </div>
                <div className="portfolio-stat highlight">
                  <span className="value">9.3%</span>
                  <span className="label">Y1 Return</span>
                </div>
              </div>
              <p className="portfolio-description">The Oaks of Moritz. Loan distress acquisition December 2025. Strong initial year performance.</p>
            </div>

            <div className="portfolio-card">
              <div className="portfolio-header">
                <h3>3406 N 38th Street</h3>
                <span className="location">Phoenix, AZ</span>
              </div>
              <div className="portfolio-stats">
                <div className="portfolio-stat">
                  <span className="value">15</span>
                  <span className="label">Units</span>
                </div>
                <div className="portfolio-stat">
                  <span className="value">$211K</span>
                  <span className="label">Per Unit</span>
                </div>
                <div className="portfolio-stat highlight">
                  <span className="value">5%</span>
                  <span className="label">Annual</span>
                </div>
              </div>
              <p className="portfolio-description">Arcadia Lite submarket. Acquired via 1031 exchange. Capital preservation focus in premium Phoenix location.</p>
            </div>
          </div>

          <div className="portfolio-summary">
            <div className="summary-stat">
              <span className="value">143</span>
              <span className="label">Total Units</span>
            </div>
            <div className="summary-stat">
              <span className="value">5</span>
              <span className="label">Properties</span>
            </div>
            <div className="summary-stat">
              <span className="value">2</span>
              <span className="label">Markets</span>
            </div>
            <div className="summary-stat">
              <span className="value">$20M+</span>
              <span className="label">Transaction Volume</span>
            </div>
          </div>
        </div>
      </section>

      {/* Markets Section */}
      <section className="section">
        <div className="container">
          <div className="section-header">
            <p className="section-label">Geographic Focus</p>
            <h2>Target Markets</h2>
          </div>
          <div className="markets-grid">
            <div className="market-card">
              <div className="market-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                  <circle cx="12" cy="10" r="3"></circle>
                </svg>
              </div>
              <h3>Houston, Texas</h3>
              <p>{"Nation's fourth-largest metro with sustained population and job growth. Diversified economy spanning energy, healthcare, aerospace, and technology reduces single-sector risk."}</p>
              <ul className="market-highlights">
                <li>4 active properties</li>
                <li>128 units under management</li>
                <li>Top 10 U.S. job growth market</li>
                <li>Strong workforce housing fundamentals</li>
              </ul>
            </div>
            <div className="market-card">
              <div className="market-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                  <circle cx="12" cy="10" r="3"></circle>
                </svg>
              </div>
              <h3>Phoenix, Arizona</h3>
              <p>One of the fastest-growing metros in the U.S. with strong in-migration trends from higher-cost coastal markets. Business-friendly environment drives sustained demand.</p>
              <ul className="market-highlights">
                <li>1 active property (Arcadia Lite)</li>
                <li>15 units under management</li>
                <li>Top 5 U.S. population growth</li>
                <li>Premium submarket positioning</li>
              </ul>
            </div>
          </div>
          <div className="sunbelt-thesis">
            <h4>Sunbelt Thesis</h4>
            <p>Both markets benefit from favorable tax environments, business-friendly policies, lower cost of living relative to coastal metros, and sustained domestic migration. These structural tailwinds support long-term rental demand and property value appreciation.</p>
          </div>
        </div>
      </section>

      {/* Approach Section */}
      <section id="approach" className="section section-alt">
        <div className="container">
          <div className="section-header">
            <p className="section-label">Why RC</p>
            <h2>Competitive Advantages</h2>
          </div>
          <div className="advantages-grid">
            <div className="advantage-item">
              <div className="advantage-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                  <circle cx="9" cy="7" r="4"></circle>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
              </div>
              <h3>Boutique, Disciplined Team</h3>
              <p>Small, focused organization enables hands-on execution and rapid decision-making without bureaucratic delays common at larger firms.</p>
            </div>
            <div className="advantage-item">
              <div className="advantage-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="M21 21l-4.35-4.35"></path>
                </svg>
              </div>
              <h3>Off-Market Deal Sourcing</h3>
              <p>Proprietary broker relationships, direct seller access, and property manager networks surface deals before broad marketing begins.</p>
            </div>
            <div className="advantage-item">
              <div className="advantage-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                  <circle cx="12" cy="10" r="3"></circle>
                </svg>
              </div>
              <h3>Deep Market Knowledge</h3>
              <p>Granular submarket expertise in Houston and Phoenix enables confident underwriting and accurate rent projections based on hyperlocal data.</p>
            </div>
            <div className="advantage-item">
              <div className="advantage-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                </svg>
              </div>
              <h3>Aligned Interests</h3>
              <p>GP co-investment of 5-10% of total equity ensures principals have meaningful capital at risk alongside investors in every transaction.</p>
            </div>
            <div className="advantage-item">
              <div className="advantage-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="3" y1="9" x2="21" y2="9"></line>
                  <line x1="9" y1="21" x2="9" y2="9"></line>
                </svg>
              </div>
              <h3>Conservative Approach</h3>
              <p>Low leverage, fixed-rate debt preference, and stress-tested assumptions protect capital in all market conditions and interest rate environments.</p>
            </div>
            <div className="advantage-item">
              <div className="advantage-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                </svg>
              </div>
              <h3>Operational Excellence</h3>
              <p>Proven playbook for repositioning, rent optimization, and expense management drives consistent value creation across the portfolio.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Risk Management */}
      <section className="section">
        <div className="container">
          <div className="section-header">
            <p className="section-label">Capital Preservation</p>
            <h2>Risk Management Framework</h2>
          </div>
          <div className="risk-pillars">
            <div className="risk-pillar">
              <div className="pillar-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                </svg>
              </div>
              <h4>Low Basis Focus</h4>
              <p>Acquire at meaningful discount to replacement cost</p>
            </div>
            <div className="risk-pillar">
              <div className="pillar-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="12" y1="1" x2="12" y2="23"></line>
                  <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                </svg>
              </div>
              <h4>Cash Flow First</h4>
              <p>Durable income reduces reliance on exit assumptions</p>
            </div>
            <div className="risk-pillar">
              <div className="pillar-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
              </div>
              <h4>Conservative Leverage</h4>
              <p>Financing structured to withstand volatility</p>
            </div>
            <div className="risk-pillar">
              <div className="pillar-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                </svg>
              </div>
              <h4>Prudent CapEx</h4>
              <p>Phased capital plans driven by returns</p>
            </div>
            <div className="risk-pillar">
              <div className="pillar-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                </svg>
              </div>
              <h4>Stress Testing</h4>
              <p>Exit caps, rates, and refi scenarios modeled</p>
            </div>
          </div>
        </div>
      </section>

      {/* Investment Terms */}
      <section className="section section-alt">
        <div className="container">
          <div className="section-header">
            <p className="section-label">Partnership Terms</p>
            <h2>Investment Structure</h2>
          </div>
          <div className="terms-grid">
            <div className="terms-card">
              <h3>Deal Structure</h3>
              <table className="terms-table">
                <tbody>
                  <tr><td>Minimum Investment</td><td>$100,000</td></tr>
                  <tr><td>Target Equity Raise</td><td>$1.5M - $2.5M</td></tr>
                  <tr><td>Hold Period</td><td>5-7 Years</td></tr>
                  <tr><td>Distributions</td><td>Quarterly</td></tr>
                  <tr><td>Target IRR</td><td>{'18% - 25%'}</td></tr>
                  <tr><td>Target Equity Multiple</td><td>2.0x+</td></tr>
                </tbody>
              </table>
            </div>
            <div className="terms-card">
              <h3>Fee Structure</h3>
              <table className="terms-table">
                <tbody>
                  <tr><td>Acquisition Fee</td><td>2.0% of purchase price</td></tr>
                  <tr><td>Asset Management</td><td>2.0% of EGI annually</td></tr>
                  <tr><td>Promote</td><td>{'15-20% (deal dependent)'}</td></tr>
                  <tr><td>Disposition Fee</td><td>1.0% of sale price</td></tr>
                  <tr><td>Refinance Fee</td><td>0.5% of loan amount</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="section">
        <div className="container">
          <div className="section-header">
            <p className="section-label">Leadership</p>
            <h2>Meet the Principals</h2>
          </div>
          <div className="team-grid">
            <div className="team-card">
              <div className="team-avatar">MR</div>
              <div className="team-info">
                <h3>Michael Rosen</h3>
                <p className="team-title">Co-Founder &amp; Principal</p>
                <p className="team-bio">Oversees acquisitions, investor relations, and capital strategy. Responsible for deal sourcing, underwriting, and LP partnership development.</p>
              </div>
            </div>
            <div className="team-card">
              <div className="team-avatar">BC</div>
              <div className="team-info">
                <h3>Bradley Couch</h3>
                <p className="team-title">Co-Founder &amp; Principal</p>
                <p className="team-bio">Leads asset management, operations, and capital improvements. Responsible for property performance, vendor relationships, and value creation execution.</p>
              </div>
            </div>
          </div>
          <div className="team-commitment">
            <h4>Our Commitment</h4>
            <p>As owner-operators who invest meaningful personal capital alongside our partners, we are fully aligned with LP interests. Our success is measured by investor returns, not assets under management.</p>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="section section-dark">
        <div className="container">
          <div className="contact-content">
            <div className="contact-text">
              <p className="section-label">Get Started</p>
              <h2>Partner With Us</h2>
              <p>We work with family offices and accredited investors seeking passive exposure to institutional-quality multifamily investments through a trusted operating partner.</p>
              <div className="next-steps">
                <div className="step">
                  <span className="step-number">1</span>
                  <div>
                    <h4>Introductory Call</h4>
                    <p>Discuss investment objectives and partnership fit</p>
                  </div>
                </div>
                <div className="step">
                  <span className="step-number">2</span>
                  <div>
                    <h4>Due Diligence</h4>
                    <p>Review track record, references, and sample materials</p>
                  </div>
                </div>
                <div className="step">
                  <span className="step-number">3</span>
                  <div>
                    <h4>Deal Review</h4>
                    <p>Evaluate current or upcoming opportunities</p>
                  </div>
                </div>
                <div className="step">
                  <span className="step-number">4</span>
                  <div>
                    <h4>Partnership</h4>
                    <p>Execute documentation and fund investment</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="contact-form-wrapper">
              <form className="contact-form" id="contactForm">
                <div className="form-group">
                  <label htmlFor="name">Name</label>
                  <input type="text" id="name" name="name" required />
                </div>
                <div className="form-group">
                  <label htmlFor="email">Email</label>
                  <input type="email" id="email" name="email" required />
                </div>
                <div className="form-group">
                  <label htmlFor="phone">Phone</label>
                  <input type="tel" id="phone" name="phone" />
                </div>
                <div className="form-group">
                  <label htmlFor="investor-type">Investor Type</label>
                  <select id="investor-type" name="investor-type" defaultValue="">
                    <option value="">Select...</option>
                    <option value="family-office">Family Office</option>
                    <option value="accredited">Accredited Individual</option>
                    <option value="hnw">High Net Worth Professional</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                <div className="form-group">
                  <label htmlFor="message">Message</label>
                  <textarea id="message" name="message" rows={4}></textarea>
                </div>
                <button type="submit" className="btn btn-primary btn-full">Request Information</button>
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
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
                <li><a href="#about">About</a></li>
                <li><a href="#portfolio">Portfolio</a></li>
                <li><a href="#approach">Approach</a></li>
                <li><a href="#contact">Contact</a></li>
              </ul>
            </div>
            <div className="footer-links">
              <h4>Resources</h4>
              <ul>
                <li><Link href="/blog">Market Insights</Link></li>
                <li><a href="#approach">Investment Criteria</a></li>
                <li><a href="#contact">Contact Us</a></li>
              </ul>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2025 RC Investment Properties. All rights reserved.</p>
            <p className="disclaimer">This website is for informational purposes only and does not constitute an offer to sell or a solicitation of an offer to buy any securities. Past performance is not indicative of future results.</p>
          </div>
        </div>
      </footer>
    </>
  );
}
