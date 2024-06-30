import boto3
from botocore.exceptions import ClientError

# Crear clientes de DynamoDB en diferentes regiones
dynamodb_us_west_2 = boto3.client('dynamodb', region_name='us-west-2')
dynamodb_us_east_1 = boto3.client('dynamodb', region_name='us-east-1')

# Nombre de la tabla
table_name = 'TablapruebaGlobal'

# Definición de la tabla
table_definition = {
    'TableName': table_name,
    'KeySchema': [
        {
            'AttributeName': 'Id',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'Fecha',
            'KeyType': 'RANGE'
        }
    ],
    'AttributeDefinitions': [
        {
            'AttributeName': 'Id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'Fecha',
            'AttributeType': 'S'
        }
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
}

try:
    # Crear tabla en us-west-2
    response_us_west_2 = dynamodb_us_west_2.create_table(**table_definition)
    print(f"Tabla creada en us-west-2: {response_us_west_2}")

    # Crear tabla en us-east-1
    response_us_east_1 = dynamodb_us_east_1.create_table(**table_definition)
    print(f"Tabla creada en us-east-1: {response_us_east_1}")

    # Esperar a que ambas tablas estén activas
    dynamodb_us_west_2.get_waiter('table_exists').wait(TableName=table_name)
    dynamodb_us_east_1.get_waiter('table_exists').wait(TableName=table_name)

    # Asociar la tabla como tabla global
    dynamodb_us_west_2.update_table(
        TableName=table_name,
        ReplicationGroup=[
            {
                'RegionName': 'us-east-1'
            }
        ]
    )

    print(f"Tabla global '{table_name}' creada exitosamente.")

except ClientError as e:
    print(f"Error al crear la tabla global: {e}")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
