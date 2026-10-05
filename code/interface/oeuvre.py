import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from util.oeuvre import Oeuvre
from util.config import POLICE_TITRE, POLICE_TEXTE

class FenetreOeuvre(tk.Toplevel):
    def __init__(self, parent, oeuvre: Oeuvre):
        super().__init__(parent)
        self.title(oeuvre.nom)
        self.geometry("400x600")
        
        # Titre de l'oeuvre
        label_nom = ttk.Label(self, text=oeuvre.nom, font=POLICE_TITRE)
        label_nom.pack(pady=10)

        # Affichage de l'image de l'oeuvre si elle existe
        if oeuvre.image:  # Vérifiez si l'image existe
            try:
                image = Image.open(oeuvre.image)
                image = image.resize((200, 200))  # Redimensionner si nécessaire
                photo = ImageTk.PhotoImage(image)
                label_image = ttk.Label(self, image=photo)
                label_image.image = photo  # Garder une référence à l'image
                label_image.pack(pady=10)
            except Exception as e:
                print(f"Erreur lors du chargement de l'image: {e}")
        
        # Affichage des autres informations
        ttk.Label(self, text=f"Créateur: {oeuvre.createur}", font=POLICE_TEXTE).pack(pady=5)
        ttk.Label(self, text=f"Valeur: {oeuvre.valeur} €", font=POLICE_TEXTE).pack(pady=5)
        ttk.Label(self, text=f"État: {oeuvre.etat}", font=POLICE_TEXTE).pack(pady=5)
        ttk.Label(self, text=f"Date de création: {oeuvre.dateCreation.strftime('%d/%m/%Y')}", font=POLICE_TEXTE).pack(pady=5)
        ttk.Label(self, text=f"Mode d'acquisition: {oeuvre.modeAcquisition}", font=POLICE_TEXTE).pack(pady=5)

        # Bouton de fermeture
        bouton_fermer = ttk.Button(self, text="Fermer", command=self.destroy)
        bouton_fermer.pack(pady=10)