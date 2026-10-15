import pygame


def show_end_menu(state):
    state.username = ""
    state.score_saved = False
    state.screen = "menu_fin"
    pygame.key.start_text_input()

#Compte combien de plats ont été servis et ajoute le score et l'argent du joueur
def register_served_dish(state, price):
    state.served_dishes += 1
    state.score += 1
    state.money += price

    if state.served_dishes >= state.daily_target:
        if state.day >= 3:
            show_end_menu(state)
        else:
            state.day += 1
            state.served_dishes = 0
            state.daily_target += 5



