import tkinter as tk
from tkinter import ttk
from datetime import date
from interface.accueil import AccueilPage
from interface.modifier import ModifierPage
from interface.inventaire import InventairePage
from util.config import COULEUR_SECONDAIRE
from util.inventaire import Inventaire
from util.oeuvre import Oeuvre

class GestionCollectionApp:
    def __init__(self, root, inventaire:Inventaire):
        self.root = root
        self.root.title("🎨 Gestion de Collection")
        self.root.geometry("850x650")
        self.root.configure(bg=COULEUR_SECONDAIRE)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        self.page_accueil = AccueilPage(self.notebook, inventaire)
        self.page_modifier = ModifierPage(self.notebook, inventaire)
        self.page_inventaire = InventairePage(self.notebook, inventaire)

        self.notebook.add(self.page_accueil, text='🏠 Accueil')
        self.notebook.add(self.page_modifier, text='✏️ Modifier')
        self.notebook.add(self.page_inventaire, text='📦 Inventaire')

if __name__ == "__main__":
    inventaire = Inventaire("./save.json")
