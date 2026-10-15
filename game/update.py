import pygame
from systems.cooking import update_cooking, update_sushi_preparation, update_salad_preparation
from systems.progression import show_end_menu
from entities.customer import Customer

#S'occupe de mettre a jour le jeu a chaque frame
def update_game(game, delta_seconds):
    move_player(game)#deplace le joueur
    update_cooking(game.state)#met a jour les recettes en cours de cuisson
    update_sushi_preparation(game.state)#met a jour la préparation du sushi
    update_salad_preparation(game.state)#met a jour la préparation de la salade

    update_customers(game, delta_seconds)

#S'occupe de faire spawn ou dispawn les clients selon le temps écoulé 
def update_customers(game, delta_seconds):
    now = pygame.time.get_ticks()

    for customer in game.customers[:]:
        if customer.departing:
            customer_left = customer.update_departure(delta_seconds)
            if customer_left:
                game.customers.remove(customer)
                game.schedule_customer_spawn()
            continue
        if now >= customer.order_deadline:
            customer.start_departure()
            game.state.unserved_customers += 1
            if game.state.unserved_customers >= 5:
                show_end_menu(game.state)
                return

    if (now >= game.state.next_customer_spawn and len(game.customers) < game.max_customers()):
        game.customers.append(Customer(game.state.day))
        game.schedule_customer_spawn()


#Update le personnage en le faisant bouger selon les touches préssées par le joueur 
def move_player(game):
    touches = pygame.key.get_pressed()

    if touches[pygame.K_d]:
        game.player.move_right()

    elif touches[pygame.K_q]:
        game.player.move_left()


    if touches[pygame.K_z]:
        game.player.move_up()

    if touches[pygame.K_s]:
        game.player.move_down()

