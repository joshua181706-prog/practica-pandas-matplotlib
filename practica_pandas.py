# ==============================================================================
# TECNOLÓGICO NACIONAL DE MÉXICO - INSTITUTO TECNOLÓGICO DE CIUDAD MADERO
# Departamento de Sistemas y Computación | Ingeniería en Sistemas Computacionales
# Asignatura: Tópicos Avanzados de Programación
# Docente: Alejandro Estrada Padilla
# Práctica de laboratorio: Análisis y visualización de calificaciones con Pandas y Matplotlib
# Estudiante: Luis Fernando Salas
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuración estética general de Matplotlib
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

print("=" * 80)
print("PRÁCTICA DE LABORATORIO: ANÁLISIS Y VISUALIZACIÓN DE CALIFICACIONES")
print("=" * 80)

# ==============================================================================
# EJERCICIO 1. Carga y revisión
# ==============================================================================
print("\n" + "=" * 40)
print("EJERCICIO 1: CARGA Y REVISIÓN")
print("=" * 40)

# 1. Carga del archivo CSV
df = pd.read_csv("calificaciones_isc.csv")

# 2. Primeras 5 filas
print("\n--- Primeras 5 filas del DataFrame ---")
print(df.head())

# 3. Número de filas y de columnas
filas, columnas = df.shape
print(f"\n--- Dimensiones del dataset ---")
print(f"Filas: {filas} | Columnas: {columnas}")

# 4. Tipo de dato de cada columna
print("\n--- Tipos de datos por columna ---")
print(df.dtypes)

# 5. Resumen estadístico de calificacion y asistencias
print("\n--- Resumen estadístico (calificacion y asistencias) ---")
print(df[["calificacion", "asistencias"]].describe())

# COMENTARIO EXPLICATIVO (Requisito Ejercicio 1):
# ¿Por qué el archivo tiene 288 registros y no 24?
# Explicación: Existen 24 estudiantes matriculados en total (12 en el Grupo A y
# 12 en el Grupo B). Sin embargo, cada alumno cursa 4 materias distintas
# (Programacion, Bases de datos, Redes y Matematicas discretas), y a su vez
# cada materia es evaluada en 3 unidades independientes.
# Por consiguiente: 24 alumnos * 4 materias * 3 unidades = 288 registros en total.


# ==============================================================================
# EJERCICIO 2. Filtros
# ==============================================================================
print("\n" + "=" * 40)
print("EJERCICIO 2: FILTROS (SIN MODIFICAR df)")
print("=" * 40)

# Filtro 1: Solo el grupo A
filtro_grupo_a = df[df["grupo"] == "A"]
conteo_grupo_a = len(filtro_grupo_a)
print(f"\n1. Registros pertenecientes únicamente al Grupo A: {conteo_grupo_a} filas")

# Filtro 2: Unidades con calificación menor a 70 (Reprobadas)
filtro_menor_70 = df[df["calificacion"] < 70]
conteo_menor_70 = len(filtro_menor_70)
print(f"2. Unidades con calificación reprobatoria (< 70): {conteo_menor_70} filas")

# Filtro 3: Bases de datos, del grupo B, con calificación de al menos 80
filtro_bd_b_80 = df[(df["materia"] == "Bases de datos") & (df["grupo"] == "B") & (df["calificacion"] >= 80)]
conteo_bd_b_80 = len(filtro_bd_b_80)
print(f"3. Materia 'Bases de datos' en Grupo B con calificación >= 80: {conteo_bd_b_80} filas")


# ==============================================================================
# EJERCICIO 3. Columna calculada
# ==============================================================================
print("\n" + "=" * 40)
print("EJERCICIO 3: COLUMNA CALCULADA ('situacion')")
print("=" * 40)

# Creamos la columna 'situacion' usando np.where (vectorizado, sin ciclos)
df["situacion"] = np.where(df["calificacion"] >= 70, "Aprobado", "Reprobado")

