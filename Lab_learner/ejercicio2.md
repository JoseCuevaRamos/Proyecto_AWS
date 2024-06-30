<p align="left""><img src="https://semanadelcannabis.cayetano.edu.pe/assets/img/logo-upch.png" width="150">
<h1 align="center">Ejercicio2: Conceptos clave para Amazon DynamoDB</h1>
</p>
<p>Usando AWS SDK para Python (boto3), escribir un script que cree una tabla en DynamoDB
con una clave de partición y una clave de ordenación.</p>
<hr>

<p>
Comienzo creando un cliente Dynamodb en la region us-west-2  y creamos unas variables para los nombres de la tabla y las PartitionKey y el SortKey 
</p>

```
import boto3

# Crear un cliente de DynamoDB
dynamodb = boto3.client('dynamodb', region_name='us-west-2')

# Crear la tabla
table_name = 'Tablaprueba'
partition_key = 'Id'
sort_key = 'Fecha'

```

<p>
En la siguiente parte creamos la tabla de DynamoDB en la parte de KeySchema creamos tanto la PartitionKey del KeyType "HASH" y el SorKey con el KeyType "Range" 
</p>

```
response = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {   # Clave de partición
                'AttributeName': partition_key,
                'KeyType': 'HASH'  
            },
            
            {    # Clave de ordenación
                'AttributeName': sort_key,
                'KeyType': 'RANGE' 
            }
        ],

```

<p>
En el apartado de AttributeDefinitions le asignamos el tipo de atributos a la PartitionKey y al SortKey, en este caso le ponemos "S" de string , pero tambien puede aceptar "N" de numero y "B" de binario
</p>


```
AttributeDefinitions=[
            {
                'AttributeName': partition_key,
                'AttributeType': 'S' 
            },
            {
                'AttributeName': sort_key,
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
)       

```
Al final se ejecuta el arhivo.py y se crea la base de datos

![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297438/3e60a471-325b-4608-9232-4067bb6706e3)

![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297438/22564fce-a6e9-446c-a419-67ed502bbb28)


![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297438/2c92b0b0-fcd4-428e-9870-bd1cd9aaa7d4)



