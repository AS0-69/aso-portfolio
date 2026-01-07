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
    /* Système de filtrage des projets              */
    /* ============================================= */
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectBlocks = document.querySelectorAll('.project-block');

    if (filterButtons.length > 0 && projectBlocks.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                // Retirer la classe active de tous les boutons
                filterButtons.forEach(btn => btn.classList.remove('active'));
                // Ajouter la classe active au bouton cliqué
                button.classList.add('active');

                const filter = button.getAttribute('data-filter');

                // Filtrer les projets
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
    /* Système de Modale pour les projets            */
    /* ============================================= */
    const projectsData = [
        {
            title: 'Lyon Central',
            date: 'Septembre 2025',
            description: `Jeu de gestion en ligne inspiré de "911 Operator", développé dans le cadre d'un projet universitaire de groupe.
            
            Fonctionnalités du jeu :
            - Gestion en temps réel des interventions d'urgence
            - Système de comptes utilisateurs avec authentification sécurisée
            - Scoreboard global avec classement des joueurs
            - Carte interactive de Lyon avec Leaflet.js
            - Architecture client-serveur avec Node.js et Express
            - Base de données pour la persistance des scores
            
            Ce projet m'a permis de développer mes compétences en architecture logicielle et en travail d'équipe.`,
            images: ['images/lyoncentral1.png', 'images/lyoncentral2.png', 'images/lyoncentral3.png', 'images/lyoncentral4.png', 'images/lyoncentral5.png', 'images/lyoncentral6.png', 'images/lyoncentral7.png'],
            tech: ['Node.js', 'Express.js', 'JavaScript', 'Leaflet.js', 'PHP'],
            link: 'https://lyoncentral.bouaouina.com'
        },
        {
            title: 'Application de guidage – Fête des Lumières',
            date: 'Février 2025',
            description: `Application mobile développée dans le cadre d'un projet universitaire, reprenant le design de TCL (Agence des Mobilités de Lyon).
            
            Fonctionnalités principales :
            - Calcul d'itinéraire optimisé entre les installations lumineuses
            - Intégration de cartes interactives avec Leaflet.js
            - Interface intuitive inspirée du design system de TCL
            - Gestion des données de localisation en temps réel
            - Mode hors-ligne pour économiser la batterie
            
            Ce projet m'a permis de développer mes compétences en développement d'applications mobiles et en intégration de cartographie interactive.`,
            images: ['images/lyonlumiere.png'],
            tech: ['Swing', 'Java', 'Leaflet.js'],
            link: 'https://github.com/votre-username/lyon-lumiere'
        },
        {
            title: 'Ascenseur automatique pour parking miniature',
            date: 'Mars 2024',
            description: `Prototype de parking automatisé de style japonais, piloté par une carte Arduino. Projet universitaire combinant électronique et développement web.
            
            Caractéristiques du système :
            - Contrôle automatisé via Arduino pour la gestion de l'ascenseur
            - Interface web de contrôle et monitoring en temps réel
            - Visualisation des places disponibles avec mise à jour dynamique
            - Système de capteurs pour la détection des véhicules
            - Protocole de communication série entre Arduino et serveur web
            
            Ce projet m'a permis d'explorer l'IoT et la communication entre hardware et software.`,
            images: ['images/elevator.png', 'images/elevator2.png'],
            tech: ['C++', 'PHP', 'HTML', 'CSS'],
            link: 'https://github.com/votre-username/elevator-parking'
        },
        {
            title: 'Jeu d\'Échecs en Python',
            date: 'Novembre 2025',
            description: `Projet universitaire de jeu d'échecs complet développé en Python avec Pygame, respectant toutes les règles officielles du jeu.
            
            Fonctionnalités :
            - Interface graphique 2D avec plateau et pièces visuels
            - Implémentation complète des règles d'échecs (déplacements, prises, échec et mat)
            - Mouvements spéciaux : roque, prise en passant, promotion du pion
            - Détection des situations d'échec, échec et mat, et pat
            - Indicateurs visuels pour les coups possibles
            - Mode 2 joueurs en local
            - Historique des coups joués
            
            Ce projet académique m'a permis d'approfondir mes compétences en programmation orientée objet et en gestion de logique de jeu complexe.`,
            images: [],
            tech: ['Python', 'Pygame'],
            link: 'https://github.com/votre-username/echecs'
        },
        {
            title: 'Jeu de puzzle 2048',
            date: 'Août 2025',
            description: `Implémentation moderne du célèbre jeu 2048, un puzzle addictif où le joueur doit combiner des tuiles pour atteindre la tuile 2048.
            
            Fonctionnalités :
            - Interface utilisateur responsive et intuitive
            - Système de score avec sauvegarde locale (LocalStorage)
            - Animations fluides lors des déplacements de tuiles
            - Détection automatique de fin de partie
            - Possibilité de recommencer à tout moment
            - Design moderne avec des couleurs adaptatives
            
            Ce projet m'a permis de perfectionner mes compétences en JavaScript et en gestion d'état d'application.`,
            images: ['images/2048_1.png', 'images/2048_2.png', 'images/2048_3.png', 'images/2048_4.png'],
            tech: ['HTML', 'JavaScript', 'CSS'],
            link: 'https://github.com/votre-username/2048'
        },
        {
            title: 'Calculatrice en Java',
            date: 'Mai 2025',
            description: `Application de calculatrice simple développée en Java, permettant d'effectuer les opérations arithmétiques de base.
            
            Fonctionnalités :
            - Interface graphique claire et ergonomique
            - Opérations de base : addition, soustraction, multiplication, division
            - Gestion des nombres décimaux
            - Historique des calculs
            - Gestion des erreurs (division par zéro, etc.)
            
            Ce projet m'a permis de pratiquer la programmation orientée objet en Java et de créer une interface utilisateur fonctionnelle.`,
            images: ['images/cal1.png', 'images/cal2.png', 'images/cal3.png'],
            tech: ['Java'],
            link: 'https://github.com/votre-username/calculatrice'
        },
        {
            title: 'Jeu du Pendu en console',
            date: 'Décembre 2023',
            description: `Implémentation classique du jeu du Pendu en C++, jouable dans le terminal.
            
            Fonctionnalités :
            - Liste de mots aléatoires tirés d'un dictionnaire
            - Affichage visuel du pendu en ASCII art
            - Compteur de tentatives restantes
            - Système de score et de statistiques
            - Gestion des lettres déjà proposées
            - Difficulté ajustable
            
            Ce projet m'a permis de renforcer mes bases en C++ et en gestion de la logique de jeu.`,
            images: ['images/pednu1.png', 'images/pednu2.png', 'images/pednu3.png'],
            tech: ['C++'],
            link: 'https://github.com/votre-username/pendu'
        },
        {
            title: 'Application de dessin simplifiée',
            date: 'Juillet 2025',
            description: `Clone simplifié de Microsoft Paint développé en Python avec Tkinter, permettant de dessiner librement.
            
            Fonctionnalités :
            - Outils de dessin : crayon, pinceau, ligne, rectangle, cercle
            - Palette de couleurs personnalisable
            - Réglage de l'épaisseur du trait
            - Gomme pour effacer
            - Sauvegarde et chargement d'images
            - Interface intuitive et facile d'utilisation
            
            Ce projet m'a permis de découvrir Tkinter et la gestion d'événements graphiques en Python.`,
            images: ['images/paint1.png', 'images/paint2.png', 'images/paint3.png'],
            tech: ['Python', 'Tkinter'],
            link: 'https://github.com/votre-username/paint-simple'
        },
        {
            title: 'Site vitrine pour une start-up de communication digitale',
            date: 'Juin 2025',
            description: `Projet universitaire réalisé dans le cadre de ma formation, NexusFlow est une plateforme conçue pour une start-up spécialisée dans la production de vidéos publicitaires pour les réseaux sociaux.
            
            Spécifications techniques :
            - Maquettage complet du site sur Figma avec prototype interactif
            - Développement du site sous WordPress avec personnalisation du thème
            - Design moderne et responsive adapté à tous les supports
            - Galerie de portfolio interactive avec filtres dynamiques
            - Formulaire de contact intégré
            - Optimisation SEO et des performances
            
            Ce projet m'a permis d'approfondir mes compétences en conception UI/UX avec Figma et en développement WordPress.`,
            images: ['images/nexusflow.png'],
            tech: ['WordPress', 'Figma'],
            link: 'https://agence-nexusflow.com'
        },
        {
            title: 'Jeu de plateforme 2D',
            date: 'Décembre 2025',
            description: `Jeu de plateforme 2D développé avec Pygame, où le joueur doit traverser différents niveaux en évitant des obstacles.
            
            Fonctionnalités :
            - Physique réaliste avec gravité et collisions
            - Plusieurs niveaux avec difficulté progressive
            - Système de vies et de points
            - Ennemis avec patterns de déplacement
            - Power-ups et bonus collectables
            - Musique et effets sonores
            
            Ce projet m'a permis d'approfondir mes connaissances en développement de jeux vidéo et en gestion de la physique 2D.`,
            images: ['images/AP_1.png', 'images/AP_2.png', 'images/AP_3.png', 'images/AP_4.png', 'images/AP_5.png', 'images/AP_6.png'],
            tech: ['Python', 'Pygame'],
            link: 'https://github.com/votre-username/plateforme'
        },
        {
            title: 'Jeu du Snake classique',
            date: 'Juillet 2025',
            description: `Réimplémentation du jeu classique Snake avec Pygame, où le serpent grandit en mangeant de la nourriture.
            
            Fonctionnalités :
            - Contrôles fluides au clavier (flèches directionnelles)
            - Vitesse progressive augmentant avec le score
            - Système de high score avec sauvegarde
            - Détection de collision avec les murs et le corps
            - Design rétro fidèle au jeu original
            - Mode pause
            
            Ce projet a été ma première incursion dans le développement de jeux avec Python et Pygame.`,
            images: ['images/snake_1.png', 'images/snake_2.png', 'images/snake_3.png', 'images/snake_4.png'],
            tech: ['Python', 'Pygame'],
            link: 'https://github.com/votre-username/snake'
        },
        {
            title: 'Jeu de Morpion (Tic-Tac-Toe)',
            date: 'Juillet 2025',
            description: `Jeu de Morpion développé en C# avec une interface graphique Windows Forms.
            
            Fonctionnalités :
            - Mode 2 joueurs en local
            - Interface graphique intuitive et réactive
            - Détection automatique de victoire ou match nul
            - Compteur de scores pour plusieurs parties
            - Animations visuelles lors de la victoire
            - Possibilité de recommencer rapidement
            
            Ce projet m'a permis de découvrir C# et le framework .NET pour le développement d'applications Windows.`,
            images: ['images/tictactoe_1.png', 'images/tictactoe_2.png', 'images/tictactoe_3.png'],
            tech: ['C#', '.NET'],
            link: 'https://github.com/votre-username/morpion'
        },
        {
            title: 'Jeu La Famille en Or',
            date: 'Décembre 2025',
            description: `Reproduction interactive du célèbre jeu télévisé "La Famille en Or", développée pour la CIMG Mosquée Bleue de Villefranche-sur-Saône afin d'animer des événements communautaires.
            
            Fonctionnalités :
            - Système de questions avec réponses multiples et scores
            - Mode solo ou mode équipe configurable
            - Compteur d'erreurs personnalisable (1 à illimité)
            - Système d'indices optionnel pour aider les joueurs
            - Plusieurs catégories de questions thématiques
            - Animations et effets sonores pour une expérience immersive
            - Interface fidèle au jeu télévisé avec tableau de scores
            - Gestion des manches et calcul automatique des points
            
            Projet commandé par le CIMG pour rassembler la communauté autour d'une activité ludique et conviviale.`,
            images: ['images/feo1.png', 'images/feo2.png', 'images/feo3.png'],
            tech: ['HTML', 'CSS', 'JavaScript'],
            link: 'https://famille-en-or.vercel.app/'
        }
    ];

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
        viewMoreButtons.forEach((button, index) => {
            button.addEventListener('click', (e) => {
                e.stopPropagation();
                const projectBlock = button.closest('.project-block');
                const projectId = parseInt(projectBlock.getAttribute('data-project'));
                openModal(projectId);
            });
        });

        // Fonction pour ouvrir la modale
        function openModal(projectId) {
            currentProjectId = projectId;
            currentImageIndex = 0;
            const project = projectsData[projectId];
            
            // Remplir les informations
            document.getElementById('modalTitle').textContent = project.title;
            document.getElementById('modalDate').querySelector('span').textContent = project.date;
            document.getElementById('modalDescription').innerHTML = project.description.replace(/\n/g, '<br><br>');
            document.getElementById('modalLink').href = project.link;
            
            // Remplir les technologies
            const modalTech = document.getElementById('modalTech');
            modalTech.innerHTML = '';
            project.tech.forEach(tech => {
                const tag = document.createElement('span');
                tag.className = 'tech-tag';
                tag.textContent = tech;
                modalTech.appendChild(tag);
            });
            
            // Afficher la première image
            updateGalleryImage();
            
            // Démarrer le carousel automatique
            startCarousel();
            
            // Afficher la modale
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        // Fonction pour mettre à jour l'image de la galerie
        function updateGalleryImage() {
            const project = projectsData[currentProjectId];
            const modalImage = document.getElementById('modalImage');
            const galleryCounter = document.getElementById('galleryCounter');
            const modalGallery = document.querySelector('.modal-gallery');
            
            // Vérifier si le projet a des images
            if (project.images && project.images.length > 0) {
                // Retirer l'animation puis la réappliquer pour la relancer
                modalImage.style.animation = 'none';
                modalImage.style.display = 'block';
                modalGallery.classList.remove('no-image');
                setTimeout(() => {
                    modalImage.src = project.images[currentImageIndex];
                    modalImage.style.animation = 'fadeInImage 0.5s ease-in-out';
                }, 10);
                
                galleryCounter.textContent = `${currentImageIndex + 1} / ${project.images.length}`;
            } else {
                // Pas d'image - afficher un placeholder
                modalImage.style.display = 'none';
                modalGallery.classList.add('no-image');
                galleryCounter.textContent = 'Pas d\'images disponibles';
            }
        }

        // Fonction pour démarrer le carousel automatique
        function startCarousel() {
            // Arrêter les intervalles existants
            stopCarousel();
            
            // Réinitialiser et démarrer la barre de progression
            resetProgressBar();
            
            // Durée totale : 5 secondes pour un meilleur timing
            const totalDuration = 5000; // 5 secondes
            const updateInterval = 50; // Mise à jour toutes les 50ms
            const progressStep = 100 / (totalDuration / updateInterval);
            
            // Animer la barre de progression
            progressInterval = setInterval(() => {
                progressValue += progressStep;
                if (progressValue >= 100) {
                    progressValue = 100;
                }
                updateProgressBar();
            }, updateInterval);
            
            // Démarrer un nouveau carousel avec la même durée
            carouselInterval = setInterval(() => {
                nextImage();
            }, totalDuration);
        }

        // Fonction pour réinitialiser la barre de progression
        function resetProgressBar() {
            progressValue = 0;
            updateProgressBar();
        }

        // Fonction pour mettre à jour la barre de progression
        function updateProgressBar() {
            const progressBar = document.getElementById('carouselProgress');
            if (progressBar) {
                progressBar.style.width = progressValue + '%';
            }
        }

        // Fonction pour arrêter le carousel
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

        // Fonction pour l'image suivante
        function nextImage() {
            const project = projectsData[currentProjectId];
            currentImageIndex = (currentImageIndex + 1) % project.images.length;
            updateGalleryImage();
            // Redémarrer le carousel et la barre de progression
            startCarousel();
        }

        // Fonction pour l'image précédente
        function prevImage() {
            const project = projectsData[currentProjectId];
            currentImageIndex = (currentImageIndex - 1 + project.images.length) % project.images.length;
            updateGalleryImage();
            // Redémarrer le carousel et la barre de progression
            startCarousel();
        }

        // Boutons de navigation de la galerie
        const galleryPrev = document.getElementById('galleryPrev');
        const galleryNext = document.getElementById('galleryNext');

        if (galleryPrev) {
            galleryPrev.addEventListener('click', () => {
                prevImage();
            });
        }

        if (galleryNext) {
            galleryNext.addEventListener('click', () => {
                nextImage();
            });
        }

        // Fermer la modale
        function closeModal() {
            modal.classList.remove('active');
            document.body.style.overflow = '';
            stopCarousel(); // Arrêter le carousel quand on ferme la modale
            resetProgressBar(); // Réinitialiser la barre
        }

        modalClose.addEventListener('click', closeModal);
        modalOverlay.addEventListener('click', closeModal);

        // Fermer avec Échap
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

        if (mentionsClose) {
            mentionsClose.addEventListener('click', closeMentionsModal);
        }

        if (mentionsOverlay) {
            mentionsOverlay.addEventListener('click', closeMentionsModal);
        }

        // Fermer avec Échap
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && mentionsModal.classList.contains('active')) {
                closeMentionsModal();
            }
        });
    }

}); // Fin de DOMContentLoaded
