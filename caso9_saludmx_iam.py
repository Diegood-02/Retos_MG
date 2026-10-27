import json

def auditar_politica_iam(politica_json: dict) -> list:
    """
    Audita una política de control de acceso IAM en la nube para identificar
    violaciones críticas al principio de Cero Confianza (Zero Trust).
    """
    hallazgos_seguridad = []

    statements = politica_json.get('Statement', [])
    if isinstance(statements, dict):
        statements = [statements]

    for idx, stmt in enumerate(statements):
        efecto = stmt.get('Effect', '')
        accion = stmt.get('Action', [])
        recurso = stmt.get('Resource', '')

        # Regla 1: Detección de comodín total en acciones (*)
        if efecto == 'Allow' and (accion == '*' or '*' in accion):
            hallazgos_seguridad.append({
                'severidad': 'CRÍTICA',
                'statement_index': idx,
                'regla': 'No se permite el uso de comodines (*) en Action bajo Cero Confianza.',
                'recomendacion': 'Especifique explícitamente los permisos mínimos requeridos.'
            })

        # Regla 2: Detección de acceso público o no restringido en recursos (*)
        if efecto == 'Allow' and recurso == '*':
            hallazgos_seguridad.append({
                'severidad': 'ALTA',
                'statement_index': idx,
                'regla': 'El recurso está configurado como universal (*).',
                'recomendacion': 'Restrinja el ARN del recurso a los buckets o bases de datos específicas.'
            })

    return hallazgos_seguridad

# Ejemplo de prueba con una política insegura común
politica_insegura_ejemplo = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AccesoMedicosInseguro",
            "Effect": "Allow",
            "Action": "*",
            "Resource": "*"
        }
    ]
}

if __name__ == "__main__":
    reporte_auditoria = auditar_politica_iam(politica_insegura_ejemplo)
    print("=== REPORTE DE AUDITORÍA DE SEGURIDAD IAM ZERO TRUST ===")
    print(json.dumps(reporte_auditoria, indent=2, ensure_ascii=False))
