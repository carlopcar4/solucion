import os, shutil, subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="http://localhost:5173")

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "instancias"))

def slugy(name):
    return name.strip().lower().replace(" ", "_")

@app.route("/crear_instancia", methods=["POST"])
def crear_instancia():
    datos = request.get_json()
    id = datos.get("id")
    puerto = datos.get("puerto_org")
    col = datos.get("collaborations", [])
    serv = datos.get("services", [])
    logo = datos.get("logo", "")
    banner = datos.get("banner", "")
    nombre = datos.get("name")
    
    slug = slugy(nombre)
    nombre_mun = f"decidim_{slug}"
    ruta_mun = os.path.join(BASE_DIR, nombre_mun)
    
    if os.path.exists(ruta_mun):
        shutil.rmtree(ruta_mun)
    
    os.makedirs(ruta_mun, exist_ok=True)
    os.makedirs(os.path.join(ruta_mun, "data"), exist_ok=True)
    
    env_lines = [
        f"NAME={nombre}",
        f"ID={id}",
        f"PORT={puerto}",
        f"COLLABORATIONS={','.join(col)}",
        f"SERVICES={','.join(serv)}",
        f"LOGO={logo}",
        f"BANNER={banner}",
        "DB_HOST=db",
        f"DB_NAME={slug}",
        "DB_USERNAME=postgres",
        "DB_PASSWORD=postgres"
    ]
    with open(os.path.join(ruta_mun, ".env"), "w") as f:
        f.write("\n".join(env_lines))
    
    compose_content = f"""
version: '3.9'

services:
    decidim:
        image: decidim/decidim:latest
        env_file: .env
        ports:
            - "${{PORT}}:3000"
        volumes:
            - ./data:/app/public
        container_name: {nombre_mun}
        networks:
            - external_net
        
networks:
    external_net:
        external: true
        name: solucion_default
"""
    with open(os.path.join(ruta_mun, "docker-compose.yml"), "w") as f:
        f.write(compose_content.strip() + "\n")

    try:
        subprocess.run(
            ["docker-compose", "-f", os.path.join(ruta_mun, "docker-compose.yml"), "up", "--build", "-d"],
            check=True,
            cwd=ruta_mun
        )
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"docker-compose falló: {e}"}), 500

    return jsonify({"message": "Instancia creada correctamente", "path": ruta_mun}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4001)