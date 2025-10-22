# auth_app.py
# Application de connexion sécurisée avec Tkinter et MySQL

import tkinter as tk
from tkinter import messagebox
import mysql.connector
import bcrypt
import sys
import re
import main_app
from subprocess import Popen

# Fonction pour se connecter à la base de données MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="TP_Interface_Data"
    )

# Vérification de la sécurité du mot de passe
def mot_de_passe_valide(pwd):
    if len(pwd) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
    if not re.search(r"[A-Z]", pwd):
        return False, "Le mot de passe doit contenir une majuscule"
    if not re.search(r"[a-z]", pwd):
        return False, "Le mot de passe doit contenir une minuscule"
    if not re.search(r"\d", pwd):
        return False, "Le mot de passe doit contenir un chiffre"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
        return False, "Le mot de passe doit contenir un caractère spécial"
    return True, "Mot de passe valide"

# Classe principale pour la fenêtre de connexion
class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connexion sécurisée")
        self.geometry("420x260")
        self.resizable(False, False)
        self.attempts = 0 # compteur d'essais
        self.create_widgets()

    # Création des champs et boutons de la fenêtre
    def create_widgets(self):
        tk.Label(self, text="Nom d'utilisateur").pack(pady=(20,5))
        self.user_entry = tk.Entry(self)
        self.user_entry.pack(pady=5, ipadx=60)

        tk.Label(self, text="Mot de passe").pack(pady=5)
        self.pwd_entry = tk.Entry(self, show="*")
        self.pwd_entry.pack(pady=5, ipadx=60)

        # Case à cocher pour afficher ou cacher le mot de passe
        self.show_var = tk.IntVar()
        tk.Checkbutton(self, text="Afficher mot de passe", variable=self.show_var, command=self.toggle_pwd).pack(pady=(5,10))

        tk.Button(self, text="Se connecter", width=20, command=self.connexion).pack(pady=5)
        tk.Button(self, text="Créer un compte", command=open_register, bg="#2a4a7a", fg="white").pack(pady=10)


    # Affiche ou cache le mot de passe
    def toggle_pwd(self):
        self.pwd_entry.config(show="" if self.show_var.get() else "*")

    # Vérifie les identifiants dans la base
    def connexion(self):
        user = self.user_entry.get().strip()
        pwd = self.pwd_entry.get()

        if not user or not pwd:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs")
            return

        valid, msg = mot_de_passe_valide(pwd)
        if not valid:
            messagebox.showwarning("Erreur", msg)
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT mot_de_passe FROM utilisateurs WHERE nom_utilisateur=%s", (user,))
            result = cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Erreur base de données", str(e))
            return
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

        # Vérifie si le mot de passe correspond au hash stocké
        if result and bcrypt.checkpw(pwd.encode('utf-8'), result[0].encode('utf-8')):
            messagebox.showinfo("Succès", "Connexion réussie")
            self.destroy()
            main_app.MainWindow(user)
        else:
            self.echec()

    # Gestion des tentatives échouées
    def echec(self):
        self.attempts += 1
        if self.attempts >= 3:
            messagebox.showerror("Verrouillage", "3 tentatives échouées. L'application va se fermer.")
            self.destroy()
            sys.exit(1)
        else:
            messagebox.showerror("Erreur", f"Identifiant ou mot de passe incorrect ({self.attempts}/3)")

def open_register():
    Popen(["python", "register_app.py"])

# Lancement de la fenêtre
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
