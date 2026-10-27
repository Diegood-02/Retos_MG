import json
import logging

# Configuración de registro estructurado para CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Manejador Serverless para la API de rastreo de paquetes de Logística Express MX.
    Implementa validación de entrada, manejo de excepciones y estructura resiliente.
    """
    try:
        # Extraer parámetros de la petición HTTP recibida vía API Gateway
        query_params = event.get('queryStringParameters', {})
        if not query_params or 'numero_guia' not in query_params:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'El parámetro numero_guia es obligatorio.'})
            }

        numero_guia = query_params['numero_guia']
        logger.info(f"Procesando rastreo para guía: {numero_guia}")

        # Simulación de consulta a base de datos NoSQL altamente disponible (DynamoDB)
        # En producción se utilizaría boto3.resource('dynamodb')
        estado_paquete = consultar_estado_paquete_mock(numero_guia)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'numero_guia': numero_guia,
                'estatus': estado_paquete['estatus'],
                'ubicacion_actual': estado_paquete['ubicacion'],
                'fecha_estimada_entrega': estado_paquete['fecha_entrega']
            })
        }

    except Exception as e:
        logger.error(f"Error no controlado en Lambda Rastreo: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Error interno de procesamiento en la nube.'})
        }

def consultar_estado_paquete_mock(guia: str) -> dict:
    # Datos simulados de respuesta rápida
    return {
        'estatus': 'EN_TRANSITO',
        'ubicacion': 'Centro de Distribución Tepotzotlán, Edomex',
        'fecha_entrega': '2026-09-25'
    }

# --- Bloque de prueba local (simula las peticiones que mandaría API Gateway) ---
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("=== PRUEBA 1: Petición válida con número de guía ===")
    evento_ok = {'queryStringParameters': {'numero_guia': 'GUIA-987654'}}
    print(json.dumps(lambda_handler(evento_ok, None), indent=2, ensure_ascii=False))

    print("\n=== PRUEBA 2: Petición sin número de guía (error 400) ===")
    evento_sin_guia = {'queryStringParameters': None}
    print(json.dumps(lambda_handler(evento_sin_guia, None), indent=2, ensure_ascii=False))
