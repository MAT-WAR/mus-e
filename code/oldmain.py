import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

COULEUR_PRIMAIRE = "#4A90E2"
COULEUR_SECONDAIRE = "#F5F5F5"
POLICE_TITRE = ("Comfortaa", 16, "bold")
POLICE_TEXTE = ("Comfortaa", 11)

articles = []

def mettre_a_jour_statistiques():
    total_articles = len(articles)
    valeur_totale = sum(article['valeur'] for article in articles)
    total_prets = sum(1 for article in articles if article.get('prete'))
    createurs = {}
    for article in articles:
        createurs[article['createur']] = createurs.get(article['createur'], 0) + 1
    
    texte_stats.set(f"Nombre d'articles : {total_articles}\n"
                    f"Valeur totale : {valeur_totale} €\n"
                    f"Nombre de prêts : {total_prets}\n")

def ajouter_article():
    try:
        nom = entree_nom.get()
        etat = entree_etat.get()
        createur = entree_createur.get()
        description = entree_description.get()
        valeur = float(entree_valeur.get())
        date_ajout = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        articles.append({
            'nom': nom,
            'etat': etat,
            'createur': createur,
            'description': description,
            'valeur': valeur,
            'date_ajout': date_ajout,
            'lieu': "Stock",
            'prete': False
        })
        mettre_a_jour_statistiques()
        rafraichir_inventaire()
        vider_formulaire()
        messagebox.showinfo("Ajouté", f"Article '{nom}' ajouté avec succès.")
    except ValueError:
        messagebox.showerror("Erreur", "Valeur invalide pour le champ valeur.")

def supprimer_article():
    selectionne = tree.selection()
    if not selectionne:
        messagebox.showwarning("Aucun article", "Sélectionnez un article.")
        return
    if messagebox.askyesno("Confirmer", "Êtes-vous sûr de vouloir supprimer ?"):
        index = int(tree.item(selectionne[0], 'tags')[0])
        del articles[index]
        rafraichir_inventaire()
        mettre_a_jour_statistiques()

def rafraichir_inventaire(filtered=None):
    tree.delete(*tree.get_children())
    infos = filtered if filtered is not None else articles
    for idx, article in enumerate(infos):
        tree.insert('', 'end', values=(article['nom'], article['createur'], article['valeur'], article['etat']), tags=(str(idx),))

def rechercher_articles(*args):
    requete = var_recherche.get().lower()
    filtres = [article for article in articles if requete in article['nom'].lower()]
    rafraichir_inventaire(filtres)

def vider_formulaire():
    entree_nom.delete(0, tk.END)
    entree_etat.delete(0, tk.END)
    entree_createur.delete(0, tk.END)
    entree_description.delete(0, tk.END)
    entree_valeur.delete(0, tk.END)

# --------- FONCTIONS DE TRI ---------
def trier_par_valeur(croissant=True):
    articles_tries = sorted(articles, key=lambda x: x['valeur'], reverse=not croissant)
    rafraichir_inventaire(articles_tries)

def trier_par_etat():
    articles_tries = sorted(articles, key=lambda x: x['etat'].lower())
    rafraichir_inventaire(articles_tries)

def trier_par_createur():
    articles_tries = sorted(articles, key=lambda x: x['createur'].lower())
    rafraichir_inventaire(articles_tries)

# --------- INTERFACE ---------
root = tk.Tk()
root.title("🎨 Gestion de Collection")
root.geometry("850x650")
root.configure(bg=COULEUR_SECONDAIRE)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", font=POLICE_TEXTE, rowheight=25)
style.configure("TButton", font=POLICE_TEXTE, padding=6)
style.configure("TLabel", font=POLICE_TEXTE, background=COULEUR_SECONDAIRE)
style.configure("TFrame", background=COULEUR_SECONDAIRE)

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# --------- PAGE ACCUEIL ---------
page_accueil = ttk.Frame(notebook)
notebook.add(page_accueil, text='🏠 Accueil')

label_titre = ttk.Label(page_accueil, text="Statistiques de la Collection", font=POLICE_TITRE)
label_titre.pack(pady=10)

texte_stats = tk.StringVar()
mettre_a_jour_statistiques()
label_stats = ttk.Label(page_accueil, textvariable=texte_stats, justify='left', font=POLICE_TEXTE)
label_stats.pack(pady=10)

frame_boutons = ttk.Frame(page_accueil)
frame_boutons.pack(pady=20)

btn_modifier = ttk.Button(frame_boutons, text="✏️ Modifier", command=lambda: notebook.select(page_modifier))
btn_modifier.grid(row=0, column=0, padx=10)

btn_inventaire = ttk.Button(frame_boutons, text="📦 Inventaire", command=lambda: notebook.select(page_inventaire))
btn_inventaire.grid(row=0, column=1, padx=10)

# --------- PAGE MODIFIER ---------
page_modifier = ttk.Frame(notebook)
notebook.add(page_modifier, text='✏️ Modifier')

label_form_title = ttk.Label(page_modifier, text="Ajouter un Article", font=POLICE_TITRE)
label_form_title.grid(row=0, column=0, columnspan=2, pady=10)

labels = ["Nom", "État", "Créateur", "Description", "Valeur (€)"]
for i, text in enumerate(labels):
    ttk.Label(page_modifier, text=f"{text} :").grid(row=i+1, column=0, sticky='e', padx=10, pady=5)

entree_nom = ttk.Entry(page_modifier, width=30)
entree_etat = ttk.Entry(page_modifier, width=30)
entree_createur = ttk.Entry(page_modifier, width=30)
entree_description = ttk.Entry(page_modifier, width=30)
entree_valeur = ttk.Entry(page_modifier, width=30)

entree_nom.grid(row=1, column=1, pady=5)
entree_etat.grid(row=2, column=1, pady=5)
entree_createur.grid(row=3, column=1, pady=5)
entree_description.grid(row=4, column=1, pady=5)
entree_valeur.grid(row=5, column=1, pady=5)

btn_ajouter = ttk.Button(page_modifier, text="Ajouter l'Article", command=ajouter_article)
btn_ajouter.grid(row=6, column=0, columnspan=2, pady=15)

# --------- PAGE INVENTAIRE ---------
page_inventaire = ttk.Frame(notebook)
notebook.add(page_inventaire, text='📦 Inventaire')

label_inv_title = ttk.Label(page_inventaire, text="Liste des Articles", font=POLICE_TITRE)
label_inv_title.pack(pady=10)

# Recherche
var_recherche = tk.StringVar()
var_recherche.trace_add('write', rechercher_articles)
frame_recherche = ttk.Frame(page_inventaire)
frame_recherche.pack(pady=5)

ttk.Label(frame_recherche, text="🔍 Rechercher: ").pack(side='left')
entree_recherche = ttk.Entry(frame_recherche, textvariable=var_recherche, width=30)
entree_recherche.pack(side='left')

# Treeview
colonnes = ("Nom", "Créateur", "Valeur (€)", "État")
tree = ttk.Treeview(page_inventaire, columns=colonnes, show='headings')
for col in colonnes:
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

btn_supprimer = ttk.Button(page_inventaire, text="🗑️ Supprimer l'Article Sélectionné", command=supprimer_article)
btn_supprimer.pack(pady=10)

root.mainloop()
