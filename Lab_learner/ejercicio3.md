<p align="left""><img src="https://semanadelcannabis.cayetano.edu.pe/assets/img/logo-upch.png" width="150">
<h1 align="center">Ejercicio 3:Particiones y distribución de datos</h1>

<p>Investigar cómo DynamoDB distribuye los datos en particiones y cómo esto afecta el
rendimiento.</p>
<ul>
<li>Crea un script que inserte datos en la tabla y analice cómo se distribuyen las
particiones.</li>
</ul>
<hr>
<h2>Respuesta</h2>
<p>DynamoDB distribuye los datos en particiones logicas, donde cada particion es una unidad de escalado independiente ademas cada particion tiene su propia capacidad de lectura y escritura por segundo asignada , basada en el volumen de datos y el rendimiento provisionado</p>
<p>
Cada item almacenado en DynamoDb deber tener una clave de particion unica.Esta particion determina dond ese almacenara fisicamente el item .
</p>
<p>
DynamoDb usa un algoritmo interno para distibuir los items entre las particiones disponibles uniformemente.
</p>
<p>
¿Como impacta al rendimiento?
</p>
<ul>
<li>Puede escalar horinzontalmete distribuyendo particiones entre los multiples nodos de almacenamiento segun sea necesario</li>
<li>Asignar  capacidades de rendimiento a nivel de particion puede generar un rendimiento predecible para las operaciones de lectura y escritura</li>
<li>En una distribucion desigual puede generar hot partitions, en donde una particion experimenta una carga de trabajo desproporcionalmente alta en comparacion con otras.Esto puede generar latencias altas y afectar el rendimiento de las tablas</li>
</ul>
<hr>
<h2>
Script
</h2>
<p>
Comienzo creando un cliente de DynamoDB en las region us-west-2
</p>
<p>Creo las variables que usare para crear el nuevo item por ejemplo : uso la tabla creada en el ejercicio anterior , de esta manera necesito el nombre de la tabla , el PartitionKey , SortKey que en este caso son Id y Fecha</p>

```
import boto3

#Crear un cliente de DynamoDB en la región usada
dynamodb = boto3.client('dynamodb', region_name='us-west-2')

#tabla existente en DynamoDB
table_name = 'Tablaprueba'

# Claves de partición y ordenación de tu ítem
partition_key_value = '123'  #valor para la clave de partición 'Id'
sort_key_value = '2024-06-30'  # valor para la clave de ordenación 'Fecha'

```
<p>
Luego creo la item que se desea agregar a la tabla y probamos añadiendo un atributo adicional en la estructura del item
</p>


```
item = {
    'Id': {'S': partition_key_value},
    'Fecha': {'S': sort_key_value},
    'Estado': {'S': 'Activo'}  #añadir otros atributro a la tabla
}


```
<p>
Insertamos el item creado  con la funcion "put_item" el cual acepta el nombre de tabla y el item.
</p>

```
try:
    response = dynamodb.put_item(
        TableName=table_name,
        Item=item
    )
    print("se añadio con exito", response)
except Exception as e:
    print("Error :", e)

```