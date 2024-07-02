import boto3
from botocore.exceptions import ClientError

# Crear un cliente para DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('prueba')

try:
    # Añadir un nuevo elemento para generar un evento
    response = table.put_item(
        Item={
            'Id': '2',     # Clave de partición
            'Datte': '2024-07-02T00:00:00Z',  # Clave de clasificación, usando formato de fecha como ejemplo
            'OtherAttribute': 'Valor de prueba2'  # Otros atributos adicionales
        }
    )
    print("Elemento añadido:", response)

    # Actualizar el elemento para generar otro evento
    response = table.update_item(
        Key={
            'Id': '2',     # Clave de partición
            'Datte': '2024-07-02T00:00:00Z'  # Clave de clasificación
        },
        UpdateExpression='SET OtherAttribute = :val1',
        ExpressionAttributeValues={':val1': 'Nuevo valor'}
    )
    print("Elemento actualizado:", response)

    # Eliminar el elemento para generar otro evento
    response = table.delete_item(
        Key={
            'Id': '2',     # Clave de partición
            'Datte': '2024-07-02T00:00:00Z'  # Clave de clasificación
        }
    )
    print("Elemento eliminado:", response)

except ClientError as e:
    print(f"Error al manipular la tabla: {e}")
