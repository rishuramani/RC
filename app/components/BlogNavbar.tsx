'use client';

import { useEffect } from 'react';
import Link from 'next/link';

export default function BlogNavbar() {
  useEffect(() => {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn && navLinks) {
      const handler = () => {
        navLinks.classList.toggle('active');
        mobileMenuBtn.classList.toggle('active');
      };
      mobileMenuBtn.addEventListener('click', handler);
      return () => mobileMenuBtn.removeEventListener('click', handler);
    }
  }, []);

  useEffect(() => {
    const navbar = document.querySelector('.navbar') as HTMLElement;
    if (!navbar) return;

    function updateNavbar() {
      if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
      } else {
        navbar.style.boxShadow = '0 2px 4px rgba(0,0,0,0.05)';
      }
    }

    window.addEventListener('scroll', updateNavbar);
    updateNavbar();
    return () => window.removeEventListener('scroll', updateNavbar);
  }, []);

  return (
    <nav className="navbar">
      <div className="container">
        <Link href="/" className="logo">RC Investment Properties</Link>
        <ul className="nav-links">
          <li><Link href="/#about">About</Link></li>
          <li><Link href="/#portfolio">Portfolio</Link></li>
          <li><Link href="/#approach">Approach</Link></li>
          <li><Link href="/blog">Insights</Link></li>
          <li><Link href="/#contact" className="btn-nav">Contact</Link></li>
        </ul>
        <button className="mobile-menu-btn" aria-label="Toggle menu">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </nav>
  );
}
