import pygame
import sys

# Initialisation
pygame.init()

# Constantes
LARGEUR = 1200
HAUTEUR = 800
HAUTEUR_BARRE = 80
FPS = 60

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (50, 50, 50)
GRIS_CLAIR = (80, 80, 80)
BLEU_SELECTION = (100, 150, 255)
JAUNE = (255, 255, 0)

# Palette de couleurs
PALETTE = [
    NOIR,
    BLANC,
    (255, 0, 0),      # Rouge
    (0, 255, 0),      # Vert
    (0, 0, 255),      # Bleu
    (255, 255, 0),    # Jaune
    (255, 0, 255),    # Magenta
    (0, 255, 255),    # Cyan
    (255, 165, 0),    # Orange
    (128, 0, 128)     # Violet
]

class PaintApp:
    def __init__(self):
        self.fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Paint App - Python")
        self.clock = pygame.time.Clock()
        
        # Canvas où on dessine
        self.canvas = pygame.Surface((LARGEUR, HAUTEUR - HAUTEUR_BARRE))
        self.canvas.fill(BLANC)
        
        # Paramètres
        self.outil = "dessiner"  # dessiner, gomme, rectangle, cercle, triangle
        self.couleur = NOIR
        self.taille_pinceau = 5
        self.est_en_train_de_dessiner = False
        self.position_debut = None
        self.canvas_temporaire = None
        
        self.font = pygame.font.Font(None, 24)
        self.running = True
    
    def executer(self):
        while self.running:
            self.gerer_evenements()
            self.dessiner()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def gerer_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                souris_x, souris_y = event.pos
                
                # Clic dans la barre d'outils
                if souris_y < HAUTEUR_BARRE:
                    self.gerer_clic_barre(souris_x)
                else:
                    # Clic sur le canvas
                    self.est_en_train_de_dessiner = True
                    self.position_debut = (souris_x, souris_y - HAUTEUR_BARRE)
                    
                    # Sauvegarder le canvas pour les formes
                    if self.outil in ["rectangle", "cercle", "triangle"]:
                        self.canvas_temporaire = self.canvas.copy()
                    
                    # Dessiner un point initial pour le pinceau
                    if self.outil in ["dessiner", "gomme"]:
                        self.dessiner_point(self.position_debut)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.est_en_train_de_dessiner and self.outil in ["rectangle", "cercle", "triangle"]:
                    # Finaliser la forme
                    souris_x, souris_y = event.pos
                    position_fin = (souris_x, souris_y - HAUTEUR_BARRE)
                    self.dessiner_forme(self.position_debut, position_fin)
                    self.canvas_temporaire = None
                
                self.est_en_train_de_dessiner = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.est_en_train_de_dessiner:
                    souris_x, souris_y = event.pos
                    position_actuelle = (souris_x, souris_y - HAUTEUR_BARRE)
                    
                    if self.outil in ["dessiner", "gomme"]:
                        self.dessiner_point(position_actuelle)
                    elif self.outil in ["rectangle", "cercle", "triangle"]:
                        # Prévisualiser la forme
                        self.canvas = self.canvas_temporaire.copy()
                        self.dessiner_forme(self.position_debut, position_actuelle)
    
    def gerer_clic_barre(self, x):
        # Boutons d'outils
        if 10 <= x <= 150:
            self.outil = "dessiner"
        elif 160 <= x <= 310:
            self.outil = "gomme"
        elif 320 <= x <= 420:
            self.outil = "rectangle"
        elif 430 <= x <= 530:
            self.outil = "cercle"
        elif 540 <= x <= 640:
            self.outil = "triangle"
        
        # Palette de couleurs
        elif x >= 700:
            index = (x - 700) // 50
            if 0 <= index < len(PALETTE):
                self.couleur = PALETTE[index]
    
    def dessiner_point(self, position):
        couleur = BLANC if self.outil == "gomme" else self.couleur
        pygame.draw.circle(self.canvas, couleur, position, self.taille_pinceau)
    
    def dessiner_forme(self, debut, fin):
        if self.outil == "rectangle":
            largeur = fin[0] - debut[0]
            hauteur = fin[1] - debut[1]
            pygame.draw.rect(self.canvas, self.couleur, (debut[0], debut[1], largeur, hauteur), 3)
        
        elif self.outil == "cercle":
            rayon = int(((fin[0] - debut[0])**2 + (fin[1] - debut[1])**2)**0.5)
            if rayon > 0:
                pygame.draw.circle(self.canvas, self.couleur, debut, rayon, 3)
        
        elif self.outil == "triangle":
            points = [
                (debut[0], fin[1]),
                ((debut[0] + fin[0]) // 2, debut[1]),
                (fin[0], fin[1])
            ]
            pygame.draw.polygon(self.canvas, self.couleur, points, 3)
    
    def dessiner(self):
        # Fond
        self.fenetre.fill(GRIS)
        
        # Barre d'outils
        self.dessiner_barre_outils()
        
        # Canvas
        self.fenetre.blit(self.canvas, (0, HAUTEUR_BARRE))
        
        pygame.display.flip()
    
    def dessiner_barre_outils(self):
        # Fond de la barre
        pygame.draw.rect(self.fenetre, GRIS, (0, 0, LARGEUR, HAUTEUR_BARRE))
        
        # Boutons
        self.dessiner_bouton(10, 10, 140, 60, "Dessiner", self.outil == "dessiner")
        self.dessiner_bouton(160, 10, 140, 60, "Gomme", self.outil == "gomme")
        self.dessiner_bouton(320, 10, 90, 60, "Rectangle", self.outil == "rectangle")
        self.dessiner_bouton(430, 10, 90, 60, "Cercle", self.outil == "cercle")
        self.dessiner_bouton(540, 10, 90, 60, "Triangle", self.outil == "triangle")
        
        # Palette de couleurs
        for i, couleur in enumerate(PALETTE):
            x = 700 + i * 50
            pygame.draw.rect(self.fenetre, couleur, (x, 20, 40, 40))
            
            # Bordure (jaune si sélectionné)
            if couleur == self.couleur:
                pygame.draw.rect(self.fenetre, JAUNE, (x, 20, 40, 40), 4)
            else:
                pygame.draw.rect(self.fenetre, BLANC, (x, 20, 40, 40), 2)
    
    def dessiner_bouton(self, x, y, largeur, hauteur, texte, selectionne):
        couleur = BLEU_SELECTION if selectionne else GRIS_CLAIR
        pygame.draw.rect(self.fenetre, couleur, (x, y, largeur, hauteur))
        pygame.draw.rect(self.fenetre, BLANC, (x, y, largeur, hauteur), 2)
        
        texte_surface = self.font.render(texte, True, BLANC)
        texte_rect = texte_surface.get_rect(center=(x + largeur // 2, y + hauteur // 2))
        self.fenetre.blit(texte_surface, texte_rect)

if __name__ == "__main__":
    app = PaintApp()
    app.executer()
