import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

PRIMARY_COLOR = "#4A90E2"
SECONDARY_COLOR = "#F5F5F5"
FONT_TITLE = ("Helvetica", 16, "bold")
FONT_TEXT = ("Helvetica", 11)

items = []

def update_stats():
    total_items = len(items)
    total_value = sum(item['valeur'] for item in items)
    total_prets = sum(1 for item in items if item.get('prete'))
    createurs = {}
    for item in items:
        createurs[item['createur']] = createurs.get(item['createur'], 0) + 1
    top_createur = max(createurs, key=createurs.get) if createurs else "Aucun"
    
    stats_text.set(f"Nombre d'items : {total_items}\n"
                   f"Valeur totale : {total_value} €\n"
                   f"Nombre de prêts : {total_prets}\n")

def ajouter_item():
    try:
        nom = entry_nom.get()
        etat = entry_etat.get()
        createur = entry_createur.get()
        description = entry_description.get()
        valeur = float(entry_valeur.get())
        date_ajout = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        items.append({
            'nom': nom,
            'etat': etat,
            'createur': createur,
            'description': description,
            'valeur': valeur,
            'date_ajout': date_ajout,
            'lieu': "Stock",
            'prete': False
        })
        update_stats()
        refresh_inventaire()
        clear_form()
        messagebox.showinfo("Ajouté", f"Item '{nom}' ajouté avec succès.")
    except ValueError:
        messagebox.showerror("Erreur", "Valeur invalide pour le champ valeur.")

def supprimer_item():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Aucun item", "Sélectionnez un item.")
        return
    if messagebox.askyesno("Confirmer", "Êtes-vous sûr de vouloir supprimer ?"):
        index = int(tree.item(selected[0], 'tags')[0])
        del items[index]
        refresh_inventaire()
        update_stats()

def refresh_inventaire(filtered=None):
    tree.delete(*tree.get_children())
    data = filtered if filtered is not None else items
    for idx, item in enumerate(data):
        tree.insert('', 'end', values=(item['nom'], item['createur'], item['valeur'], item['etat']), tags=(str(idx),))

def search_items(*args):
    query = search_var.get().lower()
    filtered = [item for item in items if query in item['nom'].lower()]
    refresh_inventaire(filtered)

def clear_form():
    entry_nom.delete(0, tk.END)
    entry_etat.delete(0, tk.END)
    entry_createur.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    entry_valeur.delete(0, tk.END)

# --------- TRI FONCTIONS ---------
def trier_par_valeur(croissant=True):
    sorted_items = sorted(items, key=lambda x: x['valeur'], reverse=not croissant)
    refresh_inventaire(sorted_items)

def trier_par_etat():
    sorted_items = sorted(items, key=lambda x: x['etat'].lower())
    refresh_inventaire(sorted_items)

def trier_par_createur():
    sorted_items = sorted(items, key=lambda x: x['createur'].lower())
    refresh_inventaire(sorted_items)

# --------- INTERFACE ---------
root = tk.Tk()
root.title("🎨 Gestion de Collection")
root.geometry("850x650")
root.configure(bg=SECONDARY_COLOR)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", font=FONT_TEXT, rowheight=25)
style.configure("TButton", font=FONT_TEXT, padding=6)
style.configure("TLabel", font=FONT_TEXT, background=SECONDARY_COLOR)
style.configure("TFrame", background=SECONDARY_COLOR)

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# --------- PAGE ACCUEIL ---------
page_accueil = ttk.Frame(notebook)
notebook.add(page_accueil, text='🏠 Accueil')

label_title = ttk.Label(page_accueil, text="Statistiques de la Collection", font=FONT_TITLE)
label_title.pack(pady=10)

stats_text = tk.StringVar()
update_stats()
label_stats = ttk.Label(page_accueil, textvariable=stats_text, justify='left', font=FONT_TEXT)
label_stats.pack(pady=10)

