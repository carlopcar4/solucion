from flask import Flask, request, jsonify
import subprocess, os, shutil

app = Flask(__name__)

@app.route('/crear_instancia', methods=['POST'])
def crear_instancia():
    datos = request.get_json(force=True) or {}
    id = datos.get('id')
    puerto = datos.get('puerto_org')
    col = datos.get('collaborations', [])
    serv = datos.get('services', [])
    logo = datos.get('logo')
    banner = datos.get('banner')
    nombre = datos.get('name')

    os.makedirs("instancias", exist_ok=True)
    municipio = f"decidim_{nombre.replace(' ', '_').lower()}"
    ruta = os.path.join("instancias", municipio)
    os.makedirs(ruta, exist_ok=True)
    decidim = "/app/decidim_base"


    env = f"""\
NAME={nombre}
ID={id}
PORT={puerto}
COLLABORATIONS={', '.join(col)}
SERVICES={', '.join(serv)}
LOGO={logo}
BANNER={banner}
"""

    path_env = os.path.join(ruta, '.env')
    with open(path_env, 'w') as f:
        f.write(env)

    try:
        shutil.copytree(decidim, ruta, dirs_exist_ok=True)
        os.chdir(ruta)
        print(f"Construyendo imagen Docker para {municipio}...")
        build_result = subprocess.run(["docker-compose", "build"], check=True, capture_output=True, text=True)
        print("Docker Build Output:", build_result.stdout)
        result = subprocess.run(["docker-compose", "up", "-d"], check=True,
            capture_output=True,text=True)
        if build_result.stderr:
            print("Docker Build Error:", build_result.stderr)
        print(f"Desplegando instancia {municipio}...")
        result = subprocess.run(["docker-compose", "up", "-d"], check=True, capture_output=True, text=True)
        os.chdir("../..")
        return jsonify({"status": "ok", "message": f"instancia creada", "output": result.stdout}), 201
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Error al desplegar la instancia {nombre}",
            "details": e.stderr, "stdout": e.stdout}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001)
