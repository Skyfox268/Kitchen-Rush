import pygame


#Cette fonction est la fonction principale qui utilise toute les fonctions ci dessous pour dessiner chaque éléments du jeu a l'écran
def draw_game(game):
    game.screen.blit(game.background, (0, 0))

    draw_preparations(game)
    draw_trash(game)
    if game.state.day >= 3:
        draw_bowl(game)
    draw_inventory(game)
    draw_customers(game)
    draw_crates(game)
    draw_player(game)
    draw_hud(game)


    pygame.display.flip()


def draw_preparations(game):
    state = game.state
    preparations = []

    if state.cooking:#Si le joueur est en train de cuire le poisson, on affiche le temps restant pour la cuisson
        remaining_seconds = max(0, (state.cooking_end - pygame.time.get_ticks()) // 1000)
        preparations.append(("LE POISSON CUIT...", remaining_seconds, (255, 210, 100)))

    if state.sushi_preparation:
        remaining_seconds = max(0, (state.sushi_preparation_end - pygame.time.get_ticks()) // 1000)
        preparations.append(("PREPARATION DU SUSHI...", remaining_seconds, (130, 210, 255)))

    if state.salad_preparation:
        remaining_seconds = max(0, (state.salad_preparation_end - pygame.time.get_ticks()) // 1000)
        preparations.append(("PREPARATION DE LA SALADE...", remaining_seconds, (130, 255, 160)))

    for index, (title, remaining_seconds, color) in enumerate(preparations):
        game.hud.draw_preparation(
            game.screen,
            title,
            remaining_seconds,
            color,
            760 + index * 120,
        )

def draw_trash(game):
    game.screen.blit(game.images["poubelle"], game.trash_rect)

#Système d'inventaire a l'écran
def draw_inventory(game):
    state = game.state
    player_rect = game.player.rect

    objets = [
        ("raw_fish", "fish"),
        ("cooked_fish", "fish_cuit"),
        ("raw_salmon", "saumon_cru"),
        ("ready_sushi", "sushi_pret"),
        ("raw_salad", "salade_crue"),
        ("ready_salad", "salade_prete"),
        ("tomato", "tomate"),
    ] 

    objets_actifs = [
        image_name
        for attribut, image_name in objets
        if getattr(state, attribut)
    ]
    if not objets_actifs:
        return

    slot_size = 56
    margin = 4
    columns = 4
    rows = (len(objets_actifs) + columns - 1) // columns
    panel_rect = pygame.Rect(
        player_rect.right + margin,
        player_rect.top,
        columns * slot_size + margin,
        rows * slot_size + margin,
    )
    if panel_rect.right > game.screen.get_width():
        panel_rect.right = player_rect.left - margin

    panel = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
    panel.fill((18, 28, 48, 220))
    game.screen.blit(panel, panel_rect.topleft)
    pygame.draw.rect(
        game.screen,
        (226, 173, 76),
        panel_rect,
        width=2,
        border_radius=12,
    )

    for index, image_name in enumerate(objets_actifs):
        column = index % columns
        row = index // columns
        slot_rect = pygame.Rect(
            panel_rect.x + margin // 2 + column * slot_size,
            panel_rect.y + margin // 2 + row * slot_size,
            slot_size - margin,
            slot_size - margin,
        )
        image = pygame.transform.smoothscale(
            game.images[image_name],
            (slot_rect.width - 4, slot_rect.height - 4),
        )
        image_rect = image.get_rect(center=slot_rect.center)
        game.screen.blit(image, image_rect)

#Dessiner les clients a l'écran et les commandes qu'ils ont passé
def draw_customers(game):
    order_panels = []

    for customer in game.customers:
        if customer.departing:
            game.screen.blit(customer.image, customer.rect)
            continue
        game.screen.blit(customer.image, customer.rect)

        remaining_seconds = max(
            0,
            (customer.order_deadline - pygame.time.get_ticks()) // 1000,
        ) #Timer de la commande du client, si le timer arrive a 0, le client partira et le joueur perdra de l'argent
        panel_rect = find_order_position(
            game.screen.get_rect(),
            customer.rect,
            order_panels,
            pygame.Rect(20, 20, 425, 175),
        )
        order_panels.append(panel_rect)
        game.hud.draw_order_panel(
            game.screen,
            customer,
            remaining_seconds,
            panel_rect,
        )

#Va permettre d'empecher les collision entre les boites de commandes des clients entre eux
def find_order_position(
    screen_rect,
    customer_rect,
    existing_panels,
    protected_rect=None,
):
    width = 250
    height = 92
    spacing = 8
    candidates = [
        pygame.Rect(0, 0, width, height),
        pygame.Rect(0, 0, width, height),
        pygame.Rect(0, 0, width, height),
        pygame.Rect(0, 0, width, height),
    ]
    candidates[0].midbottom = customer_rect.midtop
    candidates[0].y -= spacing
    candidates[1].midtop = customer_rect.midbottom
    candidates[1].y += spacing
    candidates[2].midright = customer_rect.midleft
    candidates[2].x -= spacing
    candidates[3].midleft = customer_rect.midright
    candidates[3].x += spacing

    for candidate in candidates:
        candidate.clamp_ip(screen_rect)
        overlaps_panel = any(
            candidate.colliderect(panel)
            for panel in existing_panels
        )
        overlaps_protected = (
            protected_rect is not None
            and candidate.colliderect(protected_rect)
        )#Si le panel de commande du client chevauche un autre panel ou une zone protégée, on passe au panel suivant
        if not overlaps_panel and not overlaps_protected:
            return candidate

    candidate = candidates[0].copy()
    offset = (len(existing_panels) + 1) * (height + spacing)#Décale le panel si aucun emplacement n'est disponible
    while candidate.y > screen_rect.top:
        candidate.y -= height + spacing
        candidate.clamp_ip(screen_rect)
        if (
            not any(candidate.colliderect(panel) for panel in existing_panels)
            and (
                protected_rect is None
                or not candidate.colliderect(protected_rect)
            )
        ):
            return candidate
    candidate.y = max(screen_rect.top, candidate.y - offset)
    candidate.clamp_ip(screen_rect)#Empêche le panel de sortir de l'écran
    return candidate

#Dessiner les caisses de poissons, de saumons, de salades et de tomates a l'écran
def draw_crates(game):
    state = game.state

    #Caisse de poisson
    game.screen.blit(game.fish_crate.image, game.fish_crate.rect)

    #Caisse de saumon
    if state.day >= 2:
        game.screen.blit(game.salmon_crate.image, game.salmon_crate.rect)

    #Caisse de salade
    if state.day >= 3:
        game.screen.blit(game.salad_crate.image, game.salad_crate.rect)
        game.screen.blit(game.tomato_crate.image, game.tomato_crate.rect)

def draw_bowl(game):
    game.screen.blit(game.images["bol"], game.bowl_rect)

def draw_player(game):
    game.screen.blit(game.player.image, game.player.rect)

def draw_hud(game):
    game.hud.draw_progress(game.screen, game.state)
