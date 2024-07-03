import boto3
from botocore.exceptions import ClientError

# Crear un cliente para DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('pruebafinalaws')

try:
    # Añadir un nuevo elemento para generar un evento
    response = table.put_item(
        Item={
            'Id': '2',     # Clave de partición
            'Date': '2024-01-01',  # Clave de clasificación, usando formato de fecha como ejemplo
            'OtherAttribute': 'Valor de prueba2'  # Otros atributos adicionales
        }
    )
    print("Elemento añadido:", response)

except ClientError as e:
    print(f"Error al manipular la tabla: {e}")
