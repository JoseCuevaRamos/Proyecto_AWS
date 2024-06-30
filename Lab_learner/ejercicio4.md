<p align="left""><img src="https://semanadelcannabis.cayetano.edu.pe/assets/img/logo-upch.png" width="150">
<h1 align="center">Ejercicio 4: Indices secundarios</h1>

<li>Crea un índice secundario global (GSI) en la tabla para permitir consultas eficientes en
atributos no clave.</li>
<li>Escribe un script para crear y consultar el GSI.</li>
</ul>
<hr>
<h2>
Respuesta
</h2>
<h3>
Indice Secundario Global(GSI)
</h3>
<p>
Un indice global secundario es una estructura que nos permite realizar consultas mas eficientes  y flexibles en las tablas de Dynamodb.Estos indices permiten definir un esquema de claves diferentes al de la tabla base, lo que fecilita realizar consultas usando diferentes atributos como claves de particion sin modificar el diseño de la tabla principal
</p>
<h2>Script</h2>

<p>
Primero creamos el clinete dynamodb  y creamos variables con los nombres que vamos a usar para crear el GSI como lo son el nombre del GSI , el nombre del nuevo PartitionKey y el nuevo SortKey
</p>

```
import boto3
#Crear un cliente dynamodb
dynamodb=boto3.client('dynamodb' , region_name='us-west-2')
#nombre de la tabla creada anteiormente
table='Tablaprueba'

#definimos un CSI

GSI= 'Index_GSI'
pk='Costo'
sk='Tipo'

```
<p>
Despues usamos el metodo 'update_table' para añadirle mas atributos a nuestra tabla los cuales vamos a udar como el partitionkey y el sortkey de nuestro indice secundario global.
</p>

```
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
```
<p>
En la siguiente parte de GlobalSecondaryIndexUpdates en donde vamos a crear el nuevo GSI  usaremos la varaible GSI para el nombre y los atributos recien creados seran usados como partitionkey y sortkey del nuevo index
</p>

```
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
```
<p>
Quiero hacer enfasis en esta parte en la que se especifica que atributos de la tabla deben ser proyectados  en el indice. En este caso usamos 'ALL' en el cual estamos incluyendo todos los atributos , pero tambien existe 'KEYS_ONLY' en la que solo los atributos que conforman la clave primaria forman parte del indice. Tambien existe el 'INCLUDE' y 'NonKeyAttributes' en la que tenemos que seleccionar los atributos que queremos.

</p>

```
'Projection': {
    'ProjectionType': 'ALL'
}
```

