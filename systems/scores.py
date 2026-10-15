import json
from pathlib import Path

SCORES_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    /"scores.json"
)

#On load le JSON
def load_scores():
    if not SCORES_FILE.exists():
        return {
            "jours": {
                "1": [],
                "2": [],
                "3": [],
            }
        }

    with SCORES_FILE.open("r", encoding ="utf-8") as file:
        data = json.load(file)

    if "jours" not in data:
        raise ValueError(
            "Le file scores.json doit contenir une clé 'jours'."
        )

    return data

#On recuperer les scores du jour concerné
def save_score(username, score, day):
    data = load_scores()

    day_key = str(day)

    if day_key not in data["jours"]:
        data["jours"][day_key] = []

    data["jours"][day_key].append(
        {
            "pseudo": username,
            "score": score
        }
    )

    data["jours"][day_key].sort(
        key=lambda result: result["score"],
        reverse = True
    )

    # Créer le répertoire si nécessaire
    SCORES_FILE.parent.mkdir(exist_ok = True)
    with SCORES_FILE.open("w", encoding="utf-8") as file:#Mode écriture pour le fichier JSON
        json.dump(data, file, ensure_ascii = False, indent = 4)#on insere les valeurs 
        

