import boto3
#Crear un cliente dynamodb
dynamodb=boto3.client('dynamodb' , region_name='us-west-2')
#nombre de la tabla creada anteiormente
table='Tablaprueba'

#definimos un CSI

GSI= 'Index_GSI'
pk='Costo'
sk='Tipo'
try:
    # Agregar el GSI a la tabla existente
    response = dynamodb.update_table(
        TableName=table,
        AttributeDefinitions=[
            {
                'AttributeName': pk,
                'AttributeType': 'N'  #Tipo de atributo: 'N' para número
            },
            {
                'AttributeName': sk,
                'AttributeType': 'S'  #Tipo de atributo: 'S' para string
            }
        ],
        GlobalSecondaryIndexUpdates=[
            {
                'Create': {
                    'IndexName': GSI,
                    'KeySchema': [
                        {
                            'AttributeName': pk,
                            'KeyType': 'HASH'  #Clave de partición
                        },
                        {
                            'AttributeName': sk,
                            'KeyType': 'RANGE'  #Clave de ordenación
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'  #Incluir todos los atributos
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            }
        ]
    )

    print("Exito", response)
except Exception as e:
    print("Error", e)