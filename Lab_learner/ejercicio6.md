<p align="left""><img src="https://semanadelcannabis.cayetano.edu.pe/assets/img/logo-upch.png" width="150">
<h1 align="center">Ejercicio 6: Streams y tablas globales</h1>

<h3>Streams</h3>
<ul>
<li>Habilita streams en la tabla y escribir un script para procesar los eventos del stream.</li>
</ul>
<h2>Respuesta</h2>

### ¿Qué es un Stream en Amazon?

son los flujos de registros de cambios de datos en una base de datos DynamoDB, gracias a este flujo podemos llevar registro de los cambios como eliminaciones, inserciones o actualizaciones de items en una tabla.

En el escript, comenzamos con la creación de un cliente de dynamodb en la región us-west-2
```
response= dynamodb.update_table(
        TableName=table_name,
        StreamSpecification={
            "StreamEnabled":True, # Cambiamos el estado del stream a Activado
            "StreamViewType":"NEW_AND_OLD_IMAGES" #especificamos el tipo de dato usado
        }
    )
```
activamos el stream con el valor de True y establecemos el tipo de dato en NEW_AND_OLD_IMAGES
<br>
Luego creamos el cliente de DynamoDB Streams
```
dynamodbstreams = boto3.client('dynamodbstreams', region_name='us-west-2') #creamos un cliente de dynamostreams
```

Luego, extraemos el Amazon Resource Name (ARN), que actúa como identificador único para nuestro recurso, el ARN, podiendo usarlo para establecer políticas de seguridad o identificar diversos recursos para su configuración a través de APIs
```
stream_arn = response['Table']['LatestStreamArn']
```
Luego usamos el ARN para obtener detalles mediante la función "describe stream"  y lo acumulamos en una variable

```
response = dynamodbstreams.describe_stream(StreamArn=stream_arn)
stream_description = response['StreamDescription']
```

### Shards:

Son particiones de datos que contienen un conjunto de registros de cambios de la tabla DynamoDB

### Shard Iterator:
Es un puntero que indica la posicón donde se deben leer los registros 

En el código, identificamos los shards, guardamos sus IDs y las usamos para encontrar los registros en nuestro stream, guardándolos en la variable "records"

```
while True:
        response = dynamodbstreams.get_records(ShardIterator=shard_iterator)
        records = response['Records']
        if records:
            print("Records:")
            for record in records:
                print(record)

        # Obtenemos el siguiente iterador
        shard_iterator = response['NextShardIterator']

        # Pausamos un poco antes de la próxima lectura
        sleep(5)
```

![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/3a3ce04b-f0bf-4cc0-8ea0-378c37725156)





## Tabla global:

Para la creación de una tabla global, seguiremos usando el SDK boto3,
creando 2 diferentes clientes en las regiones,
```
dynamodb_us_west_2 = boto3.client('dynamodb', region_name='us-west-2')
dynamodb_us_east_1 = boto3.client('dynamodb', region_name='us-east-1')
```
configurando los atributos del tipo string
```
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
```
y con un una capacidad de lectura y escritura establecida en 5 en ambos casos. 
```
ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
}
```

Para, finalmente, asociar la tabla como una tabla global asignando la región de us-east-1 como secundaria garantizando la replicación entre tablas.

```
dynamodb_us_west_2.update_table(
        TableName=table_name,
        ReplicationGroup=[
            {
                'RegionName': 'us-east-1'
            }
        ]
    )

```



![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/4e0da43f-9d64-4e44-9657-24b2f1b499b3)

![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/cded0c97-87f4-4a7b-a162-e885a852d1b4)
