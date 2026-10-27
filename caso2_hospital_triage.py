import sqlite3

# Conexión a un archivo de base de datos SQLite (se crea solo si no existe)
conn = sqlite3.connect("hospital_del_angel.db")
cur = conn.cursor()

# --- Creación de la estructura del modelo de datos para la Gestión de Incidentes del Hospital ---
cur.executescript("""
DROP TABLE IF EXISTS incidentes_ti;
DROP TABLE IF EXISTS areas_hospital;

CREATE TABLE areas_hospital (
  id_area INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre_area VARCHAR(100) NOT NULL,
  nivel_criticidad INT NOT NULL -- 1: Crítico (Quirófano, UCI), 2: Medio (Consultorios), 3: Bajo (Administrativo)
);

CREATE TABLE incidentes_ti (
  id_incidente INTEGER PRIMARY KEY AUTOINCREMENT,
  descripcion_problema TEXT NOT NULL,
  id_area INT REFERENCES areas_hospital(id_area),
  estado VARCHAR(50) DEFAULT 'Abierto',
  prioridad_calculada VARCHAR(20),
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# --- Insertar datos semilla de ejemplo para las áreas del hospital ---
cur.executescript("""
INSERT INTO areas_hospital (nombre_area, nivel_criticidad) VALUES
('Quirófano Central 3', 1),
('Unidad de Cuidados Intensivos (UCI)', 1),
('Consultorio de Pediatría 12', 2),
('Oficina de Recursos Humanos', 3);
""")

# --- Insertar incidentes reportados para simular el análisis automatizado ---
cur.executescript("""
INSERT INTO incidentes_ti (descripcion_problema, id_area) VALUES
('La pantalla del monitor de signos vitales conectada a la red de anestesia no carga el expediente electrónico', 1),
('No se puede imprimir el reporte del estado de nómina del mes pasado en la impresora del pasillo central', 4),
('El sistema de expedientes del consultorio tarda 2 minutos en abrir la receta electrónica', 3);
""")

conn.commit()

# --- Consulta SQL Avanzada que simula el algoritmo del Triage de TI ---
# Nota: ILIKE (PostgreSQL) se adapta aquí a LOWER()+LIKE, que hace exactamente lo mismo en SQLite
query = """
SELECT
  id_incidente,
  descripcion_problema,
  nombre_area,
  nivel_criticidad,
  CASE
    WHEN nivel_criticidad = 1 AND (LOWER(descripcion_problema) LIKE '%expediente%' OR LOWER(descripcion_problema) LIKE '%red%' OR LOWER(descripcion_problema) LIKE '%anestesia%') THEN 'P1 - Crítico'
    WHEN nivel_criticidad = 1 OR nivel_criticidad = 2 AND (LOWER(descripcion_problema) LIKE '%sistema%' OR LOWER(descripcion_problema) LIKE '%receta%') THEN 'P2 - Alto'
    WHEN nivel_criticidad = 3 THEN 'P3 - Medio'
    ELSE 'P4 - Bajo'
  END AS prioridad_automatizada
FROM incidentes_ti
JOIN areas_hospital ON incidentes_ti.id_area = areas_hospital.id_area;
"""

cur.execute(query)
rows = cur.fetchall()
cols = [desc[0] for desc in cur.description]

# --- Imprimir resultados en formato de tabla legible ---
print(" | ".join(cols))
print("-" * 100)
for row in rows:
    print(" | ".join(str(x) for x in row))

conn.close()