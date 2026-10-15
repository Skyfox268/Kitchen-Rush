import pygame
from pathlib import Path

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        #charger l'image du cuistot (joueur)
        assets_dir = Path(__file__).resolve().parent.parent / "assets"
        self.image = pygame.image.load(str(assets_dir / "player_cuistot.png"))
        self.image = pygame.transform.scale(self.image, (120,120))
        
        #On recupere la hitbox du joueur
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 50
    
    # les déplacements basique (z,q,s,d) du joueur
    def move_right(self):
        self.rect.x += 10
    
    def move_left(self):
        self.rect.x -= 10
    
    def move_up(self):
        self.rect.y -= 10
    
    def move_down(self):
        self.rect.y += 10



