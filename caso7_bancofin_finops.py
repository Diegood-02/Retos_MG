import pandas as pd
import numpy as np

def analizar_costos_y_recursos_inactivos(datos_recursos: pd.DataFrame) -> dict:
    """
    Simula la auditoría FinOps de recursos en la nube pública para detectar
    desperdicio financiero por volúmenes no adjuntados e instancias subutilizadas.
    """
    # Filtrar volúmenes de almacenamiento huérfanos (unattached)
    volumenes_huerfanos = datos_recursos[
        (datos_recursos['tipo_recurso'] == 'EBS_Volume') &
        (datos_recursos['estado'] == 'available')
    ]
    costo_desperdiciado_almacenamiento = volumenes_huerfanos['costo_mensual_usd'].sum()

    # Filtrar instancias EC2 con uso promedio de CPU menor al 5% (Idle)
    instancias_inactivas = datos_recursos[
        (datos_recursos['tipo_recurso'] == 'EC2_Instance') &
        (datos_recursos['uso_cpu_promedio_pct'] < 5.0)
    ]
    costo_desperdiciado_cómputo = instancias_inactivas['costo_mensual_usd'].sum()

    costo_total_mensual = datos_recursos['costo_mensual_usd'].sum()
    costo_desperdiciado_total = costo_desperdiciado_almacenamiento + costo_desperdiciado_cómputo
    porcentaje_ahorro_potencial = (costo_desperdiciado_total / costo_total_mensual) * 100

    return {
        "costo_total_mensual_usd": round(costo_total_mensual, 2),
        "volumenes_huerfanos_detectados": len(volumenes_huerfanos),
        "instancias_inactivas_detectadas": len(instancias_inactivas),
        "costo_desperdiciado_total_usd": round(costo_desperdiciado_total, 2),
        "porcentaje_ahorro_potencial": round(porcentaje_ahorro_potencial, 2)
    }

# Prueba del script con dataset simulado
if __name__ == "__main__":
    np.random.seed(42)
    recursos_simulados = pd.DataFrame({
        'id_recurso': [f'res-{i:04d}' for i in range(100)],
        'tipo_recurso': np.random.choice(['EC2_Instance', 'EBS_Volume', 'RDS_Database'], size=100, p=[0.5, 0.4, 0.1]),
        'estado': np.random.choice(['in-use', 'available'], size=100, p=[0.8, 0.2]),
        'uso_cpu_promedio_pct': np.random.uniform(0.5, 85.0, size=100),
        'costo_mensual_usd': np.random.uniform(20.0, 450.0, size=100)
    })

    resultado_auditoria = analizar_costos_y_recursos_inactivos(recursos_simulados)
    print("=== INFORME DE AUDITORÍA FINOPS BANCOFIN-MX ===")
    for clave, valor in resultado_auditoria.items():
        print(f"{clave}: {valor}")
