# 📊 Práctica de Laboratorio: Análisis y Visualización de Calificaciones con Pandas y Matplotlib

**Tecnológico Nacional de México • Instituto Tecnológico de Ciudad Madero**  
**Departamento de Sistemas y Computación • Ingeniería en Sistemas Computacionales**  
**Asignatura:** Tópicos Avanzados de Programación  
**Docente:** Alejandro Estrada Padilla  
**Estudiante:** Luis Fernando Salas  

---

## 🎯 Objetivo de la Práctica
Cargar un archivo CSV en un DataFrame de Pandas, filtrar registros de forma condicional y vectorizada, construir columnas calculadas, resumir información estadística con `groupby` y comunicar los resultados de manera visual a través de tres gráficas especializadas con Matplotlib.

---

## 📂 Estructura del Repositorio

| Archivo / Carpeta | Descripción |
| :--- | :--- |
| **`practica_pandas.py`** | Script principal en Python que resuelve los 6 ejercicios de la práctica. |
| **`calificaciones_isc.csv`** | Dataset fuente con 288 registros (24 alumnos × 4 materias × 3 unidades). |
| **`promedios_alumnos.csv`** | Archivo CSV exportado con el ranking de calificaciones sin índice de Pandas. |
| **`promedio_materias.png`** | Gráfica de barras verticales del promedio por materia (escala 0 a 100). |
| **`histograma.png`** | Histograma de distribución de todas las calificaciones con línea vertical en 70. |
| **`tendencia_unidades.png`** | Gráfica multilínea que visualiza la tendencia de promedios por unidad y materia. |
| **`index.html`** | Página web interactiva y presentable del reporte de la práctica. |
| **`style.css`** | Hoja de estilos con diseño moderno, modo oscuro/claro y glassmorphism. |
| **`app.js`** | Lógica JavaScript interactiva con buscador de alumnos y métricas dinámicas. |
| **`data.json`** | Datos analíticos preprocesados para el funcionamiento offline del dashboard. |

---

## 🚀 Requisitos e Instalación

Para ejecutar la práctica de laboratorio localmente, asegúrate de contar con Python 3.10 o superior y las siguientes librerías:

```bash
pip install pandas matplotlib numpy
```

### Ejecución del Script de Python
```bash
python practica_pandas.py
```

### Visualización de la Página Web
Simplemente abre el archivo `index.html` en cualquier navegador web moderno o levanta un servidor local:
```bash
python -m http.server 8085
```
Luego visita `http://localhost:8085`.

---

## 📋 Resumen de Ejercicios y Resultados

### Ejercicio 1. Carga y Revisión
- Carga de `calificaciones_isc.csv` en un DataFrame llamado `df`.
- Impresión de primeras 5 filas (`df.head()`), dimensiones (288 filas × 7 columnas), tipos de datos y resumen estadístico descriptivo con `df[["calificacion", "asistencias"]].describe()`.
- **¿Por qué 288 registros y no 24?** Porque son 24 estudiantes cursando 4 materias distintas, y cada materia cuenta con 3 unidades de evaluación evaluadas individualmente:
  $$24 \times 4 \times 3 = 288 \text{ registros}$$

### Ejercicio 2. Filtros (sin modificar `df` y sin bucles)
1. **Solo el grupo A:** `len(df[df["grupo"] == "A"])` → **144 filas**.
2. **Unidades con calificación menor a 70:** `len(df[df["calificacion"] < 70])` → **122 filas**.
3. **Bases de datos, grupo B, calificación ≥ 80:** `len(...)` → **16 filas**.

### Ejercicio 3. Columna Calculada (`situacion`)
Se utilizó `np.where` de forma vectorizada:
```python
df["situacion"] = np.where(df["calificacion"] >= 70, "Aprobado", "Reprobado")
```
- **Aprobadas:** 166 unidades (57.64%)
- **Reprobadas:** 122 unidades (42.36%)

### Ejercicio 4. Resúmenes Estadísticos con `groupby`
- Promedio por materia:
  - **Redes:** 76.86
  - **Bases de datos:** 76.71
  - **Programación:** 71.38
  - **Matemáticas discretas:** 66.12 *(promedio más bajo)*
- Promedio por grupo y materia calculado para ambos grupos.
- Promedio por alumno exportado a `promedios_alumnos.csv` usando `.reset_index()` e `index=False`.
- Promedio general por unidad: Unidad 1 (76.45), Unidad 2 (74.04), Unidad 3 (67.81).

### Ejercicio 5. Gráficas con Matplotlib
- Todas las figuras se guardaron con `plt.savefig(..., dpi=300)` **antes** de invocaciones a `plt.show()` para asegurar imágenes nítidas y no vacías.
- Títulos, leyendas y nombres de ejes completamente rotulados.

### Ejercicio 6. Lectura e Interpretación de Resultados
1. **¿Qué materia quedó con el promedio más bajo?** Matemáticas discretas con **66.12 puntos**.
2. **¿El promedio de la unidad 3 es menor que el de 1 y 2?** **SÍ**; la Unidad 3 promedió **67.81**, cayendo frente a la Unidad 1 (76.45) y Unidad 2 (74.04).
3. **¿Cuántos alumnos quedan bajo 70 en su promedio general?** Un total de **4 alumnos** (Sebastian Herrera con 69.75, Luis Salas con 68.92, Carlos Hernandez con 68.83 y Ricardo Reyes con 68.00).

---

## 🛡️ Control de Calidad y Criterios Docentes
- [x] Sin reasignaciones erróneas de filtrado (`df["grupo"] = "A"` evitado).
- [x] `plt.savefig()` ejecutado antes de `plt.show()`.
- [x] `index=False` implementado en exportación de CSV.
- [x] `reset_index()` ejecutado tras `groupby` para preservar nombres y matrículas.
- [x] Sin bucles iterativos `for` en filtros o transformaciones.
