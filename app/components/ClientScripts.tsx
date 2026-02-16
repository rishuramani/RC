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

  const handlePortfolioHover = useCallback(() => {
    document.querySelectorAll('.portfolio-card').forEach((card) => {
      const el = card as HTMLElement;
      el.addEventListener('mouseenter', function () {
        this.style.transform = 'translateY(-4px)';
      });
      el.addEventListener('mouseleave', function () {
        this.style.transform = 'translateY(0)';
      });
    });
  }, []);

  const handleThesisHover = useCallback(() => {
    document.querySelectorAll('.thesis-card').forEach((card) => {
      const el = card as HTMLElement;
      el.addEventListener('mouseenter', function () {
        this.style.boxShadow = '0 8px 24px rgba(0,0,0,0.12)';
      });
      el.addEventListener('mouseleave', function () {
        this.style.boxShadow = '0 2px 4px rgba(0,0,0,0.05)';
      });
    });
  }, []);

  const handleCounterAnimation = useCallback(() => {
    function animateCounter(element: HTMLElement, target: number, duration = 2000) {
      const increment = target / (duration / 16);
      let current = 0;
      const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
          element.textContent = String(target);
          clearInterval(timer);
        } else {
          element.textContent = String(Math.floor(current));
        }
      }, 16);
    }

    const counterObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const target = parseInt((entry.target as HTMLElement).dataset.target || '0');
            if (target) {
              animateCounter(entry.target as HTMLElement, target);
            }
            counterObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.5 }
    );

    document.querySelectorAll('[data-counter]').forEach((counter) => {
      counterObserver.observe(counter);
    });
  }, []);

  useEffect(() => {
    handleMobileMenu();
    handleSmoothScroll();
    const cleanupNavbar = handleNavbarScroll();
    handleContactForm();
    handleScrollAnimations();
    handlePortfolioHover();
    handleThesisHover();
    handleCounterAnimation();

    return () => {
      cleanupNavbar?.();
    };
  }, [handleMobileMenu, handleSmoothScroll, handleNavbarScroll, handleContactForm, handleScrollAnimations, handlePortfolioHover, handleThesisHover, handleCounterAnimation]);

  return null;
}
