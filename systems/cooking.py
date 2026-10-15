import pygame

COOKING_TIME = 6_000
SUSHI_PREPARATION_TIME = 5_000
SALAD_PREPARATION_TIME = 5_000

#Préparation du saumon 
def cut_salmon(state):
    if state.raw_salmon and not state.ready_sushi:
        state.raw_salmon = False
        state.sushi_preparation = True
        state.sushi_preparation_end = pygame.time.get_ticks() + SUSHI_PREPARATION_TIME

#Commence la cuisson ou préparation et lance le timer pour la fin de la cuisson ou préparation
def start_cooking(state):
    if state.raw_fish and not state.cooking:
        state.cooking = True
        state.cooking_end = pygame.time.get_ticks() + COOKING_TIME
        state.raw_fish = False

#Jeter item a l'aide de la poubelle
def discard_items(state):
    if (
        state.raw_fish
        or state.cooked_fish
        or state.raw_salmon
        or state.ready_sushi
        or state.raw_salad
        or state.ready_salad
        or state.tomato
    ): #Verifie qu'il a bien un item a jeter
        state.raw_fish = False
        state.cooked_fish = False
        state.raw_salmon = False
        state.ready_sushi = False
        state.raw_salad = False
        state.ready_salad = False
        state.tomato = False
        state.money -= 5 #retire 5$ du joueur pour chaque item jeté
 

def update_cooking(state):
    if not state.cooking:
        return

    if pygame.time.get_ticks() >= state.cooking_end:
        state.cooking = False
        state.cooked_fish = True
        state.cooked_fish_count += 1

#Lorsque fin de preparation sushi -> give un sushi pret au joueur
def update_sushi_preparation(state):
    if not state.sushi_preparation:
        return

    if pygame.time.get_ticks() >= state.sushi_preparation_end:
        state.sushi_preparation = False
        state.ready_sushi = True

#Lorsque fin de preparation salade -> give une salade prete au joueur
def update_salad_preparation(state):
    if not state.salad_preparation:
        return

    if pygame.time.get_ticks() >= state.salad_preparation_end:
        state.salad_preparation = False
        state.ready_salad = True

