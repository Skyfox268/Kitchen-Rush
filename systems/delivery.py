from systems.progression import register_served_dish

#Fonction simple de livraison de plat en verifiant si le joueur a bien le bon item concerné
def deliver_order(state, customer):
    if customer.order == "Poisson cuit":
        if not state.cooked_fish:
            return False

        state.cooked_fish = False
        state.cooked_fish_count -= 1
        register_served_dish(state, 10)
        return True

    if customer.order == "Sushi":
        if not state.ready_sushi:
            return False

        state.ready_sushi = False
        register_served_dish(state, 15)
        return True

    if customer.order == "Salade":
        if not state.ready_salad:
            return False

        state.ready_salad = False
        register_served_dish(state, 12)
        return True

    return False

