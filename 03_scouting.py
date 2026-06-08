"""
Scouting - Belgrano Analytics
Busca jugadores disponibles en el mercado con perfil compatible
Autor: Laureano
Fecha: Junio 2026
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

os.makedirs("data", exist_ok=True)

# ─────────────────────────────────────────────
# 1. PERFIL DE BELGRANO
# ─────────────────────────────────────────────

# Basado en el analisis que hicimos:
# - Sistema: transiciones rapidas, presion alta
# - Necesidad: delantero goleador, mediocampista creativo
# - Perfil etario: mix de experiencia (30+) y juventud (20-24)

print("Belgrano Analytics — Modulo de Scouting")
print("="*50)
print("Perfil de busqueda:")
print("  - Posiciones: FW, MF")
print("  - Edad: 20-33 anos")
print("  - Liga: Argentina y Sudamerica")
print("="*50)

# ─────────────────────────────────────────────
# 2. DATOS DE JUGADORES LIBRES - LIGA ARGENTINA
# ─────────────────────────────────────────────

# Usamos datos estaticos curados de jugadores sin contrato
# o con contrato por vencer en Argentina (fuente: Transfermarkt publica)

jugadores_disponibles = [
    # Delanteros disponibles
    {"Player": "Mauro Icardi",        "Pos": "FW", "Age": 31, "Nacionalidad": "Argentina", "Liga_actual": "Libre",          "Valor_mercado": 3.0,  "Contrato": "Libre"},
    {"Player": "Lautaro Acosta",      "Pos": "FW", "Age": 34, "Nacionalidad": "Argentina", "Liga_actual": "Lanus",          "Valor_mercado": 0.8,  "Contrato": "Jun 2025"},
    {"Player": "Dario Benedetto",     "Pos": "FW", "Age": 34, "Nacionalidad": "Argentina", "Liga_actual": "Libre",          "Valor_mercado": 0.5,  "Contrato": "Libre"},
    {"Player": "Lucas Pratto",        "Pos": "FW", "Age": 36, "Nacionalidad": "Argentina", "Liga_actual": "Libre",          "Valor_mercado": 0.3,  "Contrato": "Libre"},
    {"Player": "Cristian Pavon",      "Pos": "FW", "Age": 28, "Nacionalidad": "Argentina", "Liga_actual": "Libre",          "Valor_mercado": 2.0,  "Contrato": "Libre"},
    {"Player": "Jonathan Calleri",    "Pos": "FW", "Age": 30, "Nacionalidad": "Argentina", "Liga_actual": "Sao Paulo",      "Valor_mercado": 3.5,  "Contrato": "Dic 2025"},
    {"Player": "Gaston Gimenez",      "Pos": "MF", "Age": 32, "Nacionalidad": "Argentina", "Liga_actual": "Chicago Fire",   "Valor_mercado": 1.5,  "Contrato": "Dic 2025"},
    {"Player": "Hernan Perez",        "Pos": "MF", "Age": 33, "Nacionalidad": "Argentina", "Liga_actual": "Libre",          "Valor_mercado": 0.4,  "Contrato": "Libre"},
    {"Player": "Fernando Zuqui",      "Pos": "MF", "Age": 32, "Nacionalidad": "Argentina", "Liga_actual": "Estudiantes",    "Valor_mercado": 1.2,  "Contrato": "Jun 2025"},
    {"Player": "Leonardo Gil",        "Pos": "MF", "Age": 33, "Nacionalidad": "Argentina", "Liga_actual": "Colo-Colo",      "Valor_mercado": 1.0,  "Contrato": "Dic 2025"},
    {"Player": "Rodrigo Bentancur",   "Pos": "MF", "Age": 27, "Nacionalidad": "Uruguay",   "Liga_actual": "Tottenham",      "Valor_mercado": 28.0, "Contrato": "Jun 2026"},
    {"Player": "Nicolas Lodeiro",     "Pos": "MF", "Age": 35, "Nacionalidad": "Uruguay",   "Liga_actual": "Libre",          "Valor_mercado": 0.5,  "Contrato": "Libre"},
    {"Player": "Joaquin Correa",      "Pos": "FW", "Age": 30, "Nacionalidad": "Argentina", "Liga_actual": "Inter Milan",    "Valor_mercado": 8.0,  "Contrato": "Jun 2025"},
    {"Player": "Angel Correa",        "Pos": "FW", "Age": 29, "Nacionalidad": "Argentina", "Liga_actual": "Atletico Madrid","Valor_mercado": 18.0, "Contrato": "Jun 2026"},
    {"Player": "Marcos Acuna",        "Pos": "MF", "Age": 32, "Nacionalidad": "Argentina", "Liga_actual": "Sevilla",        "Valor_mercado": 5.0,  "Contrato": "Jun 2025"},
    {"Player": "Lucas Ocampos",       "Pos": "MF", "Age": 30, "Nacionalidad": "Argentina", "Liga_actual": "Ajax",           "Valor_mercado": 12.0, "Contrato": "Jun 2026"},
    {"Player": "Exequiel Palacios",   "Pos": "MF", "Age": 26, "Nacionalidad": "Argentina", "Liga_actual": "Bayer Leverkusen","Valor_mercado": 20.0,"Contrato": "Jun 2026"},
    {"Player": "Alexis Mac Allister", "Pos": "MF", "Age": 26, "Nacionalidad": "Argentina", "Liga_actual": "Liverpool",      "Valor_mercado": 70.0, "Contrato": "Jun 2028"},
    # Jugadores de ligas locales accesibles
    {"Player": "Brian Romero",        "Pos": "FW", "Age": 27, "Nacionalidad": "Argentina", "Liga_actual": "River Plate",    "Valor_mercado": 3.0,  "Contrato": "Dic 2025"},
    {"Player": "Ramiro Carrera",      "Pos": "MF", "Age": 28, "Nacionalidad": "Argentina", "Liga_actual": "Tigre",          "Valor_mercado": 1.0,  "Contrato": "Jun 2025"},
]

df_mercado = pd.DataFrame(jugadores_disponibles)

# ─────────────────────────────────────────────
# 3. SCORING DE COMPATIBILIDAD CON BELGRANO
# ─────────────────────────────────────────────

print("\nCalculando compatibilidad con perfil de Belgrano...")

def calcular_score(row):
    score = 0
    
    # Edad ideal: 24-31 (experiencia sin ser muy mayor)
    if 24 <= row["Age"] <= 31:
        score += 30
    elif 22 <= row["Age"] <= 33:
        score += 20
    else:
        score += 5
    
    # Disponibilidad
    if row["Contrato"] == "Libre":
        score += 35  # Jugador libre = prioridad maxima
    elif "2025" in str(row["Contrato"]):
        score += 25  # Contrato por vencer pronto
    else:
        score += 10
    
    # Valor de mercado accesible para Belgrano (menos de 5M)
    if row["Valor_mercado"] <= 2.0:
        score += 25
    elif row["Valor_mercado"] <= 5.0:
        score += 15
    else:
        score += 5
    
    # Liga argentina o sudamericana (adaptacion mas facil)
    ligas_locales = ["Libre", "Lanus", "Estudiantes", "River Plate", "Tigre", "Boca Juniors"]
    if row["Liga_actual"] in ligas_locales:
        score += 10
    
    return score

df_mercado["Score_Compatibilidad"] = df_mercado.apply(calcular_score, axis=1)
df_mercado = df_mercado.sort_values("Score_Compatibilidad", ascending=False)

# ─────────────────────────────────────────────
# 4. RESULTADOS POR POSICION
# ─────────────────────────────────────────────

print("\n" + "="*50)
print("TOP CANDIDATOS PARA BELGRANO")
print("="*50)

print("\nDELANTEROS (FW):")
fw = df_mercado[df_mercado["Pos"] == "FW"].head(5)
print(fw[["Player","Age","Liga_actual","Valor_mercado","Contrato","Score_Compatibilidad"]].to_string(index=False))

print("\nMEDIOCAMPISTAS (MF):")
mf = df_mercado[df_mercado["Pos"] == "MF"].head(5)
print(mf[["Player","Age","Liga_actual","Valor_mercado","Contrato","Score_Compatibilidad"]].to_string(index=False))

# ─────────────────────────────────────────────
# 5. EXPORTAR PARA POWER BI
# ─────────────────────────────────────────────

df_mercado.to_csv("data/scouting_candidatos.csv", index=False, decimal=",")
print(f"\nExportado: data/scouting_candidatos.csv")
print(f"Total candidatos analizados: {len(df_mercado)}")
print("\nScouting completado!")
