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