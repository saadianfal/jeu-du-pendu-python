"""Mot mystère : un pendu amélioré.

Fonctionnalités :
- mot choisi au hasard selon le niveau de difficulté
- affichage « _ a _ _ » avec les lettres trouvées
- compteur d'erreurs et dessin ASCII du pendu
- liste des lettres déjà essayées
- saisie invalide refusée (chiffres, plusieurs caractères, lettre déjà jouée)
"""

import random
import string
import unicodedata

MOTS = {
    "facile": ["chat", "soleil", "maison", "arbre", "livre", "fleur", "pomme", "table"],
    "moyen": ["ordinateur", "montagne", "bibliotheque", "chocolat", "voyageur", "tortue"],
    "difficile": ["algorithmique", "extraordinaire", "hippopotame", "labyrinthe", "kaleidoscope"],
}

ERREURS_MAX = {"facile": 8, "moyen": 7, "difficile": 6}

# Dessin ASCII : un état par nombre d'erreurs (0 à 8)
DESSINS = [
    "\n\n\n\n\n\n=========",
    "\n      |\n      |\n      |\n      |\n      |\n=========",
    "  +---+\n      |\n      |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========",
]


def normaliser(texte):
    """Met en minuscules et retire les accents (é -> e)."""
    texte = unicodedata.normalize("NFD", texte.lower())
    return "".join(c for c in texte if unicodedata.category(c) != "Mn")


def choisir_niveau():
    while True:
        choix = normaliser(input("Niveau (facile / moyen / difficile) : ").strip())
        if choix in MOTS:
            return choix
        print("Niveau inconnu, réessaie.")


def afficher_mot(mot, trouvees):
    return " ".join(lettre if lettre in trouvees else "_" for lettre in mot)


def afficher_dessin(erreurs, erreurs_max):
    # On adapte l'index du dessin au nombre d'erreurs autorisées
    index = round(erreurs * (len(DESSINS) - 1) / erreurs_max)
    print(DESSINS[index])


def demander_lettre(deja_jouees):
    while True:
        saisie = normaliser(input("Propose une lettre : ").strip())
        if len(saisie) != 1 or saisie not in string.ascii_lowercase:
            print("Saisie invalide : entre une seule lettre (a-z).")
        elif saisie in deja_jouees:
            print("Tu as déjà essayé cette lettre.")
        else:
            return saisie


def jouer():
    niveau = choisir_niveau()
    mot = random.choice(MOTS[niveau])
    erreurs_max = ERREURS_MAX[niveau]
    trouvees = set()
    ratees = set()

    print(f"\nMot de {len(mot)} lettres, {erreurs_max} erreurs maximum. Bonne chance !")

    while True:
        print()
        afficher_dessin(len(ratees), erreurs_max)
        print("\nMot :", afficher_mot(mot, trouvees))
        print("Lettres ratées :", " ".join(sorted(ratees)) or "aucune")
        print(f"Erreurs : {len(ratees)}/{erreurs_max}")

        if all(lettre in trouvees for lettre in mot):
            print(f"\nBravo, tu as gagné ! Le mot était « {mot} ».")
            return
        if len(ratees) >= erreurs_max:
            print(f"\nPerdu ! Le mot était « {mot} ».")
            return

        lettre = demander_lettre(trouvees | ratees)
        if lettre in mot:
            trouvees.add(lettre)
            print("Bien joué !")
        else:
            ratees.add(lettre)
            print("Raté.")


def main():
    print("=== MOT MYSTÈRE ===")
    while True:
        jouer()
        if normaliser(input("\nRejouer ? (o/n) : ").strip()) != "o":
            print("À bientôt !")
            break


if __name__ == "__main__":
    main()