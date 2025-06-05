import os, shutil, subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "instancias"))

def slugy(name):
    return name.strip().lower().replace(" ", "_")

@app.route("/crear_instancia", methods=["POST"])
def crear_instancia():
    datos   = request.get_json()
    id      = datos.get("id")
    puerto  = datos.get("puerto_org")
    col     = datos.get("collaborations", [])
    serv    = datos.get("services", [])
    logo    = datos.get("logo", "")
    banner  = datos.get("banner", "")
    nombre  = datos.get("name")

    slug       = slugy(nombre)
    nombre_mun = f"decidim_{slug}"
    ruta_mun   = os.path.join(BASE_DIR, nombre_mun)

    if os.path.exists(ruta_mun):
        shutil.rmtree(ruta_mun)

    os.makedirs(ruta_mun, exist_ok=True)


    # 4) Copiar seeds vacío a ruta_mun/db/seeds.rb
    src_seeds  = "/app/gems/decidim_tasks/seeds_empty.rb"
    dest_db    = os.path.join(ruta_mun, "db")
    os.makedirs(dest_db, exist_ok=True)
    shutil.copy(src_seeds, os.path.join(dest_db, "seeds.rb"))

    # 5) Copiar entrypoint.sh y darle permiso de ejecución (chmod 755)
    # src_entry  = "/app/entrypoint.sh"                    # archivo en el contenedor Flask
    # dest_entry = os.path.join(ruta_mun, "entrypoint.sh") # destino en la instancia
    # shutil.copy(src_entry, dest_entry)
    # os.chmod(dest_entry, 0o755)  # permiso: propietario=rwx, grupo=r-x, otros=r-x

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
        working_dir: /app
        volumes:
            - ./db/seeds.rb:/app/db/seeds.rb
        container_name: {nombre_mun}
        networks:
            - external_net
        ports:
            - "${{PORT}}:3000"

networks:
    external_net:
        external: true
        name: solucion_default
"""
    with open(os.path.join(ruta_mun, "docker-compose.yml"), "w") as f:
        f.write(compose_content.strip() + "\n")

    # -----------------------
    # 8) Ejecutar docker-compose up -d en la carpeta de la instancia
    try:
        subprocess.run(
            ["docker-compose",
                "-f", os.path.join(ruta_mun, "docker-compose.yml"),
                "up", "--build", "-d"],
            check=True,
            cwd=ruta_mun
        )
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"docker-compose falló: {e}"}), 500

    return jsonify({"message": "Instancia creada correctamente", "path": ruta_mun}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4001)
