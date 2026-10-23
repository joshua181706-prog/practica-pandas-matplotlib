import pandas as pd
import numpy as np

np.random.seed(42)

estudiantes = [
    # Grupo A (12 alumnos)
    ("ISC240100", "Ana Lopez", "A"),
    ("ISC240101", "Carlos Hernandez", "A"),
    ("ISC240102", "Maria Garcia", "A"),
    ("ISC240103", "Juan Martinez", "A"),
    ("ISC240104", "Sofia Rodriguez", "A"),
    ("ISC240105", "Luis Salas", "A"),
    ("ISC240106", "Valeria Gomez", "A"),
    ("ISC240107", "Jorge Ramirez", "A"),
    ("ISC240108", "Fernanda Diaz", "A"),
    ("ISC240109", "Diego Torres", "A"),
    ("ISC240110", "Camila Morales", "A"),
    ("ISC240111", "Alejandro Castro", "A"),
    # Grupo B (12 alumnos)
    ("ISC240112", "Paola Ortiz", "B"),
    ("ISC240113", "Daniel Silva", "B"),
    ("ISC240114", "Andrea Vargas", "B"),
    ("ISC240115", "Mateo Mendoza", "B"),
    ("ISC240116", "Natalia Cruz", "B"),
    ("ISC240117", "Ricardo Reyes", "B"),
    ("ISC240118", "Elena Morales", "B"),
    ("ISC240119", "Gabriel Jimenez", "B"),
    ("ISC240120", "Ximena Gutierrez", "B"),
    ("ISC240121", "Emilio Ruiz", "B"),
    ("ISC240122", "Mariana Chavez", "B"),
    ("ISC240123", "Sebastian Herrera", "B"),
]

materias = ["Programacion", "Bases de datos", "Redes", "Matematicas discretas"]
unidades = [1, 2, 3]

filas = []

for matricula, nombre, grupo in estudiantes:
    for materia in materias:
        for unidad in unidades:
            if matricula == "ISC240100" and materia == "Programacion":
                if unidad == 1:
                    calif, asist = 55, 5
                elif unidad == 2:
                    calif, asist = 54, 5
                else:
                    calif, asist = 50, 8
            else:
                # Modulación realista de notas según materia y unidad
                base_media = 74
                if materia == "Matematicas discretas":
                    base_media = 68
                elif materia == "Bases de datos":
                    base_media = 80
                elif materia == "Programacion":
                    base_media = 72
                elif materia == "Redes":
                    base_media = 76

                # La unidad 3 suele ser más demandante
                if unidad == 3:
                    base_media -= 5
                elif unidad == 1:
                    base_media += 2

                calif = int(np.clip(np.random.normal(loc=base_media, scale=14), 40, 100))
                asist = int(np.random.choice([5, 6, 7, 8, 9, 10], p=[0.1, 0.15, 0.25, 0.3, 0.15, 0.05]))
                
            filas.append({
                "matricula": matricula,
                "nombre": nombre,
                "grupo": grupo,
                "materia": materia,
                "unidad": unidad,
                "calificacion": calif,
                "asistencias": asist
            })

df = pd.DataFrame(filas)
df.to_csv(r"C:\Users\Luis Fernando Salas\.gemini\antigravity-ide\scratch\practica_pandas_web\calificaciones_isc.csv", index=False)
print(f"Generado exitosamente: {len(df)} filas.")
print(df.head(10))
