import pygame
from systems.scores import save_score

#Boucle principale de gestion des événements de jeu nottament les entrées clavier
def handle_events(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

        #Gestion de la touche E pour interagir
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and game.state.screen == "jeu":
                game.interact()

            #Permet de revenir en arrière lors de la saisie du nom d'utilisateur a la fin 
            if event.key == pygame.K_BACKSPACE and game.state.screen == "menu_fin" and not game.state.score_saved:
                game.state.username = game.state.username[:-1]

            #Permet de lancger le jeu depuis le menu de debut et de quitter le jeu depuis le menu de fin
            if event.key == pygame.K_SPACE:
                if game.state.screen == "menu_debut":
                    game.state.screen = "jeu"
                    game.schedule_customer_spawn()

                elif (
                    game.state.screen == "menu_fin"
                    and game.state.score_saved
                ):
                    game.running = False

            #Acceder au menu des scores 
            elif event.key == pygame.K_TAB:
                if game.state.screen == "menu_debut":
                    game.state.screen = "menu_scores"
                elif game.state.screen == "menu_scores":
                    game.state.screen = "menu_debut"

            elif (
                event.key == pygame.K_RETURN
                and game.state.screen == "menu_fin"
                and not game.state.score_saved
            ):
                username = game.state.username.strip() or "Anonymous"
                save_score(username, game.state.score, game.state.day)
                game.state.username = username
                game.state.score_saved = True
                pygame.key.stop_text_input()

            #Permet d'afficher le menu de debut depuis le menu des scores ou depuis le jeu en cours
            elif event.key == pygame.K_ESCAPE:
                if game.state.screen == "menu_scores":
                    game.state.screen = "menu_debut"
                elif game.state.screen == "jeu":
                    game.state.screen = "menu_debut"

        #Permet de gerer l'entrée de texte par l'utilisateur 
        elif event.type == pygame.TEXTINPUT:
            if (
                game.state.screen == "menu_fin"
                and not game.state.score_saved
                and len(game.state.username) < 10
            ):
                game.state.username += event.text
            


