from datetime import date

class Oeuvre :
    def __init__ (self,numero_oeuvre:int ,createur:str,date_creation: date,valeur: float,etat: str,description:str):
        self.numero_oeuvre = numero_oeuvre
        self.createur = createur
        self.date_creation = date_creation
        self.valeur = valeur
        self.etat = etat
        self.description = description
        
    def afficher_details(self):
        return (f"Createur :{self.createur},Date de créatoin: {self.date_creation},Valeur: {self.valeur}, Etat: {self.etat},Description : {self.description}")  
       
    #methode
    def modifier_createur(self,nouveau_createur:str):
        self.createur = nouveau_createur
        
    def modifier_date_creation(self,nouveau_date_creation:date):
        self.date_creation =nouveau_date_creation
        
    def modifier_valeur(self,nouveau_valeur: float):
        if nouveau_valeur >= 0:
            self.valeur = nouveau_valeur
        else:
            print("Erreur: ta putain de valeur est negative")
            
    def modifier_etat(self, nouvelle_etat: str):
            self.etat = nouvelle_etat

    def modifier_description(self, nouvelle_description: str):
            self.description = nouvelle_description

oeuvre1= Oeuvre(1,"Ferrari", date(2019,8,1), 250000.0, "Excellent", "sf90")  

oeuvre1.modifier_valeur(550000.0)

print(oeuvre1.afficher_details())
    