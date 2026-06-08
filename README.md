# ⚽ Belgrano Analytics — Football Intelligence Platform

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

## 📌 Descripción

Plataforma de análisis de datos deportivos desarrollada para el Club Atlético Belgrano (Córdoba, Argentina), actual campeón de la Liga Profesional Argentina. El proyecto incluye un pipeline ETL completo, dashboard interactivo en Power BI, radar charts de jugadores estilo Wyscout y un módulo de scouting con scoring de compatibilidad.

---

## 🖼️ Capturas del Dashboard

### Rendimiento de Jugadores
![Rendimiento](screenshots/rendimiento_jugadores.png)

### Comparativa Liga
![Comparativa](screenshots/comparativa_liga.png)

### Perfil Belgrano + Radar Charts
![Perfil](screenshots/perfil_belgrano.png)

### Scouting - Fichajes
![Scouting](screenshots/scouting_fichajes.png)

---

## 🔍 Insights clave encontrados

1. **Belgrano gana sin tener la pelota** — Con solo 48.5% de posesión (por debajo del promedio de 50%), el equipo convirtió 33 goles, un 24% por encima del promedio de la liga (26.6). Perfil claro de equipo de transiciones rápidas.

2. **Franco Jara es el jugador más determinante** — 13 goles en 21 partidos como titular, el mejor ratio goles/partido del equipo. Veterano de 35 años que sostiene el ataque.

3. **Bryan Reyna es el más creativo** — 3 goles y 4 asistencias, el jugador con mayor impacto ofensivo combinado entre los menores de 30 años.

4. **Alta intensidad física** — 74 tarjetas amarillas, 11% por encima del promedio de la liga. Consistente con el estilo de presión alta del equipo.

5. **Cristian Pavón es el mejor candidato para fichar** — Jugador libre, 28 años, valor de mercado accesible. Score de compatibilidad 100/100 con el perfil táctico de Belgrano.

---

## 🛠️ Stack tecnológico

| Herramienta | Uso |
|---|---|
| Python 3.13 | ETL, scraping, visualizaciones, scouting |
| pandas | Limpieza y transformación de datos |
| ScraperFC | Extracción de datos de FBref |
| mplsoccer + matplotlib | Radar charts estilo Wyscout |
| SQLite | Base de datos local |
| Power BI | Dashboard interactivo |
| GitHub | Control de versiones |

---

## 📁 Estructura del proyecto

```
portfolio-belgrano/
│
├── 01_etl_belgrano.py        # ETL: descarga y carga de datos
├── 02_radar_jugadores.py     # Generacion de radar charts
├── 03_scouting.py            # Modulo de scouting con scoring
├── belgrano.db               # Base de datos SQLite
├── README.md                 # Este archivo
│
├── data/                     # Datos procesados
│   ├── belgrano_jugadores_limpio.csv
│   ├── stats_equipos_limpio.csv
│   └── scouting_candidatos.csv
│
├── visualizaciones/          # Radar charts generados
│   ├── radar_Franco_Jara.png
│   ├── radar_Bryan_Reyna.png
│   └── ...
│
└── screenshots/              # Capturas del dashboard
    ├── rendimiento_jugadores.png
    ├── comparativa_liga.png
    ├── perfil_belgrano.png
    └── scouting_fichajes.png
```

---

## ⚙️ Cómo reproducir el proyecto

### 1. Clonar el repositorio
```bash
git clone https://github.com/Laureano229/portfolio-belgrano.git
cd portfolio-belgrano
```

### 2. Instalar dependencias
```bash
pip install pandas ScraperFC matplotlib mplsoccer scikit-learn seaborn beautifulsoup4
```

### 3. Ejecutar ETL
```bash
python 01_etl_belgrano.py
```

### 4. Generar radar charts
```bash
python 02_radar_jugadores.py
```

### 5. Ejecutar módulo de scouting
```bash
python 03_scouting.py
```

### 6. Abrir dashboard
Abrir `dashboard-belgrano.pbix` en Power BI Desktop.

---

## 📊 Métricas del dataset

| Métrica | Valor |
|---|---|
| Temporada analizada | Liga Profesional 2024 |
| Jugadores de Belgrano | 35 |
| Equipos en la liga | 28 |
| Candidatos de scouting | 20 |
| Radar charts generados | 30 |

---

## 🎯 Módulo de Scouting

El sistema evalúa jugadores disponibles en el mercado usando un algoritmo de scoring que pondera:

- **Edad** (30pts) — Rango ideal 24-31 años
- **Disponibilidad** (35pts) — Libre > contrato por vencer > contrato vigente
- **Valor de mercado** (25pts) — Accesible para el presupuesto del club
- **Liga de origen** (10pts) — Adaptación cultural y deportiva

**Top candidatos identificados:**
- FW: Cristian Pavón (100pts), Mauro Icardi (90pts)
- MF: Hernán Pérez (90pts), Ramiro Carrera (90pts)

---

## 👤 Autor

**Laureano** — Analista de Datos  
📧 [Tu email]  
💼 [Tu LinkedIn]  
🌐 [Tu Upwork o Workana]
