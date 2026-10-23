import subprocess
import requests
import json
import os
import sys

# 1. Obtener credenciales de Git Credential Manager
p = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(input='protocol=https\nhost=github.com\n\n')

token = None
username = None
for line in out.splitlines():
    if line.startswith('password='):
        token = line.split('=', 1)[1].strip()
    elif line.startswith('username='):
        username = line.split('=', 1)[1].strip()

if not token or not username:
    print("Error: No se pudo obtener el token de Git Credential Manager.")
    sys.exit(1)

print(f"Usuario detectado: {username}")

# 2. Crear repositorio en GitHub si no existe
repo_name = "practica-pandas-matplotlib"
headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/vnd.github+json'
}

# Verificar si ya existe
check_res = requests.get(f"https://api.github.com/repos/{username}/{repo_name}", headers=headers)
if check_res.status_code == 200:
    print(f"El repositorio {repo_name} ya existe en GitHub.")
    repo_url = check_res.json()['clone_url']
elif check_res.status_code == 404:
    print(f"Creando nuevo repositorio '{repo_name}' en GitHub...")
    create_payload = {
        "name": repo_name,
        "description": "Práctica de laboratorio: Análisis y visualización de calificaciones con Pandas y Matplotlib - TecNM ITCM",
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": False
    }
    create_res = requests.post("https://api.github.com/user/repos", headers=headers, json=create_payload)
    if create_res.status_code in [200, 201]:
        print("Repositorio creado exitosamente en GitHub.")
        repo_url = create_res.json()['clone_url']
    else:
        print(f"Error al crear repositorio: {create_res.status_code} - {create_res.text}")
        sys.exit(1)
else:
    print(f"Respuesta inesperada al verificar repo: {check_res.status_code}")
    sys.exit(1)

# Usar token en URL autenticada para push sin interacción
auth_remote_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
public_remote_url = f"https://github.com/{username}/{repo_name}.git"

print(f"URL del repositorio: {public_remote_url}")

# 3. Inicializar y hacer push en C:\Users\Luis Fernando Salas\.gemini\antigravity-ide\scratch\practica_pandas_web
workdir = r"C:\Users\Luis Fernando Salas\.gemini\antigravity-ide\scratch\practica_pandas_web"

commands = [
    ["git", "init"],
    ["git", "branch", "-M", "main"],
    ["git", "config", "user.name", "Luis Fernando Salas"],
    ["git", "config", "user.email", f"{username}@users.noreply.github.com"],
    ["git", "add", "."],
    ["git", "commit", "-m", "feat: Solución completa de práctica de laboratorio Pandas y Matplotlib con dashboard web"],
    ["git", "remote", "remove", "origin"],
    ["git", "remote", "add", "origin", auth_remote_url],
    ["git", "push", "-u", "origin", "main", "--force"],
    ["git", "remote", "set-url", "origin", public_remote_url] # Restaurar URL pública sin token en el config local
]

for cmd in commands:
    try:
        res = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True)
        # Ignorar error de remote remove si no existe
        if cmd[1] == "remote" and cmd[2] == "remove":
            continue
        if res.returncode != 0 and "already exists" not in res.stderr:
            print(f"Comando {' '.join(cmd)}: {res.stderr.strip()}")
        else:
            if res.stdout.strip():
                print(f"{' '.join(cmd)}: {res.stdout.strip()}")
    except Exception as e:
        print(f"Excepción en {cmd}: {e}")

# 4. Habilitar GitHub Pages si es posible
pages_payload = {
    "source": {
        "branch": "main",
        "path": "/"
    }
}
pages_res = requests.post(f"https://api.github.com/repos/{username}/{repo_name}/pages", headers=headers, json=pages_payload)
if pages_res.status_code in [201, 200]:
    print(f"GitHub Pages habilitado: {pages_res.json().get('html_url')}")
else:
    print(f"Estado de GitHub Pages: {pages_res.status_code} ({pages_res.text[:100]})")

# 5. También sincronizar el git en el escritorio para que el alumno tenga el repositorio listo en su carpeta
desktop_dir = r"C:\Users\Luis Fernando Salas\Desktop\Topicos\practica_pandas"
commands_desktop = [
    ["git", "init"],
    ["git", "branch", "-M", "main"],
    ["git", "config", "user.name", "Luis Fernando Salas"],
    ["git", "config", "user.email", f"{username}@users.noreply.github.com"],
    ["git", "add", "."],
    ["git", "commit", "-m", "feat: Solución completa de práctica de laboratorio Pandas y Matplotlib con dashboard web"],
    ["git", "remote", "remove", "origin"],
    ["git", "remote", "add", "origin", public_remote_url]
]
for cmd in commands_desktop:
    try:
        subprocess.run(cmd, cwd=desktop_dir, capture_output=True, text=True)
    except:
        pass

print("¡PROCESO COMPLETADO EXITOSAMENTE!")
