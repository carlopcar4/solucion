from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/crear_instancia', methods=['POST'])
def crear_instancia():
    data = request.get_json(force=True, silent=True) or {}
    app.logger.info(f"Recibido: {data}")
    return jsonify({"status": "ok"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001)