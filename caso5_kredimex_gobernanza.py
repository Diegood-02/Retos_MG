# Sistema Automatizado de Evaluación y Aprobación de Cambios para KrediMex
import datetime

# Base de datos simulada de registros de cambios (Log de Auditoría para CNBV)
log_auditoria_cambios = []

def evaluar_cambio(id_cambio, modulo, lineas_afectadas, criticidad_modulo, desarrollador, revisor):
    # Regla estricta de Gobernanza (COBIT/CNBV): Segregación de funciones
    if desarrollador == revisor:
        return {
            "ID": id_cambio,
            "Estado": "RECHAZADO",
            "Motivo": "Violación de segregación de funciones: El desarrollador no puede ser el mismo revisor."
        }

    # Evaluar nivel de riesgo del cambio
    if criticidad_modulo == "ALTA" or lineas_afectadas > 200:
        categoria_cambio = "NORMAL (Requiere aprobación humana del Líder de TI)"
        estado_aprobacion = "PENDIENTE_AUTORIZACION"
    else:
        categoria_cambio = "ESTÁNDAR (Pre-aprobado automáticamente)"
        estado_aprobacion = "APROBADO_AUTOMÁTICAMENTE"

    registro = {
        "ID": id_cambio,
        "Módulo": modulo,
        "Categoría": categoria_cambio,
        "Estado": estado_aprobacion,
        "Fecha_Registro": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Desarrollador": desarrollador,
        "Revisor": revisor
    }
    log_auditoria_cambios.append(registro)
    return registro


# Caso 1: Cambio riesgoso que requiere revisión
cambio_1 = evaluar_cambio(101, "Core_Transacciones", 350, "ALTA", "Ing. Pedro López", "Ing. Sofía Pérez")
# Caso 2: Intento de violación de segregación de funciones (Hackeo interno)
cambio_2 = evaluar_cambio(102, "UI_Banners", 10, "BAJA", "Ing. Juan Gómez", "Ing. Juan Gómez")
# Caso 3: Cambio estándar de bajo riesgo
cambio_3 = evaluar_cambio(103, "Login_Interface", 25, "MEDIA", "Ing. Ana Torres", "Ing. Carlos Ruiz")

print("=== EVALUACIÓN DE CAMBIOS EN TIEMPO REAL ===")
for c in [cambio_1, cambio_2, cambio_3]:
    print(f"Cambio ID {c['ID']}: Estado: {c['Estado']} | Motivo/Categoría: {c.get('Motivo', c.get('Categoría'))}")