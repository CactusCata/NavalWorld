"""
En Python, l'indentation est importante, elle permet de définir les constructions de contrôle
(elle remplace les accolades dans des langages comme le C ou le Java)
"""

# ---===== Exemple 1 =====--- Fonction main

if __name__ == "__main__":
    pass

# ---===== Exemple 2 =====--- Variables globales

import ......
# Some code

STATE = 1

# Some code

# ---===== Exemple 3 =====--- Classe et instanciation

class Car:

    # La variable self correspond à l'instance de l'objet
    # Elle est directement stocké de façon 'invisible'.
    # Pour intéragir dans notre objet, nous sommes obligé de renseigner
    # la variable 'self'.
    # Elle est semblable à la variable 'this' de Java
    def __init__(self, carName, carColor):
        self.carName = carName
        self.setCarColor(carColor)

    def getCarColor(self):
        return self.carColor

    def setCarColor(self, carColor):
        self.carColor = carColor

if __name__ == "__main__":
    # Instanciation de l'objet Car
    # La variable self prévue dans le constructeur se créer entre l'instanciation et l'arrivée dans le constructeur
    someCar = Car("Hyundai", "Black")
    # Pour intéragir avec l'object, nous n'avons pas besoin de renseigner la variable self:
    # elle correspond en réalité à 'someCar'
    print(someCar.getCarColor())
    someCar.setCarColor("Bleu")

# ---===== Exemple 4 =====--- Maps

deplacements = {}
deplacements["foo"] = 42

# ---===== Exemple 5 =====--- String format

a = 5;
b = 12;
print(f"{a} + {b} = {a + b}");

# ---===== Exemple 6 =====--- Paramètre optionnel

def log(self, message, level="Normal"):
    print(f"[{level}]: {message}")

if __name__ == "__main__":
    log("Bonsoir")
    # >> [Normal] Bonsoir
    log("Bonjour", level="Warning")
    # >> [Warning] Bonjour
