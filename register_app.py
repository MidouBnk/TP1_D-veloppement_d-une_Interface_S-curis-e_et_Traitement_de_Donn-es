import tkinter as tk
from tkinter import messagebox
import mysql.connector
import bcrypt
import re

# --- Vérification de la complexité du mot de passe ---
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

# --- Fonction d'inscription ---
def register_user():
    username = entry_username.get().strip()
    password = entry_password.get()
    confirm = entry_confirm.get()

    if not username or not password or not confirm:
        messagebox.showwarning("Champs vides", "Veuillez remplir tous les champs.")
        return

    # Vérification de la correspondance des mots de passe
    if password != confirm:
        messagebox.showwarning("Erreur", "Les mots de passe ne correspondent pas.")
        return

    # Vérification de la validité du mot de passe
    valide, message = mot_de_passe_valide(password)
    if not valide:
        messagebox.showerror("Mot de passe invalide", message)
        return

    # Hachage du mot de passe
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Mets ton mot de passe MySQL si nécessaire
            database="TP_Interface_Data"
        )
        cursor = conn.cursor()

        # Vérifie si le nom d'utilisateur existe déjà
        cursor.execute("SELECT * FROM utilisateurs WHERE nom_utilisateur = %s", (username,))
        if cursor.fetchone():
            messagebox.showerror("Erreur", "Ce nom d'utilisateur est déjà utilisé.")
            conn.close()
            return

        # Insertion dans la table
        cursor.execute(
            "INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe) VALUES (%s, %s)",
            (username, hashed_pw.decode('utf-8'))
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Succès", "Inscription réussie ! Vous pouvez maintenant vous connecter.")
        window.destroy()

    except mysql.connector.Error as err:
        messagebox.showerror("Erreur", f"Problème de connexion : {err}")

# --- Interface graphique ---
window = tk.Tk()
window.title("Inscription")
window.geometry("400x400")
window.config(bg="#1f3865")

tk.Label(window, text="Créer un compte", font=("Arial", 18, "bold"), bg="#1f3865", fg="white").pack(pady=20)

tk.Label(window, text="Nom d'utilisateur :", bg="#1f3865", fg="white").pack()
entry_username = tk.Entry(window, width=30)
entry_username.pack(pady=5)

tk.Label(window, text="Mot de passe :", bg="#1f3865", fg="white").pack()
entry_password = tk.Entry(window, show="*", width=30)
entry_password.pack(pady=5)

tk.Label(window, text="Confirmer le mot de passe :", bg="#1f3865", fg="white").pack()
entry_confirm = tk.Entry(window, show="*", width=30)
entry_confirm.pack(pady=5)

tk.Button(window, text="S'inscrire", bg="#c99c33", fg="white", width=15, command=register_user).pack(pady=20)

window.mainloop()