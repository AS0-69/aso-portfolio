import pygame
import random
import sys

# Initialisation de pygame
pygame.init()

# Constantes
LARGEUR = 600
HAUTEUR = 600
TAILLE_CASE = 20
FPS = 10

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
GRIS_FONCE = (40, 40, 40)
GRIS_MOYEN = (30, 30, 30)
ORANGE = (255, 165, 0)

class Snake:
    def __init__(self):
        self.longueur = 1
        self.positions = [((LARGEUR // 2), (HAUTEUR // 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.couleur = VERT
        self.score = 0

    def obtenir_tete(self):
        return self.positions[0]

    def tourner(self, point):
        if self.longueur > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def deplacer(self):
        cur = self.obtenir_tete()
        x, y = self.direction
        nouvelle = (cur[0] + (x * TAILLE_CASE), cur[1] + (y * TAILLE_CASE))
        
        # Vérifier collision avec les murs
        if nouvelle[0] < TAILLE_CASE or nouvelle[0] >= LARGEUR - TAILLE_CASE or nouvelle[1] < TAILLE_CASE or nouvelle[1] >= HAUTEUR - TAILLE_CASE:
            return False  # Game Over
        # Vérifier collision avec soi-même
        elif len(self.positions) > 2 and nouvelle in self.positions[2:]:
            return False  # Game Over
        else:
            self.positions.insert(0, nouvelle)
            if len(self.positions) > self.longueur:
                self.positions.pop()
            return True  # Continue

    def reinitialiser(self):
        self.longueur = 1
        self.positions = [((LARGEUR // 2), (HAUTEUR // 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.score = 0

    def dessiner(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.couleur, (p[0], p[1], TAILLE_CASE, TAILLE_CASE))
            pygame.draw.rect(surface, BLANC, (p[0], p[1], TAILLE_CASE, TAILLE_CASE), 1)

    def gerer_touches(self, event):
        if event.key == pygame.K_UP:
            self.tourner((0, -1))
        elif event.key == pygame.K_DOWN:
            self.tourner((0, 1))
        elif event.key == pygame.K_LEFT:
            self.tourner((-1, 0))
        elif event.key == pygame.K_RIGHT:
            self.tourner((1, 0))

class Nourriture:
    def __init__(self):
        self.position = (0, 0)
        self.couleur = ROUGE
        self.generer()

    def generer(self):
        # Générer la nourriture à l'intérieur des murs
        self.position = (random.randint(1, (LARGEUR // TAILLE_CASE) - 2) * TAILLE_CASE,
                        random.randint(1, (HAUTEUR // TAILLE_CASE) - 2) * TAILLE_CASE)

    def dessiner(self, surface):
        pygame.draw.rect(surface, self.couleur, (self.position[0], self.position[1], TAILLE_CASE, TAILLE_CASE))
        pygame.draw.rect(surface, BLANC, (self.position[0], self.position[1], TAILLE_CASE, TAILLE_CASE), 1)

def afficher_score(score, surface, font):
    texte = font.render(f"Score: {score}", True, BLANC)
    surface.blit(texte, (10, 10))

def dessiner_damier(surface):
    """Dessine un damier sur le fond"""
    for ligne in range(0, HAUTEUR // TAILLE_CASE):
        for colonne in range(0, LARGEUR // TAILLE_CASE):
            if (ligne + colonne) % 2 == 0:
                couleur = GRIS_FONCE
            else:
                couleur = GRIS_MOYEN
            pygame.draw.rect(surface, couleur, (colonne * TAILLE_CASE, ligne * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))

def dessiner_murs(surface):
    """Dessine les murs sur les bords"""
    # Mur du haut
    for i in range(0, LARGEUR // TAILLE_CASE):
        pygame.draw.rect(surface, ORANGE, (i * TAILLE_CASE, 0, TAILLE_CASE, TAILLE_CASE))
        pygame.draw.rect(surface, BLANC, (i * TAILLE_CASE, 0, TAILLE_CASE, TAILLE_CASE), 1)
    
    # Mur du bas
    for i in range(0, LARGEUR // TAILLE_CASE):
        pygame.draw.rect(surface, ORANGE, (i * TAILLE_CASE, HAUTEUR - TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
        pygame.draw.rect(surface, BLANC, (i * TAILLE_CASE, HAUTEUR - TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 1)
    
    # Mur de gauche
    for i in range(0, HAUTEUR // TAILLE_CASE):
        pygame.draw.rect(surface, ORANGE, (0, i * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
        pygame.draw.rect(surface, BLANC, (0, i * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 1)
    
    # Mur de droite
    for i in range(0, HAUTEUR // TAILLE_CASE):
        pygame.draw.rect(surface, ORANGE, (LARGEUR - TAILLE_CASE, i * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
        pygame.draw.rect(surface, BLANC, (LARGEUR - TAILLE_CASE, i * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 1)

def afficher_ecran_start(surface, font_titre, font_texte):
    """Affiche l'écran de démarrage"""
    titre = font_titre.render("SNAKE", True, VERT)
    instruction = font_texte.render("Appuyez sur une flèche pour commencer", True, BLANC)
    
    surface.blit(titre, (LARGEUR // 2 - titre.get_width() // 2, HAUTEUR // 2 - 100))
    surface.blit(instruction, (LARGEUR // 2 - instruction.get_width() // 2, HAUTEUR // 2 + 50))

def afficher_game_over(surface, font_titre, font_texte, score):
    """Affiche l'écran de game over"""
    game_over = font_titre.render("GAME OVER", True, ROUGE)
    score_texte = font_texte.render(f"Score: {score}", True, BLANC)
    instruction = font_texte.render("Appuyez sur une flèche pour recommencer", True, BLANC)
    
    surface.blit(game_over, (LARGEUR // 2 - game_over.get_width() // 2, HAUTEUR // 2 - 100))
    surface.blit(score_texte, (LARGEUR // 2 - score_texte.get_width() // 2, HAUTEUR // 2))
    surface.blit(instruction, (LARGEUR // 2 - instruction.get_width() // 2, HAUTEUR // 2 + 50))

def main():
    # Configuration de la fenêtre
    screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Jeu de Snake")
    clock = pygame.time.Clock()
    font_score = pygame.font.Font(None, 36)
    font_titre = pygame.font.Font(None, 72)
    font_texte = pygame.font.Font(None, 30)

    # Création du snake et de la nourriture
    snake = Snake()
    nourriture = Nourriture()

    # États du jeu: 'start', 'jeu', 'game_over'
    etat = 'start'

    # Boucle principale du jeu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Démarrer le jeu depuis l'écran de start
                if etat == 'start':
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        etat = 'jeu'
                        snake.gerer_touches(event)
                # Recommencer depuis game over
                elif etat == 'game_over':
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        snake.reinitialiser()
                        nourriture.generer()
                        etat = 'jeu'
                        snake.gerer_touches(event)
                # Gérer les touches pendant le jeu
                elif etat == 'jeu':
                    snake.gerer_touches(event)

        # Affichage du damier et des murs pour tous les états
        dessiner_damier(screen)
        dessiner_murs(screen)

        if etat == 'start':
            # Écran de démarrage
            afficher_ecran_start(screen, font_titre, font_texte)
        
        elif etat == 'jeu':
            # Déplacement du snake
            vivant = snake.deplacer()
            
            if not vivant:
                etat = 'game_over'
            else:
                # Vérifier si le snake mange la nourriture
                if snake.obtenir_tete() == nourriture.position:
                    snake.longueur += 1
                    snake.score += 10
                    nourriture.generer()

            # Affichage du jeu
            snake.dessiner(screen)
            nourriture.dessiner(screen)
            afficher_score(snake.score, screen, font_score)
        
        elif etat == 'game_over':
            # Afficher le snake et la nourriture en arrière-plan
            snake.dessiner(screen)
            nourriture.dessiner(screen)
            # Écran de game over
            afficher_game_over(screen, font_titre, font_texte, snake.score)
        
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
