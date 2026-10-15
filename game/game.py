import pygame
from pathlib import Path
from random import randint

from game.assets import load_images
from game.state import GameState
from game.events import handle_events
from game.update import update_game
from game.renderer import draw_game
from game.menus import (
    draw_start_menu,
    draw_end_menu,
    draw_scores_menu,
)

from entities.player import Player
from entities.customer import Customer
from entities.ingredient_crate import IngredientCrate
from ui.hud import HUD
from systems.cooking import start_cooking, SALAD_PREPARATION_TIME
from systems.delivery import deliver_order
from systems.cooking import cut_salmon, discard_items



class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Kitchen Rush")

        self.clock = pygame.time.Clock()
        self.running = True

        self.state = GameState()
        self.hud = HUD()
        self.images = load_images()

        assets_dir = (
            Path(__file__).resolve().parent.parent / "assets"
        )

        self.background = pygame.image.load(str(assets_dir / "lobby_final.png"))
        self.background = pygame.transform.scale(self.background, (1920, 1080))

        self.player = Player()
        self.customers = [Customer(self.state.day)]

        #Globalement de la ligne  52 a 66 on initialise les positions et les caisses / objets avec lesquels le joueur pourra interagir dans le jeu
        self.tomato_crate = IngredientCrate(
            "caisse_tomates.png", 1100, 305, (130, 130)
        )
        self.salad_crate = IngredientCrate(
            "caisse_salade.png", 1250, 305, (130, 130)
        )
        self.salmon_crate = IngredientCrate(
            "caisse_saumon.png", 1400, 305
        )
        self.fish_crate = IngredientCrate("caisse.png", 1550, 305)
        self.stove_rect = pygame.Rect(1300, 80, 120, 70)
        self.cutting_board_rect = pygame.Rect(1220, 210, 80, 80)
        self.bowl_rect = pygame.Rect(1210, 70, 70, 70)
        self.trash_rect = pygame.Rect(965, 110, 130, 130)
        self.trash_interaction_rect = self.trash_rect.copy()

    #Permet de definir une limite de nombres de clients par round
    def max_customers(self):
        return min(2 + self.state.day, 8)

    #Le temps de spawn aleatoire entre chaque client
    def schedule_customer_spawn(self):
        delay = randint(4_000, 9_000)
        self.state.next_customer_spawn = (pygame.time.get_ticks() + delay)

    #Boucle principale du jeu qui permet de mettre a l'écran les différents menus 
    def run(self):
        while self.running:
            delta_seconds = self.clock.tick(60) / 1000
            handle_events(self)

            if self.state.screen == "menu_debut":
                draw_start_menu(self)

            elif self.state.screen == "menu_scores":
                draw_scores_menu(self)

            elif self.state.screen == "jeu":
                update_game(self, delta_seconds)
                self.draw()

            elif self.state.screen == "menu_fin":
                draw_end_menu(self)

        pygame.quit()


    def draw(self):
        draw_game(self)

    #Permet de gerer les collisions entre le joueur et les differents objets du jeu et de definir les actions qui en découlent
    def interact(self):
        state = self.state
        player_rect = self.player.rect

        #Récuperation du poisson cru
        if player_rect.colliderect(self.fish_crate.interaction_rect):
            if not state.raw_fish:
                state.raw_fish = True

        #Commencer la cuisson
        if player_rect.colliderect(self.stove_rect):
            start_cooking(state)

        #Livrer une commande au client si le joueur est en collision avec lui
        for customer in self.customers:
            if customer.departing:
                continue
            if player_rect.colliderect(customer.rect):
                order_delivered = deliver_order(state, customer)

                if order_delivered:
                    self.customers.remove(customer)
                    self.schedule_customer_spawn()

                break # Sortir de la boucle aprés avoir livré
            

        #Récuperation du saumon cru (seulement a partir du jour 2)
        if player_rect.colliderect(self.salmon_crate.interaction_rect):
            if not state.raw_salmon and state.day >= 2:
                state.raw_salmon = True

        #Transformer le saumon cru en sushi pret
        if player_rect.colliderect(self.cutting_board_rect):
            cut_salmon(state)

        #Récuperation de la salade (seulement a partir du jour 3)
        if player_rect.colliderect(self.salad_crate.interaction_rect):
            if not state.raw_salad and state.day >= 3:
                state.raw_salad = True

        #Réuperation de la tomate (seulement a partir du jour 3)
        if player_rect.colliderect(self.tomato_crate.interaction_rect):
            if not state.tomato and state.day >= 3:
                state.tomato = True

        #Mettre la salade dans le bol
        if player_rect.colliderect(self.bowl_rect):
            if state.raw_salad:
                state.raw_salad = False
                state.salad_in_bowl = True

        #Mettre la tomate dans le bol 
        if player_rect.colliderect(self.bowl_rect):
            if state.tomato and state.salad_in_bowl:
                state.tomato = False
                state.salad_in_bowl = False
                state.salad_preparation = True
                state.salad_preparation_end = (
                    pygame.time.get_ticks() + SALAD_PREPARATION_TIME
                )

        #Interagir avec la poubelle
        if player_rect.colliderect(self.trash_interaction_rect):
            discard_items(state)
            

        

       

