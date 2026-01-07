import pygame
import sys

# Initialisation
pygame.init()

# Constantes
LARGEUR_ECRAN = 1200
HAUTEUR_ECRAN = 600
FPS = 60

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU_CIEL = (135, 206, 235)
VERT = (34, 139, 34)
MARRON = (139, 69, 19)
ROUGE = (255, 0, 0)
GRIS = (128, 128, 128)
JAUNE = (255, 223, 0)

# Physique
GRAVITE = 0.6
VITESSE_SAUT = -16
VITESSE_DEPLACEMENT = 6
ACCELERATION = 1.2
FRICTION = 0.8  # Remis comme avant
CONTROLE_AIR = 0.4

# États du jeu
MENU = 0
AIDE = 1
SELECTION_NIVEAU = 2
JEU = 3
VICTOIRE = 4
GAME_OVER = 5

class Joueur(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(ROUGE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.spawn_x = x
        self.spawn_y = y
        
        # Physique
        self.vitesse_x = 0
        self.vitesse_y = 0
        self.sur_sol = False
        self.direction = 1  # 1 = droite, -1 = gauche
        self.peut_sauter = True
        self.temps_saut = 0
        self.invincible = False
        self.temps_invincible = 0
        
        # Saut amélioré
        self.saut_demande = False  # Si le joueur a demandé un saut
        self.temps_saut_buffer = 0  # Temps depuis la demande de saut
        self.temps_depuis_sol = 0   # Temps depuis qu'on a quitté le sol (coyote time)
        
        # Stats
        self.vies = 3
        self.score = 0
        
    def update(self, plateformes):
        # Gérer l'invincibilité temporaire
        if self.invincible:
            self.temps_invincible -= 1
            if self.temps_invincible <= 0:
                self.invincible = False
        
        # Gérer le buffer de saut
        if self.temps_saut_buffer > 0:
            self.temps_saut_buffer -= 1
        
        # Gérer le coyote time (permet de sauter juste après avoir quitté le sol)
        if self.sur_sol:
            self.temps_depuis_sol = 8  # 8 frames de tolérance
        elif self.temps_depuis_sol > 0:
            self.temps_depuis_sol -= 1
        
        # Gravité
        self.vitesse_y += GRAVITE
        
        # Limiter la vitesse de chute
        if self.vitesse_y > 18:
            self.vitesse_y = 18
        
        # Appliquer la friction horizontale quand sur le sol
        if self.sur_sol:
            self.vitesse_x *= FRICTION
            if abs(self.vitesse_x) < 0.5:
                self.vitesse_x = 0
        
        # Déplacement vertical
        self.rect.y += self.vitesse_y
        
        # Collision avec les plateformes (vertical)
        ancien_sur_sol = self.sur_sol
        self.sur_sol = False
        for plateforme in plateformes:
            if self.rect.colliderect(plateforme.rect):
                if self.vitesse_y > 0:  # Tombe
                    self.rect.bottom = plateforme.rect.top
                    self.vitesse_y = 0
                    self.sur_sol = True
                    self.peut_sauter = True
                    
                    # Exécuter le saut si bufferé
                    if self.temps_saut_buffer > 0:
                        self.vitesse_y = VITESSE_SAUT
                        self.sur_sol = False
                        self.temps_saut_buffer = 0
                elif self.vitesse_y < 0:  # Saute et tape la tête
                    self.rect.top = plateforme.rect.bottom
                    self.vitesse_y = 0
        
        # Déplacement horizontal
        self.rect.x += self.vitesse_x
        
        # Collision avec les plateformes (horizontal)
        for plateforme in plateformes:
            if self.rect.colliderect(plateforme.rect):
                if self.vitesse_x > 0:  # Déplacement vers la droite
                    self.rect.right = plateforme.rect.left
                    self.vitesse_x = 0
                elif self.vitesse_x < 0:  # Déplacement vers la gauche
                    self.rect.left = plateforme.rect.right
                    self.vitesse_x = 0
        
        # Limites de l'écran
        if self.rect.left < 0:
            self.rect.left = 0
            self.vitesse_x = 0
        if self.rect.right > LARGEUR_ECRAN:
            self.rect.right = LARGEUR_ECRAN
            self.vitesse_x = 0
        
        # Tomber hors de l'écran = respawn
        if self.rect.top > HAUTEUR_ECRAN:
            self.respawn()
    
    def sauter(self):
        # Saut ultra réactif avec buffer et coyote time
        # Si on est sur le sol ou qu'on vient de quitter le sol (coyote time)
        if self.sur_sol or self.temps_depuis_sol > 0:
            self.vitesse_y = VITESSE_SAUT
            self.sur_sol = False
            self.temps_depuis_sol = 0
            self.temps_saut_buffer = 0
        else:
            # Sinon, on buffer le saut pour quand on touchera le sol
            self.temps_saut_buffer = 10  # 10 frames de buffer
    
    def deplacer(self, direction):
        # Contrôle fluide avec accélération
        if direction != 0:
            # Contrôle en l'air réduit
            facteur = CONTROLE_AIR if not self.sur_sol else 1.0
            vitesse_cible = direction * VITESSE_DEPLACEMENT
            
            # Accélération progressive
            if abs(self.vitesse_x) < abs(vitesse_cible):
                self.vitesse_x += direction * ACCELERATION * facteur
            else:
                self.vitesse_x = vitesse_cible * facteur
            
            # Limiter la vitesse max
            if abs(self.vitesse_x) > VITESSE_DEPLACEMENT:
                self.vitesse_x = direction * VITESSE_DEPLACEMENT
            
            self.direction = direction
    
    def respawn(self):
        """Faire réapparaître le joueur au point de spawn"""
        self.vies -= 1
        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y
        self.vitesse_x = 0
        self.vitesse_y = 0
        self.sur_sol = False
        # Invincibilité temporaire pour éviter les respawns en boucle
        self.invincible = True
        self.temps_invincible = 60  # 1 seconde à 60 FPS
    
    def reinitialiser(self):
        """Réinitialiser le joueur pour une nouvelle partie"""
        self.vies = 3
        self.score = 0
        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y
        self.vitesse_x = 0
        self.vitesse_y = 0
        self.sur_sol = False
        self.invincible = False
        self.temps_invincible = 0
        self.saut_demande = False
        self.temps_saut_buffer = 0
        self.temps_depuis_sol = 0
    
    def dessiner(self, ecran):
        # Corps (rectangle rouge)
        pygame.draw.rect(ecran, ROUGE, self.rect)
        pygame.draw.rect(ecran, NOIR, self.rect, 3)
        
        # Œil (grand œil au centre qui bouge)
        oeil_x = self.rect.centerx + (5 * self.direction)
        oeil_y = self.rect.centery
        # Blanc de l'œil
        pygame.draw.circle(ecran, BLANC, (oeil_x, oeil_y), 12)
        pygame.draw.circle(ecran, NOIR, (oeil_x, oeil_y), 12, 2)
        # Pupille
        pygame.draw.circle(ecran, NOIR, (oeil_x + 3 * self.direction, oeil_y), 5)
        
        # Cheveux sur la tête (2-3 pics)
        cheveu1_x = self.rect.centerx - 10
        cheveu2_x = self.rect.centerx
        cheveu3_x = self.rect.centerx + 10
        cheveu_base_y = self.rect.top
        cheveu_haut_y = self.rect.top - 8
        
        pygame.draw.line(ecran, NOIR, (cheveu1_x, cheveu_base_y), (cheveu1_x - 3, cheveu_haut_y), 3)
        pygame.draw.line(ecran, NOIR, (cheveu2_x, cheveu_base_y), (cheveu2_x, cheveu_haut_y - 3), 3)
        pygame.draw.line(ecran, NOIR, (cheveu3_x, cheveu_base_y), (cheveu3_x + 3, cheveu_haut_y), 3)

class Plateforme(pygame.sprite.Sprite):
    def __init__(self, x, y, largeur, hauteur):
        super().__init__()
        self.image = pygame.Surface((largeur, hauteur))
        self.image.fill(VERT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def dessiner(self, ecran):
        pygame.draw.rect(ecran, MARRON, self.rect)
        pygame.draw.rect(ecran, (90, 45, 10), self.rect, 3)

class Sol(pygame.sprite.Sprite):
    def __init__(self, x, y, largeur, hauteur):
        super().__init__()
        self.image = pygame.Surface((largeur, hauteur))
        self.image.fill(VERT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def dessiner(self, ecran):
        # Herbe verte
        pygame.draw.rect(ecran, VERT, self.rect)
        pygame.draw.rect(ecran, (20, 100, 20), self.rect, 3)
        # Ajouter quelques brins d'herbe
        for i in range(0, int(self.rect.width), 30):
            x = self.rect.x + i
            y = self.rect.top
            pygame.draw.line(ecran, (0, 150, 0), (x, y), (x - 2, y - 5), 2)
            pygame.draw.line(ecran, (0, 150, 0), (x + 5, y), (x + 7, y - 4), 2)
            pygame.draw.line(ecran, (0, 150, 0), (x + 10, y), (x + 10, y - 6), 2)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, largeur, hauteur):
        super().__init__()
        self.image = pygame.Surface((largeur, hauteur))
        self.image.fill(GRIS)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def dessiner(self, ecran):
        # Monstre triangle bleu avec un œil
        centre_x = self.rect.centerx
        centre_y = self.rect.centery
        
        # Triangle bleu
        points = [
            (centre_x, self.rect.top),           # Sommet haut
            (self.rect.left, self.rect.bottom),  # Coin bas gauche
            (self.rect.right, self.rect.bottom)  # Coin bas droit
        ]
        pygame.draw.polygon(ecran, (0, 100, 255), points)
        pygame.draw.polygon(ecran, (0, 50, 150), points, 3)
        
        # Œil du monstre
        oeil_y = centre_y + 5
        pygame.draw.circle(ecran, BLANC, (centre_x, oeil_y), 8)
        pygame.draw.circle(ecran, NOIR, (centre_x, oeil_y), 8, 2)
        pygame.draw.circle(ecran, ROUGE, (centre_x, oeil_y), 4)

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = 0
    
    def dessiner(self, ecran):
        # Pièce d'or animée
        self.angle += 2
        pygame.draw.circle(ecran, JAUNE, self.rect.center, 15)
        pygame.draw.circle(ecran, (200, 180, 0), self.rect.center, 15, 3)
        pygame.draw.circle(ecran, (255, 240, 100), self.rect.center, 8)

class Jeu:
    def __init__(self):
        pygame.init()
        self.ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
        pygame.display.set_caption("Aventure Plateforme")
        self.horloge = pygame.time.Clock()
        self.en_cours = True
        self.etat = MENU
        self.timer = 0
        self.temps_debut = 0
        self.temps_final = 0
        self.etoiles = 0
        self.niveau_actuel = 1
        self.etoiles_par_niveau = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}  # Étoiles obtenues par niveau
        
        # Police pour le texte
        self.font_titre = pygame.font.Font(None, 80)
        self.font_bouton = pygame.font.Font(None, 50)
        self.font_texte = pygame.font.Font(None, 36)
        self.font_petit = pygame.font.Font(None, 28)
        
        # Créer le joueur
        self.joueur = Joueur(100, 100)
        
        # Créer les plateformes (parcours plus facile)
        self.plateformes = pygame.sprite.Group()
        self.plateformes.add(Plateforme(0, HAUTEUR_ECRAN - 40, LARGEUR_ECRAN, 40))  # Sol
        self.plateformes.add(Plateforme(300, 480, 200, 20))  # Plateforme 1
        self.plateformes.add(Plateforme(600, 420, 200, 20))  # Plateforme 2
        self.plateformes.add(Plateforme(900, 360, 200, 20))  # Plateforme 3
        self.plateformes.add(Plateforme(400, 300, 200, 20))  # Plateforme 4
        self.plateformes.add(Plateforme(700, 240, 200, 20))  # Plateforme 5
        self.plateformes.add(Plateforme(1000, 180, 150, 20)) # Plateforme 6
        
        # Créer les obstacles (pierres) - moins nombreux
        self.obstacles = pygame.sprite.Group()
        self.obstacles.add(Obstacle(500, 380, 40, 40))
        self.obstacles.add(Obstacle(800, 320, 40, 40))
        
        # Créer les collectibles (mieux placées)
        self.collectibles = pygame.sprite.Group()
        self.collectibles_initiaux = [
            (400, 440), (700, 380), (500, 260), (800, 200), (1070, 140)
        ]
        for pos in self.collectibles_initiaux:
            self.collectibles.add(Collectible(pos[0], pos[1]))
    
    def dessiner_bouton(self, texte, x, y, largeur, hauteur, couleur_normale, couleur_survol):
        """Dessine un bouton et retourne True si cliqué"""
        souris = pygame.mouse.get_pos()
        clic = pygame.mouse.get_pressed()
        
        # Vérifier si la souris survole le bouton
        if x < souris[0] < x + largeur and y < souris[1] < y + hauteur:
            pygame.draw.rect(self.ecran, couleur_survol, (x, y, largeur, hauteur))
            if clic[0] == 1:
                return True
        else:
            pygame.draw.rect(self.ecran, couleur_normale, (x, y, largeur, hauteur))
        
        # Dessiner le contour
        pygame.draw.rect(self.ecran, NOIR, (x, y, largeur, hauteur), 3)
        
        # Dessiner le texte
        texte_surface = self.font_bouton.render(texte, True, NOIR)
        texte_rect = texte_surface.get_rect(center=(x + largeur // 2, y + hauteur // 2))
        self.ecran.blit(texte_surface, texte_rect)
        
        return False
    
    def charger_niveau(self, numero_niveau):
        """Charge un niveau spécifique"""
        self.niveau_actuel = numero_niveau
        self.plateformes.empty()
        self.obstacles.empty()
        self.collectibles.empty()
        
        # Sol d'herbe commun à tous les niveaux
        self.plateformes.add(Sol(0, HAUTEUR_ECRAN - 40, LARGEUR_ECRAN, 40))
        
        if numero_niveau == 1:
            # Niveau 1 - Facile
            self.plateformes.add(Plateforme(300, 480, 200, 20))
            self.plateformes.add(Plateforme(600, 420, 200, 20))
            self.plateformes.add(Plateforme(900, 360, 200, 20))
            self.plateformes.add(Plateforme(400, 300, 200, 20))
            self.plateformes.add(Plateforme(700, 240, 200, 20))
            
            self.obstacles.add(Obstacle(500, 380, 40, 40))
            self.obstacles.add(Obstacle(800, 320, 40, 40))
            
            self.collectibles_initiaux = [(400, 440), (700, 380), (500, 260), (800, 200)]
        
        elif numero_niveau == 2:
            # Niveau 2 - Moyen
            self.plateformes.add(Plateforme(250, 480, 150, 20))
            self.plateformes.add(Plateforme(500, 420, 150, 20))
            self.plateformes.add(Plateforme(750, 360, 150, 20))
            self.plateformes.add(Plateforme(1000, 300, 150, 20))
            self.plateformes.add(Plateforme(350, 250, 150, 20))
            self.plateformes.add(Plateforme(700, 180, 150, 20))
            
            self.obstacles.add(Obstacle(400, 380, 40, 40))
            self.obstacles.add(Obstacle(650, 320, 40, 40))
            self.obstacles.add(Obstacle(900, 260, 40, 40))
            
            self.collectibles_initiaux = [(350, 380), (600, 320), (850, 260), (450, 210), (800, 140)]
        
        elif numero_niveau == 3:
            # Niveau 3 - Difficile
            self.plateformes.add(Plateforme(200, 500, 120, 20))
            self.plateformes.add(Plateforme(450, 440, 120, 20))
            self.plateformes.add(Plateforme(700, 380, 120, 20))
            self.plateformes.add(Plateforme(950, 320, 120, 20))
            self.plateformes.add(Plateforme(300, 260, 120, 20))
            self.plateformes.add(Plateforme(600, 200, 120, 20))
            self.plateformes.add(Plateforme(900, 140, 120, 20))
            
            self.obstacles.add(Obstacle(350, 400, 40, 40))
            self.obstacles.add(Obstacle(600, 340, 40, 40))
            self.obstacles.add(Obstacle(850, 280, 40, 40))
            self.obstacles.add(Obstacle(500, 160, 40, 40))
            
            self.collectibles_initiaux = [(260, 460), (510, 400), (760, 340), (360, 220), (660, 160), (960, 100)]
        
        elif numero_niveau == 4:
            # Niveau 4 - Très difficile (ajusté)
            self.plateformes.add(Plateforme(180, 480, 100, 20))
            self.plateformes.add(Plateforme(380, 430, 100, 20))  # Descendu de 10px
            self.plateformes.add(Plateforme(580, 370, 100, 20))  # Descendu de 10px
            self.plateformes.add(Plateforme(780, 310, 100, 20))  # Descendu de 10px
            self.plateformes.add(Plateforme(980, 250, 100, 20))  # Descendu de 10px
            self.plateformes.add(Plateforme(400, 190, 100, 20))  # Descendu de 10px
            self.plateformes.add(Plateforme(700, 130, 100, 20))  # Descendu de 10px
            
            self.obstacles.add(Obstacle(280, 390, 40, 40))
            self.obstacles.add(Obstacle(480, 330, 40, 40))
            self.obstacles.add(Obstacle(680, 270, 40, 40))
            self.obstacles.add(Obstacle(880, 210, 40, 40))
            self.obstacles.add(Obstacle(600, 90, 40, 40))
            
            self.collectibles_initiaux = [(230, 440), (430, 390), (630, 330), (830, 270), (1030, 210), (450, 150), (750, 90)]
        
        elif numero_niveau == 5:
            # Niveau 5 - Expert
            self.plateformes.add(Plateforme(150, 500, 80, 20))
            self.plateformes.add(Plateforme(320, 460, 80, 20))
            self.plateformes.add(Plateforme(490, 400, 80, 20))
            self.plateformes.add(Plateforme(660, 340, 80, 20))
            self.plateformes.add(Plateforme(830, 280, 80, 20))
            self.plateformes.add(Plateforme(1000, 220, 80, 20))
            self.plateformes.add(Plateforme(300, 180, 80, 20))
            self.plateformes.add(Plateforme(550, 120, 80, 20))
            self.plateformes.add(Plateforme(850, 100, 80, 20))
            
            self.obstacles.add(Obstacle(230, 420, 40, 40))
            self.obstacles.add(Obstacle(400, 360, 40, 40))
            self.obstacles.add(Obstacle(570, 300, 40, 40))
            self.obstacles.add(Obstacle(740, 240, 40, 40))
            self.obstacles.add(Obstacle(910, 180, 40, 40))
            self.obstacles.add(Obstacle(450, 80, 40, 40))
            
            self.collectibles_initiaux = [(190, 460), (360, 420), (530, 360), (700, 300), (870, 240), (340, 140), (590, 80), (890, 60)]
        
        # Créer les collectibles
        for pos in self.collectibles_initiaux:
            self.collectibles.add(Collectible(pos[0], pos[1]))
    
    def reinitialiser_niveau(self):
        """Réinitialise le niveau actuel"""
        self.joueur.reinitialiser()
        self.charger_niveau(self.niveau_actuel)
        self.timer = 0
        self.temps_debut = pygame.time.get_ticks()
    
    def calculer_etoiles(self, temps):
        """Calcule le nombre d'étoiles en fonction du temps"""
        if temps < 20:
            return 3
        elif temps < 40:
            return 2
        else:
            return 1
    
    def dessiner_etoile(self, centre_x, centre_y, taille, couleur):
        """Dessine une étoile à 5 branches"""
        points = []
        for j in range(5):
            angle = j * 144 - 90
            x = centre_x + taille * pygame.math.Vector2(1, 0).rotate(angle).x
            y = centre_y + taille * pygame.math.Vector2(1, 0).rotate(angle).y
            points.append((x, y))
        pygame.draw.polygon(self.ecran, couleur, points)
        if couleur == JAUNE:
            pygame.draw.polygon(self.ecran, (200, 200, 0), points, 3)
        else:
            pygame.draw.polygon(self.ecran, (100, 100, 100), points, 3)
    
    def dessiner_perso_mini(self, x, y, taille=30):
        """Dessine une miniature du personnage"""
        rect = pygame.Rect(x, y, taille, int(taille * 1.5))
        pygame.draw.rect(self.ecran, ROUGE, rect)
        pygame.draw.rect(self.ecran, NOIR, rect, 2)
        # Œil
        oeil_x = rect.centerx + 3
        oeil_y = rect.centery
        pygame.draw.circle(self.ecran, BLANC, (oeil_x, oeil_y), 8)
        pygame.draw.circle(self.ecran, NOIR, (oeil_x, oeil_y), 8, 1)
        pygame.draw.circle(self.ecran, NOIR, (oeil_x + 2, oeil_y), 3)
        # Cheveux
        pygame.draw.line(self.ecran, NOIR, (rect.centerx - 8, rect.top), (rect.centerx - 10, rect.top - 5), 2)
        pygame.draw.line(self.ecran, NOIR, (rect.centerx, rect.top), (rect.centerx, rect.top - 6), 2)
        pygame.draw.line(self.ecran, NOIR, (rect.centerx + 8, rect.top), (rect.centerx + 10, rect.top - 5), 2)
    
    def dessiner_monstre_mini(self, x, y, taille=30):
        """Dessine une miniature du monstre"""
        # Triangle bleu
        points = [
            (x + taille // 2, y),
            (x, y + taille),
            (x + taille, y + taille)
        ]
        pygame.draw.polygon(self.ecran, (0, 100, 255), points)
        pygame.draw.polygon(self.ecran, (0, 50, 150), points, 2)
        # Œil
        pygame.draw.circle(self.ecran, BLANC, (x + taille // 2, y + int(taille * 0.6)), 6)
        pygame.draw.circle(self.ecran, NOIR, (x + taille // 2, y + int(taille * 0.6)), 6, 1)
        pygame.draw.circle(self.ecran, ROUGE, (x + taille // 2, y + int(taille * 0.6)), 3)
    
    def dessiner_piece_mini(self, x, y, taille=15):
        """Dessine une miniature de pièce"""
        pygame.draw.circle(self.ecran, JAUNE, (x, y), taille)
        pygame.draw.circle(self.ecran, (200, 180, 0), (x, y), taille, 2)
        pygame.draw.circle(self.ecran, (255, 240, 100), (x, y), int(taille * 0.5))
    
    def dessiner_coeur(self, x, y, taille=15):
        """Dessine un cœur avec une belle forme"""
        # Forme de cœur avec polygone lisse
        points = [
            # Haut gauche (arrondi)
            (x - taille * 0.8, y - taille * 0.1),
            (x - taille * 0.9, y + taille * 0.2),
            (x - taille * 0.8, y + taille * 0.5),
            # Milieu gauche
            (x - taille * 0.5, y + taille * 0.7),
            # Pointe du bas
            (x, y + taille * 1.2),
            # Milieu droit
            (x + taille * 0.5, y + taille * 0.7),
            # Haut droit (arrondi)
            (x + taille * 0.8, y + taille * 0.5),
            (x + taille * 0.9, y + taille * 0.2),
            (x + taille * 0.8, y - taille * 0.1),
            # Centre haut
            (x + taille * 0.4, y - taille * 0.3),
            (x, y),
            (x - taille * 0.4, y - taille * 0.3),
        ]
        
        # Remplissage du cœur
        pygame.draw.polygon(self.ecran, ROUGE, points)
        
        # Deux cercles pour arrondir le haut
        pygame.draw.circle(self.ecran, ROUGE, (int(x - taille * 0.45), int(y - taille * 0.15)), int(taille * 0.45))
        pygame.draw.circle(self.ecran, ROUGE, (int(x + taille * 0.45), int(y - taille * 0.15)), int(taille * 0.45))
        
        # Contour foncé
        pygame.draw.circle(self.ecran, (180, 0, 0), (int(x - taille * 0.45), int(y - taille * 0.15)), int(taille * 0.45), 2)
        pygame.draw.circle(self.ecran, (180, 0, 0), (int(x + taille * 0.45), int(y - taille * 0.15)), int(taille * 0.45), 2)
        pygame.draw.polygon(self.ecran, (180, 0, 0), points, 2)
        
        # Reflet pour effet brillant
        pygame.draw.circle(self.ecran, (255, 150, 150), (int(x - taille * 0.3), int(y - taille * 0.1)), int(taille * 0.2))
    
    def dessiner_menu(self):
        """Dessine le menu principal décoré"""
        # Fond ciel avec dégradé
        for y in range(HAUTEUR_ECRAN):
            couleur_r = 135
            couleur_g = 206 - int(y * 0.1)
            couleur_b = 235 - int(y * 0.08)
            pygame.draw.line(self.ecran, (couleur_r, couleur_g, couleur_b), (0, y), (LARGEUR_ECRAN, y))
        
        # Soleil
        pygame.draw.circle(self.ecran, (255, 255, 100), (150, 100), 50)
        pygame.draw.circle(self.ecran, (255, 255, 0), (150, 100), 50, 3)
        
        # Nuages décoratifs
        pygame.draw.circle(self.ecran, BLANC, (900, 80), 30)
        pygame.draw.circle(self.ecran, BLANC, (930, 80), 40)
        pygame.draw.circle(self.ecran, BLANC, (960, 80), 30)
        
        pygame.draw.circle(self.ecran, BLANC, (1050, 120), 25)
        pygame.draw.circle(self.ecran, BLANC, (1075, 120), 35)
        pygame.draw.circle(self.ecran, BLANC, (1100, 120), 25)
        
        # Titre avec ombre
        ombre = self.font_titre.render("AVENTURE PLATEFORME", True, (50, 50, 50))
        ombre_rect = ombre.get_rect(center=(LARGEUR_ECRAN // 2 + 3, 123))
        self.ecran.blit(ombre, ombre_rect)
        
        titre = self.font_titre.render("AVENTURE PLATEFORME", True, NOIR)
        titre_rect = titre.get_rect(center=(LARGEUR_ECRAN // 2, 120))
        self.ecran.blit(titre, titre_rect)
        
        # Décoration - personnages en miniature
        self.dessiner_perso_mini(100, 500, 40)
        self.dessiner_monstre_mini(250, 510, 40)
        self.dessiner_piece_mini(950, 520, 20)
        self.dessiner_piece_mini(1000, 500, 20)
        self.dessiner_piece_mini(1050, 520, 20)
        
        # Plateformes décoratives
        pygame.draw.rect(self.ecran, MARRON, (50, 560, 150, 20))
        pygame.draw.rect(self.ecran, (90, 45, 10), (50, 560, 150, 20), 3)
        pygame.draw.rect(self.ecran, MARRON, (900, 550, 180, 20))
        pygame.draw.rect(self.ecran, (90, 45, 10), (900, 550, 180, 20), 3)
        
        # Boutons
        if self.dessiner_bouton("JOUER", 400, 250, 400, 80, VERT, (100, 255, 100)):
            self.etat = SELECTION_NIVEAU
            pygame.time.wait(200)
        
        if self.dessiner_bouton("AIDE", 400, 360, 400, 80, JAUNE, (255, 255, 150)):
            self.etat = AIDE
            pygame.time.wait(200)
        
        if self.dessiner_bouton("QUITTER", 400, 470, 400, 80, ROUGE, (255, 150, 150)):
            self.en_cours = False
    
    def dessiner_selection_niveau(self):
        """Dessine le menu de sélection des niveaux décoré"""
        # Fond dégradé
        for y in range(HAUTEUR_ECRAN):
            couleur_r = 150
            couleur_g = 200 - int(y * 0.08)
            couleur_b = 255 - int(y * 0.1)
            pygame.draw.line(self.ecran, (couleur_r, couleur_g, couleur_b), (0, y), (LARGEUR_ECRAN, y))
        
        # Nuages
        pygame.draw.circle(self.ecran, BLANC, (200, 80), 25)
        pygame.draw.circle(self.ecran, BLANC, (225, 80), 35)
        pygame.draw.circle(self.ecran, BLANC, (250, 80), 25)
        
        pygame.draw.circle(self.ecran, BLANC, (950, 100), 30)
        pygame.draw.circle(self.ecran, BLANC, (980, 100), 40)
        pygame.draw.circle(self.ecran, BLANC, (1010, 100), 30)
        
        # Pièces décoratives
        self.dessiner_piece_mini(80, 150, 15)
        self.dessiner_piece_mini(1120, 150, 15)
        self.dessiner_piece_mini(100, 500, 12)
        self.dessiner_piece_mini(1100, 500, 12)
        
        # Titre avec ombre
        ombre = self.font_titre.render("SELECTION NIVEAU", True, (50, 50, 50))
        ombre_rect = ombre.get_rect(center=(LARGEUR_ECRAN // 2 + 2, 62))
        self.ecran.blit(ombre, ombre_rect)
        
        titre = self.font_titre.render("SELECTION NIVEAU", True, NOIR)
        titre_rect = titre.get_rect(center=(LARGEUR_ECRAN // 2, 60))
        self.ecran.blit(titre, titre_rect)
        
        # Grille de niveaux (5 cases)
        debut_x = 200
        y_cases = 200
        largeur_case = 150
        hauteur_case = 200
        espacement = 30
        
        for niveau in range(1, 6):
            x = debut_x + (niveau - 1) * (largeur_case + espacement)
            
            # Vérifier si le niveau est débloqué
            if niveau == 1 or self.etoiles_par_niveau[niveau - 1] >= 1:
                debloque = True
                couleur = VERT
                couleur_survol = (100, 255, 100)
            else:
                debloque = False
                couleur = (150, 150, 150)
                couleur_survol = (150, 150, 150)
            
            # Dessiner la case
            souris = pygame.mouse.get_pos()
            clic = pygame.mouse.get_pressed()
            
            if x < souris[0] < x + largeur_case and y_cases < souris[1] < y_cases + hauteur_case:
                pygame.draw.rect(self.ecran, couleur_survol, (x, y_cases, largeur_case, hauteur_case))
                if clic[0] == 1 and debloque:
                    self.niveau_actuel = niveau
                    self.etat = JEU
                    self.reinitialiser_niveau()
                    pygame.time.wait(200)
            else:
                pygame.draw.rect(self.ecran, couleur, (x, y_cases, largeur_case, hauteur_case))
            
            pygame.draw.rect(self.ecran, NOIR, (x, y_cases, largeur_case, hauteur_case), 3)
            
            # Numéro du niveau
            texte_niveau = self.font_bouton.render(f"Niveau {niveau}", True, NOIR)
            texte_rect = texte_niveau.get_rect(center=(x + largeur_case // 2, y_cases + 40))
            self.ecran.blit(texte_niveau, texte_rect)
            
            # Étoiles obtenues (3 étoiles - grises ou jaunes)
            etoiles_obtenues = self.etoiles_par_niveau[niveau]
            for i in range(3):
                etoile_x = x + 30 + i * 35
                etoile_y = y_cases + 110
                if i < etoiles_obtenues:
                    self.dessiner_etoile(etoile_x, etoile_y, 15, JAUNE)
                else:
                    self.dessiner_etoile(etoile_x, etoile_y, 15, GRIS)
        
        # Bouton retour
        if self.dessiner_bouton("RETOUR", 450, 500, 300, 70, ROUGE, (255, 150, 150)):
            self.etat = MENU
            pygame.time.wait(200)
    
    def dessiner_aide(self):
        """Dessine l'écran d'aide avec visuels"""
        self.ecran.fill((200, 230, 255))
        
        # Titre
        titre = self.font_titre.render("COMMENT JOUER", True, NOIR)
        titre_rect = titre.get_rect(center=(LARGEUR_ECRAN // 2, 50))
        self.ecran.blit(titre, titre_rect)
        
        # Section gauche - Objectif
        y = 130
        texte = self.font_texte.render("OBJECTIF :", True, NOIR)
        self.ecran.blit(texte, (100, y))
        texte = self.font_petit.render("Collecte toutes les pieces d'or !", True, NOIR)
        self.ecran.blit(texte, (100, y + 35))
        self.dessiner_piece_mini(280, y + 75, 18)
        texte = self.font_petit.render("Pieces d'or", True, NOIR)
        self.ecran.blit(texte, (310, y + 65))
        
        # Section milieu - Contrôles
        y = 130
        texte = self.font_texte.render("CONTROLES :", True, NOIR)
        self.ecran.blit(texte, (480, y))
        controles = [
            "<- / -> ou Q / D : Deplacer",
            "ESPACE / Z / ^ : Sauter",
        ]
        y_ctrl = y + 35
        for ctrl in controles:
            texte = self.font_petit.render(ctrl, True, NOIR)
            self.ecran.blit(texte, (480, y_ctrl))
            y_ctrl += 30
        
        # Section droite - Danger
        y = 130
        texte = self.font_texte.render("ATTENTION !", True, (200, 0, 0))
        self.ecran.blit(texte, (900, y))
        texte = self.font_petit.render("Evite les monstres !", True, NOIR)
        self.ecran.blit(texte, (900, y + 35))
        self.dessiner_monstre_mini(980, y + 70, 35)
        texte = self.font_petit.render("Monstre", True, NOIR)
        self.ecran.blit(texte, (940, y + 110))
        
        # Section bas - Personnage et règles
        y = 300
        pygame.draw.rect(self.ecran, (180, 220, 255), (60, y, 1080, 195), border_radius=10)
        pygame.draw.rect(self.ecran, NOIR, (60, y, 1080, 195), 3, border_radius=10)
        
        # Ton personnage - à gauche
        texte = self.font_texte.render("TON PERSONNAGE :", True, NOIR)
        self.ecran.blit(texte, (100, y + 20))
        self.dessiner_perso_mini(150, y + 90, 35)
        
        # Règles - à droite, bien espacées
        x_regles = 350
        y_start = y + 20
        
        texte = self.font_petit.render("Tu as 3 vies (coeurs rouges)", True, NOIR)
        self.ecran.blit(texte, (x_regles, y_start))
        
        texte = self.font_petit.render("Finis vite pour avoir des etoiles :", True, NOIR)
        self.ecran.blit(texte, (x_regles, y_start + 40))
        
        # Ligne 1 : < 20s = 3 étoiles
        y_etoiles = y_start + 80
        texte = self.font_petit.render("Moins de 20s =", True, NOIR)
        self.ecran.blit(texte, (x_regles, y_etoiles))
        for i in range(3):
            self.dessiner_etoile(x_regles + 170 + i * 30, y_etoiles + 8, 11, JAUNE)
        
        # Ligne 2 : < 40s = 2 étoiles
        texte = self.font_petit.render("Moins de 40s =", True, NOIR)
        self.ecran.blit(texte, (x_regles + 320, y_etoiles))
        for i in range(2):
            self.dessiner_etoile(x_regles + 490 + i * 30, y_etoiles + 8, 11, JAUNE)
        self.dessiner_etoile(x_regles + 490 + 2 * 30, y_etoiles + 8, 11, GRIS)
        
        # Ligne 3 : > 40s = 1 étoile
        y_etoiles2 = y_etoiles + 40
        texte = self.font_petit.render("Plus de 40s =", True, NOIR)
        self.ecran.blit(texte, (x_regles, y_etoiles2))
        self.dessiner_etoile(x_regles + 170, y_etoiles2 + 8, 11, JAUNE)
        self.dessiner_etoile(x_regles + 170 + 30, y_etoiles2 + 8, 11, GRIS)
        self.dessiner_etoile(x_regles + 170 + 60, y_etoiles2 + 8, 11, GRIS)
        
        # Ligne 4 : Game over = 0 étoile
        texte = self.font_petit.render("Echec (0 vie) =", True, NOIR)
        self.ecran.blit(texte, (x_regles + 320, y_etoiles2))
        for i in range(3):
            self.dessiner_etoile(x_regles + 490 + i * 30, y_etoiles2 + 8, 11, GRIS)
        
        # Bouton retour
        if self.dessiner_bouton("RETOUR", 400, 490, 400, 70, JAUNE, (255, 255, 150)):
            self.etat = MENU
            pygame.time.wait(200)
    
    def dessiner_hud(self):
        """Dessine le HUD (timer, vies, score)"""
        # Timer
        temps_ecoule = (pygame.time.get_ticks() - self.temps_debut) // 1000
        texte_timer = self.font_texte.render(f"Temps: {temps_ecoule}s", True, NOIR)
        self.ecran.blit(texte_timer, (10, 10))
        
        # Vies (cœurs)
        for i in range(self.joueur.vies):
            self.dessiner_coeur(200 + i * 40, 25, 12)
        
        # Score (pièces collectées)
        pieces_total = len(self.collectibles_initiaux)
        pieces_restantes = len(self.collectibles)
        pieces_collectees = pieces_total - pieces_restantes
        texte_score = self.font_texte.render(f"Pieces: {pieces_collectees}/{pieces_total}", True, NOIR)
        self.ecran.blit(texte_score, (LARGEUR_ECRAN - 220, 10))
    
    def dessiner_victoire(self):
        """Dessine l'écran de victoire"""
        self.ecran.fill((100, 255, 100))
        
        # Titre
        titre = self.font_titre.render("VICTOIRE !", True, NOIR)
        titre_rect = titre.get_rect(center=(LARGEUR_ECRAN // 2, 80))
        self.ecran.blit(titre, titre_rect)
        
        # Numéro du niveau
        texte_niveau = self.font_texte.render(f"Niveau {self.niveau_actuel} termine !", True, NOIR)
        texte_rect = texte_niveau.get_rect(center=(LARGEUR_ECRAN // 2, 150))
        self.ecran.blit(texte_niveau, texte_rect)
        
        # Temps
        texte_temps = self.font_texte.render(f"Temps: {self.temps_final}s", True, NOIR)
        texte_rect = texte_temps.get_rect(center=(LARGEUR_ECRAN // 2, 200))
        self.ecran.blit(texte_temps, texte_rect)
        
        # Étoiles (3 grises avec les obtenues en jaune)
        texte_etoiles = self.font_bouton.render("Etoiles:", True, NOIR)
        texte_rect = texte_etoiles.get_rect(center=(LARGEUR_ECRAN // 2, 260))
        self.ecran.blit(texte_etoiles, texte_rect)
        
        for i in range(3):
            centre_x = 450 + i * 100
            centre_y = 340
            if i < self.etoiles:
                self.dessiner_etoile(centre_x, centre_y, 40, JAUNE)
            else:
                self.dessiner_etoile(centre_x, centre_y, 40, GRIS)
        
        # Boutons
        bouton_y = 450
        if self.niveau_actuel < 5:
            # Proposer niveau suivant
            if self.dessiner_bouton("NIVEAU SUIVANT", 200, bouton_y, 280, 70, VERT, (100, 255, 100)):
                self.niveau_actuel += 1
                self.etat = JEU
                self.reinitialiser_niveau()
                pygame.time.wait(200)
            
            if self.dessiner_bouton("REJOUER", 520, bouton_y, 200, 70, JAUNE, (255, 255, 150)):
                self.etat = JEU
                self.reinitialiser_niveau()
                pygame.time.wait(200)
            
            if self.dessiner_bouton("NIVEAUX", 760, bouton_y, 200, 70, (150, 150, 255), (200, 200, 255)):
                self.etat = SELECTION_NIVEAU
                pygame.time.wait(200)
        else:
            # Dernier niveau
            if self.dessiner_bouton("REJOUER", 350, bouton_y, 200, 70, VERT, (100, 255, 100)):
                self.etat = JEU
                self.reinitialiser_niveau()
                pygame.time.wait(200)
            
            if self.dessiner_bouton("NIVEAUX", 600, bouton_y, 200, 70, JAUNE, (255, 255, 150)):
                self.etat = SELECTION_NIVEAU
                pygame.time.wait(200)
    
    def dessiner_game_over(self):
        """Dessine l'écran de game over"""
        self.ecran.fill((255, 100, 100))
        
        # Titre
        titre = self.font_titre.render("GAME OVER", True, NOIR)
        titre_rect = titre.get_rect(center=(LARGEUR_ECRAN // 2, 80))
        self.ecran.blit(titre, titre_rect)
        
        # Numéro du niveau
        texte_niveau = self.font_texte.render(f"Niveau {self.niveau_actuel}", True, NOIR)
        texte_rect = texte_niveau.get_rect(center=(LARGEUR_ECRAN // 2, 150))
        self.ecran.blit(texte_niveau, texte_rect)
        
        # Temps
        texte_temps = self.font_texte.render(f"Temps: {self.temps_final}s", True, NOIR)
        texte_rect = texte_temps.get_rect(center=(LARGEUR_ECRAN // 2, 200))
        self.ecran.blit(texte_temps, texte_rect)
        
        # Étoiles grises (0 obtenue)
        texte_etoiles = self.font_bouton.render("Etoiles:", True, NOIR)
        texte_rect = texte_etoiles.get_rect(center=(LARGEUR_ECRAN // 2, 260))
        self.ecran.blit(texte_etoiles, texte_rect)
        
        for i in range(3):
            centre_x = 450 + i * 100
            centre_y = 340
            self.dessiner_etoile(centre_x, centre_y, 40, GRIS)
        
        texte_message = self.font_texte.render("Tu as perdu toutes tes vies !", True, NOIR)
        texte_rect = texte_message.get_rect(center=(LARGEUR_ECRAN // 2, 410))
        self.ecran.blit(texte_message, texte_rect)
        
        # Boutons (pas de niveau suivant)
        if self.dessiner_bouton("REJOUER", 350, 480, 200, 70, VERT, (100, 255, 100)):
            self.etat = JEU
            self.reinitialiser_niveau()
            pygame.time.wait(200)
        
        if self.dessiner_bouton("NIVEAUX", 600, 480, 200, 70, JAUNE, (255, 255, 150)):
            self.etat = SELECTION_NIVEAU
            pygame.time.wait(200)
    
    def dessiner_fond_jeu(self):
        """Dessine le fond avec décor"""
        # Ciel bleu dégradé
        for y in range(HAUTEUR_ECRAN):
            couleur_r = 135
            couleur_g = 206 - int(y * 0.15)
            couleur_b = 235 - int(y * 0.1)
            pygame.draw.line(self.ecran, (couleur_r, couleur_g, couleur_b), (0, y), (LARGEUR_ECRAN, y))
        
        # Soleil
        pygame.draw.circle(self.ecran, (255, 255, 100), (1000, 100), 50)
        pygame.draw.circle(self.ecran, (255, 255, 0), (1000, 100), 50, 3)
        
        # Nuages
        # Nuage 1
        pygame.draw.circle(self.ecran, BLANC, (200, 120), 30)
        pygame.draw.circle(self.ecran, BLANC, (230, 120), 40)
        pygame.draw.circle(self.ecran, BLANC, (260, 120), 30)
        
        # Nuage 2
        pygame.draw.circle(self.ecran, BLANC, (600, 80), 25)
        pygame.draw.circle(self.ecran, BLANC, (625, 80), 35)
        pygame.draw.circle(self.ecran, BLANC, (650, 80), 25)
        
        # Nuage 3
        pygame.draw.circle(self.ecran, BLANC, (400, 150), 28)
        pygame.draw.circle(self.ecran, BLANC, (428, 150), 38)
        pygame.draw.circle(self.ecran, BLANC, (456, 150), 28)
    
    def dessiner_jeu(self):
        """Dessine l'écran de jeu"""
        self.dessiner_fond_jeu()
        
        # Dessiner les plateformes
        for plateforme in self.plateformes:
            plateforme.dessiner(self.ecran)
        
        # Dessiner les obstacles
        for obstacle in self.obstacles:
            obstacle.dessiner(self.ecran)
        
        # Dessiner le joueur (avec clignotement si invincible)
        if not self.joueur.invincible or self.joueur.temps_invincible % 10 < 5:
            self.joueur.dessiner(self.ecran)
        
        # Dessiner les collectibles
        for collectible in self.collectibles:
            collectible.dessiner(self.ecran)
        
        # Dessiner le HUD
        self.dessiner_hud()
    
    def dessiner(self):
        if self.etat == MENU:
            self.dessiner_menu()
        elif self.etat == AIDE:
            self.dessiner_aide()
        elif self.etat == SELECTION_NIVEAU:
            self.dessiner_selection_niveau()
        elif self.etat == JEU:
            self.dessiner_jeu()
        elif self.etat == VICTOIRE:
            self.dessiner_victoire()
        elif self.etat == GAME_OVER:
            self.dessiner_game_over()
    
    def update(self):
        if self.etat != JEU:
            return
        
        self.joueur.update(self.plateformes)
        
        # Vérifier collision avec obstacles (pierres) seulement si pas invincible
        if not self.joueur.invincible:
            for obstacle in self.obstacles:
                if self.joueur.rect.colliderect(obstacle.rect):
                    # Respawn au point de départ
                    self.joueur.respawn()
                    
                    # Vérifier game over
                    if self.joueur.vies <= 0:
                        self.temps_final = (pygame.time.get_ticks() - self.temps_debut) // 1000
                        self.etat = GAME_OVER
                    break  # Sortir de la boucle pour éviter les bugs
        
        # Vérifier collision avec les collectibles
        collectes = pygame.sprite.spritecollide(self.joueur, self.collectibles, True)
        
        # Vérifier victoire (toutes les pièces collectées)
        if len(self.collectibles) == 0:
            self.temps_final = (pygame.time.get_ticks() - self.temps_debut) // 1000
            self.etoiles = self.calculer_etoiles(self.temps_final)
            # Sauvegarder les étoiles si c'est mieux que le record
            if self.etoiles > self.etoiles_par_niveau[self.niveau_actuel]:
                self.etoiles_par_niveau[self.niveau_actuel] = self.etoiles
            self.etat = VICTOIRE
    
    def gerer_evenements(self):
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                self.en_cours = False
            elif evenement.type == pygame.KEYDOWN and self.etat == JEU:
                if evenement.key == pygame.K_SPACE or evenement.key == pygame.K_UP or evenement.key == pygame.K_z:
                    self.joueur.sauter()
        
        # Gestion continue des touches (seulement en jeu)
        if self.etat == JEU:
            touches = pygame.key.get_pressed()
            if touches[pygame.K_LEFT] or touches[pygame.K_q]:
                self.joueur.deplacer(-1)
            if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
                self.joueur.deplacer(1)
            
            # Permettre le saut en maintenant la touche
            if touches[pygame.K_SPACE] or touches[pygame.K_UP] or touches[pygame.K_z]:
                self.joueur.sauter()
    
    def executer(self):
        while self.en_cours:
            self.gerer_evenements()
            self.update()
            self.dessiner()
            pygame.display.flip()
            self.horloge.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    jeu = Jeu()
    jeu.executer()
