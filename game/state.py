class GameState:

    #On definie toutes les variables utilisés pour le jeu
    def __init__(self):

        #On definit l'état du jeu (menu de debut, menu de fin, menu des scores, en cours de jeu)
        self.screen = "menu_debut"
        self.score = 0
        self.money = 0
        self.day = 1
        self.daily_target = 5
        self.served_dishes = 0
        self.unserved_customers = 0
        self.next_customer_spawn = 0

        #Les attributs du joueur (pseudo, score)
        self.username = ""
        self.score_saved = False

        #Les items
        self.cooked_fish_count = 0
        self.raw_fish = False
        self.cooked_fish = False
        self.raw_salmon = False
        self.ready_sushi = False
        self.raw_salad = False
        self.ready_salad = False
        self.tomato = False
        self.salad_in_bowl = False

        #La préparation des plats
        self.cooking = False
        self.cooking_end = 0
        self.sushi_preparation = False
        self.sushi_preparation_end = 0
        self.salad_preparation = False
        self.salad_preparation_end = 0

        