print("\n--- Vista de la nueva columna calculada 'situacion' (primeras 8 filas) ---")
print(df[["matricula", "nombre", "materia", "unidad", "calificacion", "situacion"]].head(8))


# ==============================================================================
# EJERCICIO 4. Resúmenes
# ==============================================================================
print("\n" + "=" * 40)
print("EJERCICIO 4: RESÚMENES ESTADÍSTICOS")
print("=" * 40)

# 1. Promedio de calificación por materia
promedio_materia = df.groupby("materia")["calificacion"].mean().round(2)
print("\n1. Promedio de calificación por materia:")
print(promedio_materia)

# 2. Promedio por grupo y materia
promedio_grupo_materia = df.groupby(["grupo", "materia"])["calificacion"].mean().round(2)
print("\n2. Promedio de calificación por Grupo y Materia:")
print(promedio_grupo_materia)

# 3. Promedio general de cada alumno, ordenado de mayor a menor
promedios_alumnos = df.groupby(["matricula", "nombre"])["calificacion"].mean().round(2).reset_index()
promedios_alumnos = promedios_alumnos.rename(columns={"calificacion": "promedio"})
promedios_alumnos = promedios_alumnos.sort_values(by="promedio", ascending=False)
print("\n3. Promedio general por alumno (Ordenado de mayor a menor):")
print(promedios_alumnos.to_string(index=False))

# 4. Promedio general por unidad, con todas las materias juntas
promedio_unidad = df.groupby("unidad")["calificacion"].mean().round(2)
print("\n4. Promedio general por unidad:")
print(promedio_unidad)

# 5. Cuántas unidades salieron aprobadas y cuántas reprobadas
conteo_situacion = df["situacion"].value_counts()
print("\n5. Conteo global de unidades aprobadas y reprobadas:")
print(conteo_situacion)

# Exportación a promedios_alumnos.csv sin guardar el índice de pandas
promedios_alumnos.to_csv("promedios_alumnos.csv", index=False)
print("\n>>> Archivo 'promedios_alumnos.csv' exportado con éxito (sin índice de Pandas).")


# ==============================================================================
# EJERCICIO 5. Gráficas con Matplotlib
# ==============================================================================
print("\n" + "=" * 40)
print("EJERCICIO 5: GENERACIÓN DE GRÁFICAS")
print("=" * 40)

