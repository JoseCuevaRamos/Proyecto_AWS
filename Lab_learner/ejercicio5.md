<p align="left""><img src="https://semanadelcannabis.cayetano.edu.pe/assets/img/logo-upch.png" width="150">
<h1 align="center">Ejercicio 5: Indices secundarios Throughput de lectura/escritura y cálculo de RCU y WCU</h1>

<h3>Cálculo de unidades de capacidad</h3>
<ul>
<li>Escribe un script para calcular las Unidades de Capacidad de Lectura (RCU) y Escritura (WCU)
basándose en el tamaño de los ítems y la tasa de acceso.</li>
</ul>
<h2>Respuesta</h2>

<p>
En AWS DynamoDB, la capacidad de lectura y escritura de una tabla se mide en unidades de capacidad, conocidas como Read Capacity Units(RCU) y Write Capacity Unit(WCU). Estas unidades determinan cuantas operaciones de lectura y escritura se pueden realizar por segundo en la tabla y son cruciales para dimensionar y optimizar el rendimiento y el costo de la base de datos. 
</p>
<p>
RCU representa una lectura consistente fuerte  y lectura eventual consistente.
</p>
<p>Lectura consistente fuerte</p>
<ul>
<li>Garantiza que leerás la última versión del ítem</li>
<li>Una lectura consistente fuerte de hasta 4KB consume 1RCU  y si el tamaño es mayor es necesario redondear al siguiente múltiplo de 4KB</li>
</ul>
<p>
Lectura eventual consistente
</p>

<ul>
<li>No garantiza que siempre leerás la última version de un Item pero ofrece mayor capacidad de lectura
</li>
<li>Una lectura consistente fuerte de hasta 4KB consume 0.5RCU  y si el tamaño es mayor es necesario redondear al siguiente múltiplo de 4KB
</li>
</ul>
<p>
WCU representa una escritura por segundo para un ítem hasta 1KB de tamaño
</p>
</p>
<ul>
<li>Escritura hasta 1KB consume 1 WCU</li>
<li>Si el tamaño de ítem es mayor de 1KB consume 1RCU  y si el tamaño es mayor es necesario redondear al siguiente múltiplo de 1 KB</li>
</ul>
<h2>
SCRIPT
</h2>
<p>
En esta primera parte creamos dos funciones con las que vamos a calcular el RCU y el WCU en la parte de RCU utilizamos el tamaño promedio de los item en KB , el numero de escrituras por segundo y la consistencias entre eventual y fuerte. Por otra parte en el WCU utilizamos el mismo tamaño promedio y el numero de escrituras por segundo
</p>

```
import boto3

def calculate_rcu(item_size_kb, read_rate_per_second, consistency='eventual'):
    #calcula las Unidades de Capacidad de Lectura(RCU) necesarias
    if consistency == 'fuerte':
        #Lectura consistente fuerte
        rcu_per_read = 1 if item_size_kb <= 4 else (item_size_kb // 4) + 1
    else:
        #lectura eventualmente consistente
        rcu_per_read = 0.5 if item_size_kb <= 4 else (item_size_kb // 4) / 2
    
    total_rcu = rcu_per_read * read_rate_per_second
    return total_rcu

def calculate_wcu(item_size_kb, write_rate_per_second):
    #Calcula las Unidades de Capacidad de Escritura (WCU) necesarias
    wcu_per_write = 1 if item_size_kb <= 1 else (item_size_kb // 1) + 1
    total_wcu = wcu_per_write * write_rate_per_second
    return total_wcu

#Datos de entrada
item_size_kb = 3  #tamaño promedio de los ítems en KB
read_rate_per_second = 10  #numero de lecturas por segundo
write_rate_per_second = 5  #numero de escrituras por segundo
consistency = 'eventual'  #tipo de consistencia de lectura: 'eventual' o 'fuerte'

rcu = calculate_rcu(item_size_kb, read_rate_per_second, consistency)
wcu = calculate_wcu(item_size_kb, write_rate_per_second)
```
<p>
En la siguienmte parte usamos los datos calculados previamente para actualizarlos en la tabla con el metodo 'update_table' 
</p>

```
dynamodb = boto3.client('dynamodb', region_name='us-west-2')

#configurar el autoescalado para la tabla
table_name = 'Tablaprueba'

#Ajustar las capacidades provisionadas segun los calculos
try:
    response = dynamodb.update_table(
        TableName=table_name,
        ProvisionedThroughput={
            'ReadCapacityUnits': int(rcu),
            'WriteCapacityUnits': int(wcu)
        }
    )
    print("Exito:", response)
except Exception as e:
    print("Error", e)

```
