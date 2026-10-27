# Motor de Reglas para Aprobación de Cambios en Software Médico Crítico
# (Sistemas de Soporte de Vida - Alta Criticidad)

class MotorAprobacionMedica:
    def __init__(self):
        self.log_auditoria = []

    def evaluar_cambio(self, id_cambio, modulo, criticidad_modulo, lineas_codigo_modificadas,
                        desarrollador, aprobador, cobertura_pruebas_pct, id_ticket_aprobacion):

        resultado = {
            "ID": id_cambio,
            "Módulo": modulo,
            "Estado": None,
            "Motivo": None
        }

        # Regla 1: Segregación de funciones - NUNCA el mismo desarrollador puede autoaprobarse
        if desarrollador == aprobador:
            resultado["Estado"] = "RECHAZADO"
            resultado["Motivo"] = "Violación crítica de segregación de funciones: el desarrollador no puede aprobar su propio cambio."
            self.log_auditoria.append(resultado)
            return resultado

        # Regla 2: Todo cambio en módulo de ALTA criticidad requiere ticket de aprobación formal
        if criticidad_modulo == "ALTA" and not id_ticket_aprobacion:
            resultado["Estado"] = "RECHAZADO"
            resultado["Motivo"] = "Módulo de soporte de vida sin ID de ticket de aprobación formal asignado."
            self.log_auditoria.append(resultado)
            return resultado

        # Regla 3: Cobertura de pruebas unitarias mínima obligatoria (>90%) para módulos críticos
        if criticidad_modulo == "ALTA" and cobertura_pruebas_pct < 90:
            resultado["Estado"] = "RECHAZADO"
            resultado["Motivo"] = f"Cobertura de pruebas insuficiente ({cobertura_pruebas_pct}%). Se exige mínimo 90% para módulos de soporte de vida."
            self.log_auditoria.append(resultado)
            return resultado

        # Regla 4: Volumen de código modificado - cambios grandes en módulos críticos requieren revisión extendida
        if criticidad_modulo == "ALTA" and lineas_codigo_modificadas > 150:
            resultado["Estado"] = "PENDIENTE_REVISION_EXTENDIDA"
            resultado["Motivo"] = f"Cambio de {lineas_codigo_modificadas} líneas en módulo crítico: requiere revisión de un segundo ingeniero senior antes de aprobación final."
            self.log_auditoria.append(resultado)
            return resultado

        # Si pasa todas las validaciones
        resultado["Estado"] = "APROBADO"
        resultado["Motivo"] = "Cambio validado: segregación de funciones correcta, cobertura de pruebas suficiente, ticket formal asignado."
        self.log_auditoria.append(resultado)
        return resultado


# --- Simulación de casos ---
motor = MotorAprobacionMedica()

# Caso A: Intento de autoaprobación (debe rechazarse de inmediato)
caso_a = motor.evaluar_cambio(
    id_cambio=201, modulo="Monitor_Signos_Vitales", criticidad_modulo="ALTA",
    lineas_codigo_modificadas=45, desarrollador="Ing. Laura Méndez", aprobador="Ing. Laura Méndez",
    cobertura_pruebas_pct=95, id_ticket_aprobacion="TCK-4521"
)

# Caso B: Módulo crítico sin ticket de aprobación (debe rechazarse)
caso_b = motor.evaluar_cambio(
    id_cambio=202, modulo="Bomba_Infusion", criticidad_modulo="ALTA",
    lineas_codigo_modificadas=30, desarrollador="Ing. Marco Ruiz", aprobador="Ing. Diana Solís",
    cobertura_pruebas_pct=95, id_ticket_aprobacion=None
)

# Caso C: Cobertura de pruebas insuficiente (debe rechazarse)
caso_c = motor.evaluar_cambio(
    id_cambio=203, modulo="Ventilador_Mecanico", criticidad_modulo="ALTA",
    lineas_codigo_modificadas=60, desarrollador="Ing. Marco Ruiz", aprobador="Ing. Diana Solís",
    cobertura_pruebas_pct=78, id_ticket_aprobacion="TCK-4530"
)

# Caso D: Cambio grande en módulo crítico, todo correcto pero requiere revisión extendida
caso_d = motor.evaluar_cambio(
    id_cambio=204, modulo="Monitor_Signos_Vitales", criticidad_modulo="ALTA",
    lineas_codigo_modificadas=220, desarrollador="Ing. Marco Ruiz", aprobador="Ing. Diana Solís",
    cobertura_pruebas_pct=96, id_ticket_aprobacion="TCK-4540"
)

# Caso E: Cambio aprobado exitosamente
caso_e = motor.evaluar_cambio(
    id_cambio=205, modulo="Dashboard_Reportes", criticidad_modulo="MEDIA",
    lineas_codigo_modificadas=40, desarrollador="Ing. Ana Torres", aprobador="Ing. Carlos Ruiz",
    cobertura_pruebas_pct=92, id_ticket_aprobacion="TCK-4550"
)

print("=== EVALUACIÓN DE CAMBIOS EN SISTEMAS DE SOPORTE DE VIDA ===")
for caso in [caso_a, caso_b, caso_c, caso_d, caso_e]:
    print(f"Cambio ID {caso['ID']} ({caso['Módulo']}): {caso['Estado']}")
    print(f"   → {caso['Motivo']}\n")