@app.route("/crear_instancia", methods=["POST"])
def crear_instancia():
    datos = request.get_json()
    id       = datos.get("id")
    puerto   = datos.get("puerto_org")
    col      = datos.get("collaborations", [])
    serv     = datos.get("services", [])
    logo     = datos.get("logo", "")
    banner   = datos.get("banner", "")
    nombre   = datos.get("name")

    slug       = slugy(nombre)
    nombre_mun = f"decidim_{slug}"
    ruta_mun   = os.path.join(BASE_DIR, nombre_mun)

    # 1) Si ya existía, lo borramos
    if os.path.exists(ruta_mun):
        shutil.rmtree(ruta_mun)

    # 2) Creamos carpeta principal y subcarpeta "data"
    os.makedirs(ruta_mun, exist_ok=True)
    os.makedirs(os.path.join(ruta_mun, "data"), exist_ok=True)

    # 3) Copiar tarea Rake a lib/tasks
    src_rake   = "/app/gems/decidim_tasks/crear_instancia.rake"
    dest_tasks = os.path.join(ruta_mun, "lib", "tasks")
    os.makedirs(dest_tasks, exist_ok=True)
    shutil.copy(src_rake, os.path.join(dest_tasks, "crear_instancia.rake"))

    # 4) Copiar seeds vacío a db/seeds.rb
    src_seeds  = "/app/gems/decidim_tasks/seeds_empty.rb"
    dest_db    = os.path.join(ruta_mun, "db")
    os.makedirs(dest_db, exist_ok=True)
    shutil.copy(src_seeds, os.path.join(dest_db, "seeds.rb"))

    # 5) Copiar entrypoint.sh y darle permiso de ejecución
    src_entry  = "/app/entrypoint.sh"
    dest_entry = os.path.join(ruta_mun, "entrypoint.sh")
    shutil.copy(src_entry, dest_entry)
    os.chmod(dest_entry, 0o755)

    # 6) Ahora creamos el .env
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

    # 7) Generar el docker-compose.yml para la instancia
    compose_content = f"""
version: '3.9'

services:
    decidim:
        image: decidim/decidim:latest
        env_file: .env
        working_dir: /app
        volumes:
            - ./data:/app/public
            - ./entrypoint.sh:/app/entrypoint.sh
            - ./db/seeds.rb:/app/db/seeds.rb
            - ./lib/tasks/crear_instancia.rake:/app/lib/tasks/crear_instancia.rake
        entrypoint: ["/app/entrypoint.sh"]
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

    # 8) Levantar la instancia con Docker Compose
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
