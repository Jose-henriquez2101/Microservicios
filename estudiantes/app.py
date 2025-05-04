from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': os.getenv('DB_HOST', 'db'),
    'database': os.getenv('DB_NAME', 'microservicios'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

def get_db_connection():
    conn = psycopg2.connect(**db_config)
    return conn
#crear estudiante
@app.route('/estudiantes', methods=['POST'])
def crear_estudiante():
    data = request.get_json()
    rut = data['rut']
    nombre = data['nombre']
    edad = data['edad']
    curso = data['curso']
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO estudiantes (rut, nombre, edad, curso) VALUES (%s, %s, %s, %s)',
        (rut, nombre, edad, curso)
    )
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({'mensaje': 'Estudiante creado exitosamente'}), 201
#obtener todos los estudiantes
@app.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM estudiantes')
    estudiantes = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify(estudiantes)
#obtener estudiantes por rut
@app.route('/estudiantes/<rut>', methods=['GET'])
def obtener_estudiante(rut):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM estudiantes WHERE rut = %s', (rut,))
    estudiante = cur.fetchone()
    cur.close()
    conn.close()
    
    if estudiante is None:
        return jsonify({'mensaje': 'Estudiante no encontrado'}), 404
    
    return jsonify(estudiante)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)