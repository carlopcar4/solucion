from flask import Flask, request, jsonify
import os, shutil, subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

DIR_DECIDIM = BASE_DIR / 'decidim_base'

INSTANCIAS_DIR = BASE_DIR / 'instancias'
INSTANCIAS_DIR.mkdir(exist_ok=True)


app = Flask(__name__)

@app.route('/crear_instancia', methods=['POST'])
def crear_instancia():
    datos = request.get_json(force=True)
    nombre = datos.get('name').replace(' ','_').lower()
    puerto = datos.get('puerto_org')
    id = datos.get('id')
    colaboraciones = ",".join(datos.get('collaborations', []))
    servicios      = ",".join(datos.get('services', []))
    logo           = datos.get('logo', '')
    banner         = datos.get('banner', '')
    
    instancia_dir = INSTANCIAS_DIR / f"decidim_{nombre}"
    instancia_dir.mkdir(exist_ok=True)
    
    shutil.copytree(DIR_DECIDIM, instancia_dir, dirs_exist_ok=True)

    env_content = f"""\
NOMBRE={nombre}
ID={id}
PORT={puerto}
COLLABORATIONS={colaboraciones}
SERVICES={servicios}
LOGO={logo}
BANNER={banner}
"""

    env_path = instancia_dir / '.env'
    with open(env_path, 'w') as f:
        f.write(env_content)
        print(f"Archivo .env de {nombre} creado")
        cwd = os.getcwd()
    
    try:
        os.chdir(instancia_dir)
        print(f"[INFO] Ejecutar el docker-compose para {nombre}")
        result_build = subprocess.run(["docker-compose", "build", "--no-cache"], check=True, capture_output=True, text=True)
        print(f"[INFO] Docker Build STDOUT:\n{result_build.stdout}")
        if result_build.stderr:
            print(f"[WARN] {result_build.stderr}")

        result_up = subprocess.run(["docker-compose", "up"], check=True, capture_output=True, text=True)
        print(f"[INFO] Docker Up:\n{result_up.stdout}")
        if result_up.stderr:
            print(f"[WARN] {result_up.stderr}")

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Falló comando: {' '.join(e.cmd)}")
        print(f"[ERROR] Código salida: {e.returncode}")
        print(f"[ERROR] STDOUT:\n{e.stdout}")
        print(f"[ERROR] STDERR:\n{e.stderr}")
        return jsonify({
            "status": "error",
            "message": f"Fallo al inicializar instancia {nombre}",
            "cmd": e.cmd,
            "stdout": e.stdout,
            "stderr": e.stderr
        }), 500
    
    finally:
        os.chdir(cwd)



    return jsonify({
        "status": "ok",
        "message": f"Instancia '{nombre}' creada y corriendo en el puerto {puerto}"
    }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001, debug=True)