import boto3
from botocore.exceptions import ClientError

# Inicializar el cliente de DynamoDB
dynamodb = boto3.client('dynamodb', region_name='us-west-2')

# Definir las operaciones transaccionales
transact_items = [
    {
        'Update': {
            'TableName': 'Tablap',
            'Key': {
                'Id': {'S': '1'},
                'Fecha': {'S': '2'}
            },
            'UpdateExpression': 'SET Costo = :new_cost, Tipo = :new_type',
            'ExpressionAttributeValues': {
                ':new_cost': {'N': '3000'},
                ':new_type': {'S': 'F'}
            }
        }
    },
    {
        'Update': {
            'TableName': 'Tablaprueba',
            'Key': {
                'Id': {'S': '3'},
                'Fecha': {'S': '4'}
            },
            'UpdateExpression': 'SET Costo = :new_cost, Tipo = :new_type',
            'ExpressionAttributeValues': {
                ':new_cost': {'N': '300'},
                ':new_type': {'S': 'H'}
            }
        }
    }
]

# Ejecutar la transacción
try:
    response = dynamodb.transact_write_items(TransactItems=transact_items)
    print("Transacción completada con éxito")
except ClientError as e:
    print(f"Error en la transacción: {e.response['Error']['Message']}")
