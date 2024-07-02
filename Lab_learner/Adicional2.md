<p align="left""><img src="https://semanadelcannabis.cayetano.edu.pe/assets/img/logo-upch.png" width="150">
<h1 align="center">Ejercicio2: Implementación de un sistema de backup y restauración</h1>
</p>

<p>
 Desarrolla un sistema automatizado de backup y restauración para una tabla
DynamoDB.
</p>

<h3>
Tareas
</h3>

<ul>
<li>Investiga las opciones disponibles para realizar copias de seguridad y restauraciones en
DynamoDB.</li>
<li>Implementa un script en Python que realice copias de seguridad periódicas de una tabla
DynamoDB</li>
<li>Diseña un procedimiento para restaurar la tabla desde una copia de seguridad en caso de
pérdida de datos</li>
<li>Realiza pruebas de recuperación de desastres para evaluar la efectividad y la velocidad del
sistema de restauración.</li>
</ul>
<h2>Script
</h2>
<p>
Para la primera parte del ejercicio creamos una funcion lambda que nos va a ayudar a que el codigo de creacion de copia de seguridad. En esta funcion Lambda ponemos el codigo adaptado del ejercico 7 paa la funcion lambda. Finalmente le ponemos un trigger que va a ser el detonante de el evento . En este caso ya que queremos que se cree una copia de seguridad cada dia a la misma hora usamos el eventBridge (CloudWatch Events) para crear un evento acada dia que active el lambda
</p>

```
import boto3
import datetime

def lambda_handler(event, context):
    # Crear un cliente de DynamoDB y de Backup
    dynamodb = boto3.client('dynamodb', region_name='us-west-2')
    backup = boto3.client('backup', region_name='us-west-2')

    # Nombre de la tabla
    table_name = 'Tablaprueba'

    # Crear una copia de seguridad con un nombre único basado en la fecha y hora actual
    backup_name = f"backup_{table_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

    try:
        response = dynamodb.create_backup(
            TableName=table_name,
            BackupName=backup_name
        )
        return {
            'statusCode': 200,
            'body': f"Exito: {response['BackupDetails']['BackupArn']}"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {e}"
        }


```
![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297438/c0878c10-48b4-4475-a611-a926437f5010)

![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297438/cce19f1c-519c-40ce-859e-740429d74dd5)

![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297438/20bd62e2-aa3f-480f-8d66-01261e440ce2)





<p>
Para la segunda parte del ejercicio tenemos que crear un sistema de restauracion en caso de que exista perdida de datos. Para esto Creamos una funcion lambda en la cual vamos a adaptar el codigo creado en la parte 7 para restaurar una copia de seguridad,a este lambda le pondremos como trigger el dynamodb, ya que queremos que se la restauracion se active cuando se elimine un elemento de la base de datos(de esta maner simulando la perdidad de datos). Para esto primero que todo tenemos que activar stream en nuestra tabla de dynamodb
</p>

```

import boto3
import time

def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb', region_name='us-west-2')
    
    backup_arn = 'arn:aws:dynamodb:us-west-2:983477961749:table/Tablaprueba/backup/01719901842190-1c1f39de'
    new_table_name = 'Tablaprueba_Restored2223'
    
    # Verificar si el evento es una eliminación
    for record in event['Records']:
        if record['eventName'] == 'REMOVE':
            try:
                response = dynamodb.restore_table_from_backup(
                    TargetTableName=new_table_name,
                    BackupArn=backup_arn
                )
                
                new_table_arn = response['TableDescription']['TableArn']
                
                while True:
                    status_response = dynamodb.describe_table(TableName=new_table_name)
                    table_status = status_response['Table']['TableStatus']
                    if table_status == 'ACTIVE':
                        break
                    time.sleep(5)  # Esperar 5 segundos antes de verificar nuevamente
                
                return {
                    'statusCode': 200,
                    'body': f"EXITO: {new_table_arn}"
                }
            except Exception as e:
                return {
                    'statusCode': 500,
                    'body': f"Error: {e}"
                }
    
    return {
        'statusCode': 200,
        'body': "No se detectaron eliminaciones"
    }



```

![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297438/7bcdc889-4b43-41e1-b396-524e0fe165bf)
![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297438/ad3e425e-766b-430f-955a-38a6b4dccef9)
![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297438/5af7dc15-9359-43b0-b7dc-7043153b7da2)
