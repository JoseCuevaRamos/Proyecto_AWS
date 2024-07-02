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

<h2>Desarrollo</h2>

<p>
En la primera parte planificamos quen funciones vamos a usar en la interfza y de esta menera sabremos que funciones usadas previamente utilizaremos en la interfaz de usuario
</p>
<p>Funciones escogidas para la interfaz</p>
<ul>
<li>Creacion de Tablas</li>
<li>Crear Indices Secundarios</li>
<li>Calcular Unides de lectura y escritura</li>
<li>Habilitar y crear Streams </li>
<li>Crear tablas globales</li>
<li>Crear copia de seguridad</li>
<li>Crear, Leer, Actualizar o Eliminar elementos de una tabla</li>
</ul>

<p>En la segunda parte diseñamos las funciones que seran llamadas en la interfaz teniendo en cuenta los codigos generados en los ejercicios anteriores , ajustamos los codigo para que sean llamados como funcion</p>

<p>Iniciamos importando las librerias que vasmo a usar en nuestor codigo , estas librerias son las que sabemos que hemos utilizado en nuestros codigos anteriores</p>

```
import boto3
from botocore.exceptions import ClientError
from time import sleep
import datetime
```

<p>La primera fucnion que creamos es la funcion para crear tabla que fue adaptada de el ejercicio numero 2 en la cual tiene como argumento de entrada el nombre de la tabla nueva , la partitionkey y la sortkey de la nueva tabla </p>

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

<p>Para la segunda funcion adaptamos la funcion creada en el ejercicio numeor 3 para crear indice secundarios globales, esta funcion tiene como argumento El nombre del indice que se va aa crear , nueva partitionkey y sortkey para el nuevo indice y la tabla a la que se va a crear el indice secundario </p>

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

<p>Para la tercera funcion en la que calcularemos los RCU y WCU utilizando las funciones del ejercicio 5 en la cual creamos dos funciones una para clacular el WCU y otra para calcular RCU para finalmente actualizar los parametros en la tabla. Esta funcion va a tener como argumento el nombre de la tabla a la que se le van a hacer los cambios , el perso promedio de los itemas en KB , el read rate per second , el write rate per second , la consistencia de lectura </p>

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

