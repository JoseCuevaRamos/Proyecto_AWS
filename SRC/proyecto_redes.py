import boto3
from botocore.exceptions import ClientError
from time import sleep
import datetime

def creartabla(Nombre, region,partitionkey,sortkey):
    dynamodb=boto3.client('dynamodb',region_name=region)

    try:
        response=dynamodb.create_table(
                TableName=Nombre,
                KeySchema=[
                    {
                        'AttributeName':partitionkey,
                        'KeyType':'HASH'
                    },
                    {
                        'AttributeName':sortkey,
                        'KeyType':'RANGE'
                    }
                      
                ],

                AttributeDefinitions=[
                     {
                          'AttributeName':partitionkey,
                          'AttributeType':'S'
                     },
                     
                     {
                          'AttributeName':sortkey,
                          'AttributeType':'S'
                     }



                ],
                ProvisionedThroughput={
                     'ReadCapacityUnits':5,
                     'WriteCapacityUnits':5
                }
        
        )
        print("Tabla creada con éxito:", response)
    except Exception as e:
            print("Error",e)


 



def crear_GSI(GSI_name, partitionkey, sortkey, region_name, tablename):
    dynamodb = boto3.client('dynamodb', region_name=region_name)
    
    try:
        response = dynamodb.update_table(
            TableName=tablename,
            AttributeDefinitions=[
                {
                    'AttributeName': partitionkey,
                    'AttributeType': 'S'  # Tipo de atributo: 'N' para número si corresponde
                },
                {
                    'AttributeName': sortkey,
                    'AttributeType': 'S'  # Tipo de atributo: 'S' para string
                }
            ],
            GlobalSecondaryIndexUpdates=[
                {
                    'Create': {
                        'IndexName': GSI_name,
                        'KeySchema': [
                            {
                                'AttributeName': partitionkey,
                                'KeyType': 'HASH'  # Clave de partición
                            },
                            {
                                'AttributeName': sortkey,
                                'KeyType': 'RANGE'  # Clave de ordenación
                            }
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL'  # Incluir todos los atributos
                        },
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        }
                    }
                }
            ]
        )
        print("exito:", response)
    except Exception as e:
        print("Error al crear el GSI:", e)   





