"""
Radar Charts - Belgrano Analytics
Genera visualizaciones de rendimiento por jugador estilo Wyscout
Autor: Laureano
Fecha: Junio 2026
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs("visualizaciones", exist_ok=True)

# ─────────────────────────────────────────────
# 1. CARGAR DATOS
# ─────────────────────────────────────────────

df = pd.read_csv("data/belgrano_jugadores_limpio.csv")

# Convertir columnas numericas
cols_num = ["Age", "MP", "Starts", "Min", "90s", "Gls", "Ast",
            "G+A", "G-PK", "PK", "PKatt", "CrdY", "CrdR",
            "Gls_90", "Ast_90", "G+A_90", "G-PK_90", "G+A-PK_90"]
for col in cols_num:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Filtrar jugadores con al menos 5 partidos
df_filtrado = df[df["MP"] >= 5].copy()
print(f"Jugadores con 5+ partidos: {len(df_filtrado)}")

# ─────────────────────────────────────────────
# 2. FUNCION RADAR CHART
# ─────────────────────────────────────────────

def radar_chart(jugador_nombre, df, metricas, labels, color="#003087"):
    """Genera un radar chart estilo Wyscout para un jugador"""
    
    jugador = df[df["Player"] == jugador_nombre]
    if jugador.empty:
        print(f"  Jugador no encontrado: {jugador_nombre}")
        return
    
    # Valores del jugador
    valores = []
    for m in metricas:
        val = jugador[m].values[0] if m in jugador.columns else 0
        val = float(val) if pd.notna(val) else 0
        valores.append(val)
    
    # Normalizar valores (0 a 1) usando max de cada metrica en el equipo
    valores_norm = []
    for i, m in enumerate(metricas):
        max_val = df[m].max() if m in df.columns else 1
        max_val = max_val if max_val > 0 else 1
        valores_norm.append(valores[i] / max_val)
    
    # Configuracion del radar
    N = len(metricas)
    angulos = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    valores_norm += valores_norm[:1]
    angulos += angulos[:1]
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#0d1117")
    ax.set_facecolor("#0d1117")
    
    # Dibujar radar
    ax.plot(angulos, valores_norm, color=color, linewidth=2)
    ax.fill(angulos, valores_norm, color=color, alpha=0.3)
    
    # Configurar ejes
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(labels, size=11, color="white", fontweight="bold")
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["25%", "50%", "75%", "100%"], size=8, color="gray")
    ax.grid(color="gray", alpha=0.3)
    ax.spines["polar"].set_color("gray")
    
    # Titulo
    pos = jugador["Pos"].values[0] if "Pos" in jugador.columns else ""
    age = int(jugador["Age"].values[0]) if "Age" in jugador.columns else ""
    
    plt.title(
        f"{jugador_nombre}\n{pos} | {age} años | Belgrano 2024",
        size=14, color="white", fontweight="bold", pad=20
    )
    
    # Valores en cada punto
    for i, (ang, val_norm, val_real) in enumerate(zip(angulos[:-1], valores_norm[:-1], valores)):
        ax.annotate(
            f"{val_real:.1f}",
            xy=(ang, val_norm),
            xytext=(ang, val_norm + 0.08),
            ha="center", va="center",
            color="white", fontsize=9,
            fontweight="bold"
        )
    
    # Guardar
    nombre_archivo = jugador_nombre.replace(" ", "_").replace("é", "e").replace("á", "a").replace("í", "i").replace("ó", "o").replace("ú", "u")
    ruta = f"visualizaciones/radar_{nombre_archivo}.png"
    plt.tight_layout()
    plt.savefig(ruta, dpi=150, bbox_inches="tight", facecolor="#0d1117")
    plt.close()
    print(f"  Guardado: {ruta}")

# ─────────────────────────────────────────────
# 3. GENERAR RADARES POR POSICION
# ─────────────────────────────────────────────

print("\nGenerando radar charts...")

# Metricas para delanteros y mediocampistas ofensivos
metricas_ataque = ["Gls", "Ast", "G+A", "MP", "Starts", "CrdY"]
labels_ataque   = ["Goles", "Asistencias", "G+A", "Partidos", "Titularidades", "Amarillas"]

# Metricas para defensores
metricas_defensa = ["MP", "Starts", "Min", "CrdY", "G+A", "Gls"]
labels_defensa   = ["Partidos", "Titular", "Minutos", "Amarillas", "G+A", "Goles"]

# Jugadores destacados para generar radares
jugadores_ataque = ["Franco Jara", "Bryan Reyna", "Nicolas Fernandez"]
jugadores_defensa = ["Alejandro Rebola", "Rafael Marcelo Delgado", "Mariano Troilo"]

# Buscar nombres exactos en el dataframe
print("\nJugadores disponibles:")
for nombre in df_filtrado["Player"].tolist():
    print(f"  {nombre}")

print("\nGenerando radares de atacantes...")
for jugador in df_filtrado["Player"].tolist():
    pos = df_filtrado[df_filtrado["Player"] == jugador]["Pos"].values[0]
    if any(p in str(pos) for p in ["FW", "MF"]):
        radar_chart(jugador, df_filtrado, metricas_ataque, labels_ataque, color="#1a75ff")

print("\nGenerando radares de defensores...")
for jugador in df_filtrado["Player"].tolist():
    pos = df_filtrado[df_filtrado["Player"] == jugador]["Pos"].values[0]
    if "DF" in str(pos) or "GK" in str(pos):
        radar_chart(jugador, df_filtrado, metricas_defensa, labels_defensa, color="#00cc66")

print("\nTodos los radar charts generados en carpeta: visualizaciones/")
