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
#crear evaluaciones
@app.route('/evaluaciones', methods=['POST'])
def crear_evaluacion():
    data = request.get_json()
    rut_estudiante = data['rut_estudiante']
    semestre = data['semestre']
    asignatura = data['asignatura']
    evaluacion = data['evaluacion']
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO evaluaciones (rut_estudiante, semestre, asignatura, evaluacion) VALUES (%s, %s, %s, %s)',
        (rut_estudiante, semestre, asignatura, evaluacion)
    )
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({'mensaje': 'Evaluación creada exitosamente'}), 201
#obtener todas las evaluaciones 
@app.route('/evaluaciones', methods=['GET'])
def obtener_evaluaciones():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM evaluaciones')
    evaluaciones = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify(evaluaciones)
#obtener evaluaciones por rut estudiante
@app.route('/evaluaciones/<rut_estudiante>', methods=['GET'])
def obtener_evaluaciones_estudiante(rut_estudiante):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM evaluaciones WHERE rut_estudiante = %s', (rut_estudiante,))
    evaluaciones = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify(evaluaciones)
#obtener evaluaciones por id de las evaluaciones
@app.route('/evaluaciones/<int:id>', methods=['GET'])
def obtener_evaluacion_por_id(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM evaluaciones WHERE id = %s', (id,))
    evaluacion = cur.fetchone()
    cur.close()
    conn.close()
    
    if evaluacion is None:
        return jsonify({'mensaje': 'Evaluación no encontrada'}), 404
    
    return jsonify({
        'id': evaluacion[0],
        'rut_estudiante': evaluacion[1],
        'semestre': evaluacion[2],
        'asignatura': evaluacion[3],
        'evaluacion': float(evaluacion[4])
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)