frame_buttons = ttk.Frame(page_accueil)
frame_buttons.pack(pady=20)

btn_modifier = ttk.Button(frame_buttons, text="✏️ Modifier", command=lambda: notebook.select(page_modifier))
btn_modifier.grid(row=0, column=0, padx=10)

btn_inventaire = ttk.Button(frame_buttons, text="📦 Inventaire", command=lambda: notebook.select(page_inventaire))
btn_inventaire.grid(row=0, column=1, padx=10)

# --------- PAGE MODIFIER ---------
page_modifier = ttk.Frame(notebook)
notebook.add(page_modifier, text='✏️ Ajouter')

label_form_title = ttk.Label(page_modifier, text="Ajouter un Item", font=FONT_TITLE)
label_form_title.grid(row=0, column=0, columnspan=2, pady=10)

labels = ["Nom", "État", "Créateur", "Description", "Valeur (€)"]
for i, text in enumerate(labels):
    ttk.Label(page_modifier, text=f"{text} :").grid(row=i+1, column=0, sticky='e', padx=10, pady=5)

entry_nom = ttk.Entry(page_modifier, width=30)
entry_etat = ttk.Entry(page_modifier, width=30)
entry_createur = ttk.Entry(page_modifier, width=30)
entry_description = ttk.Entry(page_modifier, width=30)
entry_valeur = ttk.Entry(page_modifier, width=30)

entry_nom.grid(row=1, column=1, pady=5)
entry_etat.grid(row=2, column=1, pady=5)
entry_createur.grid(row=3, column=1, pady=5)
entry_description.grid(row=4, column=1, pady=5)
entry_valeur.grid(row=5, column=1, pady=5)

btn_ajouter = ttk.Button(page_modifier, text="Ajouter l'Item", command=ajouter_item)
btn_ajouter.grid(row=6, column=0, columnspan=2, pady=15)

# --------- PAGE INVENTAIRE ---------
page_inventaire = ttk.Frame(notebook)
notebook.add(page_inventaire, text='📦 Inventaire')

label_inv_title = ttk.Label(page_inventaire, text="Liste des Items", font=FONT_TITLE)
label_inv_title.pack(pady=10)

# Recherche
search_var = tk.StringVar()
search_var.trace_add('write', search_items)
frame_search = ttk.Frame(page_inventaire)
frame_search.pack(pady=5)

ttk.Label(frame_search, text="🔍 Rechercher: ").pack(side='left')
search_entry = ttk.Entry(frame_search, textvariable=search_var, width=30)
search_entry.pack(side='left')

# Treeview
columns = ("Nom", "Créateur", "Valeur (€)", "État")
tree = ttk.Treeview(page_inventaire, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor='center', width=180)
tree.pack(pady=10, fill='both', expand=True)

# Boutons tri
frame_tri = ttk.Frame(page_inventaire)
frame_tri.pack(pady=5)

btn_tri_val_croissant = ttk.Button(frame_tri, text="Valeur ↑", command=lambda: trier_par_valeur(croissant=True))
btn_tri_val_croissant.grid(row=0, column=0, padx=5)

btn_tri_val_decroissant = ttk.Button(frame_tri, text="Valeur ↓", command=lambda: trier_par_valeur(croissant=False))
btn_tri_val_decroissant.grid(row=0, column=1, padx=5)

btn_tri_etat = ttk.Button(frame_tri, text="État A-Z", command=trier_par_etat)
btn_tri_etat.grid(row=0, column=2, padx=5)

btn_tri_createur = ttk.Button(frame_tri, text="Créateur A-Z", command=trier_par_createur)
btn_tri_createur.grid(row=0, column=3, padx=5)

btn_supprimer = ttk.Button(page_inventaire, text="🗑️ Supprimer l'Item Sélectionné", command=supprimer_item)
btn_supprimer.pack(pady=10)

root.mainloop()
