// Global Variables
let currentSlide = 0;
let isAutoPlaying = true;
let autoSlideTimer;
const slides = document.querySelectorAll('.carousel-slide');
const indicators = document.querySelectorAll('.indicator');
const captionText = document.getElementById('carousel-caption-text');

// Carousel data
const carouselData = [
    {
        caption: "تراث عريق من الشجاعة والفروسية"
    },
    {
        caption: "أصالة الماضي وعزة الحاضر"
    },
    {
        caption: "استمرار التقاليد في العصر الحديث"
    }
];

// Navigation functionality
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link, .nav-link-mobile, .nav-dropdown-link');
    const sections = document.querySelectorAll('section[id]');
    
    // Handle navigation clicks
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetSection = link.getAttribute('data-section');
            if (targetSection) {
                scrollToSection(targetSection);
                
                // Update active states
                updateActiveNavLinks(targetSection);
                
                // Close mobile menu if open
                closeMobileMenu();
            }
        });
    });
    
    // Initialize dropdown functionality
    initDropdownMenu();
    
    // Intersection Observer for active section detection
    const observerOptions = {
        threshold: [0, 0.3, 0.7],
        rootMargin: '-80px 0px -50% 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && entry.intersectionRatio > 0.3) {
                updateActiveNavLinks(entry.target.id);
            }
        });
    }, observerOptions);
    
    // Observe all sections
    sections.forEach(section => {
        observer.observe(section);
    });
}

// Scroll to section function
function scrollToSection(sectionId) {
    if (!sectionId) {
        return;
    }

    const element = document.getElementById(sectionId);
    if (element) {
        const offset = 80; // Account for fixed navigation
        const elementPosition = element.offsetTop - offset;
        window.scrollTo({
            top: elementPosition,
            behavior: 'smooth'
        });
        return;
    }

    const { homeUrl = '/' } = document.body.dataset || {};
    try {
        const target = new URL(homeUrl || '/', window.location.origin);
        target.hash = sectionId;
        window.location.href = target.toString();
    } catch (error) {
        window.location.href = `/#${sectionId}`;
    }
}

// Update active navigation links
function updateActiveNavLinks(activeSection) {
    const allNavLinks = document.querySelectorAll('.nav-link, .nav-link-mobile, .nav-dropdown-link');
    allNavLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-section') === activeSection) {
            link.classList.add('active');
        }
    });
}

// Dropdown menu functionality
function initDropdownMenu() {
    const dropdowns = document.querySelectorAll('.nav-dropdown');
    
    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.nav-dropdown-toggle');
        const menu = dropdown.querySelector('.nav-dropdown-menu');
        
        // Toggle dropdown on click
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            // Close other dropdowns
            dropdowns.forEach(otherDropdown => {
                if (otherDropdown !== dropdown) {
                    otherDropdown.classList.remove('open');
                }
            });
            
            // Toggle current dropdown
            dropdown.classList.toggle('open');
        });
        
        // Handle dropdown link clicks
        const dropdownLinks = dropdown.querySelectorAll('.nav-dropdown-link');
        dropdownLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetSection = link.getAttribute('data-section');
                if (targetSection) {
                    scrollToSection(targetSection);
                    updateActiveNavLinks(targetSection);
                    dropdown.classList.remove('open');
                    closeMobileMenu();
                }
            });
        });
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.nav-dropdown')) {
            dropdowns.forEach(dropdown => {
                dropdown.classList.remove('open');
            });
        }
    });
}

// Mobile menu functionality
function initMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileNav = document.getElementById('mobile-nav');
    
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenuBtn.classList.toggle('open');
        mobileNav.classList.toggle('open');
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!mobileMenuBtn.contains(e.target) && !mobileNav.contains(e.target)) {
            closeMobileMenu();
        }
    });
}

function closeMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileNav = document.getElementById('mobile-nav');
    
    mobileMenuBtn.classList.remove('open');
    mobileNav.classList.remove('open');
}

// Carousel functionality
function initCarousel() {
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    
    // Event listeners for controls
    prevBtn.addEventListener('click', prevSlide);
    nextBtn.addEventListener('click', nextSlide);
    
    // Event listeners for indicators
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => goToSlide(index));
    });
    
    // Auto-play functionality
    startAutoSlide();
    
    // Pause on hover
    const heroSection = document.querySelector('.hero');
    heroSection.addEventListener('mouseenter', pauseAutoSlide);
    heroSection.addEventListener('mouseleave', resumeAutoSlide);
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            nextSlide();
        } else if (e.key === 'ArrowRight') {
            prevSlide();
        }
    });
    
    // Touch/swipe support for mobile
    initTouchSupport();
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    updateSlide();
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    updateSlide();
}

