# 📊 Análisis y Visualización de Calificaciones con Pandas y Matplotlib

**Tecnológico Nacional de México • Instituto Tecnológico de Ciudad Madero**  
**Departamento de Sistemas y Computación • Ingeniería en Sistemas Computacionales**  
**Asignatura:** Tópicos Avanzados de Programación  
**Docente:** Alejandro Estrada Padilla  
**Estudiante:** Luis Fernando Salas  

---

## Objetivo
Al terminar la práctica, el estudiante será capaz de cargar un archivo CSV en un DataFrame, filtrar registros, construir columnas, resumir información con groupby y comunicar los resultados con tres gráficas de Matplotlib.

---

## Estructura del Proyecto

| Archivo | Descripción |
| :--- | :--- |
| **`practica_pandas.py`** | Script en Python que procesa los datos, genera las tablas, gráficas y métricas. |
| **`calificaciones_isc.csv`** | Conjunto de datos con 288 registros (24 alumnos × 4 materias × 3 unidades). |
| **`promedios_alumnos.csv`** | Promedio general por alumno ordenado de mayor a menor con matrícula y nombre. |
| **`promedio_materias.png`** | Gráfica de barras verticales del promedio por materia de 0 a 100. |
| **`histograma.png`** | Histograma de distribución de calificaciones con línea en 70. |
| **`tendencia_unidades.png`** | Gráfica multilínea de promedios por unidad según cada materia. |
| **`index.html`** | Página web con los resultados, visualizaciones y tablas interactivas. |
| **`style.css`** | Hoja de estilos de la interfaz web. |
| **`app.js`** | Lógica de filtrado, búsqueda de alumnos e interactividad. |
| **`data.json`** | Datos analíticos preprocesados para funcionamiento local. |

---

## Resultados del Análisis

### Carga y Estructura
- Dimensiones: 288 filas y 7 columnas (`matricula`, `nombre`, `grupo`, `materia`, `unidad`, `calificacion`, `asistencias`).
- Calificación promedio global: **72.77** (mínima de 40, máxima de 100).
- Justificación: 24 alumnos cursando 4 materias con 3 unidades de evaluación = 288 registros.

### Filtros
- Grupo A: **144 registros**.
- Calificaciones menores a 70: **122 registros**.
- Bases de datos en Grupo B con calificación ≥ 80: **16 registros**.

### Situación Académica
- Aprobados (calificación ≥ 70): **166 unidades** (57.64%).
- Reprobados (calificación < 70): **122 unidades** (42.36%).

### Resúmenes Estadísticos
- Promedios por materia:
  - Redes: **76.86**
  - Bases de datos: **76.71**
  - Programación: **71.38**
  - Matemáticas discretas: **66.12**
- Promedios por unidad:
  - Unidad 1: **76.45**
  - Unidad 2: **74.04**
  - Unidad 3: **67.81**

### Lectura e Interpretación
- Materia con promedio más bajo: **Matemáticas discretas** (66.12 puntos).
- Comportamiento de la Unidad 3: **Sí**, su promedio (67.81) es menor al de las unidades 1 (76.45) y 2 (74.04).
- Alumnos con promedio menor a 70: **4 estudiantes** (Sebastian Herrera, Luis Salas, Carlos Hernandez y Ricardo Reyes).

---

## Ejecución Local
```bash
pip install pandas matplotlib numpy
python practica_pandas.py
```
Para ver la página web, abre `index.html` en el navegador.
