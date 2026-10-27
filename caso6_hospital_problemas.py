import sqlite3

conn = sqlite3.connect("hospital_universitario_norte.db")
cur = conn.cursor()

# --- Creación de la tabla de Incidentes de Soporte del Hospital ---
cur.executescript("""
DROP TABLE IF EXISTS incidentes_soporte;

CREATE TABLE incidentes_soporte (
  id_incidente INTEGER PRIMARY KEY,
  modulo_afectado TEXT,
  descripcion_falla TEXT,
  solucion_aplicada TEXT,
  fecha_reporte TIMESTAMP,
  tiempo_resolucion_minutos INTEGER,
  id_problema_asociado INTEGER
);
""")

# --- Inserción de logs históricos que demuestran el patrón repetitivo ---
cur.executescript("""
INSERT INTO incidentes_soporte VALUES (1, 'Expediente_Clinico', 'Lentitud extrema en urgencias', 'Reinicio de servidor de BD', '2026-08-20 11:05:00', 15, NULL);
INSERT INTO incidentes_soporte VALUES (2, 'Expediente_Clinico', 'Pantalla congelada al guardar receta', 'Reinicio de servidor de BD', '2026-08-21 11:12:00', 18, NULL);
INSERT INTO incidentes_soporte VALUES (3, 'Expediente_Clinico', 'Error de timeout en base de datos', 'Reinicio de servidor de BD', '2026-08-22 11:08:00', 14, NULL);
INSERT INTO incidentes_soporte VALUES (4, 'Impresoras', 'No imprime ticket de farmacia', 'Limpieza de cola de impresión', '2026-08-22 14:30:00', 5, NULL);
""")

conn.commit()

# --- Consulta de Análisis de Inteligencia para detección automática de Problemas ---
# Agrupa incidentes similares para alertar al equipo de soporte de un patrón repetitivo
query = """
SELECT
  modulo_afectado,
  COUNT(*) as cantidad_incidentes_repetidos,
  AVG(tiempo_resolucion_minutos) as promedio_tiempo_paralizado_min,
  solucion_aplicada as solucion_temporal_comun
FROM incidentes_soporte
WHERE id_problema_asociado IS NULL
GROUP BY modulo_afectado, solucion_aplicada
HAVING COUNT(*) > 2;
"""

cur.execute(query)
rows = cur.fetchall()
cols = [desc[0] for desc in cur.description]

print(" | ".join(cols))
print("-" * 100)
for row in rows:
    print(" | ".join(str(x) for x in row))

conn.close()