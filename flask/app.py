from flask import Flask, request, jsonify
import subprocess, os

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
    municipio = f"decidim_{nombre.replace(' ','_').lower()}"
    
    ruta = os.path.join("instancias", municipio)
    os.makedirs(ruta, exist_ok=True)

    env = f"""\
NAME={nombre}
ID={id}
PORT={puerto}
COLLABORATIONS={', '.join(col)}
SERVICES={', '.join(serv)}
LOGO={logo}
BANNER={banner}
"""

    docker_compose = f"""
version: '3.9'

services:
    pg:
        image: postgres:15
        environment:
            POSTGRES_USER: postgres
            POSTGRES_PASSWORD: postgres
        volumes:
            - pg-data:/var/lib/postgresql/data
        networks:
            - decidim_net

    app:
        image: decidim/decidim:latest
        env_file: ./.env
        working_dir: /app
        volumes:
            - ./flask/instancias/decidim_{nombre.replace(' ','_').lower()}:/app
            - bundle:/usr/local/bundle
            - node_modules:/app/node_modules
        environment:
            - PORT=3000
            - DATABASE_HOST=pg
            - DATABASE_USERNAME=postgres
            - DATABASE_PASSWORD=postgres
            - RAILS_ENV=development
        ports:
            - "{puerto}:3000"
        networks:
            - decidim_net
        depends_on:
            - pg
        command: bundle exec puma

volumes:
    pg-data: 
    node_modules: 
    bundle: 

networks:
    decidim_net:
"""

    path_env = os.path.join(ruta, '.env')
    with open(path_env, 'w') as f:
        f.write(env)

    path_docker = os.path.join(ruta, 'docker-compose.yml')
    with open(path_docker, 'w') as f:
        f.write(docker_compose)

    try:
        os.chdir(ruta)
        subprocess.run(["docker-compose", "up", "-d"], check=True, capture_output=True, text=True)
        os.chdir(os.path.dirname(os.path.abspath(__file__))) # Asegúrate de volver al directorio original
        print(f"Instancia {nombre} desplegada con éxito.")
        return jsonify({"status": "ok", "message": f"Instancia {nombre} creada y desplegada."}), 201
    except subprocess.CalledProcessError as e:
        os.chdir(os.path.dirname(os.path.abspath(__file__))) # Asegúrate de volver al directorio original
        print(f"Error al desplegar la instancia {nombre}: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return jsonify({"status": "error", "message": f"Error al desplegar la instancia {nombre}", "details": e.stderr}), 500

    # return jsonify({"status": "ok"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001)