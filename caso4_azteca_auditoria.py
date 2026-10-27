# Script de Auditoría de Activos y Redundancia de Software para Distribuidora Azteca
import pandas as pd

# Simulación de datos recolectados de los 15 CEDIS regionales
datos_activos = {
    'CEDIS': ['Monterrey', 'Monterrey', 'Guadalajara', 'Guadalajara', 'Mérida', 'Tijuana', 'Tijuana', 'CDMX', 'CDMX'],
    'Software': ['ERP SAP', 'Office 365', 'Custom ERP', 'Google Workspace', 'Excel Hojas', 'ERP Oracle', 'Office 365', 'ERP SAP', 'Office 365'],
    'Costo_Mensual_USD': [1500, 15, 800, 12, 0, 1200, 15, 5000, 12]
}

df_activos = pd.DataFrame(datos_activos)

print("=== REPORTE DE SOFTWARE ENCONTRADO EN LA DISTRIBUIDORA ===")
print(df_activos)

# Identificar redundancias en el core corporativo (ERPs paralelos)
erps_encontrados = df_activos[df_activos['Software'].str.contains('ERP|Custom')]
costo_total_erp = erps_encontrados['Costo_Mensual_USD'].sum()

print("\n=== ANÁLISIS DE REDUNDANCIA EN SISTEMAS ERP ===")
print(f"Número de sistemas ERP diferentes activos: {erps_encontrados['Software'].nunique()}")
print(f"Costo acumulado mensual de ERPs fragmentados: ${costo_total_erp} USD")

# Recomendación de consolidación bajo el modelo federado de la OCTI
print("\n=== PLAN DE ACCIÓN RECOMENDADO POR LA OCTI ===")
print("1. Migrar CEDIS Guadalajara y Tijuana a la instancia centralizada de ERP SAP de CDMX.")
print("2. Cancelar contratos de ERP locales para consolidar un único descuento corporativo por volumen.")
print("3. Estimar ahorro potencial mensual: Ahorro aproximado de 35% en costos de licenciamiento corporativo.")