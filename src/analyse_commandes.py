# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 20:51:56 2026

@author: lasug
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Reproductibilité et chemin de sortie
np.random.seed(42)
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# 2. Simulation de 75 jours de préparation de commandes
dates = pd.date_range(start="2026-08-15", periods=75, freq="D")
df = pd.DataFrame({"date": dates})
df["jour_semaine"] = df["date"].dt.day_name()

# Volume de base + effet jour + pics promo ponctuels
base_commandes = np.random.normal(loc=1100, scale=140, size=len(df))
facteur_jour = df["date"].dt.dayofweek.map({
    0: 1.15,  # Lundi (cumul week-end)
    1: 1.05,  # Mardi
    2: 1.00,  # Mercredi
    3: 1.02,  # Jeudi
    4: 1.08,  # Vendredi
    5: 0.70,  # Samedi
    6: 0.65,  # Dimanche
})

df["nb_commandes"] = (base_commandes * facteur_jour).round().astype(int)

# Ajout de 4 pics commerciaux / promos
pics_idx = [12, 27, 45, 63]
for idx in pics_idx:
    df.loc[idx : idx + 2, "nb_commandes"] = (
        df.loc[idx : idx + 2, "nb_commandes"] * 1.45
    ).round().astype(int)

# Articles moyens par commande et temps moyen de préparation (en minutes)
df["articles_par_commande"] = np.round(np.random.normal(loc=2.6, scale=0.4, size=len(df)).clip(1.5, 4.5), 2)
temps_prep_min = (df["nb_commandes"] * (1.8 + 0.45 * df["articles_par_commande"])) * 1.10  # +10% aléas
df["heures_charge_requises"] = np.round(temps_prep_min / 60, 1)

# Effectif présent (ex. 7h effectives de prod par personne) et capacité maximale en heures
df["preparateurs_presents"] = np.random.choice([10, 11, 12, 13], size=len(df), p=[0.25, 0.35, 0.25, 0.15])
HEURES_PAR_PERSONNE = 7.0
df["heures_capacite_dispo"] = df["preparateurs_presents"] * HEURES_PAR_PERSONNE

# Écart de charge et recommandation d'effectif (avec marge de sécurité de 5%)
df["ecart_heures"] = np.round(df["heures_charge_requises"] - df["heures_capacite_dispo"], 1)
df["preparateurs_recommandes"] = np.ceil((df["heures_charge_requises"] * 1.05) / HEURES_PAR_PERSONNE).astype(int)
df["renfort_interim_a_prevoir"] = (df["preparateurs_recommandes"] - df["preparateurs_presents"]).clip(lower=0)

# 3. Indicateurs clés (KPIs)
jours_en_retard = (df["ecart_heures"] > 0).sum()
max_retard_h = df["ecart_heures"].max()
total_renforts = df["renfort_interim_a_prevoir"].sum()

print("=== RÉSUMÉ ANALYSE CHARGE & CAPACITÉ ===")
print(f"Jours avec charge > capacité : {jours_en_retard} / {len(df)} jours")
print(f"Retard maximum estimé : {max_retard_h} heures de préparation")
print(f"Total journées-renfort recommandées sur la période : {total_renforts}")

# 4. Graphique 1 : Charge requise vs Capacité disponible
plt.figure(figsize=(12, 5))
plt.plot(df["date"], df["heures_charge_requises"], label="Charge requise (heures)", linewidth=2)
plt.plot(df["date"], df["heures_capacite_dispo"], label="Capacité équipe actuelle (heures)", linestyle="--", linewidth=2)
plt.fill_between(
    df["date"],
    df["heures_charge_requises"],
    df["heures_capacite_dispo"],
    where=(df["heures_charge_requises"] > df["heures_capacite_dispo"]),
    alpha=0.25,
    label="Surcharge / Risque de fin de journée incomplète",
)
plt.title("Anticipation de la charge de préparation vs Capacité d'équipe")
plt.xlabel("Date")
plt.ylabel("Heures de préparation")
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "charge_vs_capacite.png", dpi=150)
plt.close()

# 5. Graphique 2 : Renforts recommandés lors des pics
df_pics = df[df["renfort_interim_a_prevoir"] > 0].tail(20)
plt.figure(figsize=(12, 4.5))
plt.bar(df_pics["date"].dt.strftime("%d/%m"), df_pics["renfort_interim_a_prevoir"])
plt.title("Renforts préparateurs recommandés (20 derniers jours en surcharge)")
plt.xlabel("Date (JJ/MM)")
plt.ylabel("Nombre de préparateurs supplémentaires")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "renforts_recommandes.png", dpi=150)
plt.close()