<p align="left""><img src="https://semanadelcannabis.cayetano.edu.pe/assets/img/logo-upch.png" width="150">
<h1 align="center">Ejercicio 1: Integración de DynamoDB Streams con AWS Lambda</h1>
</p>

<p>
 Integra DynamoDB Streams con AWS Lambda para procesar eventos en tiempo real
</p>

<h3>
Tareas:
</h3>

- Configura DynamoDB Streams en una tabla existente y crea una función Lambda para procesar los eventos del stream.
![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/451b5a49-2d1b-4c9a-ba00-45846bd88655)

La función Lambda tiene la siguiente estructura:
![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/d8fd9e68-84b4-494b-8ef6-595ebb551238)

Tiene como desencadenador las operaciones en DynamoDB y el siguiente código:
```
import json

def lambda_handler(event, context):
    for record in event['Records']:
        print(f"EventID: {record['eventID']}")
        print(f"EventName: {record['eventName']}")

        # Procesar la imagen del evento
        if 'NewImage' in record['dynamodb']:
            new_image = record['dynamodb']['NewImage']
            print(f"NewImage: {json.dumps(new_image, indent=2)}")

        if 'OldImage' in record['dynamodb']:
            old_image = record['dynamodb']['OldImage']
            print(f"OldImage: {json.dumps(old_image, indent=2)}")

    return {
        'statusCode': 200,
        'body': json.dumps('Procesamiento completo')
    }

```
se encarga de administrar y registrar los eventos como la creación de un nuevo item. que se puede ver en el siguiente código


- Escribe un script en Python para generar eventos en la tabla DynamoDB y desencadenar la función Lambda.
```
import boto3
from botocore.exceptions import ClientError

# Crear un cliente para DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('pruebafinalaws')

try:
    # Añadir un nuevo elemento para generar un evento
    response = table.put_item(
        Item={
            'Id': '2',     # Clave de partición
            'Date': '2024-01-01',  # Clave de clasificación, usando formato de fecha como ejemplo
            'OtherAttribute': 'Valor de prueba2'  # Otros atributos adicionales
        }
    )
    print("Elemento añadido:", response)

except ClientError as e:
    print(f"Error al manipular la tabla: {e}")

```

Donde creamos un item en la tabla para generar el evento y activar la función Lambda

![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/c94b6521-b667-404f-9a95-2d747d889223)

- Diseña y ejecuta pruebas para validar que la función Lambda procesa correctamente los eventos del stream y toma acciones específicas basadas en los datos del evento.

Podemos revisar la administración de eventos en la pesataña de monitoreo de la función Lambda gracias a Cloudwatch y sus métricas, mostrando la activación 

![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/f5009d95-8b56-4f50-8633-4a00b8e5245f)
