# traitement.py
# Chargement, nettoyage, normalisation et fusion des données

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import messagebox, filedialog

# Connexion à la base MySQL
def get_engine():
    return create_engine("mysql+mysqlconnector://root:@localhost/TP_Interface_Data")

# Chargement des deux tables base1 et base2
def charger_bases():
    engine = get_engine()
    df1 = pd.read_sql("SELECT * FROM base1", engine)
    df2 = pd.read_sql("SELECT * FROM base2", engine)
    return df1, df2

# Chargement séparé (pour les onglets)
def charger_base1():
    engine = get_engine()
    try:
        df1 = pd.read_sql("SELECT * FROM base1", engine)
        return df1
    except Exception as e:
        print("Erreur lors du chargement de base1 :", e)
        return pd.DataFrame()

def charger_base2():
    engine = get_engine()
    try:
        df2 = pd.read_sql("SELECT * FROM base2", engine)
        return df2
    except Exception as e:
        print("Erreur lors du chargement de base2 :", e)
        return pd.DataFrame()
    
# Nettoyage des colonnes textuelles (supprime espaces et valeurs vides)
def nettoyer_textes(df):
    for c in df.select_dtypes(include='object').columns:
        df[c] = df[c].astype(str).str.strip()
        # remplacer string "nan" ou "" par NaN réel
        df[c] = df[c].replace({"": np.nan, "nan": np.nan})
    return df

# Imputation 
# Remplace les valeurs manquantes
def imputer(df):
    for c in df.columns:
        if pd.api.types.is_numeric_dtype(df[c]):
            df[c] = df[c].fillna(df[c].mean())
        else:
            df[c] = df[c].fillna("Inconnu")
    return df

# Normalisation 
# Normalise les valeurs numériques entre 0 et 1
def normaliser(df):
    num_cols = df.select_dtypes(include='number').columns
    num_cols = [col for col in num_cols if 'id' not in col.lower()]
    if len(num_cols) > 0:
        scaler = MinMaxScaler()
        df[num_cols] = scaler.fit_transform(df[num_cols])
    return df

# Fusion
# Fusion des deux bases sur la colonne "nom"
def fusionner_bases():
    df1, df2 = charger_bases()
    df1 = nettoyer_textes(imputer(df1))
    df2 = nettoyer_textes(imputer(df2))
    if 'nom' in df1.columns and 'nom' in df2.columns:
        merged = pd.merge(df1, df2, on='nom', how='outer', suffixes=('_base1', '_base2'))
    else:
        merged = pd.concat([df1, df2], ignore_index=True)
    merged = normaliser(merged)
    return merged

# Exporte le résultat dans un fichier CSV
def exporter_csv(df, nom_fichier="base_fusionnee.csv"):
    df.to_csv(nom_fichier, index=False, encoding="utf-8-sig")
    print(f"Fichier {nom_fichier} exporté avec succès!")

# Afficher stats valeurs manquantes (UI-friendly)
def afficher_stats_manquantes(df):
    if df is None or df.empty:
        messagebox.showinfo("Valeurs manquantes", "Aucune donnée.")
        return
    manquantes = df.isnull().sum()
    total = manquantes.sum()
    msg = "Statistiques des valeurs manquantes :\n\n"
    for col, cnt in manquantes.items():
        pct = (cnt / len(df)) * 100
        msg += f"{col}: {cnt} ({pct:.1f}%)\n"
    msg += f"\nTotal manquantes : {total}"
    messagebox.showinfo("Valeurs manquantes", msg)