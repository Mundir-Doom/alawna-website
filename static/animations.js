// Creative Website Animations
document.addEventListener('DOMContentLoaded', function() {
    initScrollAnimations();
    initInteractiveEffects();
    ensureHashtagVisibility();
});

function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('section, .card, .priority-item, .blog-post').forEach(el => {
        el.classList.add('animate-on-scroll');
        observer.observe(el);
    });
}

function initInteractiveEffects() {
    // Add stable hover effects to cards
    document.querySelectorAll('.card, .priority-item, .blog-post').forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.classList.add('is-hovered');
        });
        card.addEventListener('mouseleave', () => {
            card.classList.remove('is-hovered');
        });
    });

    // Navbar scroll effect
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100 && currentScroll > lastScroll) {
            navbar.classList.add('navbar-hidden');
        } else {
            navbar.classList.remove('navbar-hidden');
        }
        lastScroll = currentScroll;
    });
}

// Ensure hashtag is always visible - Fix for animation bug
function ensureHashtagVisibility() {
    const heroBadge = document.querySelector('.hero-badge');
    const footerHashtag = document.querySelector('.footer-hashtag');
    
    // Force visibility for hero badge
    if (heroBadge) {
        heroBadge.style.opacity = '1';
        heroBadge.style.visibility = 'visible';
        heroBadge.style.display = 'inline-block';
        
        // Add safety check after animation should complete
        setTimeout(() => {
            heroBadge.style.opacity = '1';
            heroBadge.style.visibility = 'visible';
        }, 1500);
    }
    
    // Force visibility for footer hashtag
    if (footerHashtag) {
        footerHashtag.style.opacity = '1';
        footerHashtag.style.visibility = 'visible';
        footerHashtag.style.display = 'inline-block';
    }
    
    console.log('✅ Hashtag visibility ensured: #اتحاد_قبائل_العلاونة');
}
