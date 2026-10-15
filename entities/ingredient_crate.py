import pygame
from pathlib import Path

#On initialise les caisses d'ingrédients (poisson, poisson cuit, sushi, salade, tomate)
class IngredientCrate(pygame.sprite.Sprite):
    def __init__(self, image_name, x, y, size=(130, 130)):
        super().__init__()

        assets_dir = Path(__file__).resolve().parent.parent / "assets"

        self.image = pygame.image.load(
            str(assets_dir / image_name)
        )
        self.image = pygame.transform.scale(
            self.image,
            size
        )

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.interaction_rect = self.rect.inflate(-20, -20)

