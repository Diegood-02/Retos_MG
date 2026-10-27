import os
import sys
import json
# Simulación de un pipeline de despliegue continuo con verificación automatizada de gobernanza e IA
# En un entorno real se importaría openai (pip install openai)
# Establecemos el mock-up del validador de gobernanza de cambios para MoneyFast

class GovernanceGatekeeper:
    def __init__(self, commit_message, author, has_cab_approval, rollback_plan):
        self.commit_message = commit_message
        self.author = author
        self.has_cab_approval = has_cab_approval
        self.rollback_plan = rollback_plan

    def evaluate_change(self):
        print("=== Iniciando Verificación de Gobernanza de Cambios ===")
        print(f"Autor del cambio: {self.author}")
        print(f"Mensaje de cambio: {self.commit_message}")

        # Regla de Gobernanza 1: Segregación de Funciones
        # El autor de la modificación en producción no puede ser un desarrollador junior sin supervisión
        junior_developers = ["dev_juan", "dev_pedro", "dev_sofia"]
        if self.author in junior_developers:
            print("[ALERTA DE SEGURIDAD] Cambio iniciado por desarrollador junior sin segregación de funciones aprobada.")
            return False, "Rechazado: El cambio en producción no puede ser ejecutado directamente por personal de desarrollo junior."

        # Regla de Gobernanza 2: Aprobación formal del Comité de Cambios (CAB) para cambios mayores
        # Evaluamos la complejidad del cambio de forma simulada
        is_high_risk = "database" in self.commit_message.lower() or "schema" in self.commit_message.lower() or "auth" in self.commit_message.lower()

        if is_high_risk:
            print("[INFO] El cambio involucra elementos críticos de base de datos o autenticación. Se requiere aprobación CAB.")
            if not self.has_cab_approval:
                return False, "Rechazado: Cambio de alto riesgo detectado sin la aprobación requerida por el Comité de Cambios (CAB)."

        # Regla de Gobernanza 3: Plan de Recuperación de Desastres (Rollback) obligatorio y estructurado
        if not self.rollback_plan or len(self.rollback_plan) < 15:
            return False, "Rechazado: Plan de rollback insuficiente o ausente. El modelo de resiliencia exige un plan detallado de reversión."

        print("[EXITO] El cambio satisface todas las directrices del modelo de gobernanza corporativo.")
        return True, "Aprobado: Despliegue autorizado por el Gatekeeper de Gobernanza."


# Simulación de ejecución del pipeline de cambios
if __name__ == "__main__":
    # Caso A: Cambio de alto riesgo sin aprobación de CAB y plan de rollback deficiente
    cambio_fallido = GovernanceGatekeeper(
        commit_message="Actualizar esquema de la base de datos de usuarios financieros en producción",
        author="dev_juan",
        has_cab_approval=False,
        rollback_plan="Ejecutar script viejo"
    )
    estatus, msg = cambio_fallido.evaluate_change()
    print(f"Resultado del pipeline de producción: {msg}\n")

    # Caso B: Cambio de alto riesgo con gobernanza impecable
    cambio_exitoso = GovernanceGatekeeper(
        commit_message="Refactorización y optimización de índices de base de datos usuarios",
        author="lead_engineer_carlos",
        has_cab_approval=True,
        rollback_plan="Revertir transacción de esquema en AWS Aurora utilizando el snapshot de respaldo backup_db_20260824"
    )
    estatus, msg = cambio_exitoso.evaluate_change()
    print(f"Resultado del pipeline de producción: {msg}")