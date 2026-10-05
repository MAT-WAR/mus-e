# main.py
import tkinter as tk
from tkinter import ttk
from util.config import POLICE_TITRE, POLICE_TEXTE
from util.inventaire import Inventaire
from util.oeuvre import Oeuvre
from fuzzywuzzy import fuzz
from interface.oeuvre import FenetreOeuvre  # Importer la nouvelle classe

class InventairePage(ttk.Frame):
    def __init__(self, parent, inventaire: Inventaire):
        super().__init__(parent, style="TFrame")
        self.inventaire = inventaire
        
        label_inv_title = ttk.Label(self, text="Liste des Articles", font=POLICE_TITRE)
        label_inv_title.pack(pady=10)
        
        self.var_recherche = tk.StringVar()
        self.var_recherche.trace_add('write', self.rechercher)
        
        frame_recherche = ttk.Frame(self)
        frame_recherche.pack(pady=5)
        ttk.Label(frame_recherche, text="🔍 Rechercher: ").pack(side='left')
        self.entree_recherche = ttk.Entry(frame_recherche, textvariable=self.var_recherche, width=30)
        self.entree_recherche.pack(side='left')
        
        colonnes = ("Numéro", "Nom", "Créateur", "Valeur (€)", "État", "Date de création", "Mode d'acquisition")
        self.tree = ttk.Treeview(self, columns=colonnes, show='headings')
        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=180)
        self.tree.pack(pady=10, fill='both', expand=True)
        
        # Ajout du double click
        self.tree.bind("<Double-1>", self.on_double_click)
        
        frame_tri = ttk.Frame(self)
        frame_tri.pack(pady=5)
        
        ttk.Button(frame_tri, text="Valeur ↑", command=lambda: self.trier('valeur', True)).grid(row=0, column=0, padx=5)
        ttk.Button(frame_tri, text="Valeur ↓", command=lambda: self.trier('valeur', False)).grid(row=0, column=1, padx=5)
        ttk.Button(frame_tri, text="État A-Z", command=lambda: self.trier('etat', True)).grid(row=0, column=2, padx=5)
        ttk.Button(frame_tri, text="Créateur A-Z", command=lambda: self.trier('createur', True)).grid(row=0, column=3, padx=5)
        ttk.Button(frame_tri, text="Date Création ↑", command=lambda: self.trier('dateCreation', True)).grid(row=1, column=0, padx=5)
        ttk.Button(frame_tri, text="Date Création ↓", command=lambda: self.trier('dateCreation', False)).grid(row=1, column=1, padx=5)
        ttk.Button(frame_tri, text="Mode Acquisition A-Z", command=lambda: self.trier('modeAcquisition', True)).grid(row=1, column=2, padx=5)
        
        btn_supprimer = ttk.Button(self, text="🗑️ Supprimer l'Article Sélectionné", command=self.supprimer)
        btn_supprimer.pack(pady=10)
        
        self.afficher_oeuvres()
        
    def afficher_oeuvres(self):
        self.tree.delete(*self.tree.get_children())
        
        for oeuvre in self.inventaire.listeOeuvres:
            self.tree.insert("", "end", values=(
                oeuvre.numeroOeuvre, oeuvre.nom, oeuvre.createur, oeuvre.valeur, oeuvre.etat,
                oeuvre.dateCreation.strftime("%d/%m/%Y"), oeuvre.modeAcquisition
            ))
        return True

    def rechercher(self, *args):
        recherche = self.var_recherche.get().lower()
        
        self.afficher_oeuvres()
        
        if not recherche: return False
        
        items_a_supprimer = []
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if (fuzz.partial_ratio(recherche, values[0].lower()) <= 70 and  
                fuzz.partial_ratio(recherche, values[1].lower()) <= 70):
                items_a_supprimer.append(item)
        
        for item in items_a_supprimer:
            self.tree.delete(item)
        return True
        
    def trier(self, critere, croissant):
        oeuvres_triees = sorted(self.inventaire.listeOeuvres, key=lambda x: getattr(x, critere), reverse=not croissant)
        self.tree.delete(*self.tree.get_children())
        for oeuvre in oeuvres_triees:
            self.tree.insert("", "end", values=(
                oeuvre.numeroOeuvre, oeuvre.nom, oeuvre.createur, oeuvre.valeur, oeuvre.etat,
                oeuvre.dateCreation.strftime("%d/%m/%Y"), oeuvre.modeAcquisition
            ))
        
    def supprimer(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)

    # Ouvrir l'oeuvre en grand
    def on_double_click(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item[0], "values")
            # Recherche de l'Oeuvre correspondant dans l'inventaire
            for oeuvre in self.inventaire.listeOeuvres:
                if str(oeuvre.numeroOeuvre) == item_values[0]:
                    FenetreOeuvre(self, oeuvre)  # Ouvrir la fenêtre de l'oeuvre sélectionnée
                    break