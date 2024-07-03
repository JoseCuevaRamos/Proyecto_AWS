import boto3
from botocore.exceptions import ClientError
from time import sleep
import datetime

def creartabla(Nombre, region,partitionkey,sortkey):
    """
    Crear una tabla de DynamoDB con el nombre y las keys especificas
    
    Argumentos:
    Nombres(str): El nombre de la nueva tabla.
    Region(str): Laregion de AWS donde se creara la tabla
    partitionkey (str): La clave de partición de la tabla.
    sortkey (str): La clave de ordenación de la tabla.

    """

    # Crear un cliente de DynamoDB
    dynamodb=boto3.client('dynamodb',region_name=region)

    try:
        response=dynamodb.create_table(
                TableName=Nombre,
                KeySchema=[
                    {
                        'AttributeName':partitionkey,
                        'KeyType':'HASH' # Clave de partición
                    },
                    {
                        'AttributeName':sortkey,
                        'KeyType':'RANGE' # Clave de ordenacion
                    }
                      
                ],

                AttributeDefinitions=[
                     {
                          'AttributeName':partitionkey,
                          'AttributeType':'S' # Tipo de dato: String
                     },
                     
                     {
                          'AttributeName':sortkey,
                          'AttributeType':'S' # Tipo de dato: String
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
    """
    Crea un Índice Secundario Global (GSI) en una tabla de DynamoDB existente.

    Argumentos:
        GSI_name (str): El nombre del nuevo GSI.
        partitionkey (str): La clave de partición para el GSI.
        sortkey (str): La clave de ordenación para el GSI.
        region_name (str): La región de AWS donde se encuentra la tabla.
        tablename (str): El nombre de la tabla donde se creará el GSI.
    """
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
    """
    Calcula las Unidades de Capacidad de Lectura (RCU) necesarias para DynamoDB.

    Args:
        item_size_kb (int): El tamaño del ítem en kilobytes.
        read_rate_per_second (int): La tasa de lectura por segundo.
        consistency (str): Tipo de consistencia ('fuerte' o 'eventual'). Por defecto es 'eventual'.

    Returns:
        float: El número total de RCU necesarias.
    """
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
    """
    Calcula las Unidades de Capacidad de Escritura (WCU) necesarias para DynamoDB.

    Args:
        item_size_kb (int): El tamaño del ítem en kilobytes.
        write_rate_per_second (int): La tasa de escritura por segundo.

    Returns:
        float: El número total de WCU necesarias.
    """
    # Calcula las Unidades de Capacidad de Escritura (WCU) necesarias
    wcu_per_write = 1 if item_size_kb <= 1 else (item_size_kb // 1)
    total_wcu = wcu_per_write * write_rate_per_second
    return total_wcu


def actualizar_rcu_y_wcu(table_name, item_size_kb, read_rate_per_second, write_rate_per_second, consistency='eventual', region_name='us-west-2'):
    """
    Calcula y actualiza las Unidades de Capacidad de Lectura (RCU) y Escritura (WCU) para una tabla de DynamoDB.

    Args:
        table_name (str): El nombre de la tabla.
        item_size_kb (int): El tamaño del ítem en kilobytes.
        read_rate_per_second (int): La tasa de lectura por segundo.
        write_rate_per_second (int): La tasa de escritura por segundo.
        consistency (str): Tipo de consistencia ('fuerte' o 'eventual'). Por defecto es 'eventual'.
        region_name (str): La región de AWS donde se encuentra la tabla. Por defecto es 'us-west-2'.
    """
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


def habilitar_y_crear_streams(nombre_tabla, region):
    """
    Habilita los streams en una tabla de DynamoDB y obtiene registros de estos streams.

    Args:
        nombre_tabla (str): El nombre de la tabla en DynamoDB.
        region (str): La región de AWS donde se encuentra la tabla.
    """
    try:
        dynamodb=boto3.client("dynamodb", region_name=region)

        # Habilitamos los streams en la tabla
        response=dynamodb.update_table(
            TableName=nombre_tabla,
            StreamSpecification={
                "StreamEnabled": True,
                "StreamViewType": "NEW_AND_OLD_IMAGES"
            }
        )
        print(f"Streams habilitados en '{nombre_tabla}'")
        print("Detalles de la tabla:", response)

        # Describir la tabla para obtener el StreamArn
        response=dynamodb.describe_table(TableName=nombre_tabla)
        stream_arn=response['Table']['LatestStreamArn']
        print(f"Stream ARN: {stream_arn}")

        # Obtener descripción del Stream
        dynamodbstreams=boto3.client('dynamodbstreams', region_name=region)
        response=dynamodbstreams.describe_stream(StreamArn=stream_arn)
        stream_description=response['StreamDescription']
        print("Descripción del Stream:", stream_description)

        # Obtener fragmentos del Stream
        shards=stream_description.get('Shards', [])
        if not shards:
            print("No hay fragmentos disponibles en el Stream.")
            return

        shard_id=shards[0]['ShardId']
        print(f"Shard ID: {shard_id}")

        shard_iterator=dynamodbstreams.get_shard_iterator(
            StreamArn=stream_arn,
            ShardId=shard_id,
            ShardIteratorType='TRIM_HORIZON'
        )['ShardIterator']

        # Obtener registros del Stream
        while True:
            response=dynamodbstreams.get_records(ShardIterator=shard_iterator)
            records=response.get('Records', [])
            if records:
                print("Registros:")
                for record in records:
                    print(record)
            shard_iterator=response.get('NextShardIterator', None)
            if not shard_iterator:
                break
            sleep(30)
    except ClientError as e:
        print(f"Error al procesar Streams: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
          



def crear_tabla_global(table_name, region_primaria, region_replica):
    """
    Crea una tabla global en DynamoDB con réplica en otra región.

    Args:
        table_name (str): El nombre de la nueva tabla.
        region_primaria (str): La región primaria de AWS.
        region_replica (str): La región de réplica de AWS.
    """
    try:
        # Crear clientes para las regiones primaria y réplica
        dynamodb_primary = boto3.client('dynamodb', region_name=region_primaria)
        dynamodb_replica = boto3.client('dynamodb', region_name=region_replica)
        
        # Definición de la tabla con streams habilitados
        table_definition = {
            'TableName': table_name,
            'KeySchema': [
                {'AttributeName': 'Id', 'KeyType': 'HASH'},
                {'AttributeName': 'Fecha', 'KeyType': 'RANGE'}
            ],
            'AttributeDefinitions': [
                {'AttributeName': 'Id', 'AttributeType': 'S'},
                {'AttributeName': 'Fecha', 'AttributeType': 'S'}
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            },
            'StreamSpecification': {
                "StreamEnabled": True,
                "StreamViewType": "NEW_AND_OLD_IMAGES"
            }
        }

        # Crear la tabla en la región primaria
        response_primary = dynamodb_primary.create_table(**table_definition)
        print(f"Tabla creada en {region_primaria}: {response_primary}")

        # Esperar a que la tabla esté disponible en la región primaria
        dynamodb_primary.get_waiter('table_exists').wait(TableName=table_name)

        # Crear la tabla en la región réplica
        response_replica = dynamodb_replica.create_table(**table_definition)
        print(f"Tabla creada en {region_replica}: {response_replica}")

        # Esperar a que la tabla esté disponible en la región réplica
        dynamodb_replica.get_waiter('table_exists').wait(TableName=table_name)

        # Crear la tabla global
        response_global = dynamodb_primary.create_global_table(
            GlobalTableName=table_name,
            ReplicationGroup=[
                {'RegionName': region_primaria},
                {'RegionName': region_replica}
            ]
        )
        print(f"Tabla global '{table_name}' creada exitosamente: {response_global}")
        
    except ClientError as e:
        print(f"Error al crear la tabla global: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

          

def gestionar_elemento_dynamodb(operacion,table_name,region):
    """
    Crea una tabla global en DynamoDB con réplica en otra región.

    Args:
        table_name (str): El nombre de la nueva tabla.
        region_primaria (str): La región primaria de AWS.
        region_replica (str): La región de réplica de AWS.
    """
    dynamodb=boto3.client('dynamodb', region_name=region)
    if operacion=='CREATE':
        item={
            "Id":{"S":"Estoesotraprueba"},
            "Date":{"S":"2020-1-2"}
        }
        try:
            response=dynamodb.put_item(
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
            "Date":{"S":"2020-1-2"}
        }
        try:
            response=dynamodb.get_item(
                TableName=table_name,
                Key=key
            )

            if 'Item' in response:
                item=response['Item']
                print("Elemento encontrado:", item)
            else:
                print("Elemento no encontrado.")
        except ClientError as e:
            print("Error al leer el elemento:", e)
        except Exception as e:
            print("Ocurrió un error inesperado:", e)

    elif operacion=="UPDATE":
        key={
            "Id":{"S":"Estoesotraprueba"},
            "Date":{"S":"2020-1-2"}
        }

        update_expression="SET Nombre = :n, Edad = :e, Correo = :c"
        expression_attribute_values={
            ":n":{"S":"Nuevo Ejemplo"},
            ":e":{"N":"30"},
            ":c":{"S":"nuevo_ejemplo@example.com"}
        }

        try:
            response=dynamodb.update_item(
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

    elif operacion=="DELETE":
        key={
            "Id":{"S":"Estoesotraprueba"},
            "Date":{"S":"2020-1-2"}
        }

        try:
            response=dynamodb.delete_item(
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


def crear_backup(region_dynamodb, table_name):
    """
    Crea una copia de seguridad de una tabla de DynamoDB.

    Args:
        region_dynamodb (str): La región de AWS donde se encuentra la tabla.
        table_name (str): El nombre de la tabla en DynamoDB.
    """
    # Crear clientes de DynamoDB y Backup
    dynamodb=boto3.client('dynamodb', region_name=region_dynamodb)

    # Crear un nombre único para la copia de seguridad basado en la fecha y hora actual
    backup_name=f"backup_{table_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    
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
    """
    Restaura una tabla de DynamoDB desde una copia de seguridad.

    Args:
        region (str): La región de AWS donde se restaurará la tabla.
        backup_arn (str): El ARN de la copia de seguridad.
        new_table_name (str): El nombre de la nueva tabla restaurada.
    """
    # Crear cliente de DynamoDB
    dynamodb=boto3.client('dynamodb', region_name=region)

    try:
        # Restaurar la tabla desde la copia de seguridad
        response=dynamodb.restore_table_from_backup(
            TargetTableName=new_table_name,
            BackupArn=backup_arn
        )
        print(f"EXITO: {response['TableDescription']['TableArn']}")
    except Exception as e:
        print(f"Error al restaurar la tabla: {e}")




print("Buenos dias y bienvenido a la interfaz de usuario que le permitirá interactuar con las bases\nde datos no relacionales de DynamoDb, un servicio de AWS")
region=input("Por favor, indique en qué región se encuentra (Recomendamos us-west-2): ")

while True:
    answer=int(input("Por favor, ingrese la accion que desea realizar\n\t1: Crear tablas\n\t2: Crear índices\n\t3: Calcular Unidades de lectura y escritura\n\t4: Habilitar y crear streams\n\t5: Crear tablas globales\n\t6: Realizar copias de seguridad \n\t7: Crear, Leer, Actualizar o Eliminar elementos de una tabla\n\t"))
    seguir=False
    if answer==1:
        
        region_name=region
        nombre_tabla=input("Ingrese nombre de la tabla: " )
        pk=input("Ingrese la PartitionKey de su tabla: ")
        sk=input("Ingrese el Sorkey de su tabla: ")
        creartabla(nombre_tabla,region_name,pk,sk)

    if answer==2:

        region_name=region
        GSIname=input("Ingrese el nombre del Indice Global Secundario para la tabla(GSI): ")
        nombre_tabla=input("Ingrese nombre de la tabla: " )
        pk=input("Ingrese la PartitionKey para su Indice secundario: ")
        sk=input("Ingrese el Sorkey para su Indice secundario: ")
        crear_GSI(GSIname,pk,sk,region_name,nombre_tabla)
    if answer==3:

        table_name=input("Ingrese el nombre de la tabla: ")
        region_name=region
        item_size_kb=int(input("Ingresa el tamaño promedio de los archivos de la tabla: "))
        read_rate_per_second=int(input("Ingresa las lecturas promedio por segundo: "))
        write_rate_per_second=int(input("Ingresa las escrituras promedio por segundo: "))
        consistency=input("Ingresar el tiopo de lectura (fuerte o eventual): ")
        
        actualizar_rcu_y_wcu(table_name, item_size_kb, read_rate_per_second, write_rate_per_second, consistency, region_name)
        


#table_name, item_size_kb, read_rate_per_second, write_rate_per_second, consistency='eventual', region_name='us-west-2'
    if answer==4:
        nombre_tabla=input("Ingrese el nombre de la tabla en la que desea crear streams: ")
        region=region
        habilitar_y_crear_streams(nombre_tabla,region)

    
    if answer==5:
        table_name=input("Ingrese el nombre de la tabla que desea crear: ")
        region_primaria=region
        region_replica=input("Ingrese el nombre de la región donde desea replicar la tabla creada: ")
        crear_tabla_global(table_name,region_primaria,region_replica)
    
    if answer==6:
        table_name=input("Ingrese el nombre de la tabla que desea copiar: ")
        region_dynamodb=input("Ingrese la región donde se encuentra la tabla de la que desea crear la copia de respaldo ( recomendamos us-west-2 ): ")
        crear_backup(region_dynamodb, table_name)

    if answer==7:
        operacion=input("Introduzca la operación que desea realizar, puede ser: \n\tCREATE\n\tREAD\n\tUPDATE\n\tDELETE\n\t")
        table_name=input("Nombre de la tabla cuyos elementos desea gestionar: ")
        region=input("Región donde se encuentra la tabla ( recomendamos us-west-2 ): ")
        gestionar_elemento_dynamodb(operacion,table_name,region)



    r=input("Desea continuar?: (Ingrese Sí/No)")
    if r.lower()=="sí" or r.lower()=="si":
        seguir=True
    else:
        seguir=False
        print("Muchas gracias por usar nuestro servicio")
        break
