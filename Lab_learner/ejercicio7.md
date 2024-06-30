<p align="left""><img src="https://semanadelcannabis.cayetano.edu.pe/assets/img/logo-upch.png" width="150">
<h1 align="center">Ejercicio 7:Backup y restauración</h1>
</p>


<h3>Copias de seguridad y restauración</h3>
<ul>
<li>Implementa scripts para realizar copias de seguridad automáticas de la tabla y restaurarlas en caso de necesidad.</li>
</ul>
<h2>
Teoria
</h2>
<p>
Las copias de seguridad (backups) y la restauración (restoration) son fundamentales para la administración de bases de datos debido a varias razones:
</p>
<ul>
<li>Los datos se pueden perder debido a errores humanos, fallos de hardware, ataques maliciosos,etc. Las copias de seguridad aseguran que puedas recuperar los datos en caso de pérdida</li>
<li>En caso de desastres o fallos en el centro de datos las copias de la base de datos te permiten restaurar la base de datos a un estado anterior</li>
<li>Son útiles cuando necesitas migrar datos a una nueva región o cuenta de AWS</li>
</ul>
<h2>SCRIPT</h2>

<p>
En el siguiente código vamos a crear un backup para la tabla creada anteriormente, esta será ubicada en la misma región y se añadirá a la tabla con el método 'create_backup' donde necesita el nombre de la tabla y el nombre de backup que lo creamos usando la fecha y hora actual para hacerlo único.
</p>

```
import boto3
import datetime

#crear un cliente de DynamoDB y de Backup
dynamodb = boto3.client('dynamodb', region_name='us-west-2')
backup = boto3.client('backup', region_name='us-west-2')

#nombre de la tabla
table_name = 'Tablaprueba'

#crear una copia de seguridad con un nombre único basado en la fecha y hora actual
backup_name = f"backup_{table_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

try:
    response = dynamodb.create_backup(
        TableName=table_name,
        BackupName=backup_name
    )
    print(f"Exito: {response['BackupDetails']['BackupArn']}")
except Exception as e:
    print(f"Error: {e}")
```

![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297438/4edb92eb-fa0e-490a-b864-2dff08b3e320)

![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297438/400023cd-1478-453f-b725-1480985931b3)


<p>
Posteriormente tenemos un codigo para restaurar la tabla desde una copia de seguridad
</p>

```
import boto3

#crear un cliente de DynamoDB
dynamodb = boto3.client('dynamodb', region_name='us-west-2')

#ARN de la copia de seguridad a restaurar
backup_arn = 'arn:aws:dynamodb:us-west-2:123456789012:table/Tablaprueba/backup/01534567891011-1234abcd'

#Nombre de la nueva tabla a crear desde la copia de seguridad
new_table_name = 'Tablaprueba_Restored'

try:
    response = dynamodb.restore_table_from_backup(
        TargetTableName=new_table_name,
        BackupArn=backup_arn
    )
    print(f"EXITO: {response['TableDescription']['TableArn']}")
except Exception as e:
    print(f"Error: {e}")
```
<p>
En esta parte final creamos un script para usarlo en conjunto con AWS Lambda la cual no ayudará a automatizar el proceso de creación de copias de seguridad. Subimos el codigo a lambda y configuramos el EventBridge que nos permitará crear una regla para que el código se ejecute cuando deseemos por ejemplo una vez al día.
</p>

```
import boto3
import datetime

def crear_copia_de_seguridad(event, context):
    dynamodb = boto3.client('dynamodb', region_name='us-west-2')
    table_name = 'Tablaprueba'
    backup_name = f"backup_{table_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

    try:
        response = dynamodb.create_backup(
            TableName=table_name,
            BackupName=backup_name
        )
        print(f"Copia de seguridad creada con éxito: {response['BackupDetails']['BackupArn']}")
    except Exception as e:
        print(f"Error al crear la copia de seguridad: {e}")

```
