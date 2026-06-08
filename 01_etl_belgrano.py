"""
ETL - Belgrano Analytics
Descarga y procesa datos de la Liga Profesional Argentina
Autor: Laureano
Fecha: Mayo 2026
"""

import pandas as pd
import sqlite3
import os
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# 1. CONFIGURACION
# ─────────────────────────────────────────────

DB_PATH = "belgrano.db"
BELGRANO = "Belgrano"

print("Belgrano Analytics — ETL iniciado\n")

# ─────────────────────────────────────────────
# 2. DESCARGA DE DATOS DESDE FBREF VIA SCRAPERFC
# ─────────────────────────────────────────────

from ScraperFC import FBref

fbref = FBref()

print("Descargando partidos de la Liga Profesional Argentina 2024...")
try:
    partidos = fbref.scrape_matches(
        year="2024",
        league="Argentina Liga Profesional"
    )
    print(f"  Partidos descargados: {len(partidos)} filas")
    print(f"  Columnas: {partidos.columns.tolist()}")
except Exception as e:
    print(f"  Error: {e}")
    partidos = pd.DataFrame()

print("\nDescargando estadisticas de jugadores 2024...")
try:
    jugadores_dict = fbref.scrape_all_stats(
        year="2024",
        league="Argentina Liga Profesional"
    )
    # Extraer stats de jugadores de cada categoria
    dfs = []
    for stat_type, subdict in jugadores_dict.items():
        if isinstance(subdict, dict) and 'player' in subdict:
            df = subdict['player']
            if isinstance(df, pd.DataFrame) and not df.empty:
                df['stat_type'] = stat_type
                dfs.append(df)
    
    if dfs:
        # Usar solo standard como base principal
        jugadores = jugadores_dict['standard']['player'].copy()
        print(f"  Jugadores descargados: {len(jugadores)} filas")
        print(f"  Columnas: {jugadores.columns.tolist()[:8]}...")
    else:
        jugadores = pd.DataFrame()
except Exception as e:
    print(f"  Error: {e}")
    jugadores = pd.DataFrame()


# ─────────────────────────────────────────────
# 3. FILTRAR DATOS DE BELGRANO
# ─────────────────────────────────────────────

print("\nFiltrando datos de Belgrano...")

if not partidos.empty:
    belgrano_partidos = partidos[
        partidos.apply(lambda r: BELGRANO in str(r.values), axis=1)
    ]
    print(f"  Partidos de Belgrano: {len(belgrano_partidos)}")
else:
    belgrano_partidos = pd.DataFrame()

if not jugadores.empty:
    team_col = None
    for col in jugadores.columns:
        if 'squad' in str(col).lower() or 'team' in str(col).lower():
            team_col = col
            break

    if team_col:
        belgrano_jugadores = jugadores[
            jugadores[team_col].str.contains(BELGRANO, case=False, na=False)
        ]
        print(f"  Jugadores de Belgrano: {len(belgrano_jugadores)}")
    else:
        belgrano_jugadores = jugadores
        print("  Columna de equipo no encontrada, usando todos")
else:
    belgrano_jugadores = pd.DataFrame()

# ─────────────────────────────────────────────
# 4. GUARDAR EN SQLITE
# ─────────────────────────────────────────────

print("\nGuardando en base de datos SQLite...")
conn = sqlite3.connect(DB_PATH)

if not partidos.empty:
    partidos.to_sql("partidos", conn, if_exists="replace", index=False)
    print("  partidos guardada")

if not belgrano_partidos.empty:
    belgrano_partidos.to_sql("belgrano_partidos", conn, if_exists="replace", index=False)
    print("  belgrano_partidos guardada")

if not jugadores.empty:
    jugadores.to_sql("stats_jugadores", conn, if_exists="replace", index=False)
    print("  stats_jugadores guardada")

if not belgrano_jugadores.empty:
    belgrano_jugadores.to_sql("belgrano_jugadores", conn, if_exists="replace", index=False)
    print("  belgrano_jugadores guardada")

conn.close()

# ─────────────────────────────────────────────
# 5. EXPORTAR CSVs PARA POWER BI
# ─────────────────────────────────────────────

print("\nExportando CSVs...")
os.makedirs("data", exist_ok=True)

if not partidos.empty:
    partidos.to_csv("data/partidos.csv", index=False)
    print("  data/partidos.csv")

if not belgrano_partidos.empty:
    belgrano_partidos.to_csv("data/belgrano_partidos.csv", index=False)
    print("  data/belgrano_partidos.csv")

if not belgrano_jugadores.empty:
    belgrano_jugadores.to_csv("data/belgrano_jugadores.csv", index=False)
    print("  data/belgrano_jugadores.csv")

print("\n" + "="*50)
print("RESUMEN DEL ETL")
print("="*50)

if not belgrano_partidos.empty:
    print(f"  Partidos de Belgrano: {len(belgrano_partidos)}")

if not belgrano_jugadores.empty:
    print(f"  Jugadores analizados: {len(belgrano_jugadores)}")

print(f"\nBase de datos: {DB_PATH}")
print("CSVs en carpeta: data/")
print("\nETL completado!")
