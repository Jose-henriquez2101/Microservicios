CREATE TABLE IF NOT EXISTS estudiantes (
    rut VARCHAR(12) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    edad INTEGER NOT NULL,
    curso VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS evaluaciones (
    id SERIAL PRIMARY KEY,
    rut_estudiante VARCHAR(12) REFERENCES estudiantes(rut),
    semestre VARCHAR(10) NOT NULL,
    asignatura VARCHAR(50) NOT NULL,
    evaluacion DECIMAL(3,1) NOT NULL
);