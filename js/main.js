// ============================================
// AIRII - Main JavaScript
// ============================================

document.addEventListener('DOMContentLoaded', function() {

    // --- Navbar scroll effect ---
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        const onScroll = () => {
            if (window.scrollY > 20) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    // --- Mobile nav toggle ---
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('mobile-open');
        });

        // Close mobile menu on link click
        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navToggle.classList.remove('active');
                navMenu.classList.remove('mobile-open');
            });
        });
    }

    // --- Fade-up animation on scroll ---
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

    document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));

    // --- Tab switching ---
    document.querySelectorAll('[data-tab-group]').forEach(tabGroup => {
        const tabs = tabGroup.querySelectorAll('.tab');
        const panels = document.querySelectorAll(`[data-tab-panel][data-group="${tabGroup.dataset.tabGroup}"]`);
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const target = tab.dataset.tab;
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                panels.forEach(p => {
                    p.style.display = p.dataset.tabPanel === target ? 'block' : 'none';
                });
            });
        });
    });

    // --- Filter tags ---
    document.querySelectorAll('.filter-tag').forEach(tag => {
        tag.addEventListener('click', () => {
            const group = tag.closest('.filter-tags');
            if (group) {
                group.querySelectorAll('.filter-tag').forEach(t => t.classList.remove('active'));
            }
            tag.classList.add('active');
        });
    });

    // --- Countdown (if exists) ---
    const countdownEl = document.getElementById('countdown');
    if (countdownEl) {
        const targetDate = new Date(countdownEl.dataset.target).getTime();
        const update = () => {
            const now = new Date().getTime();
            const diff = targetDate - now;
            if (diff < 0) {
                countdownEl.innerHTML = '<span class="countdown-expired">Event in progress</span>';
                return;
            }
            const days = Math.floor(diff / 86400000);
            const hours = Math.floor((diff % 86400000) / 3600000);
            const mins = Math.floor((diff % 3600000) / 60000);
            const secs = Math.floor((diff % 60000) / 1000);
            countdownEl.innerHTML = `
                <div class="countdown-unit"><span class="countdown-num">${days}</span><span class="countdown-label">Days</span></div>
                <div class="countdown-unit"><span class="countdown-num">${hours}</span><span class="countdown-label">Hours</span></div>
                <div class="countdown-unit"><span class="countdown-num">${mins}</span><span class="countdown-label">Min</span></div>
                <div class="countdown-unit"><span class="countdown-num">${secs}</span><span class="countdown-label">Sec</span></div>
            `;
        };
        update();
        setInterval(update, 1000);
    }

    // --- Smooth scroll for anchor links ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#wechat') {
                e.preventDefault();
                const modal = document.getElementById('wechatModal');
                if (modal) modal.classList.add('active');
                return;
            }
            const target = document.querySelector(href);
            if (target && href !== '#') {
                e.preventDefault();
                const offset = 80;
                const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
                window.scrollTo({ top, behavior: 'smooth' });
            }
        });
    });

    // --- WeChat modal close ---
    const wechatModal = document.getElementById('wechatModal');
    const closeWechat = document.getElementById('closeWechat');
    if (wechatModal && closeWechat) {
        closeWechat.addEventListener('click', () => wechatModal.classList.remove('active'));
        wechatModal.addEventListener('click', (e) => {
            if (e.target === wechatModal) wechatModal.classList.remove('active');
        });
    }
});
