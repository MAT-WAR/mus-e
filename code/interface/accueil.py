import tkinter as tk
from tkinter import ttk
from util.config import POLICE_TITRE, POLICE_TEXTE, COULEUR_SECONDAIRE
from util.inventaire import Inventaire

class AccueilPage(ttk.Frame):
    def __init__(self, parent, inventaire:Inventaire):
        self.inventaire = inventaire
        
        super().__init__(parent, style="TFrame")
        
        self.texte_stats = tk.StringVar()
        self.majStats()
        
        label_titre = ttk.Label(self, text="Statistiques de la Collection", font=POLICE_TITRE)
        label_titre.pack(pady=10)
        
        label_stats = ttk.Label(self, textvariable=self.texte_stats, justify='left', font=POLICE_TEXTE)
        label_stats.pack(pady=10)
        
        frame_boutons = ttk.Frame(self)
        frame_boutons.pack(pady=20)
        
        self.btn_modifier = ttk.Button(frame_boutons, text="✏️ Modifier", command=lambda: parent.select(1))
        self.btn_modifier.grid(row=0, column=0, padx=10)
        
        self.btn_inventaire = ttk.Button(frame_boutons, text="📦 Inventaire", command=lambda: parent.select(2))
        self.btn_inventaire.grid(row=0, column=1, padx=10)
        
    def majStats(self):
        total_articles = len(self.inventaire.listeOeuvres)
        valeur_totale = sum(article.valeur for article in self.inventaire.listeOeuvres)
        total_prets = sum(1 for article in self.inventaire.listeOeuvres if article.etat == 'prete')
        self.texte_stats.set(f"Nombre d'articles : {total_articles}\n"
                        f"Valeur totale : {valeur_totale} €\n"
                        f"Nombre de prêts : {total_prets}\n")