<p align="left""><img src="https://semanadelcannabis.cayetano.edu.pe/assets/img/logo-upch.png" width="150">
<h1 align="center">Proyecto Final</h1>

<h2>
Objetivos
</h2>
<ul>
<li>Desarrolla un sistema completo que integre todas las funcionalidades anteriores en un solo
proyecto.</li>
<li>Incluye una interfaz de usuario simple para interactuar con la base de datos DynamoDB.</li>
<li>Prepara una documentación detallada del código y el proceso de desarrollo.</li>
<li>Realiza una presentación del proyecto, destacando los desafíos enfrentados y las soluciones
implementadas</li>
</ul>
<h2> Tutorial de instalación de boto3 </h2>
Para el desarrollo de este proyecto, incluyeendo los ejercicios, hacemos uso del Software Developer Kit Boto3, que nos permite interactuar con AWS a partir de código usando las funciones y creación de clientes incluídas en la API de Python que provee Boto3. Además, haremos uso del entorno Cloud9, que aprovecha la sesión iniciada del usuario de AWS para obtener las credenciales automáticamente, proveyendo estas mismas al SDK para su correcto funcionamiento.

- Pasos para la instalación de boto3 en el entorno Cloud9
  - Iniciamos el IDLE de Cloud9 con la configuración estándard, salvo la configuración de red que será establecida en **Secure Shell (SSH)**
  - En la terminal, ejecutamos el comando *cat ~/.aws/credentials* para verificar que contemos con nuestro access key, secret access key, token y región
  - Una vez verificamos que se obtuvieron las credenciales correctamente, instalamos Boto 3 con el siguiente comando
    ```
    pip install boto3
    ```
    y verificamos la instalación con el comando
    ```
    pip show boto3
    ```
    obteniendo el siguiente resultado
    
    ![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/350299e8-b58d-4b75-be7b-a95c9daba9fe)

    


 
<h2>Desarrollo</h2>
<p>
    Primero, saludamos al usuario y le pedimos que ingrese la región en la que desea trabajar (en este caso, recomendamos us-west-2 por cuestiones de permisos en la cuenta de AWS con la que trabajamos).
</p>
<p>
Luego, planificamos qué funciones vamos a usar en la interfaz y de esta menera sabremos qué funciones usadas previamente utilizaremos en la interfaz de usuario
</p>
<p>Funciones escogidas para la interfaz</p>
<ul>
<li>1.- Creación de Tablas</li>
<li>2.- Crear Índices Secundarios</li>
<li>3.- Calcular Unides de lectura y escritura</li>
<li>4.- Habilitar y crear Streams </li>
<li>5.- Crear tablas globales</li>
<li>6.- Crear copia de seguridad</li>
<li>7.- Crear, Leer, Actualizar o Eliminar elementos de una tabla</li>
</ul>

<p>En la segunda parte diseñamos las funciones que seran llamadas en la interfaz teniendo en cuenta los códigos generados en los ejercicios anteriores, ajustamos los código para que sean llamados como funciones y reciban como input las diferentes acciones que se deben realizar o se especifiquen regiones secundarias para tablas globales</p>

<p>Iniciamos importando las librerias que vamos a usar en nuestro código, estas librerías son las que sabemos que hemos utilizado en nuestros códigos anteriores</p>

```
import boto3
from botocore.exceptions import ClientError
from time import sleep
import datetime
```

<p>La primera función que creamos es la función para crear tabla que fue adaptada del ejercicio número 2 en la cual tiene como argumento de entrada el nombre de la tabla nueva, la partitionkey y la sortkey de la nueva tabla </p>

```
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
```

<p>Para la segunda funcion adaptamos la funcion creada en el ejercicio numero 3 para crear índices secundarios globales, esta funcion tiene como argumento el nombre del índice que se va aa crear, nueva partitionkey y sortkey para el nuevo índice y la tabla a la que se va a crear el índice secundario </p>

```
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


```

<p>Para la tercera función en la que calcularemos los RCU y WCU utilizando las funciones del ejercicio 5 en el cual creamos dos funciones, una para clacular el WCU y otra para calcular RCU. Para, finalmente, actualizar los parámetros en la tabla. Esta función va a tener como argumento el nombre de la tabla a la que se le van a hacer los cambios, el peso promedio de los itemas en KB, el read rate per second, el write rate per second y la consistencia de lectura </p>