def calculate_rcu(item_size_kb, read_rate_per_second, consistency='eventual'):
    # Calcula las Unidades de Capacidad de Lectura (RCU) necesarias
    if consistency == 'fuerte':
        # Lectura consistente fuerte
        rcu_per_read = 1 if item_size_kb <= 4 else (item_size_kb // 4) + 1
    else:
        # Lectura eventualmente consistente
        rcu_per_read = 0.5 if item_size_kb <= 4 else (item_size_kb // 4) / 2
    
    total_rcu = rcu_per_read * read_rate_per_second
    return total_rcu



#calcular y actualizar el rcu y wcu 
def calculate_wcu(item_size_kb, write_rate_per_second):
    # Calcula las Unidades de Capacidad de Escritura (WCU) necesarias
    wcu_per_write = 1 if item_size_kb <= 1 else (item_size_kb // 1) + 1
    total_wcu = wcu_per_write * write_rate_per_second
    return total_wcu


def actualizar_rcu_y_wcu(table_name, item_size_kb, read_rate_per_second, write_rate_per_second, consistency='eventual', region_name='us-west-2'):
    # Calcular RCU y WCU
    rcu = calculate_rcu(item_size_kb, read_rate_per_second, consistency)
    wcu = calculate_wcu(item_size_kb, write_rate_per_second)
    
    print(f"Unidades de Capacidad de Lectura (RCU) necesarias: {rcu}")
    print(f"Unidades de Capacidad de Escritura (WCU) necesarias: {wcu}")
    
    # Crear un cliente de DynamoDB
    dynamodb = boto3.client('dynamodb', region_name=region_name)
    
    # Ajustar las capacidades provisionadas según los cálculos
    try:
        response = dynamodb.update_table(
            TableName=table_name,
            ProvisionedThroughput={
                'ReadCapacityUnits': int(rcu),
                'WriteCapacityUnits': int(wcu)
            }
        )
        print("Éxito:", response)
    except Exception as e:
        print("Error al actualizar la tabla:", e)










def habilitar_y_crear_streams(nombre_tabla,region):
    try:
        dynamodb = boto3.client("dynamodb", region_name=region)

        response = dynamodb.update_table(
            TableName=nombre_tabla,
            StreamSpecification={
                "StreamEnabled": True,
                "StreamViewType": "NEW_AND_OLD_IMAGES"
            }
        )
        print(f"Streams habilitados en '{nombre_tabla}'")
        print("Detalles de la tabla:", response)

        dynamodbstreams = boto3.client('dynamodbstreams', region_name=region)

        response = dynamodb.describe_table(TableName=nombre_tabla)
        stream_arn = response['Table']['LatestStreamArn']
        print(f"Stream ARN: {stream_arn}")

        response = dynamodbstreams.describe_stream(StreamArn=stream_arn)
        stream_description = response['StreamDescription']
        print("Descripción del Stream:", stream_description)

        shards = stream_description['Shards']
        shard_id = shards[0]['ShardId']

        shard_iterator = dynamodbstreams.get_shard_iterator(
            StreamArn=stream_arn,
            ShardId=shard_id,
            ShardIteratorType='TRIM_HORIZON'
        )['ShardIterator']

        while True:
            response = dynamodbstreams.get_records(ShardIterator=shard_iterator)
            records = response['Records']
            if records:
                print("Registros:")
                for record in records:
                    print(record)
            shard_iterator = response['NextShardIterator']
            sleep(30)
    except ClientError as e:
        print(f"Error al procesar Streams: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        


        

def crear_tabla_global(table_name,region_primaria,region_replica):
     try:
          dynamodb_primary= boto3.client('dynamodb', region_name=region_primaria)
          dynamodb_replica= boto3.client('dynamodb', region_name=region_replica)
          
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
                    'Attribute Type': 'S'
                }
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
            }   
          response_primary= dynamodb_primary.create_table(**table_definition)
          print(f"Tabla creada en {region_primaria}:{response_primary}")

          response_replica= dynamodb_replica.create_table(**table_definition)
          print(f"Tabla creada en {region_replica}:{response_replica}")
        
        
          dynamodb_primary.get_waiter('table_exists').wait(TableName=table_name)
          dynamodb_replica.get_waiter('table_exists').wait(TableName=table_name)
          
          dynamodb_primary.update_table(
            TableName=table_name,
            ReplicationGroup=[
                {
                    'RegionName': region_replica
                }
            ]
            )
          print(f"Tabla global '{table_name}' creada exitosamente")
     except ClientError as e:
        print(f"Error al crear la tabla global: {e}")
     except Exception as e:
          print(f"Error; {e}")
          

def gestionar_elemento_dynamodb(operacion,table_name,region):
    dynamodb = boto3.client('dynamodb', region_name=region)
    if operacion == 'CREATE':
        item = {
            "Id": {"S": "Estoesotraprueba"},
            "Fecha": {"S": "2024-01-01"},
            "Estado": {"S": "Activo"},
            "Nombre": {"S": "Ejemplo"},
            "Edad": {"N": "25"},
            "Correo": {"S": "ejemplo@example.com"}
        }
        try:
            response = dynamodb.put_item(
                TableName=table_name,
                Item=item
            )
            print("Elemento creado exitosamente:", response)
        except ClientError as e:
            print("Error al crear el elemento:", e)
        except Exception as e:
            print("Ocurrió un error inesperado:", e)
    elif operacion=="READ":
        key={
            "Id":{"S":"Estoesotraprueba"},
            "Fecha":{"S":"2024-01-01"}
        }
        try:
            response = dynamodb.get_item(
                TableName=table_name,
                Key=key
            )

            if 'Item' in response:
                item = response['Item']
                print("Elemento encontrado:", item)
            else:
                print("Elemento no encontrado.")
        except ClientError as e:
            print("Error al leer el elemento:", e)
        except Exception as e:
            print("Ocurrió un error inesperado:", e)

    elif operacion=="UPDATE":
        key = {
            "Id": {"S": "Estoesotraprueba"},
            "Fecha": {"S": "2024-01-01"}
        }

        update_expression = "SET Nombre = :n, Edad = :e, Correo = :c"
        expression_attribute_values = {
            ":n": {"S": "Nuevo Ejemplo"},
            ":e": {"N": "30"},
            ":c": {"S": "nuevo_ejemplo@example.com"}
        }

        try:
            response = dynamodb.update_item(
                TableName=table_name,
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
            print("Elemento actualizado exitosamente:", response)
        except ClientError as e:
            print("Error al actualizar el elemento:", e)
        except Exception as e:
            print("Ocurrió un error inesperado:", e)

    elif operacion == "DELETE":
        key = {
            "Id": {"S": "Estoesotraprueba"},
            "Fecha": {"S": "2024-01-01"}
        }

        try:
            response = dynamodb.delete_item(
                TableName=table_name,
                Key=key
            )
            print("Elemento eliminado exitosamente.")
        except ClientError as e:
            print("Error al eliminar el elemento:", e)
        except Exception as e:
            print("Ocurrió un error inesperado:", e)

    else:
        print("Operación no válida. Debe ser CREATE, READ, UPDATE o DELETE.")


def crear_backup(region_backup, region_dynamodb, table_name):
    # Crear clientes de DynamoDB y Backup
    dynamodb = boto3.client('dynamodb', region_name=region_dynamodb)
    backup = boto3.client('backup', region_name=region_backup)
    
    # Crear un nombre único para la copia de seguridad basado en la fecha y hora actual
    backup_name = f"backup_{table_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    try:
        # Crear la copia de seguridad
        response = dynamodb.create_backup(
            TableName=table_name,
            BackupName=backup_name
        )
        print(f"exito: {response['BackupDetails']['BackupArn']}")
    except Exception as e:
        print(f"Error al crear el backup: {e}")

def restaurar_tabla_desde_backup(region, backup_arn, new_table_name):
    # Crear cliente de DynamoDB
    dynamodb = boto3.client('dynamodb', region_name=region)

    try:
        # Restaurar la tabla desde la copia de seguridad
        response = dynamodb.restore_table_from_backup(
            TargetTableName=new_table_name,
            BackupArn=backup_arn
        )
        print(f"EXITO: {response['TableDescription']['TableArn']}")
    except Exception as e:
        print(f"Error al restaurar la tabla: {e}")




print("Buenos dias y bienvenido a la interfaz de usuario que le permitirá interactuar con las bases\nde datos no relacionales de DynamoDb, un servicio de AWS")






while True:
    answer=input("Por favor, ingrese la accion que desea realizar\n\t1: Crear tablas\n\t2: Crear índices\n\t3: Calcular Unidades de lectura y escritura\n\t4: Habilitar y crear streams\n\t5: Crear tablas globales\n\t6: Realizar copias de seguridad \n\t7: Crear, Leer, Actualizar o Eliminar elementos de una tabla")
    seguir=False
    if answer==1:
        creartabla()


    if answer==2:
        crear_GSI()
        pass

    if answer==3:
        actualizar_rcu_y_wcu()
        pass

    if answer==4:
        habilitar_y_crear_streams()
        pass
    
    if answer==5:
        crear_tabla_global()
        pass
    
    if answer==6:
        crear_backup()
        pass
    
    if answer==7:
        gestionar_elemento_dynamodb()
        pass


    r=input("Desea continuar?: (Ingrese Sí/No)")
    if r.lower()=="sí" or r.lower()=="si":
        seguir=True
    else:
        seguir=False
        print("Muchas gracias por usar nuestro servicio")
        break
        
        
     
