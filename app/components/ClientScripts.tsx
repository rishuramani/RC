'use client';

import { useEffect, useCallback } from 'react';

export default function ClientScripts() {
  const handleMobileMenu = useCallback(() => {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn && navLinks) {
      mobileMenuBtn.addEventListener('click', function () {
        navLinks.classList.toggle('active');
        mobileMenuBtn.classList.toggle('active');
      });
    }
  }, []);

  const handleSmoothScroll = useCallback(() => {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener('click', function (this: HTMLAnchorElement, e: Event) {
        const href = this.getAttribute('href');
        if (href === '#') return;

        const target = document.querySelector(href!);
        if (target) {
          e.preventDefault();
          const navbar = document.querySelector('.navbar');
          const navbarHeight = navbar ? navbar.getBoundingClientRect().height : 0;
          const targetPosition =
            target.getBoundingClientRect().top + window.pageYOffset - navbarHeight;

          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth',
          });

          // Close mobile menu if open
          const navLinks = document.querySelector('.nav-links');
          const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
          if (navLinks && navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            mobileMenuBtn?.classList.remove('active');
          }
        }
      });
    });
  }, []);

  const handleNavbarScroll = useCallback(() => {
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

  const handleContactForm = useCallback(() => {
    const contactForm = document.getElementById('contactForm') as HTMLFormElement;
    if (!contactForm) return;

    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();

      const formData = new FormData(contactForm);
      const data: Record<string, string> = {};
      formData.forEach((value, key) => {
        data[key] = value as string;
      });

      if (!data.name || !data.email) {
        alert('Please fill in all required fields.');
        return;
      }

      alert('Thank you for your interest. We will be in touch shortly.');
      contactForm.reset();
    });
  }, []);

  const handleScrollAnimations = useCallback(() => {
    const observerOptions = {
      root: null,
      rootMargin: '0px',
      threshold: 0.1,
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in');
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    document.querySelectorAll('.section').forEach((section) => {
      observer.observe(section);
    });
  }, []);

  useEffect(() => {
    handleMobileMenu();
    handleSmoothScroll();
    const cleanupNavbar = handleNavbarScroll();
    handleContactForm();
    handleScrollAnimations();

    return () => {
      cleanupNavbar?.();
    };
  }, [handleMobileMenu, handleSmoothScroll, handleNavbarScroll, handleContactForm, handleScrollAnimations]);

  return null;
}