```
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
    wcu_per_write = 1 if item_size_kb <= 1 else (item_size_kb // 1)
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

```
<p>En La siguiente función se usa para poder habilitar y crear streams en la tabla escogida, esta función toma como argumentos el nombre de la tabla a la que se deben crear el streams, primero se encarga de activar los streams en la tabla (que están desactivados por defecto) para luego leer los registros del stream, de manera que registre los cambios en la tabla
</p>

```
def habilitar_y_crear_streams(nombre_tabla, region):
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

```

<p>
En la función de crear tablas globales, recibimos como atributo la región previamente establecida, añadiendo el nombre de la tabla y la región en que queremos replicar dicha tabla, habilitamos también los streams y creamos la tabla de manera regular, esperando a que su creación se complete, para crearla finalmente en la región réplica (us-east-1)
</p>

```
def crear_tabla_global(table_name, region_primaria, region_replica):
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
```

<p>
Ingresar Lo de gestionar elemnto
</p>

```
def gestionar_elemento_dynamodb(operacion,table_name,region):
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
```

<p>La ultima funcion es la funcion backup la cual usara el codigo creado en el ejercicio numero 7. En esta funcion usaremos el nombre de la tabla como argumento para crearle una copia de seguridad </p>

```

def crear_backup(region_dynamodb, table_name):
    # Crear clientes de DynamoDB y Backup
    dynamodb = boto3.client('dynamodb', region_name=region_dynamodb)

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
```


<p>
En la parte final parte vamos a definir la interfaz que vamos a usar para interacturar con las funciones,usamos el nombre de la funcion y que funciones vamos a usar en cada eleccion del usuario.En esta parte tambien definimos que informacion se le va  a pedir al usuario que ingrese para poder realizar las acciones.

</p>

```
print("Buenos dias y bienvenido a la interfaz de usuario que le permitirá interactuar con las bases\nde datos no relacionales de DynamoDb, un servicio de AWS")

while True:
    answer=int(input("Por favor, ingrese la accion que desea realizar\n\t1: Crear tablas\n\t2: Crear índices\n\t3: Calcular Unidades de lectura y escritura\n\t4: Habilitar y crear streams\n\t5: Crear tablas globales\n\t6: Realizar copias de seguridad \n\t7: Crear, Leer, Actualizar o Eliminar elementos de una tabla\n\t"))
    seguir=False
    if answer==1:
        
        region_name=input("Ingrese la region (recomendamos us-west-2): ")
        nombre_tabla=input("Ingrese nombre de la tabla: " )
        pk=input("Ingrese la PartitionKey de su tabla: ")
        sk=input("Ingrese el Sorkey de su tabla: ")
        creartabla(nombre_tabla,region_name,pk,sk)

    if answer==2:

        region_name=input("Ingrese la region de la tabla: ")
        GSIname=input("Ingrese el nombre del Indice Global Secundario para la tabla(GSI): ")
        nombre_tabla=input("Ingrese nombre de la tabla: " )
        pk=input("Ingrese la PartitionKey para su Indice secundario: ")
        sk=input("Ingrese el Sorkey para su Indice secundario: ")
        crear_GSI(GSIname,pk,sk,region_name,nombre_tabla)
    if answer==3:

        table_name=input("Ingrese el nombre de la tabla: ")
        region_name=input("Region de la tabla: ")
        item_size_kb=int(input("Ingresa el tamaño promedio de los archivos de la tabla: "))
        read_rate_per_second=int(input("Ingresa las lecturas promedio por segundo: "))
        write_rate_per_second=int(input("Ingresa las escrituras promedio por segundo: "))
        consistency=input("Ingresar el tiopo de lectura (fuerte o eventual): ")
        
        actualizar_rcu_y_wcu(table_name, item_size_kb, read_rate_per_second, write_rate_per_second, consistency, region_name)
        


#table_name, item_size_kb, read_rate_per_second, write_rate_per_second, consistency='eventual', region_name='us-west-2'
    if answer==4:
        nombre_tabla=input("Ingrese el nombre de la tabla en la que desea crear streams: ")
        region=input("Ingrese una región ( recomendamos us-west-2 ): ")
        habilitar_y_crear_streams(nombre_tabla,region)

    
    if answer==5:
        table_name=input("Ingrese el nombre de la tabla que desea crear: ")
        region_primaria=input("Ingrese el nombre de la región primaria en que desea crear la tabla: ")
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
        

```

