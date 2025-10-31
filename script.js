// Attend que le DOM soit entièrement chargé pour exécuter les scripts
document.addEventListener('DOMContentLoaded', () => {

    /* ============================================= */
    /* Gestion du Menu Burger (Mobile)               */
    /* ============================================= */
    const burger = document.querySelector('.burger');
    const navLinks = document.querySelector('.nav-links');
    
    if (burger && navLinks) {
        burger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            burger.classList.toggle('active');
        });

        // Ferme le menu au clic sur un lien
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                burger.classList.remove('active');
            });
        });
    }

    /* ============================================= */
    /* Effet de "scroll" sur la navigation           */
    /* ============================================= */
    const nav = document.querySelector('nav');
    if (nav) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 100) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });
    }

    /* ============================================= */
    /* Animation au défilement (Intersection Observer) */
    /* ============================================= */
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, observerOptions);

    // Applique l'observateur uniquement aux cartes de compétences
    document.querySelectorAll('.skill-card').forEach(card => {
        observer.observe(card);
    });

    /* ============================================= */
    /* Bouton "Retour en Haut"                       */
    /* ============================================= */
    const scrollToTopBtn = document.getElementById('scrollToTop');
    if (scrollToTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                scrollToTopBtn.classList.add('visible');
            } else {
                scrollToTopBtn.classList.remove('visible');
            }
        });

        scrollToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    /* ============================================= */
    /* Gestionnaire de Thème (Clair/Sombre)          */
    /* ============================================= */
    const themeToggle = document.getElementById('themeToggle');
    const html = document.documentElement;
    
    if (themeToggle && html) {
        const themeIcon = themeToggle.querySelector('i');
        
        const savedTheme = localStorage.getItem('theme') || 'light';
        html.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);

        themeToggle.addEventListener('click', () => {
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });

        function updateThemeIcon(theme) {
            if (theme === 'dark') {
                themeIcon.className = 'fas fa-sun';
            } else {
                themeIcon.className = 'fas fa-moon';
            }
        }
    }

    /* ============================================= */
    /* Gestion du Formulaire de Contact (via Formspree) */
    /* Le formulaire HTML est géré par l'action "formspree.io", aucun JS n'est requis. */
    /* ============================================= */
    
    // (Aucun JavaScript n'est nécessaire ici car Formspree gère la soumission)

    /* ============================================= */
    /* Logique du Carrousel de Projets               */
    /* ============================================= */
    const carouselContainer = document.querySelector('.project-carousel-container');
    const track = document.querySelector('.project-carousel-track');
    const slides = Array.from(track.children);
    const nextButton = document.getElementById('carouselNext');
    const prevButton = document.getElementById('carouselPrev');

    if (carouselContainer && track && slides.length > 0 && nextButton && prevButton) {
        
        let currentIndex = 0;
        let slideWidth = slides[0].getBoundingClientRect().width;
        let autoScrollInterval;

        const goToSlide = (index) => {
            if (index < 0) index = slides.length - 1;
            if (index >= slides.length) index = 0;
            
            track.style.transform = `translateX(-${slideWidth * index}px)`;
            currentIndex = index;
        };

        nextButton.addEventListener('click', () => {
            goToSlide(currentIndex + 1);
            resetAutoScroll();
        });

        prevButton.addEventListener('click', () => {
            goToSlide(currentIndex - 1);
            resetAutoScroll();
        });

        window.addEventListener('resize', () => {
            slideWidth = slides[0].getBoundingClientRect().width;
            goToSlide(currentIndex); 
        });

        const startAutoScroll = () => {
            autoScrollInterval = setInterval(() => {
                goToSlide(currentIndex + 1);
            }, 5000); 
        };

        const stopAutoScroll = () => {
            clearInterval(autoScrollInterval);
        };

        const resetAutoScroll = () => {
            stopAutoScroll();
            startAutoScroll();
        };

        carouselContainer.addEventListener('mouseenter', stopAutoScroll);
        carouselContainer.addEventListener('mouseleave', startAutoScroll);

        goToSlide(0);
        startAutoScroll();
    }

}); // Fin de DOMContentLoaded