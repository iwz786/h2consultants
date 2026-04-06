/* ============================================================
   H2 Consultants — script.js
   Handles: navbar scroll, mobile menu, scroll animations,
            back-to-top, contact form, area chips, year
   ============================================================ */

'use strict';

/* ── DOM References ──────────────────────────────────────── */
const navbar = document.getElementById('navbar');
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
const backTop = document.getElementById('backTop');
const contactForm = document.getElementById('contactForm');
const formSuccess = document.getElementById('formSuccess');
const currentYear = document.getElementById('currentYear');

/* ── Current Year ────────────────────────────────────────── */
if (currentYear) {
    currentYear.textContent = new Date().getFullYear();
}

/* ── Navbar — scroll effects ──────────────────────────────── */
function handleNavbarScroll() {
    if (window.scrollY > 40) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
}
window.addEventListener('scroll', handleNavbarScroll, { passive: true });
handleNavbarScroll(); // run on load

/* ── Mobile Menu Toggle ───────────────────────────────────── */
function openMenu() {
    navToggle.classList.add('open');
    navLinks.classList.add('open');
    navToggle.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
}

function closeMenu() {
    navToggle.classList.remove('open');
    navLinks.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
}

navToggle.addEventListener('click', () => {
    const isOpen = navLinks.classList.contains('open');
    if (isOpen) {
        closeMenu();
    } else {
        openMenu();
    }
});

// Close menu when a nav link is clicked
navLinks.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', closeMenu);
});

// Close menu when clicking outside
document.addEventListener('click', (e) => {
    if (
        navLinks.classList.contains('open') &&
        !navbar.contains(e.target)
    ) {
        closeMenu();
    }
});

// Close on Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && navLinks.classList.contains('open')) {
        closeMenu();
        navToggle.focus();
    }
});

/* ── Smooth Scroll for anchor links ──────────────────────── */
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        const target = document.querySelector(targetId);
        if (!target) return;
        e.preventDefault();
        const navHeight = navbar.offsetHeight;
        const targetTop = target.getBoundingClientRect().top + window.scrollY - navHeight - 16;
        window.scrollTo({ top: targetTop, behavior: 'smooth' });
    });
});

/* ── Back to Top ─────────────────────────────────────────── */
function handleBackTop() {
    if (window.scrollY > 500) {
        backTop.classList.add('visible');
    } else {
        backTop.classList.remove('visible');
    }
}
window.addEventListener('scroll', handleBackTop, { passive: true });

backTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

/* ── Intersection Observer — Scroll Animations ───────────── */
const animatedEls = document.querySelectorAll('.fade-in, .fade-in-left, .fade-in-right');

if ('IntersectionObserver' in window) {
    // Delay each element in a grid/group so they stagger nicely
    const groupOffsets = new Map();

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const parent = el.parentElement;

                    // Stagger siblings in the same grid parent
                    if (!groupOffsets.has(parent)) {
                        groupOffsets.set(parent, 0);
                    }
                    const delay = groupOffsets.get(parent);
                    groupOffsets.set(parent, delay + 80);

                    setTimeout(() => {
                        el.classList.add('visible');
                    }, delay);

                    observer.unobserve(el);
                }
            });
        },
        { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );

    animatedEls.forEach((el) => observer.observe(el));
} else {
    // Fallback: show all elements immediately
    animatedEls.forEach((el) => el.classList.add('visible'));
}

/* ── Area Chips — toggle active ──────────────────────────── */
document.querySelectorAll('.chip').forEach((chip) => {
    chip.addEventListener('click', () => {
        document.querySelectorAll('.chip').forEach((c) => c.classList.remove('active'));
        chip.classList.add('active');
    });
});

/* ── Contact Form ────────────────────────────────────────── */
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();

        // Basic client-side validation
        const firstName = contactForm.firstName.value.trim();
        const lastName = contactForm.lastName.value.trim();
        const email = contactForm.email.value.trim();
        const message = contactForm.message.value.trim();

        if (!firstName || !lastName || !email || !message) {
            // Highlight empty required fields
            [
                { field: contactForm.firstName, val: firstName },
                { field: contactForm.lastName, val: lastName },
                { field: contactForm.email, val: email },
                { field: contactForm.message, val: message },
            ].forEach(({ field, val }) => {
                if (!val) {
                    field.style.borderColor = '#E53935';
                    field.addEventListener('input', () => {
                        field.style.borderColor = '';
                    }, { once: true });
                }
            });
            return;
        }

        // Email format check
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            contactForm.email.style.borderColor = '#E53935';
            contactForm.email.focus();
            return;
        }

        // ── EmailJS Submission ────────────────────────────────
        // Replace the three placeholder values below with your
        // real EmailJS credentials from https://emailjs.com:
        //   EMAILJS_SERVICE_ID  — e.g. 'service_abc123'
        //   EMAILJS_TEMPLATE_ID — e.g. 'template_xyz456'
        //   EMAILJS_PUBLIC_KEY  — e.g. 'user_XXXXXXXXXXXX'
        // ─────────────────────────────────────────────────────
        const EMAILJS_SERVICE_ID = 'service_y5z6ixa';
        const EMAILJS_TEMPLATE_ID = 'template_i6382j8';
        const EMAILJS_PUBLIC_KEY = 'SBT4Ach1b1MQfJvdy';

        const submitBtn = contactForm.querySelector('[type="submit"]');
        submitBtn.textContent = 'Sending…';
        submitBtn.disabled = true;

        const templateParams = {
            firstName,
            lastName,
            email,
            phone: contactForm.phone.value.trim(),
            businessType: contactForm.businessType.value,
            message,
        };

        emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, templateParams, EMAILJS_PUBLIC_KEY)
            .then(() => {
                formSuccess.classList.add('show');
                contactForm.reset();
                formSuccess.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            })
            .catch(() => {
                formSuccess.innerHTML = '<span>⚠️</span><span>Something went wrong. Please try calling us directly at 647-291-0141.</span>';
                formSuccess.style.background = '#FFF3E0';
                formSuccess.style.borderColor = '#FFCC80';
                formSuccess.style.color = '#E65100';
                formSuccess.classList.add('show');
            })
            .finally(() => {
                submitBtn.textContent = 'Send Message →';
                submitBtn.disabled = false;
            });
    });
}

/* ── Navbar active section highlight ────────────────────── */
const sections = document.querySelectorAll('section[id], div[id="home"]');
const navAnchors = document.querySelectorAll('.nav-links a[href^="#"]');

function setActiveNav() {
    const scrollY = window.scrollY + navbar.offsetHeight + 80;
    let current = '';

    sections.forEach((section) => {
        const top = section.offsetTop;
        const height = section.offsetHeight;
        if (scrollY >= top && scrollY < top + height) {
            current = section.getAttribute('id');
        }
    });

    navAnchors.forEach((a) => {
        a.style.color = '';
        if (a.getAttribute('href') === `#${current}`) {
            a.style.color = 'var(--primary)';
        }
    });
}

window.addEventListener('scroll', setActiveNav, { passive: true });
setActiveNav();
