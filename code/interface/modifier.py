import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, date
from util.config import POLICE_TITRE, POLICE_TEXTE
from util.inventaire import Inventaire
from util.oeuvre import ETATS, Oeuvre, MODE_ACQUISITION

class ModifierPage(ttk.Frame):
    def __init__(self, parent, inventaire: Inventaire):
        super().__init__(parent, style="TFrame")
        
        self.inventaire = inventaire

        label_form_title = ttk.Label(self, text="Ajouter un Article", font=POLICE_TITRE)
        label_form_title.grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Nom", "Créateur", "Valeur (€)", "Description"]
        self.entries = {}

        for i, text in enumerate(labels):
            ttk.Label(self, text=f"{text} :").grid(row=i+1, column=0, sticky='e', padx=10, pady=5)
            entry = ttk.Entry(self, width=30)
            entry.grid(row=i+1, column=1, pady=5)
            self.entries[text.lower()] = entry

        # Dropdown pour l'état
        ttk.Label(self, text="État :").grid(row=len(labels)+1, column=0, sticky='e', padx=10, pady=5)
        self.entries["état"] = ttk.Combobox(self, values=ETATS, width=27)
        self.entries["état"].grid(row=len(labels)+1, column=1, pady=5)
        self.entries["état"].current(0)

        # Champ texte pour la date de création
        ttk.Label(self, text="Date de création (jj/mm/aaaa) :").grid(row=len(labels)+2, column=0, sticky='e', padx=10, pady=5)
        self.entries["dateCreation"] = ttk.Entry(self, width=30)
        self.entries["dateCreation"].grid(row=len(labels)+2, column=1, pady=5)

        # Bouton pour choisir une image
        def choisir_image():
            filepath = filedialog.askopenfilename(title="Image de l'oeuvre", filetypes=[("Images", ".png .jpg .jpeg .gif")])
            if filepath:
                self.entries["image"].delete(0, tk.END)
                self.entries["image"].insert(0, filepath)

        ttk.Label(self, text="Image :").grid(row=len(labels)+3, column=0, sticky='e', padx=10, pady=5)
        imageEntree = ttk.Entry(self, width=30)
        imageEntree.grid(row=len(labels)+3, column=1, pady=5)
        self.entries["image"] = imageEntree

        btn_image = ttk.Button(self, text="Choisir une image", command=choisir_image)
        btn_image.grid(row=len(labels)+3, column=2, padx=10)

        # Dropdown pour l'emplacement
        ttk.Label(self, text="Emplacement :").grid(row=len(labels)+4, column=0, sticky='e', padx=10, pady=5)
        emplacement_options = ["Salon", "Bureau", "Chambre", "Cave", "Grenier"]
        self.entries["emplacement"] = ttk.Combobox(self, values=emplacement_options, width=27)
        self.entries["emplacement"].grid(row=len(labels)+4, column=1, pady=5)
        self.entries["emplacement"].current(0)
        
        # Dropdown pour l'état
        ttk.Label(self, text="Mode d'acquisition :").grid(row=len(labels)+4, column=0, sticky='e', padx=10, pady=5)
        self.entries["modeAcquisition"] = ttk.Combobox(self, values=MODE_ACQUISITION, width=27)
        self.entries["modeAcquisition"].grid(row=len(labels)+4, column=1, pady=5)
        self.entries["modeAcquisition"].current(0)
        
        # Bouton Ajouter
        btn_ajouter = ttk.Button(self, text="Ajouter l'Oeuvre", command=self.ajouter)
        btn_ajouter.grid(row=len(labels)+6, column=0, columnspan=2, pady=15)

    def ajouter(self):
        try:
            nom = self.entries['nom'].get().strip()
            createur = self.entries['créateur'].get().strip()

            if not nom or not createur:
                raise ValueError("Les champs Nom, Créateur et Description ne peuvent pas être vides.")

            try:
                valeur = int(self.entries['valeur (€)'].get().strip())
            except ValueError:
                raise ValueError("La valeur doit être un entier valide.")

            if valeur < 0:
                raise ValueError("La valeur doit être un entier positif.")
            
            etat = self.entries['état'].get()
            if etat not in ETATS:
                raise ValueError("L'état est invalide.\nVeuillez sélectionner parmi les états valides.")

            # Vérification de la date
            date_creation = self.entries['dateCreation'].get().strip()
            try:
                date_creation = datetime.strptime(date_creation, "%d/%m/%Y").date()
            except ValueError:
                raise ValueError("La date de création n'est pas valide.\nVérifiez que le format de la date de création soit jj/mm/aaaa.")
            
            modeAcquisition = self.entries['modeAcquisition'].get()
            if modeAcquisition not in MODE_ACQUISITION:
                raise ValueError("Le mode d'acquisition est invalide.\nVeuillez sélectionner parmi les modes d'acquisition valides.")
            
            description = self.entries['description'].get().strip()
            
            image = self.entries['image'].get().strip()

            self.inventaire.ajouterOeuvre(Oeuvre(len(self.inventaire.listeOeuvres), nom, createur, date_creation, valeur, etat, description,image,date.today(), modeAcquisition))
            messagebox.showinfo("Succès", "Article ajouté avec succès !")
            return True

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return False

    def vider_formulaire(self):
        for entry in self.entries.values():
            if isinstance(entry, ttk.Entry):
                entry.delete(0, tk.END)
        return True