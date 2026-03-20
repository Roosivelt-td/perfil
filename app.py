from flask import Flask, render_template, jsonify, request
from database import Database

app = Flask(__name__)
db = Database()

# --- RUTA PÚBLICA (PERFIL) ---
@app.route('/')
def profile():
    """
    Ruta principal que muestra el perfil profesional.
    """
    try:
        perfil_data = db.get_perfil()
        habilidades_data = db.get_habilidades()
        proyectos_data = db.get_proyectos()

        if not perfil_data:
            return "Error: No se encontró el perfil en la base de datos.", 500

        return render_template(
            'profile.html',
            perfil=perfil_data,
            habilidades=habilidades_data,
            proyectos=proyectos_data
        )
    except Exception as e:
        print(f"Error al renderizar el perfil: {e}")
        return "Ocurrió un error al cargar la página.", 500

# --- RUTA DE ADMINISTRACIÓN (DOMINIOS) ---
@app.route('/admin')
def admin_dominios():
    """
    Panel de administración para gestionar los dominios.
    """
    return render_template('admin_dominios.html')

# --- API ENDPOINTS (DOMINIOS) ---
@app.route('/api/dominios', methods=['GET'])
def get_dominios():
    try:
        dominios = db.get_all_dominios()
        return jsonify(dominios)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dominios', methods=['POST'])
def add_dominio():
    try:
        data = request.json
        if not data.get('nombre'):
            return jsonify({'error': 'El nombre es obligatorio'}), 400
        
        db.add_dominio(data)
        return jsonify({'message': 'Dominio agregado correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dominios/<int:id>', methods=['PUT'])
def update_dominio(id):
    try:
        data = request.json
        db.update_dominio(id, data)
        return jsonify({'message': 'Dominio actualizado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dominios/<int:id>', methods=['DELETE'])
def delete_dominio(id):
    try:
        db.delete_dominio(id)
        return jsonify({'message': 'Dominio eliminado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Asegúrate de configurar tus variables de entorno en .env o config.py
    app.run(debug=True, host='0.0.0.0', port=5000)
