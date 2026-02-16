'use client';

import Link from 'next/link';
import { useState } from 'react';

export default function Blog() {
  const [activeCategory, setActiveCategory] = useState('all');

  const blogPosts = [
    {
      id: 1,
      title: 'Houston Multifamily Market 2025: Supply Stabilization & Continued Opportunity',
      slug: 'houston-2025',
      category: 'market-analysis',
      date: 'January 15, 2025',
      excerpt: 'The Houston multifamily market enters 2025 with a fundamentally different backdrop than the previous two years. After the supply inflection of 2023-2024, market conditions are stabilizing.',
      readTime: '8 min read'
    },
    {
      id: 2,
      title: 'Houston Q4 2025 Market Update: The Normalization Continues',
      slug: 'houston-q4-2025',
      category: 'market-analysis',
      date: 'October 20, 2024',
      excerpt: 'As we head into Q4 2024, the Houston multifamily market continues its normalization trajectory. After extraordinary growth between 2020-2022, the market is settling into a more sustainable equilibrium.',
      readTime: '6 min read'
    }
  ];

  const filteredPosts = activeCategory === 'all' 
    ? blogPosts 
    : blogPosts.filter(post => post.category === activeCategory);

  return (
    <>
      {/* Navigation */}
      <nav className="navbar">
        <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Link href="/" className="logo">RC Investment Properties</Link>
          <ul className="nav-links" style={{ display: 'flex' }}>
            <li><a href="/#about">About</a></li>
            <li><a href="/#portfolio">Portfolio</a></li>
            <li><a href="/#approach">Approach</a></li>
            <li><Link href="/blog">Insights</Link></li>
            <li><a href="/#contact" className="btn-nav">Contact</a></li>
          </ul>
        </div>
      </nav>

      {/* Blog Hero */}
      <section className="section blog-hero">
        <div className="container">
          <div className="section-header">
            <p className="section-label">Insights & Analysis</p>
            <h1>RC Market Insights</h1>
            <p style={{ fontSize: '1.125rem', color: '#555', marginTop: '20px' }}>In-depth analysis of multifamily markets, investment trends, and opportunities.</p>
          </div>
        </div>
      </section>

      {/* Blog Content */}
      <section className="section">
        <div className="container">
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 280px', gap: '40px' }}>
            {/* Main Content */}
            <div>
              <div className="blog-grid">
                {filteredPosts.map((post) => (
                  <Link href={`/blog/${post.slug}`} key={post.id}>
                    <article className="blog-card" style={{ textDecoration: 'none', color: 'inherit' }}>
                      <div className="blog-card-header">
                        <span className="blog-category">{post.category === 'market-analysis' ? 'Market Analysis' : 'Investment'}</span>
                        <span className="blog-date">{post.date}</span>
                      </div>
                      <h3>{post.title}</h3>
                      <p>{post.excerpt}</p>
                      <div className="blog-footer">
                        <span className="read-time">{post.readTime}</span>
                        <span className="read-more">Read Article →</span>
                      </div>
                    </article>
                  </Link>
                ))}
              </div>
            </div>

            {/* Sidebar */}
            <aside className="blog-sidebar">
              <div className="sidebar-block">
                <h4>Categories</h4>
                <ul className="category-list">
                  <li>
                    <button 
                      onClick={() => setActiveCategory('all')}
                      style={{
                        background: 'none',
                        border: 'none',
                        cursor: 'pointer',
                        padding: '8px 0',
                        color: activeCategory === 'all' ? '#0A4E44' : '#555',
                        fontWeight: activeCategory === 'all' ? '600' : '400',
                        fontSize: '15px'
                      }}
                    >
                      All Articles
                    </button>
                  </li>
                  <li>
                    <button 
                      onClick={() => setActiveCategory('market-analysis')}
                      style={{
                        background: 'none',
                        border: 'none',
                        cursor: 'pointer',
                        padding: '8px 0',
                        color: activeCategory === 'market-analysis' ? '#0A4E44' : '#555',
                        fontWeight: activeCategory === 'market-analysis' ? '600' : '400',
                        fontSize: '15px'
                      }}
                    >
                      Market Analysis
                    </button>
                  </li>
                </ul>
              </div>

              <div className="sidebar-block">
                <h4>Contact Us</h4>
                <p>Have questions about our market analysis?</p>
                <a href="/#contact" className="btn btn-secondary">Get In Touch</a>
              </div>
            </aside>
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
                <li><a href="/#about">About</a></li>
                <li><a href="/#portfolio">Portfolio</a></li>
                <li><a href="/#approach">Approach</a></li>
                <li><Link href="/blog">Insights</Link></li>
                <li><a href="/#contact">Contact</a></li>
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
