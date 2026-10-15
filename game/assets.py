import pygame
from pathlib import Path

#définir la procédure pour charger une image et la redimensionner
def load_image(
    assets_dir,
    nom_fichier,
    size
):
    image = pygame.image.load(str(assets_dir / nom_fichier)).convert_alpha()
    return pygame.transform.scale(image, size)


#donner les parametres pour chaque image et appeler la fonction d'au dessus pour charger les images et les redimensionner
def load_images():
    assets_dir = (
        Path(__file__).resolve().parent.parent / "assets"
    )

    return {
        "fish": load_image(
            assets_dir,
            "fish.png",
            (100,100)
        ),

        "fish_cuit": load_image(
            assets_dir,
            "fish_cuit.png",
            (100,100)
        ),

        "sushi": load_image(
            assets_dir,
            "caisse_saumon.png",
            (100,100)
        ),

        "saumon_cru": load_image(
            assets_dir,
            "saumon_cru.png",
            (100,100)
        ),

        "sushi_pret": load_image(
            assets_dir,
            "sushi.png",
            (100,100)
        ),

        "salade": load_image(
            assets_dir,
            "caisse_salade.png",
            (100,100)
        ),

        "salade_crue": load_image(
            assets_dir,
            "salade_crue.png",
            (100,100)
        ),

        "salade_prete": load_image(
            assets_dir,
            "salade.png",
            (100,100)
        ),

        "tomate" : load_image(
            assets_dir,
            "tomates.png",
            (100,100)
        ),

        "bol": load_image(
            assets_dir,
            "bol_salade.png",
            (100,100)
        ),

        "poubelle" : load_image(
            assets_dir,
            "poubelle.png",
            (130,130)
        )

    }


