# Kitchen Rush

Jeu de cuisine en Python/Pygame : le joueur sert des clients en préparant les bons plats avant que leur temps ne soit écoulé.

## But du jeu
- Gagner des points et de l'argent
- Préparer les bonnes commandes
- Passer les objectifs du jour
- Éviter d'avoir trop de clients non servis

## Déroulé
1. Le jeu démarre dans `main.py`.
2. `Game.run()` lance la boucle principale.
3. Le joueur se déplace, récupère des ingrédients, cuisine et livre les commandes.
4. Les clients arrivent progressivement et ont une commande aléatoire selon le jour.
5. Si un client part sans être servi, la partie compte un client non servi.
6. Quand les plats requis sont servis, on avance au jour suivant.
7. Si trop de clients sont perdus, le menu de fin s'affiche.

## Fichiers importants
- `main.py` : point d'entrée du jeu
- `game/game.py` : initialise le jeu, la fenêtre, les objets et la boucle principale
- `game/state.py` : stocke toute l'état du jeu (score, argent, jour, inventaire, timers)
- `entities/customer.py` : clients, commandes, spawn, départ
- `systems/cooking.py` : cuisson et préparation des plats
- `systems/delivery.py` : vérifie si la commande est bonne et la livre
- `systems/progression.py` : score, argent, progression entre jours
- `ui/hud.py` : affiche le HUD, les commandes et les temps restants

## Mécaniques principales
- Poisson cru -> cuisson -> poisson cuit
- Saumon cru -> découpe -> sushi prêt
- Salade + tomate -> salade prête
- Le joueur doit livrer le bon plat au bon client
- Si le joueur jette un aliment il perd automatiquement 5 euros sur sa caisse finale

## Astuce de compréhension
Le jeu suit ce schéma :
- client arrive
- commande affichée
- joueur prépare le plat
- joueur livre la commande
- score / argent augmentent
- jours et objectifs avancent

## Fichiers annexes
- `systems/scores.py` : enregistre les scores dans `data/scores.json`
- `.gitignore` : ignore les fichiers temporaires Python (`__pycache__`, `.pyc`, `.pytest_cache`)