# --- Gráfica 1: Barras del promedio por materia (Eje vertical de 0 a 100) ---
fig1, ax1 = plt.subplots(figsize=(8, 5))
colores_materias = ['#2563eb', '#059669', '#d97706', '#dc2626']
barras = ax1.bar(promedio_materia.index, promedio_materia.values, color=colores_materias, width=0.55, edgecolor='#1e293b', linewidth=1)
ax1.set_title("Promedio de Calificación por Materia", fontsize=14, fontweight='bold', pad=15)
ax1.set_xlabel("Materia", fontsize=11, labelpad=10)
ax1.set_ylabel("Promedio de Calificación", fontsize=11, labelpad=10)
ax1.set_ylim(0, 100)
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# Etiquetas de valores sobre cada barra
for barra in barras:
    yval = barra.get_height()
    ax1.text(barra.get_x() + barra.get_width() / 2, yval + 2, f"{yval:.1f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
# REGLA: Llamar a savefig ANTES de show
plt.savefig("promedio_materias.png", dpi=300)
print(">>> Gráfica 1 guardada: promedio_materias.png")
# plt.show()  # En entornos desatendidos o scripts de entrega puede invocarse o comentarse
plt.close(fig1)

# --- Gráfica 2: Histograma de todas las calificaciones con línea vertical en 70 ---
fig2, ax2 = plt.subplots(figsize=(8, 5))
n, bins, patches = ax2.hist(df["calificacion"], bins=12, color='#3b82f6', edgecolor='#1e293b', alpha=0.85)
ax2.axvline(70, color='#ef4444', linestyle='--', linewidth=2.5, label='Mínimo Aprobatorio (70)')
ax2.set_title("Distribución de Todas las Calificaciones Registradas", fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel("Calificación", fontsize=11, labelpad=10)
ax2.set_ylabel("Frecuencia (Cantidad de Registros)", fontsize=11, labelpad=10)
ax2.legend(loc='upper right', frameon=True)
ax2.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig("histograma.png", dpi=300)
print(">>> Gráfica 2 guardada: histograma.png")
plt.close(fig2)

# --- Gráfica 3: Líneas de promedio por unidad, una línea por materia ---
fig3, ax3 = plt.subplots(figsize=(9, 5.5))
promedios_materia_unidad = df.groupby(["unidad", "materia"])["calificacion"].mean().unstack()

estilos_lineas = {
    'Programacion': {'color': '#2563eb', 'marker': 'o', 'lw': 2.5},
    'Bases de datos': {'color': '#059669', 'marker': 's', 'lw': 2.5},
    'Redes': {'color': '#d97706', 'marker': '^', 'lw': 2.5},
    'Matematicas discretas': {'color': '#dc2626', 'marker': 'd', 'lw': 2.5}
}

for materia in promedios_materia_unidad.columns:
    estilo = estilos_lineas.get(materia, {'color': 'gray', 'marker': 'o', 'lw': 2})
    ax3.plot(promedios_materia_unidad.index, promedios_materia_unidad[materia],
             label=materia, color=estilo['color'], marker=estilo['marker'],
             linewidth=estilo['lw'], markersize=7)

ax3.set_title("Tendencia del Promedio por Unidad según Materia", fontsize=14, fontweight='bold', pad=15)
ax3.set_xlabel("Unidad de Evaluación", fontsize=11, labelpad=10)
ax3.set_ylabel("Calificación Promedio", fontsize=11, labelpad=10)
ax3.set_xticks([1, 2, 3])
ax3.set_ylim(40, 100)
ax3.legend(title="Materias", loc='best', frameon=True)
ax3.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig("tendencia_unidades.png", dpi=300)
print(">>> Gráfica 3 guardada: tendencia_unidades.png")
plt.close(fig3)


# ==============================================================================
# EJERCICIO 6. Lectura de resultados e interpretación
# ==============================================================================
print("\n" + "=" * 40)
print("EJERCICIO 6: LECTURA DE RESULTADOS")
print("=" * 40)

# Cálculo automático de las respuestas basado en los datos reales del DataFrame:
materia_mas_baja = promedio_materia.idxmin()
valor_mas_bajo = promedio_materia.min()

prom_u1 = promedio_unidad.loc[1]
prom_u2 = promedio_unidad.loc[2]
prom_u3 = promedio_unidad.loc[3]
u3_es_menor = prom_u3 < prom_u1 and prom_u3 < prom_u2

alumnos_bajo_70 = len(promedios_alumnos[promedios_alumnos["promedio"] < 70])

interpretacion = f"""
================================================================================
INTERPRETACIÓN Y ANÁLISIS DE RESULTADOS (EJERCICIO 6)
================================================================================
1. ¿Qué materia quedó con el promedio más bajo?
   - La materia con el promedio más bajo es '{materia_mas_baja}' con una media de {valor_mas_bajo:.2f} puntos.
   
2. ¿El promedio general de la unidad 3 es menor que el de las unidades 1 y 2?
   - {'SÍ' if u3_es_menor else 'NO'}, el promedio de la Unidad 3 ({prom_u3:.2f}) {'es menor' if u3_es_menor else 'no es menor'} comparado con la Unidad 1 ({prom_u1:.2f}) y la Unidad 2 ({prom_u2:.2f}).
   Se observa una tendencia a la baja en la Unidad 3, atribuible al aumento de complejidad de los temas finales del semestre.

3. ¿Cuántos alumnos quedan bajo 70 en su promedio general?
   - Un total de {alumnos_bajo_70} alumno(s) quedaron por debajo del umbral aprobatorio de 70 en su promedio general (de los 24 alumnos evaluados).
================================================================================
"""

print(interpretacion)
