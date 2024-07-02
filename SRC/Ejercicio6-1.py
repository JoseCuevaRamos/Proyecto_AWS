import boto3
from botocore.exceptions import ClientError


dynamodb_us_west_2=boto3.client('dynamodb', region_name='us-west-2')
dynamodb_us_east_1=boto3.client('dynamodb', region_name='us-east-1')


table_name='TablapruebaGlobal'


table_definition={
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
    'BillingMode': 'PAY_PER_REQUEST'  # Usamos un modelo Pay-Per-Request para poder crear tablas adicionales en diferentes regiones 
}

try:
    response_us_west_2 = dynamodb_us_west_2.create_table(**table_definition)
    print(f"Tabla creada en us-west-2: {response_us_west_2}")

    dynamodb_us_west_2.get_waiter('table_exists').wait(TableName=table_name)

    # Replicamos la tabla en la región nel Norte de Virginia
    response_add_replica = dynamodb_us_west_2.update_table(
        TableName=table_name,
        ReplicaUpdates=[
            {
                'Create':{
                    'RegionName':'us-east-1'
                }
            }
        ]
    )

    print(f"Réplica añadida en us-east-1: {response_add_replica}")

except ClientError as e:
    print(f"Error al crear la tabla global: {e}")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
