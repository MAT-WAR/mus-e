import json
from datetime import date

ETATS = [ "Stocké", "Exposé", "Prêté", "Détruit"]
MODE_ACQUISITION = ["Prêt", "Donation", "Achat"]

# CLASSE OEUVRE
class Oeuvre:
    def __init__(self, numeroOeuvre: int, nom:str, createur: str, dateCreation: date, valeur: float, etat: str, description: str="", image: str="", dateInventaire: date=None, modeAcquisition: str=MODE_ACQUISITION[1], numeroEmplacement: int = -1):
        self.numeroOeuvre = numeroOeuvre
        self.nom = nom
        self.createur = createur
        self.dateCreation = dateCreation
        self.valeur = valeur
        self.etat = etat    
        self.description = description
        self.image = image
        self.dateInventaire = dateInventaire if dateInventaire else date.today()
        self.modeAcquisition = modeAcquisition
        self.numeroEmplacement = numeroEmplacement
        
    # Affichage d'une oeuvre
    def __str__(self):
        return (f"Numéro : {self.numeroOeuvre}, Créateur : {self.createur}, Date de création : {self.dateCreation}, Valeur : {self.valeur}, État : {self.etat}, Description : {self.description}")  
    
    # Renvoie l'oeuvre sous format JSON
    def JSON(self):
        return json.dumps({
            "numeroOeuvre": self.numeroOeuvre,
            "nom": self.nom,
            "createur": self.createur,
            "dateCreation": self.dateCreation.isoformat(),
            "valeur": self.valeur,
            "etat": self.etat,
            "description": self.description,
            "image": self.image,
            "dateInventaire": self.dateInventaire.isoformat(),
            "modeAcquisition": self.modeAcquisition,
            "numeroEmplacement": self.numeroEmplacement
        }, ensure_ascii=False, indent=4)
    
    # Crée une oeuvre depuis un JSON
    @staticmethod
    def depuisJSON(infos):
        obj = json.loads(infos) if isinstance(infos, str) else infos
        return Oeuvre(
            numeroOeuvre=obj["numeroOeuvre"],
            nom=obj["nom"],
            createur=obj["createur"],
            dateCreation=date.fromisoformat(obj["dateCreation"]),
            valeur=obj["valeur"],
            etat=obj["etat"],
            description=obj["description"],
            image=obj["image"],
            dateInventaire=date.fromisoformat(obj["dateInventaire"]),
            modeAcquisition=obj["modeAcquisition"],
            numeroEmplacement=obj["numeroEmplacement"]
        )
    # MÉTHODES DE MODIFICATION
    def modifierCreateur(self, nouveauCreateur: str):
        self.createur = nouveauCreateur
        
    def modifierDateCreation(self, nouvelleDate: date):
        self.dateCreation = nouvelleDate
        return True

    def modifierValeur(self, nouvelleValeur: float):
        if nouvelleValeur >= 0:
            self.valeur = nouvelleValeur
            return True
        return False
            
    def modifierEtat(self, nouvelEtat: str):
        self.etat = nouvelEtat

    def modifierDescription(self, nouvelleDescription: str):
        self.description = nouvelleDescription
