# from flask import Flask, request, jsonify
# import subprocess, os, shutil

# app = Flask(__name__)

# @app.route('/crear_instancia', methods=['POST'])
# def crear_instancia():
#     datos = request.get_json(force=True) or {}
#     id = datos.get('id')
#     puerto = datos.get('puerto_org')
#     col = datos.get('collaborations', [])
#     serv = datos.get('services', [])
#     logo = datos.get('logo')
#     banner = datos.get('banner')
#     nombre = datos.get('name')

#     os.makedirs("instancias", exist_ok=True)
#     municipio = f"decidim_{nombre.replace(' ', '_').lower()}"
#     ruta = os.path.join("instancias", municipio)
#     os.makedirs(ruta, exist_ok=True)
#     decidim = "/app/decidim_base"


#     env = f"""\
# NAME={nombre}
# ID={id}
# PORT={puerto}
# COLLABORATIONS={', '.join(col)}
# SERVICES={', '.join(serv)}
# LOGO={logo}
# BANNER={banner}
# """

#     path_env = os.path.join(ruta, '.env')
#     with open(path_env, 'w') as f:
#         f.write(env)

#     try:
#         shutil.copytree(decidim, ruta, dirs_exist_ok=True)
#         os.chdir(ruta)
#         print(f"Construyendo imagen Docker para {municipio}...")
#         build_result = subprocess.run(["docker-compose", "build"], check=True, capture_output=True, text=True)
#         print("Docker Build Output:", build_result.stdout)
#         result = subprocess.run(["docker-compose", "up", "-d"], check=True,
#             capture_output=True,text=True)
#         if build_result.stderr:
#             print("Docker Build Error:", build_result.stderr)
#         print(f"Desplegando instancia {municipio}...")
#         result = subprocess.run(["docker-compose", "up", "-d"], check=True, capture_output=True, text=True)
#         os.chdir("../..")
#         return jsonify({"status": "ok", "message": f"instancia creada", "output": result.stdout}), 201
#     except subprocess.CalledProcessError as e:
#         os.chdir("../..")
#         return jsonify({"status": "error", "message": f"Error al desplegar la instancia {nombre}",
#             "details": e.stderr, "stdout": e.stdout}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=4001)

from flask import Flask, request, jsonify
import subprocess, os, shutil # Importar shutil y subprocess si no están

app = Flask(__name__)

# Asegúrate de que los directorios base existan al iniciar la aplicación
# Estos son relativos a donde se ejecuta el Dockerfile de Flask
BASE_TEMPLATE_DIR = '/app/decidim_base' # Ruta absoluta dentro del contenedor Flask
INSTANCES_DIR = '/app/instancias' # Ruta absoluta dentro del contenedor Flask

# Crea los directorios si no existen al inicio del script
os.makedirs(INSTANCES_DIR, exist_ok=True)

@app.route('/crear_instancia', methods=['POST'])
def crear_instancia():
    datos = request.get_json(force=True) or {}
    id = datos.get('id') # Este ID probablemente no es necesario para Decidim.create
    puerto = datos.get('puerto_org')
    col = datos.get('collaborations', [])
    serv = datos.get('services', [])
    logo = datos.get('logo')
    banner = datos.get('banner')
    nombre = datos.get('name')

    if not all([nombre, puerto]): # Añadir 'nombre' a la validación
        print(f"ERROR: Datos faltantes: nombre={nombre}, puerto={puerto}")
        return jsonify({"error": "Faltan datos de la instancia (nombre o puerto_org)"}), 400

    municipio = f"decidim_{nombre.replace(' ', '_').lower()}"
    ruta_instancia = os.path.join(INSTANCES_DIR, municipio) # Usar ruta_instancia
    
    # Asegúrate de que el directorio de la instancia se cree antes de copiar
    os.makedirs(ruta_instancia, exist_ok=True)

    # Contenido del .env
    env_content = f"""\
NOMBRE={nombre}
ID={id}
PORT={puerto}
COLLABORATIONS={', '.join(col)}
SERVICES={', '.join(serv)}
LOGO={logo}
BANNER={banner}
"""
    path_env = os.path.join(ruta_instancia, '.env')
    with open(path_env, 'w') as f:
        f.write(env_content)
    print(f"DEBUG: Archivo .env creado en: {path_env}")

    # Necesitas guardar el directorio actual para volver a él
    original_cwd = os.getcwd()
    
    try:
        # Copiar los archivos de la plantilla (Dockerfile, docker-compose.yml, etc.)
        print(f"DEBUG: Copiando plantilla de {BASE_TEMPLATE_DIR} a {ruta_instancia}")
        shutil.copytree(BASE_TEMPLATE_DIR, ruta_instancia, dirs_exist_ok=True)
        
        # Cambiar al directorio de la instancia para ejecutar docker-compose
        os.chdir(ruta_instancia)
        print(f"DEBUG: Cambiado al directorio: {os.getcwd()}")

        print(f"DEBUG: Ejecutando 'docker-compose build' para {municipio}...")
        build_result = subprocess.run(
            ["docker-compose", "build"],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"DEBUG: Docker Build STDOUT:\n{build_result.stdout}")
        if build_result.stderr:
            print(f"DEBUG: Docker Build STDERR:\n{build_result.stderr}")

        print(f"DEBUG: Ejecutando 'docker-compose up -d' para {municipio}...")
        up_result = subprocess.run( # Renombra 'result' a 'up_result' para mayor claridad
            ["docker-compose", "up", "-d"],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"DEBUG: Docker Up STDOUT:\n{up_result.stdout}")
        if up_result.stderr:
            print(f"DEBUG: Docker Up STDERR:\n{up_result.stderr}")

        os.chdir(original_cwd) # Volver al directorio original de Flask
        print(f"DEBUG: Vuelto al directorio original: {os.getcwd()}")
        
        return jsonify({
            "status": "ok",
            "message": f"Instancia {nombre} creada y levantada correctamente.",
            "build_output": build_result.stdout,
            "deploy_output": up_result.stdout # Usar up_result
        }), 201

    except subprocess.CalledProcessError as e:
        # Asegúrate de volver al directorio original incluso si hay un error
        os.chdir(original_cwd) 
        print(f"ERROR: Docker Compose falló para la instancia {nombre}.")
        print(f"ERROR: Comando: {' '.join(e.cmd)}")
        print(f"ERROR: Código de salida: {e.returncode}")
        print(f"ERROR: STDOUT del fallo:\n{e.stdout}")
        print(f"ERROR: STDERR del fallo:\n{e.stderr}")
        return jsonify({
            "status": "error",
            "message": f"Error al desplegar la instancia {nombre}",
            "details": e.stderr,
            "stdout": e.stdout,
            "command": ' '.join(e.cmd),
            "returncode": e.returncode
        }), 500
    except Exception as e:
        # Asegúrate de volver al directorio original incluso si hay un error
        os.chdir(original_cwd) 
        print(f"ERROR: Se produjo un error inesperado al crear la instancia {nombre}: {e}")
        return jsonify({"error": f"Error interno del servidor: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001, debug=False) # Deja debug en False en producción