import json
import random
from util.oeuvre import Oeuvre

# CLASSE INVENTAIRE
class Inventaire:
    def __init__(self, fichierSauv: str = "", listeOeuvres: list[Oeuvre] = []):
        self.fichierSauv = fichierSauv
        self.listeOeuvres = []
        
        if fichierSauv:
            self.__chargerSauvegarde__()
        
        self.listeOeuvres.extend(listeOeuvres)

    # Charger la sauvegarde de l'inventaire depuis un fichier JSON
    def __chargerSauvegarde__(self):
        try:
            with open(self.fichierSauv, "r", encoding="utf-8") as f:
                infos = json.load(f)
                self.listeOeuvres = [Oeuvre.depuisJSON(oeuvre) for oeuvre in infos]
        except (FileNotFoundError, json.JSONDecodeError):
            self.listeOeuvres = []

    # Sauvegarder l'inventaire dans un fichier JSON
    def __sauvegarder__(self):
        with open(self.fichierSauv, "w", encoding="utf-8") as f:
            print(f)
            json.dump([oeuvre.JSON() for oeuvre in self.listeOeuvres], f, ensure_ascii=False, indent=4)
  
    # Afficher l'inventaire
    def __str__(self):
        message = "Voici l'inventaire du musée :\n"
        for oeuvre in self.listeOeuvres:
            message += str(oeuvre) + "\n"
        return message
    
    # Ajouter une œuvre à l'inventaire
    def ajouterOeuvre(self, oeuvre: Oeuvre):
        if not isinstance(oeuvre, Oeuvre):
            return False
        
        self.listeOeuvres.append(oeuvre)
        self.__sauvegarder__()
        return True
    
    # Récupérer une œuvre dans la liste avec son identifiant
    def recupererOeuvre(self, numeroOeuvre: int):
        for oeuvre in self.listeOeuvres:
            if oeuvre.numeroOeuvre == numeroOeuvre:
                return oeuvre
        return None
    
    # Supprimer une œuvre de la liste
    def supprimerOeuvre(self, numeroOeuvre: int):
        for i, oeuvre in enumerate(self.listeOeuvres):
            if oeuvre.numeroOeuvre == numeroOeuvre:
                self.listeOeuvres.pop(i)
                self.__sauvegarder__()
                return True
        return False
    
    # Faire disparaître une œuvre avec une chance sur 69
    def disparaitreOeuvre(self, numeroOeuvre: int):
        if random.randint(1, 69) == 1:
            return self.supprimerOeuvre(numeroOeuvre)
        return False