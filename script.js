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
    /* Système de filtrage des projets              */
    /* ============================================= */
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectBlocks = document.querySelectorAll('.project-block');

    if (filterButtons.length > 0 && projectBlocks.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                filterButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');

                const filter = button.getAttribute('data-filter');

                projectBlocks.forEach(block => {
                    const category = block.getAttribute('data-category');
                    
                    if (filter === 'tous' || category === filter) {
                        block.classList.remove('hidden');
                        block.style.animation = 'fadeInUp 0.6s ease forwards';
                    } else {
                        block.classList.add('hidden');
                    }
                });
            });
        });
    }

    /* ============================================= */
    /* Stockage ordonné des données de Projets      */
    /* ============================================= */
    const projectsData = [
        {
            title: 'Automatisation NetDevOps & Refonte Documentaire',
            date: 'Avril 2026 - Août 2026',
            description: `Stage de 16 semaines au sein de la direction DIGIT d'EDF (Équipe Interconnexions). Mon travail s'est divisé en deux missions majeures :<br><br>
            <strong>Mission 1 : Conception d'une solution d'automatisation réseau (NetDevOps)</strong><br>
            - Développement d'un script Python sécurisé pour automatiser les bascules de flux des routeurs Arista lors des maintenances mensuelles.<br>
            - Interfaçage avec l'eAPI Arista, Nautobot (Source de Vérité) et le framework Nornir.<br>
            - Intégration logicielle sur le portail interne NAP (Django) avec développement d'un front-end dynamique en JavaScript.<br><br>
            <strong>Mission 2 : Audit et Refonte Documentaire (Méthodologie Agile)</strong><br>
            - Audit de l'existant auprès des Product Owners (POs).<br>
            - Restructuration complète de l'espace de connaissances Confluence pour les 8 services de l'équipe.<br><br>`,
            images: [
                'images/edf-stage.png'
            ],
            tech: ['Python', 'Nornir', 'Django', 'Nautobot', 'JavaScript', 'Confluence', 'Jira']
        },
        {
            title: 'Lyon Central',
            date: 'Septembre 2025',
            description: `<strong>SAÉ - Projet universitaire.</strong><br>Jeu de gestion en ligne inspiré de "911 Operator", développé dans le cadre d'un projet universitaire de groupe.<br><br>
            Fonctionnalités du jeu :<br>
            - Gestion en temps réel des interventions d'urgence<br>
            - Système de comptes utilisateurs avec authentification sécurisée<br>
            - Scoreboard global avec classement des joueurs<br>
            - Carte interactive de Lyon avec Leaflet.js<br>
            - Architecture client-serveur avec Node.js et Express<br>
            - Base de données pour la persistance des scores`,
            images: ['images/lyoncentral1.png', 'images/lyoncentral2.png', 'images/lyoncentral3.png', 'images/lyoncentral4.png', 'images/lyoncentral5.png', 'images/lyoncentral6.png', 'images/lyoncentral7.png'],
            tech: ['Node.js', 'Express.js', 'JavaScript', 'Leaflet.js', 'PHP'],
            site: 'https://lyoncentral.bouaouina.com'
        },
        {
            title: 'Application de guidage – Fête des Lumières',
            date: 'Février 2025',
            description: `<strong>SAÉ - Projet universitaire.</strong><br>Application mobile développée dans le cadre d'un projet universitaire, reprenant le design de TCL (Agence des Mobilités de Lyon).<br><br>
            Fonctionnalités principales :<br>
            - Calcul d'itinéraire optimisé entre les installations lumineuses<br>
            - Intégration de cartes interactives avec Leaflet.js<br>
            - Interface intuitive inspirée du design system de TCL<br>
            - Gestion des données de localisation en temps réel<br>
            - Mode hors-ligne pour économiser la batterie`,
            images: ['images/lyonlumiere.png'],
            tech: ['Swing', 'Java', 'Leaflet.js'],
            link: 'https://github.com/votre-username/lyon-lumiere'
        },
        {
            title: 'Ascenseur automatique pour parking miniature',
            date: 'Mars 2024',
            description: `<strong>SAÉ - Projet de lycée.</strong><br>Prototype de parking automatisé de style japonais, piloté par une carte Arduino. Projet universitaire combinant électronique et développement web.<br><br>
            Caractéristiques du système :<br>
            - Contrôle automatisé via Arduino pour la gestion de l'ascenseur<br>
            - Interface web de contrôle et monitoring en temps réel<br>
            - Visualisation des places disponibles avec mise à jour dynamique<br>
            - Système de capteurs pour la détection des véhicules<br>
            - Protocole de communication série entre Arduino et serveur web`,
            images: ['images/elevator.png', 'images/elevator2.png'],
            tech: ['C++', 'PHP', 'HTML', 'CSS'],
            link: 'https://github.com/votre-username/elevator-parking'
        },
        {
            title: 'Jeu d\'Échecs en Python',
            date: 'Novembre 2025',
            description: `<strong>SAÉ - Projet universitaire.</strong><br>Jeu d'échecs complet développé en Python avec Pygame, respectant toutes les règles officielles du jeu.<br><br>
            Fonctionnalités :<br>
            - Interface graphique 2D avec plateau et pièces visuels<br>
            - Implémentation complète des règles d'échecs (déplacements, prises, échec et mat)<br>
            - Mouvements spéciaux : roque, prise en passant, promotion du pion<br>
            - Détection des situations d'échec, échec et mat, et pat<br>
            - Indicateurs visuels pour les coups possibles`,
            images: [],
            tech: ['Python', 'Pygame'],
            link: 'https://github.com/votre-username/echecs'
        },
        {
            title: 'Jeu de puzzle 2048',
            date: 'Août 2025',
            description: `Implémentation moderne du célèbre jeu 2048, un puzzle addictif où le joueur doit combiner des tuiles pour atteindre la tuile 2048.<br><br>
            Fonctionnalités :<br>
            - Interface utilisateur responsive et intuitive<br>
            - Système de score avec sauvegarde locale (LocalStorage)<br>
            - Animations fluides lors des déplacements de tuiles`,
            images: ['images/2048_1.png', 'images/2048_2.png', 'images/2048_3.png', 'images/2048_4.png'],
            tech: ['HTML', 'JavaScript', 'CSS'],
            github: 'https://github.com/AS0-69/2048',
            site: 'https://2048-aso.vercel.app'
        },
        {
            title: 'Calculatrice en Java',
            date: 'Mai 2025',
            description: `Application de calculatrice simple développée en Java, permettant d'effectuer les opérations arithmétiques de base.`,
            images: ['images/cal1.png', 'images/cal2.png', 'images/cal3.png'],
            tech: ['Java'],
            github: 'https://github.com/AS0-69/calculatrice'
        },
        {
            title: 'Jeu du Pendu en console',
            date: 'Décembre 2023',
            description: `Implémentation classique du jeu du Pendu en C++, jouable dans le terminal.`,
            images: ['images/pednu1.png', 'images/pednu2.png', 'images/pednu3.png'],
            tech: ['C++'],
            github: 'https://github.com/AS0-69/jeu-du-pendu'
        },
        {
            title: 'Application de dessin simplifiée',
            date: 'Juillet 2025',
            description: `Clone simplifié de Microsoft Paint développé en Python avec Tkinter, permettant de dessiner librement.`,
            images: ['images/paint1.png', 'images/paint2.png', 'images/paint3.png'],
            tech: ['Python', 'Tkinter'],
            github: 'https://github.com/AS0-69/jeu-de-dessin-paint'
        },
        {
            title: 'Site vitrine pour une start-up de communication digitale',
            date: 'Juin 2025',
            description: `Réalisé dans le cadre d'une formation, NexusFlow est une plateforme conçue pour une start-up spécialisée dans la production de vidéos publicitaires pour les réseaux sociaux.`,
            images: ['images/nexusflow.png'],
            tech: ['WordPress', 'Figma'],
            site: 'https://agence-nexusflow.com'
        },
        {
            title: 'Jeu de plateforme 2D',
            date: 'Décembre 2025',
            description: `Jeu de plateforme 2D développé avec Pygame, où le joueur doit traverser différents niveaux en évitant des obstacles.`,
            images: ['images/AP_1.png', 'images/AP_2.png', 'images/AP_3.png', 'images/AP_4.png', 'images/AP_5.png', 'images/AP_6.png'],
            tech: ['Python', 'Pygame'],
            github: 'https://github.com/AS0-69/aventure-plateforme'
        },
        {
            title: 'Jeu du Snake classique',
            date: 'Juillet 2025',
            description: `Réimplémentation du jeu classique Snake avec Pygame, où le serpent grandit en mangeant de la nourriture.`,
            images: ['images/snake_1.png', 'images/snake_2.png', 'images/snake_3.png', 'images/snake_4.png'],
            tech: ['Python', 'Pygame'],
            github: 'https://github.com/AS0-69/snake'
        },
        {
            title: 'Jeu de Morpion (Tic-Tac-Toe)',
            date: 'Juillet 2025',
            description: `Jeu de Morpion développé en C# avec une interface graphique Windows Forms.`,
            images: ['images/tictactoe_1.png', 'images/tictactoe_2.png', 'images/tictactoe_3.png'],
            tech: ['C#', '.NET'],
            github: 'https://github.com/AS0-69/morpion'
        },
        {
            title: 'Jeu La Famille en Or',
            date: 'Décembre 2025',
            description: `Reproduction interactive du célèbre jeu télévisé "La Famille en Or", développée pour la CIMG Mosquée Bleue de Villefranche-sur-Saône afin d'animer des événements communautaires.`,
            images: ['images/feo1.png', 'images/feo2.png', 'images/feo3.png'],
            tech: ['HTML', 'CSS', 'JavaScript'],
            github: 'https://github.com/AS0-69/famille-en-or',
            site: 'https://famille-en-or.vercel.app'
        }
    ];

    /* ============================================= */
    /* Système de Modale pour les projets            */
    /* ============================================= */
    const modal = document.getElementById('projectModal');
    const modalClose = document.getElementById('modalClose');
    const modalOverlay = document.querySelector('.modal-overlay');
    const viewMoreButtons = document.querySelectorAll('.view-more-btn');
    
    let currentProjectId = 0;
    let currentImageIndex = 0;
    let carouselInterval = null;
    let progressInterval = null;
    let progressValue = 0;

    if (modal && viewMoreButtons.length > 0) {
        viewMoreButtons.forEach((button) => {
            button.addEventListener('click', (e) => {
                e.stopPropagation();
                const projectBlock = button.closest('.project-block');
                const projectId = parseInt(projectBlock.getAttribute('data-project'));
                openModal(projectId);
            });
        });

        function openModal(projectId) {
            currentProjectId = projectId;
            currentImageIndex = 0;
            const project = projectsData[projectId];
            
            document.getElementById('modalTitle').textContent = project.title;
            document.getElementById('modalDate').querySelector('span').textContent = project.date;
            document.getElementById('modalDescription').innerHTML = project.description;
            
            const githubLink = document.getElementById('modalGithubLink');
            const siteLink = document.getElementById('modalSiteLink');
            
            if (project.github) {
                githubLink.href = project.github;
                githubLink.style.display = 'inline-flex';
            } else {
                githubLink.style.display = 'none';
            }
            
            if (project.site) {
                siteLink.href = project.site;
                siteLink.style.display = 'inline-flex';
            } else {
                siteLink.style.display = 'none';
            }
            
            const modalTech = document.getElementById('modalTech');
            modalTech.innerHTML = '';
            project.tech.forEach(tech => {
                const tag = document.createElement('span');
                tag.className = 'tech-tag';
                tag.textContent = tech;
                modalTech.appendChild(tag);
            });
            
            updateGalleryImage();
            startCarousel();
            
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function updateGalleryImage() {
            const project = projectsData[currentProjectId];
            const modalImage = document.getElementById('modalImage');
            const galleryCounter = document.getElementById('galleryCounter');
            const modalGallery = document.querySelector('.modal-gallery');
            
            if (project.images && project.images.length > 0) {
                modalImage.style.animation = 'none';
                modalImage.style.display = 'block';
                modalGallery.classList.remove('no-image');
                setTimeout(() => {
                    modalImage.src = project.images[currentImageIndex];
                    modalImage.style.animation = 'fadeInImage 0.5s ease-in-out';
                }, 10);
                
                galleryCounter.textContent = `${currentImageIndex + 1} / ${project.images.length}`;
            } else {
                modalImage.style.display = 'none';
                modalGallery.classList.add('no-image');
                galleryCounter.textContent = 'Pas d\'images disponibles';
            }
        }

        function startCarousel() {
            stopCarousel();
            resetProgressBar();
            
            const totalDuration = 5000;
            const updateInterval = 50;
            const progressStep = 100 / (totalDuration / updateInterval);
            
            progressInterval = setInterval(() => {
                progressValue += progressStep;
                if (progressValue >= 100) {
                    progressValue = 100;
                }
                updateProgressBar();
            }, updateInterval);
            
            carouselInterval = setInterval(() => {
                nextImage();
            }, totalDuration);
        }

        function resetProgressBar() {
            progressValue = 0;
            updateProgressBar();
        }

        function updateProgressBar() {
            const progressBar = document.getElementById('carouselProgress');
            if (progressBar) {
                progressBar.style.width = progressValue + '%';
            }
        }

        function stopCarousel() {
            if (carouselInterval) {
                clearInterval(carouselInterval);
                carouselInterval = null;
            }
            if (progressInterval) {
                clearInterval(progressInterval);
                progressInterval = null;
            }
        }

        function nextImage() {
            const project = projectsData[currentProjectId];
            if(project.images && project.images.length > 0) {
                currentImageIndex = (currentImageIndex + 1) % project.images.length;
                updateGalleryImage();
                startCarousel();
            }
        }

        function prevImage() {
            const project = projectsData[currentProjectId];
            if(project.images && project.images.length > 0) {
                currentImageIndex = (currentImageIndex - 1 + project.images.length) % project.images.length;
                updateGalleryImage();
                startCarousel();
            }
        }

        const galleryPrev = document.getElementById('galleryPrev');
        const galleryNext = document.getElementById('galleryNext');

        if (galleryPrev) galleryPrev.addEventListener('click', prevImage);
        if (galleryNext) galleryNext.addEventListener('click', nextImage);

        function closeModal() {
            modal.classList.remove('active');
            document.body.style.overflow = '';
            stopCarousel();
            resetProgressBar();
        }

        modalClose.addEventListener('click', closeModal);
        modalOverlay.addEventListener('click', closeModal);

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('active')) {
                closeModal();
            }
        });
    }

    /* ============================================= */
    /* Modale Mentions Légales                       */
    /* ============================================= */
    const mentionsLink = document.getElementById('mentionsLegalesLink');
    const mentionsModal = document.getElementById('mentionsModal');
    const mentionsClose = document.getElementById('mentionsClose');
    const mentionsOverlay = mentionsModal ? mentionsModal.querySelector('.modal-overlay') : null;

    if (mentionsLink && mentionsModal) {
        mentionsLink.addEventListener('click', (e) => {
            e.preventDefault();
            mentionsModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });

        function closeMentionsModal() {
            mentionsModal.classList.remove('active');
            document.body.style.overflow = '';
        }

        if (mentionsClose) mentionsClose.addEventListener('click', closeMentionsModal);
        if (mentionsOverlay) mentionsOverlay.addEventListener('click', closeMentionsModal);

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && mentionsModal.classList.contains('active')) {
                closeMentionsModal();
            }
        });
    }
});