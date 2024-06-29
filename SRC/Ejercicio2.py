import boto3

# Crear un cliente de DynamoDB
dynamodb = boto3.client('dynamodb', region_name='us-west-2')

# Crear la tabla
table_name = 'Tablaprueba'
partition_key = 'Id'
sort_key = 'Fecha'

try:
    response = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {   # Clave de partición
                'AttributeName': partition_key,
                'KeyType': 'HASH'  
            },
            
            {    # Clave de ordenación
                'AttributeName': sort_key,
                'KeyType': 'RANGE' 
            }
        ],
        
         # Tipo de atributo: 'S' para string, 'N' para número, 'B' para binario
         
        AttributeDefinitions=[
            {
                'AttributeName': partition_key,
                'AttributeType': 'S' 
            },
            {
                'AttributeName': sort_key,
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    print("Tabla creada con éxito:", response)
except Exception as e:
    print("Error al crear:", e)