function goToSlide(index) {
    currentSlide = index;
    updateSlide();
}

function updateSlide() {
    // Update slides
    slides.forEach((slide, index) => {
        slide.classList.toggle('active', index === currentSlide);
    });
    
    // Update indicators
    indicators.forEach((indicator, index) => {
        indicator.classList.toggle('active', index === currentSlide);
    });
    
    // Update caption
    if (captionText && carouselData[currentSlide]) {
        captionText.textContent = carouselData[currentSlide].caption;
    }
}

function startAutoSlide() {
    if (isAutoPlaying) {
        autoSlideTimer = setInterval(nextSlide, 7000);
    }
}

function pauseAutoSlide() {
    isAutoPlaying = false;
    clearInterval(autoSlideTimer);
}

function resumeAutoSlide() {
    isAutoPlaying = true;
    startAutoSlide();
}

// Touch support for carousel
function initTouchSupport() {
    const hero = document.querySelector('.hero');
    let startX = 0;
    let startY = 0;
    let distX = 0;
    let distY = 0;
    
    hero.addEventListener('touchstart', (e) => {
        const touch = e.touches[0];
        startX = touch.clientX;
        startY = touch.clientY;
    }, { passive: true });
    
    hero.addEventListener('touchmove', (e) => {
        if (!startX || !startY) return;
        
        const touch = e.touches[0];
        distX = touch.clientX - startX;
        distY = touch.clientY - startY;
    }, { passive: true });
    
    hero.addEventListener('touchend', () => {
        if (!distX || !distY) return;
        
        // Only trigger if horizontal swipe is greater than vertical
        if (Math.abs(distX) > Math.abs(distY)) {
            if (Math.abs(distX) > 50) { // Minimum swipe distance
                if (distX > 0) {
                    prevSlide(); // Swipe right (previous in RTL)
                } else {
                    nextSlide(); // Swipe left (next in RTL)
                }
            }
        }
        
        // Reset values
        startX = 0;
        startY = 0;
        distX = 0;
        distY = 0;
    }, { passive: true });
}

// Scroll animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Animate cards and content blocks
    const animatedElements = document.querySelectorAll('.content-card, .cta-block, .quote');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(el);
    });
}

// Smooth navbar background on scroll
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = '0 1px 2px 0 rgba(0, 0, 0, 0.05)';
        }
    });
}

// Preload images for better performance
function preloadImages() {
    const images = document.querySelectorAll('.carousel-img');
    images.forEach(img => {
        const imageUrl = img.src;
        const preloadImage = new Image();
        preloadImage.src = imageUrl;
    });
}

// Error handling for images
function initImageErrorHandling() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('error', (e) => {
            // Fallback for broken images
            e.target.style.display = 'none';
            console.warn('Failed to load image:', e.target.src);
        });
    });
}

// Performance optimization: Throttle scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Alawna website initialized');
    
    // Initialize all functionality
    initNavigation();
    initMobileMenu();
    initCarousel();
    initScrollAnimations();
    initNavbarScroll();
    initImageErrorHandling();
    
    // Preload images after initial load
    setTimeout(preloadImages, 1000);
    
    // Set initial active navigation
    updateActiveNavLinks('home');
});

// Handle window resize
window.addEventListener('resize', throttle(() => {
    // Close mobile menu on resize to desktop
    if (window.innerWidth >= 768) {
        closeMobileMenu();
    }
}, 250));

// Handle visibility change (pause carousel when tab is not visible)
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        pauseAutoSlide();
    } else {
        resumeAutoSlide();
    }
});

// Expose scrollToSection globally for inline onclick handlers
window.scrollToSection = scrollToSection;

// Accessibility improvements
function initAccessibility() {
    // Add ARIA labels and roles
    const slides = document.querySelectorAll('.carousel-slide');
    slides.forEach((slide, index) => {
        slide.setAttribute('aria-hidden', index !== currentSlide);
    });
    
    // Update ARIA labels when slide changes
    const originalUpdateSlide = updateSlide;
    updateSlide = function() {
        originalUpdateSlide();
        slides.forEach((slide, index) => {
            slide.setAttribute('aria-hidden', index !== currentSlide);
        });
    };
    
    // Add keyboard navigation instructions
    console.log('⌨️  Keyboard navigation: Use ← → arrow keys to navigate carousel');
}

// Initialize accessibility features
document.addEventListener('DOMContentLoaded', initAccessibility);

// Service Worker registration (for PWA capabilities)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment when you have a service worker
        // navigator.serviceWorker.register('/sw.js')
        //     .then(registration => console.log('SW registered'))
        //     .catch(registrationError => console.log('SW registration failed'));
    });
}
