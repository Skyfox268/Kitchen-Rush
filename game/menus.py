import pygame
from systems.scores import load_scores


MENU_WIDTH = 760
START_MENU_HEIGHT = 620
END_MENU_HEIGHT = 560


def draw_menu_background(game, hauteur):
    game.screen.blit(game.background, (0, 0))

    overlay = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
    overlay.fill((5, 10, 25, 145))
    game.screen.blit(overlay, (0, 0))

    rectangle = pygame.Rect(
        (1920 - MENU_WIDTH) // 2,
        (1080 - hauteur) // 2,
        MENU_WIDTH,
        hauteur,
    )

    panel = pygame.Surface(rectangle.size, pygame.SRCALPHA)
    panel.fill((18, 28, 48, 235))
    game.screen.blit(panel, rectangle.topleft)
    pygame.draw.rect(
        game.screen,
        (226, 173, 76),
        rectangle,
        width=3,
        border_radius=18,
    )

    return rectangle


def draw_centered_text(game, texte, center_x, y, color=(255, 255, 255)):
    surface = game.hud.font.render(texte, True, color)
    rectangle = surface.get_rect(center=(center_x, y))
    game.screen.blit(surface, rectangle)

#Dessiner le menu de démarrage 
def draw_start_menu(game):
    panel = draw_menu_background(game, START_MENU_HEIGHT)
    center_x = panel.centerx

    draw_centered_text(game, "KITCHEN RUSH", center_x, panel.top + 65, (255, 210, 100))
    draw_centered_text(game, "COMMANDES", center_x, panel.top + 145, (130, 210, 255))
    draw_centered_text(game, "Z / Q / S / D : se déplacer", center_x, panel.top + 195)
    draw_centered_text(game, "E : interact", center_x, panel.top + 240)

    draw_centered_text(game, "OBJECTIF", center_x, panel.top + 315, (130, 210, 255))
    draw_centered_text(
        game,
        f"Servir {game.state.daily_target} clients",
        center_x,
        panel.top + 365,
    )
    draw_centered_text(game, "Jour 1 : poisson cuit", center_x, panel.top + 410)
    draw_centered_text(
        game,
        "TAB : meilleurs scores    |    ESPACE : commencer",
        center_x,
        panel.bottom - 55,
        (255, 210, 100),
    )

    pygame.display.flip()

#Menu de scores
def draw_scores_menu(game):
    panel = draw_menu_background(game, 700)
    center_x = panel.centerx
    scores = load_scores().get("jours", {})

    draw_centered_text(
        game,
        "MEILLEURS SCORES",
        center_x,
        panel.top + 60,
        (255, 210, 100),
    )

    y = panel.top + 125
    for day in ("1", "2", "3"): #Va definir le meilleure score pour chaque jour 
        draw_centered_text(
            game,
            f"JOUR {day}",
            center_x,
            y,
            (130, 210, 255),
        )
        resultats = scores.get(day, [])[:3]
        if not resultats:
            draw_centered_text(game, "Aucun score", center_x, y + 42)
        else:
            for index, result in enumerate(resultats, start=1):
                draw_centered_text(
                    game,
                    f"{index}. "
                    f"{result.get('username', result.get('pseudo', 'Anonymous'))}"
                    f" - {result['score']} pts",
                    center_x,
                    y + 42 + (index - 1) * 34,
                )
        y += 170

    draw_centered_text(
        game,
        "ECHAP ou TAB : retour",
        center_x,
        panel.bottom - 42,
        (255, 210, 100),
    )
    pygame.display.flip()

#Menu de fin
def draw_end_menu(game):
    panel = draw_menu_background(game, END_MENU_HEIGHT)
    center_x = panel.centerx

    draw_centered_text(
        game,
        f"JOUR {game.state.day} TERMINE !",
        center_x,
        panel.top + 70,
        (255, 210, 100),
    )
    message = (
        "Objectif atteint !"
        if game.state.unserved_customers < 5
        else "Défaite : trop de clients non servis"
    )
    draw_centered_text(game, message, center_x, panel.top + 140)
    draw_centered_text(game, f"Score : {game.state.score}", center_x, panel.top + 205)
    draw_centered_text(game, f"Argent : {game.state.money} $", center_x, panel.top + 260)

    if game.state.score_saved:
        draw_centered_text(
            game,
            f"Score enregistré pour {game.state.username}",
            center_x,
            panel.top + 350,
            (130, 255, 160),
        )
        instruction = "ESPACE : quitter"
    else:
        draw_centered_text(
            game,
            f"Pseudo : {game.state.username}_",
            center_x,
            panel.top + 350,
        )
        draw_centered_text(
            game,
            "ENTREE : enregistrer le score",
            center_x,
            panel.top + 410,
            (130, 210, 255),
        )
        instruction = "Tapez votre pseudo puis appuyez sur ENTREE"

    draw_centered_text(
        game,
        instruction,
        center_x,
        panel.bottom - 40,
        (255, 210, 100),
    )

    pygame.display.flip()


