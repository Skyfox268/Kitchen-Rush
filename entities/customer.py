import pygame
from pathlib import Path
from random import randint,choice

ORDER_TIME = 20_000

class Customer(pygame.sprite.Sprite):
    
    def __init__(self, day = 1):
        super().__init__()

        #permet d'ajouter un nouveau client a l'écran
        self.departing = False
        self.departure_speed = 420
        self.initialize_customer(day)


    #déplace aléatoirement le client sur l'écran
    def initialize_customer(self, day = 1):

        self.departing = False

        #permet de résoudre le chemin vers le dossier assets
        assets_dir = Path(__file__).resolve().parent.parent / "assets"

        #permet de choisir aléatoirement un client parmi les 4 images disponibles
        clients = [
            assets_dir / "client.png",
            assets_dir / "client2.png",
            assets_dir / "client3.png",
            assets_dir / "client4.png"
        ]

        #on load le client
        self.image = pygame.image.load(str(choice(clients)))
        self.image = pygame.transform.scale(self.image, (110,120))

        #la position du client avec sa hitbox
        self.rect = self.image.get_rect()
        self.rect.x = randint(100,980)
        self.rect.y = randint(100,620)

        #choisi une order aléatoire parmi les commandes du jour conecerné
        self.order = choice(self.orders_for_day(day))
        self.order_deadline = pygame.time.get_ticks() + ORDER_TIME


    #retourne les commandes du jour concerné
    def orders_for_day(self, day):
        if day == 1:
            return [
                "Poisson cuit",
            ]

        if day == 2:
            return [
                "Poisson cuit",
                "Sushi"
            ]

        if day == 3:
            return [
                "Poisson cuit",
                "Sushi",
                "Salade"
            ]

        return [
            "Poisson cuit",
            "Sushi",
            "Salade"
        ]

    #Gerer les spawn des clients
    def start_departure(self):
         self.departing = True

    def update_departure(self, delta_seconds):
         if not self.departing:
              return False

         self.rect.x += int(self.departure_speed * delta_seconds)
         return self.rect.left > 1920


