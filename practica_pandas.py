"""
Tecnológico Nacional de México - Instituto Tecnológico de Ciudad Madero
Departamento de Sistemas y Computación | Ingeniería en Sistemas Computacionales
Asignatura: Tópicos Avanzados de Programación
Docente: Alejandro Estrada Padilla
Estudiante: Luis Fernando Salas

Análisis y visualización de calificaciones con Pandas y Matplotlib
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuración visual de Matplotlib
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 0.8


# ==============================================================================
# Carga y revisión de datos
# ==============================================================================

# Lectura del archivo CSV
df = pd.read_csv("calificaciones_isc.csv")

# Primeras 5 filas
print("--- Primeras 5 filas del DataFrame ---")
print(df.head())
print()

# Número de filas y columnas
filas, columnas = df.shape
print("--- Dimensiones del dataset ---")
print(f"Filas: {filas} | Columnas: {columnas}")
print()

# Tipo de dato de cada columna
print("--- Tipo de dato de cada columna ---")
print(df.dtypes)
print()

# Resumen estadístico de calificacion y asistencias
print("--- Resumen estadístico (calificacion y asistencias) ---")
print(df[["calificacion", "asistencias"]].describe())
print()

# El archivo contiene 288 registros porque hay 24 alumnos en total cursando 4 materias
# (Programacion, Bases de datos, Redes, Matematicas discretas) y cada materia se evalúa
# en 3 unidades: 24 alumnos * 4 materias * 3 unidades = 288 registros.


# ==============================================================================
# Filtros condicionales
# ==============================================================================

# Solo el grupo A
filtro_grupo_a = df[df["grupo"] == "A"]
print(f"Grupo A: {len(filtro_grupo_a)} registros")

# Unidades con calificación menor a 70
filtro_menor_70 = df[df["calificacion"] < 70]
print(f"Calificaciones menores a 70: {len(filtro_menor_70)} registros")

# Bases de datos, del grupo B, con calificación de al menos 80
filtro_bd_b_80 = df[(df["materia"] == "Bases de datos") & (df["grupo"] == "B") & (df["calificacion"] >= 80)]
print(f"Bases de datos - Grupo B con calificación >= 80: {len(filtro_bd_b_80)} registros")
print()


# ==============================================================================
# Columna calculada: situacion
# ==============================================================================

# Se asigna Aprobado para calificación >= 70 y Reprobado para menores
df["situacion"] = np.where(df["calificacion"] >= 70, "Aprobado", "Reprobado")

print("--- Columna calculada 'situacion' ---")
print(df[["matricula", "nombre", "materia", "unidad", "calificacion", "situacion"]].head())
print()


# ==============================================================================
# Resúmenes estadísticos
# ==============================================================================

# Promedio de calificación por materia
print("--- Promedio por materia ---")
promedio_materia = df.groupby("materia")["calificacion"].mean().round(2)
print(promedio_materia)
print()

# Promedio por grupo y materia
print("--- Promedio por grupo y materia ---")
promedio_grupo_materia = df.groupby(["grupo", "materia"])["calificacion"].mean().round(2)
print(promedio_grupo_materia)
print()

# Promedio general de cada alumno, ordenado de mayor a menor
promedios_alumnos = df.groupby(["matricula", "nombre"])["calificacion"].mean().round(2).reset_index()
promedios_alumnos = promedios_alumnos.rename(columns={"calificacion": "promedio"})
promedios_alumnos = promedios_alumnos.sort_values(by="promedio", ascending=False)
print("--- Promedio general por alumno (Mayor a menor) ---")
print(promedios_alumnos.to_string(index=False))
print()

# Promedio general por unidad
print("--- Promedio general por unidad ---")
promedio_unidad = df.groupby("unidad")["calificacion"].mean().round(2)
print(promedio_unidad)
print()

# Unidades aprobadas y reprobadas
print("--- Conteo de unidades por situación ---")
conteo_situacion = df["situacion"].value_counts()
print(conteo_situacion)
print()

# Exportación del promedio por alumno conservando matrícula y nombre, sin índice
promedios_alumnos.to_csv("promedios_alumnos.csv", index=False)


# ==============================================================================
# Gráficas con Matplotlib
# ==============================================================================

# 1. Barras del promedio por materia (Eje vertical de 0 a 100)
fig1, ax1 = plt.subplots(figsize=(8, 5))
colores = ['#2563eb', '#059669', '#d97706', '#dc2626']
barras = ax1.bar(promedio_materia.index, promedio_materia.values, color=colores, width=0.55, edgecolor='#1e293b')
ax1.set_title("Promedio de Calificación por Materia", fontsize=13, fontweight='bold', pad=12)
ax1.set_xlabel("Materia", fontsize=10, labelpad=8)
ax1.set_ylabel("Calificación Promedio", fontsize=10, labelpad=8)
ax1.set_ylim(0, 100)
ax1.grid(axis='y', linestyle='--', alpha=0.7)

for barra in barras:
    yval = barra.get_height()
    ax1.text(barra.get_x() + barra.get_width() / 2, yval + 2, f"{yval:.1f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig("promedio_materias.png", dpi=300)
plt.close(fig1)

# 2. Histograma de todas las calificaciones con línea vertical en 70
fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.hist(df["calificacion"], bins=12, color='#3b82f6', edgecolor='#1e293b', alpha=0.85)
ax2.axvline(70, color='#ef4444', linestyle='--', linewidth=2.5, label='Aprobatorio (70)')
ax2.set_title("Distribución General de Calificaciones", fontsize=13, fontweight='bold', pad=12)
ax2.set_xlabel("Calificación", fontsize=10, labelpad=8)
ax2.set_ylabel("Frecuencia", fontsize=10, labelpad=8)
ax2.legend(loc='upper right')
ax2.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig("histograma.png", dpi=300)
plt.close(fig2)

# 3. Líneas del promedio por unidad, una línea por materia
fig3, ax3 = plt.subplots(figsize=(9, 5.5))
promedios_materia_unidad = df.groupby(["unidad", "materia"])["calificacion"].mean().unstack()

estilos = {
    'Programacion': {'color': '#2563eb', 'marker': 'o'},
    'Bases de datos': {'color': '#059669', 'marker': 's'},
    'Redes': {'color': '#d97706', 'marker': '^'},
    'Matematicas discretas': {'color': '#dc2626', 'marker': 'd'}
}

for materia in promedios_materia_unidad.columns:
    conf = estilos.get(materia, {'color': 'gray', 'marker': 'o'})
    ax3.plot(promedios_materia_unidad.index, promedios_materia_unidad[materia],
             label=materia, color=conf['color'], marker=conf['marker'],
             linewidth=2.5, markersize=7)

ax3.set_title("Tendencia del Promedio por Unidad", fontsize=13, fontweight='bold', pad=12)
ax3.set_xlabel("Unidad", fontsize=10, labelpad=8)
ax3.set_ylabel("Calificación Promedio", fontsize=10, labelpad=8)
ax3.set_xticks([1, 2, 3])
ax3.set_ylim(40, 100)
ax3.legend(title="Materia", loc='best')
ax3.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig("tendencia_unidades.png", dpi=300)
plt.close(fig3)


# ==============================================================================
# Lectura de resultados
# ==============================================================================

materia_menor = promedio_materia.idxmin()
promedio_menor = promedio_materia.min()

p_u1 = promedio_unidad.loc[1]
p_u2 = promedio_unidad.loc[2]
p_u3 = promedio_unidad.loc[3]
u3_menor = p_u3 < p_u1 and p_u3 < p_u2

alumnos_bajo_70 = len(promedios_alumnos[promedios_alumnos["promedio"] < 70])

print("--- Lectura de resultados ---")
print(f"Materia con el promedio más bajo: {materia_menor} ({promedio_menor:.2f})")
print(f"El promedio de la unidad 3 ({p_u3:.2f}) es menor al de las unidades 1 ({p_u1:.2f}) y 2 ({p_u2:.2f}): {'Sí' if u3_menor else 'No'}")
print(f"Alumnos con promedio general menor a 70: {alumnos_bajo_70}")
