# main_app.py
# Fenêtre principale après authentification

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import traitement
import matplotlib.pyplot as plt
import seaborn as sns

# Classe principale de l'application
class MainWindow(tk.Tk):
    def __init__(self, utilisateur):
        super().__init__()
        self.title(f"Application - Connecté : {utilisateur}")
        self.geometry("1200x700")
        # DataFrames
        self.df_base1 = None
        self.df_base2 = None
        self.df_base1_traitee = None
        self.df_base2_traitee = None
        self.df = traitement.fusionner_bases()  # Chargement initial des données fusionnées
        self.create_menu()
        self.create_toolbar()
        self.create_content()
        self.show_table()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.mainloop()

    # Barre de menu / Menu principal
    def create_menu(self):
        menubar = tk.Menu(self)

        # Menu Fichier / Workflow
        fichier = tk.Menu(menubar, tearoff=0)
        fichier.add_command(label="1. Charger données ", command=self.charger_donnees_brutes)
        fichier.add_separator()

        affichage_bases = tk.Menu(fichier, tearoff=0)
        affichage_bases.add_command(label="Afficher Base1 brute", command=lambda: self.afficher_base("base1_brute"))
        affichage_bases.add_command(label="Afficher Base2 brute", command=lambda: self.afficher_base("base2_brute"))
        affichage_bases.add_separator()
        affichage_bases.add_command(label="Comparer les deux bases", command=self.comparer_bases_brutes)
        fichier.add_cascade(label="2. Affichage des bases", menu=affichage_bases)
        fichier.add_separator()

        fichier.add_command(label="3. Standardisation des textes", command=self.standardiser_textes)
        fichier.add_command(label="4. Gestion des données manquantes", command=self.gestion_manquantes)
        fichier.add_separator()

        fichier.add_command(label="5. Normalisation des valeurs numériques", command=self.normaliser_donnees)
        fichier.add_separator()

        fichier.add_command(label="6. Fusionner les bases", command=self.fusionner_bases)
        fichier.add_separator()

        visualisation_comparative = tk.Menu(fichier, tearoff=0)
        visualisation_comparative.add_command(label="Base1: Avant/Après nettoyage", command=self.comparaison_base1_avant_apres)
        visualisation_comparative.add_command(label="Base2: Avant/Après nettoyage", command=self.comparaison_base2_avant_apres)
        visualisation_comparative.add_command(label="Comparaison Base1 vs Base2", command=self.comparaison_base1_base2)
        visualisation_comparative.add_command(label="Distribution avant/après normalisation", command=self.comparaison_normalisation)
        visualisation_comparative.add_command(label="Valeurs manquantes avant/après", command=self.comparaison_manquantes)
        fichier.add_cascade(label="7. Visualisation comparative", menu=visualisation_comparative)
        fichier.add_separator()

        fichier.add_command(label="8. Afficher résultat final", command=self.afficher_resultat_final)
        fichier.add_command(label="9. Exporter résultat final CSV", command=self.exporter_resultat_final)
        fichier.add_separator()

        fichier.add_command(label="Quitter", command=self.on_close)
        menubar.add_cascade(label="Fichier", menu=fichier)

        # Menu Visualisation
        visualisation = tk.Menu(menubar, tearoff=0)
        visualisation.add_command(label="Histogrammes", command=self.show_histogram)
        visualisation.add_command(label="Matrice de corrélation", command=self.show_heatmap)
        visualisation.add_command(label="Boxplots", command=self.show_boxplot)
        visualisation.add_command(label="Valeurs manquantes", command=self.show_missing_values)
        menubar.add_cascade(label="Visualisation", menu=visualisation)

        # Menu Aide
        aide = tk.Menu(menubar, tearoff=0)
        aide.add_command(label="À propos", command=self.afficher_a_propos)
        aide.add_command(label="Guide d'utilisation", command=self.afficher_guide)
        menubar.add_cascade(label="Aide", menu=aide)

        self.config(menu=menubar)

    # Barre d’outils avec boutons
    def create_toolbar(self):
        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        tk.Button(toolbar, text="Charger", command=self.charger_donnees_brutes).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Base1", command=lambda: self.afficher_base("base1_brute")).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Base2", command=lambda: self.afficher_base("base2_brute")).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Standardiser", command=self.standardiser_textes).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Normaliser", command=self.normaliser_donnees).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Fusionner", command=self.fusionner_bases).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Comparer", command=self.comparer_bases_brutes).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Exporter CSV", command=self.exporter_resultat_final).pack(side=tk.LEFT, padx=2, pady=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

    # Zone principale d'affichage
    def create_content(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Base1 tab
        self.tab_base1 = ttk.Frame(self.notebook)
        self.create_tab_base(self.tab_base1, "Base1")
        self.notebook.add(self.tab_base1, text="Base1")

        # Base2 tab
        self.tab_base2 = ttk.Frame(self.notebook)
        self.create_tab_base(self.tab_base2, "Base2")
        self.notebook.add(self.tab_base2, text="Base2")

        # Fusion tab
        self.tab_fusion = ttk.Frame(self.notebook)
        self.create_tab_base(self.tab_fusion, "Fusion")
        self.notebook.add(self.tab_fusion, text="Fusion")

        # Info étape
        self.etape_label = tk.Label(self, text="Prêt - Chargez les données brutes", font=("Segoe UI", 11, "bold"), fg="blue")
        self.etape_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

    def create_tab_base(self, parent, nom_base):
        frame = tk.Frame(parent, padx=20, pady=20, bg="#f5f5f5")
        frame.pack(fill=tk.BOTH, expand=True)
        
        titre_label = tk.Label(
            frame, 
            text=f"{nom_base} - Données", 
            font=("Segoe UI", 12, "bold"), 
            bg="#f5f5f5"
            )
        titre_label.pack(pady=(0, 10))
        
        info_label = tk.Label(
            frame, 
            text="Aucune donnée chargée", 
            font=("Segoe UI", 9), 
            bg="#f5f5f5", 
            fg="#333"
            )
        
        info_label.pack(anchor=tk.W, pady=(0, 10))
        
        tree_frame = tk.Frame(frame, bg="#ffffff", relief=tk.SOLID, bd=1)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        tree = ttk.Treeview(tree_frame)
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        scrollbar_x.pack(side='bottom', fill='x')
        tree.configure(xscrollcommand=scrollbar_x.set)
        
        if nom_base == "Base1":
            self.tree_base1 = tree
            self.info_base1 = info_label
        elif nom_base == "Base2":
            self.tree_base2 = tree
            self.info_base2 = info_label
        else:
            self.tree_fusion = tree
            self.info_fusion = info_label


    def charger_donnees_brutes(self):
        """Charge base1 et base2 depuis traitement.py"""
        try:
            self.df_base1 = traitement.charger_base1()
            self.df_base2 = traitement.charger_base2()
            # copies traitées initiales
            self.df_base1_traitee = self.df_base1.copy()
            self.df_base2_traitee = self.df_base2.copy()

            # Affiche les deux bases
            if self.df_base1 is not None:
                self.afficher_donnees_base(self.df_base1, self.tree_base1, self.info_base1, "Base1 - Données brutes")
            if self.df_base2 is not None:
                self.afficher_donnees_base(self.df_base2, self.tree_base2, self.info_base2, "Base2 - Données brutes")

            self.etape_label.config(text="✅ Étape 1 : Données brutes chargées", fg="green")
            messagebox.showinfo("Chargement", "Bases chargées avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur chargement", str(e))

    def afficher_base(self, type_base):
        """Affiche un onglet précis (brut/traite)"""
        if type_base == "base1_brute":
            if self.df_base1 is None:
                messagebox.showwarning("Attention", "Chargez d'abord les données brutes")
                return
            self.afficher_donnees_base(self.df_base1, self.tree_base1, self.info_base1, "Base1 - Données brutes")
            self.notebook.select(0)
        elif type_base == "base2_brute":
            if self.df_base2 is None:
                messagebox.showwarning("Attention", "Chargez d'abord les données brutes")
                return
            self.afficher_donnees_base(self.df_base2, self.tree_base2, self.info_base2, "Base2 - Données brutes")
            self.notebook.select(1)
        elif type_base == "base1_traitee":
            if self.df_base1_traitee is None:
                messagebox.showwarning("Attention", "Aucune version traitée disponible")
                return
            self.afficher_donnees_base(self.df_base1_traitee, self.tree_base1, self.info_base1, "Base1 - Données traitées")
            self.notebook.select(0)
        elif type_base == "base2_traitee":
            if self.df_base2_traitee is None:
                messagebox.showwarning("Attention", "Aucune version traitée disponible")
                return
            self.afficher_donnees_base(self.df_base2_traitee, self.tree_base2, self.info_base2, "Base2 - Données traitées")
            self.notebook.select(1)

    def comparer_bases_brutes(self):
        """Affiche graphiques comparatifs simples entre base1 et base2 brutes"""
        if self.df_base1 is None or self.df_base2 is None:
            messagebox.showwarning("Attention", "Chargez d'abord les deux bases")
            return
        try:
            fig, axes = plt.subplots(2, 2, figsize=(14,10))

            # nombre de lignes / colonnes
            axes[0,0].bar(['Base1', 'Base2'], [len(self.df_base1), len(self.df_base2)])
            axes[0,0].set_title("Nombre de lignes")

            axes[0,1].bar(['Base1', 'Base2'], [len(self.df_base1.columns), len(self.df_base2.columns)])
            axes[0,1].set_title("Nombre de colonnes")

            # valeurs manquantes totales
            m1 = self.df_base1.isnull().sum().sum()
            m2 = self.df_base2.isnull().sum().sum()
            axes[1,0].bar(['Base1', 'Base2'], [m1, m2])
            axes[1,0].set_title("Total valeurs manquantes")

            # colonnes communes vs spécifiques
            comm = len(set(self.df_base1.columns) & set(self.df_base2.columns))
            only1 = len(set(self.df_base1.columns) - set(self.df_base2.columns))
            only2 = len(set(self.df_base2.columns) - set(self.df_base1.columns))
            axes[1,1].pie([comm, only1, only2], labels=['Communes','Base1 seule','Base2 seule'], autopct='%1.1f%%')
            axes[1,1].set_title("Colonnes : communes / spécifiques")

            plt.suptitle("Comparaison Base1 vs Base2 (brutes)")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Erreur comparaison", str(e))

    def standardiser_textes(self):
        """Nettoie/standardise les colonnes textuelles sur les deux bases traitées"""
        if self.df_base1_traitee is None or self.df_base2_traitee is None:
            messagebox.showwarning("Attention", "Chargez d'abord les données brutes")
            return
        try:
            self.df_base1_traitee = traitement.nettoyer_textes(self.df_base1_traitee.copy())
            self.df_base2_traitee = traitement.nettoyer_textes(self.df_base2_traitee.copy())

            self.afficher_donnees_base(self.df_base1_traitee, self.tree_base1, self.info_base1, "Base1 - Textes standardisés")
            self.afficher_donnees_base(self.df_base2_traitee, self.tree_base2, self.info_base2, "Base2 - Textes standardisés")
            self.etape_label.config(text="Textes standardisés", fg="green")
            messagebox.showinfo("Standardisation", "Textes standardisés pour Base1 et Base2.")
        except Exception as e:
            messagebox.showerror("Erreur standardisation", str(e))

    def gestion_manquantes(self):
        """Impute les valeurs manquantes sur les deux bases traitées"""
        if self.df_base1_traitee is None or self.df_base2_traitee is None:
            messagebox.showwarning("Attention", "Chargez et standardisez d'abord les données")
            return
        try:
            avant1 = self.df_base1_traitee.isnull().sum().sum()
            avant2 = self.df_base2_traitee.isnull().sum().sum()

            self.df_base1_traitee = traitement.imputer(self.df_base1_traitee.copy())
            self.df_base2_traitee = traitement.imputer(self.df_base2_traitee.copy())

            apres1 = self.df_base1_traitee.isnull().sum().sum()
            apres2 = self.df_base2_traitee.isnull().sum().sum()

            self.afficher_donnees_base(self.df_base1_traitee, self.tree_base1, self.info_base1, "Base1 - Après imputation")
            self.afficher_donnees_base(self.df_base2_traitee, self.tree_base2, self.info_base2, "Base2 - Après imputation")

            self.etape_label.config(text="Données manquantes traitées", fg="green")
            messagebox.showinfo("Imputation", f"Base1: {avant1} → {apres1} | Base2: {avant2} → {apres2}")
        except Exception as e:
            messagebox.showerror("Erreur imputation", str(e))

    def normaliser_donnees(self):
        """Normalise les colonnes numériques (MinMax) pour les bases traitées"""
        if self.df_base1_traitee is None or self.df_base2_traitee is None:
            messagebox.showwarning("Attention", "Traitez d'abord les bases (standardisation + imputation)")
            return
        try:
            self.df_base1_traitee = traitement.normaliser(self.df_base1_traitee.copy())
            self.df_base2_traitee = traitement.normaliser(self.df_base2_traitee.copy())

            self.afficher_donnees_base(self.df_base1_traitee, self.tree_base1, self.info_base1, "Base1 - Normalisée")
            self.afficher_donnees_base(self.df_base2_traitee, self.tree_base2, self.info_base2, "Base2 - Normalisée")

            self.etape_label.config(text="Normalisation terminée", fg="green")
            messagebox.showinfo("Normalisation", "Normalisation MinMax appliquée aux colonnes numériques.")
        except Exception as e:
            messagebox.showerror("Erreur normalisation", str(e))

    def fusionner_bases(self):
        """Fusionne les bases traitées (utilise traitement.fusionner_bases)"""
        if self.df_base1_traitee is None or self.df_base2_traitee is None:
            messagebox.showwarning("Attention", "Traitez d'abord les bases avant fusion")
            return
        try:
            # On peut appeler la fonction qui recharge et fusionne ou fusionner les dataframes locales
            # Utilisation de la fonction fusionner_bases() pour garantir comportement cohérent
            self.df = traitement.fusionner_bases()
            self.afficher_donnees_base(self.df, self.tree_fusion, self.info_fusion, "Base fusionnée")
            self.notebook.select(2)
            self.etape_label.config(text="✅ Fusion terminée", fg="green")
            messagebox.showinfo("Fusion", f"Fusion terminée : {len(self.df)} lignes")
        except Exception as e:
            messagebox.showerror("Erreur fusion", str(e))

    def comparaison_base1_avant_apres(self):
        if self.df_base1 is None or self.df_base1_traitee is None:
            messagebox.showwarning("Attention", "Chargez et traitez Base1 d'abord")
            return
        self._comparaison_avant_apres(self.df_base1, self.df_base1_traitee, "BASE1")

    def comparaison_base2_avant_apres(self):
        if self.df_base2 is None or self.df_base2_traitee is None:
            messagebox.showwarning("Attention", "Chargez et traitez Base2 d'abord")
            return
        self._comparaison_avant_apres(self.df_base2, self.df_base2_traitee, "BASE2")

    def _comparaison_avant_apres(self, df_brut, df_traite, nom_base):
        try:
            fig, axes = plt.subplots(2, 2, figsize=(14,10))

            manq_av = df_brut.isnull().sum()
            manq_ap = df_traite.isnull().sum()
            axes[0,0].bar(manq_av.index, manq_av.values, alpha=0.7, label='Avant')
            axes[0,0].bar(manq_ap.index, manq_ap.values, alpha=0.7, label='Après')
            axes[0,0].set_title(f"{nom_base} - Valeurs manquantes")
            axes[0,0].tick_params(axis='x', rotation=45)
            axes[0,0].legend()

            num_cols = df_brut.select_dtypes(include='number').columns
            if len(num_cols) > 0:
                col = num_cols[0]
                axes[0,1].hist(df_brut[col].dropna(), bins=8, alpha=0.7, label='Avant')
                axes[0,1].hist(df_traite[col].dropna(), bins=8, alpha=0.7, label='Après')
                axes[0,1].set_title(f"{nom_base} - Distribution {col}")
                axes[0,1].legend()

            if 'nom' in df_brut.columns:
                noms_av = df_brut['nom'].astype(str).str.strip().value_counts().head(5)
                noms_ap = df_traite['nom'].astype(str).str.strip().value_counts().head(5)
                axes[1,0].bar(noms_av.index, noms_av.values, alpha=0.7)
                axes[1,0].set_title("Noms - Avant")
                axes[1,0].tick_params(axis='x', rotation=45)
                axes[1,1].bar(noms_ap.index, noms_ap.values, alpha=0.7)
                axes[1,1].set_title("Noms - Après")
                axes[1,1].tick_params(axis='x', rotation=45)

            plt.suptitle(f"Comparaison Avant/Après - {nom_base}")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Erreur comparaison", str(e))

    def comparaison_base1_base2(self):
        if self.df_base1 is None or self.df_base2 is None:
            messagebox.showwarning("Attention", "Chargez d'abord les deux bases")
            return
        try:
            fig, axes = plt.subplots(1, 2, figsize=(12,5))
            axes[0].bar(['Base1','Base2'], [len(self.df_base1), len(self.df_base2)])
            axes[0].set_title("Nombre de lignes")
            m1 = self.df_base1.isnull().sum().sum()
            m2 = self.df_base2.isnull().sum().sum()
            axes[1].bar(['Base1','Base2'], [m1, m2])
            axes[1].set_title("Total valeurs manquantes")
            plt.suptitle("Comparaison Base1 vs Base2")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def comparaison_normalisation(self):
        """Compare distributions avant/après normalisation pour Base1"""
        if self.df_base1 is None:
            messagebox.showwarning("Attention", "Chargez d'abord les données")
            return
        try:
            df1_brut = traitement.charger_base1()
            df1_clean = traitement.nettoyer_textes(traitement.imputer(df1_brut.copy()))
            df1_norm = traitement.normaliser(df1_clean.copy())
            num_cols = df1_clean.select_dtypes(include='number').columns
            if len(num_cols) == 0:
                messagebox.showinfo("Info", "Aucune colonne numérique à comparer")
                return
            n = min(2, len(num_cols))
            fig, axes = plt.subplots(1, n, figsize=(6*n,4))
            if n == 1:
                axes = [axes]
            for i, col in enumerate(num_cols[:n]):
                axes[i].hist(df1_clean[col].dropna(), bins=8, alpha=0.7, label='Avant')
                axes[i].hist(df1_norm[col].dropna(), bins=8, alpha=0.7, label='Après')
                axes[i].set_title(col)
                axes[i].legend()
            plt.suptitle("Avant / Après normalisation (Base1)")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Erreur normalisation comparaison", str(e))

    def comparaison_manquantes(self):
        if self.df_base1 is None:
            messagebox.showwarning("Attention", "Chargez d'abord les données")
            return
        try:
            df1_brut, df2_brut = traitement.charger_bases()
            df1_propre = traitement.nettoyer_textes(traitement.imputer(df1_brut.copy()))
            df2_propre = traitement.nettoyer_textes(traitement.imputer(df2_brut.copy()))
            fig, axes = plt.subplots(1,2,figsize=(14,5))
            manq_av1 = df1_brut.isnull().sum()
            manq_ap1 = df1_propre.isnull().sum()
            axes[0].bar(manq_av1.index, manq_av1.values, alpha=0.7, label='Avant')
            axes[0].bar(manq_ap1.index, manq_ap1.values, alpha=0.7, label='Après')
            axes[0].tick_params(axis='x', rotation=45)
            axes[0].set_title("Base1 - Manquantes Avant/Après")
            axes[0].legend()

            manq_av2 = df2_brut.isnull().sum()
            manq_ap2 = df2_propre.isnull().sum()
            axes[1].bar(manq_av2.index, manq_av2.values, alpha=0.7, label='Avant')
            axes[1].bar(manq_ap2.index, manq_ap2.values, alpha=0.7, label='Après')
            axes[1].tick_params(axis='x', rotation=45)
            axes[1].set_title("Base2 - Manquantes Avant/Après")
            axes[1].legend()

            plt.suptitle("Comparaison valeurs manquantes Avant/Après")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Erreur comparaison manquantes", str(e))

    def afficher_resultat_final(self):
        if self.df is None:
            messagebox.showwarning("Attention", "Aucune fusion réalisée")
            return
        self.afficher_donnees_base(self.df, self.tree_fusion, self.info_fusion, "RÉSULTAT FINAL - Base fusionnée")
        self.notebook.select(2)
        self.etape_label.config(text="Résultat final prêt", fg="green")
        stats = f"Lignes: {len(self.df)} | Colonnes: {len(self.df.columns)} | Manquantes: {self.df.isnull().sum().sum()}"
        messagebox.showinfo("Statistiques", stats)

    def exporter_resultat_final(self):
        if self.df is None:
            messagebox.showwarning("Attention", "Aucune fusion à exporter")
            return
        # Demande de chemin via filedialog
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")], initialfile="base_fusionnee.csv")
        if filepath:
            try:
                traitement.exporter_csv(self.df, filepath)
                messagebox.showinfo("Export", f"Fichier exporté: {filepath}")
            except Exception as e:
                messagebox.showerror("Erreur export", str(e))

    def afficher_donnees_base(self, df, tree, info_label, titre):
        tree.delete(*tree.get_children())
        if df is None or df.empty:
            info_label.config(text=f"{titre} - Aucune donnée")
            return
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))
        info_label.config(text=f"{titre} | Lignes: {len(df)} | Colonnes: {len(df.columns)}")


    # Rafraîchissement

    # Affiche les données dans le tableau
    def show_table(self):
        if self.df is None or self.df.empty:
            return

        tree = self.tree_fusion
        tree.delete(*tree.get_children())
        tree["columns"] = list(self.df.columns)
        tree["show"] = "headings"

        for col in self.df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')

        for _, row in self.df.iterrows():
            tree.insert("", "end", values=list(row))

    # Histogrammes
    # Affiche les histogrammes des colonnes numériques
    def show_histogram(self):
        num_cols = self.df.select_dtypes(include='number').columns
        if len(num_cols) == 0:
            messagebox.showinfo("Info", "Aucune colonne numérique")
            return
        self.df[num_cols].hist(figsize=(12,6))
        plt.suptitle("Histogrammes des colonnes numériques")
        plt.tight_layout()
        plt.show()

    # Corrélation
    # Affiche une matrice de corrélation
    def show_heatmap(self):
        num_cols = self.df.select_dtypes(include='number').columns
        if len(num_cols) < 2:
            messagebox.showinfo("Info", "Pas assez de colonnes numériques")
            return
        plt.figure(figsize=(10,8))
        sns.heatmap(self.df[num_cols].corr(), annot=True, cmap="coolwarm")
        plt.title("Matrice de corrélation")
        plt.tight_layout()
        plt.show()
    
    def show_boxplot(self):
        if self.df is None or self.df.empty:
            messagebox.showinfo("Info", "Aucune donnée fusionnée à visualiser")
            return
        num_cols = self.df.select_dtypes(include='number').columns
        if len(num_cols) == 0:
            messagebox.showinfo("Info", "Aucune colonne numérique")
            return
        plt.figure(figsize=(12,6))
        self.df[num_cols].boxplot()
        plt.title("Boxplots - Base fusionnée")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def show_missing_values(self):
        if self.df is None or self.df.empty:
            messagebox.showinfo("Info", "Aucune donnée fusionnée")
            return
        traitement.afficher_stats_manquantes(self.df)

    def afficher_a_propos(self):
        messagebox.showinfo("À propos", "Application de traitement et fusion de données — version corrigée.")

    def afficher_guide(self):
        messagebox.showinfo("Guide d'utilisation", "Suivez l'ordre du menu Fichier pour le workflow complet.")

    # Fermeture propre de l’application
    def on_close(self):
        if messagebox.askokcancel("Quitter", "Voulez-vous quitter ?"):
            self.destroy()