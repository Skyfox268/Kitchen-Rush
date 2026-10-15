import pygame

class HUD(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Aestura", 40)
        self.order_font = pygame.font.SysFont("Aestura", 21)
        self.preparation_font = pygame.font.SysFont("Aestura", 26)
        self.text_color = (255, 255, 255)

    #Mise en forme du message de preparation du plat avec le temps restant
    def draw_preparation(
        self,
        screen,
        title,
        remaining_seconds,
        color=(255, 210, 100),
        centre_y=830,
    ):
        panel_rect = pygame.Rect(0, 0, 450, 78)
        panel_rect.center = (960, centre_y)
        panel = pygame.Surface(panel_rect.size, pygame.SRCALPHA)#La surface supporte la transparrence
        panel.fill((18, 28, 48, 235))
        screen.blit(panel, panel_rect.topleft)
        pygame.draw.rect(
            screen,
            (226, 173, 76),
            panel_rect,
            width=2,
            border_radius=12,
        )

        title_surface = self.preparation_font.render(title, True, color)
        timer_surface = self.preparation_font.render(
            f"Temps restant : {remaining_seconds} s",
            True,
            self.text_color,
        )
        screen.blit(
            title_surface,
            title_surface.get_rect(center=(panel_rect.centerx, panel_rect.y + 24)),
        )#Le titre de la commande est centré sur le panel
        screen.blit(
            timer_surface,
            timer_surface.get_rect(center=(panel_rect.centerx, panel_rect.y + 54)),
        )#Le timer de la commande est centré sur le panel

    #Menue en haut a gauche de score
    def draw_progress(self, screen, state):
        panel_rect = pygame.Rect(20, 20, 405, 155)
        panel = pygame.Surface(panel_rect.size, pygame.SRCALPHA)#Gere la transparence du panel
        panel.fill((18, 28, 48, 220))
        screen.blit(panel, panel_rect.topleft)

        pygame.draw.rect(
            screen,
            (226, 173, 76),
            panel_rect,
            width=2,
            border_radius=12,
        )

        title = self.font.render(
            "PROGRESSION",
            True,
            (255, 210, 100),
        )
        score = self.font.render(
            f"Score : {state.score}",
            True,
            self.text_color,
        )
        money = self.font.render(
            f"Argent : {state.money} $",
            True,
            self.text_color,
        )
        target = self.font.render(
            f"Jour {state.day}  |  Plats : "
            f"{state.served_dishes}/{state.daily_target}",
            True,
            self.text_color,
        )

        screen.blit(title, (panel_rect.x + 18, panel_rect.y + 12))
        screen.blit(score, (panel_rect.x + 18, panel_rect.y + 52))
        screen.blit(money, (panel_rect.x + 210, panel_rect.y + 52))
        screen.blit(target, (panel_rect.x + 18, panel_rect.y + 100))
        #on affiche tout avec "screen.blit"

    #Affiche la boite de commande du client avec le temps restant pour le servir
    def draw_order_panel(
        self,
        screen,
        customer,
        remaining_seconds,
        panel_rect=None,
    ):
        order_names = {
            "Poisson cuit": "POISSON",
            "Sushi": "SUSHI",
            "Salade": "SALADE",
        }
        order_name = order_names.get(customer.order, customer.order.upper())

        if panel_rect is None:
            panel_rect = pygame.Rect(0, 0, 250, 92)
            panel_rect.midbottom = customer.rect.midtop
            panel_rect.y -= 8
            panel_rect.clamp_ip(screen.get_rect())

        panel = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
        panel.fill((18, 28, 48, 230))
        screen.blit(panel, panel_rect.topleft)

        pygame.draw.rect(
            screen,
            (226, 173, 76),
            panel_rect,
            width=2,
            border_radius=12,
        )

        title = self.order_font.render(
            "COMMANDE",
            True,
            (130, 210, 255),
        )
        dish = self.order_font.render(
            order_name,
            True,
            (255, 210, 100),
        )
        if remaining_seconds <= 5:
            timer_color = (255, 0, 0) # Rouge si moins de 5 secondes
        elif remaining_seconds <= 10:
            timer_color = (255, 210, 100) # Jaune si moins de 10 secondes
        else:
            timer_color = (130, 255, 150) # Vert sinon
            
        timer = self.order_font.render(
            f"Temps restant : {remaining_seconds} s",
            True,
            timer_color
        )#Systeme de changement de couleur du timer en fonction du temps restant pour servir le client

        titre_rect = title.get_rect(center=(panel_rect.centerx, panel_rect.y + 16))
        plat_rect = dish.get_rect(center=(panel_rect.centerx, panel_rect.y + 42))
        timer_rect = timer.get_rect(center=(panel_rect.centerx, panel_rect.y + 72))
        screen.blit(title, titre_rect)
        screen.blit(dish, plat_rect)
        screen.blit(timer, timer_rect)
