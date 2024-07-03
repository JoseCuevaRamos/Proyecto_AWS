<p align="left""><img src="https://semanadelcannabis.cayetano.edu.pe/assets/img/logo-upch.png" width="150">
<h1 align="center">Ejercicio 3: Creación y gestión de tablas globales</h1>
</p>

<p>
 Implementa y gestiona tablas globales en DynamoDB para replicar datos entre diferentes regiones.
</p>

<h3>
Tareas
</h3>

### Investiga cómo funcionan las tablas globales en DynamoDB y sus casos de uso.

+ Las tablas globales nos permiten replicar el contenido de una tabla en múltiples regiones (en el caso de este ejercicio, entre us-west-2 y us-east-1) para poder asegurar la redundancia y almacenamiento distribuido para asegurar la alta disponibilidad
   - Al ser una base de datos NoSQL, se considera la consistencia eventual, garantizando que llegue un punto de sincronización, mas no se asegura que sea al mismo instante de la actualización de una tabla
   - Para garantizar la evasión de conflictos, se usa la política "las writer wins" tomando como "ganador" a la tabla que se actualizó más reciéntemente, para pasar a su replicación
+ Casos de aplicación:
  - Aplicaciones de múltiples regiones: aseguramos que al tener la información duplicada en distintas regiones, los usuarios de diferentes puntos geográficos tengan acceso a una copia cercana, disminuyendo la latencia
  - Aplicaciones de recuperación de desastres: las réplicas dan una seguridad de no perder datos si ocurre un inconveniente en una de las regiones
    

### Crea una tabla global que replique datos entre al menos dos regiones.
```
import boto3
from botocore.exceptions import ClientError

# Crear clientes de DynamoDB para ambas regiones
dynamodb_west=boto3.client('dynamodb',region_name='us-west-2')
dynamodb_east=boto3.client('dynamodb',region_name='us-east-1')

# Nombre de la tabla global
table_name='TablapruebaGlobalfinal'

def crear():  # CREATE
    item={
        "Id":{"S": "EstoesotrapruebaGLOBAL2"},
        "Fecha":{"S": "2024-01-01"},
        "Estado":{"S": "Activo"},
        "Nombre":{"S": "Ejemplo"},
        "Edad":{"N": "25"},
        "Correo":{"S": "ejemplo@example.com"}
    }
    
    try:
        response=dynamodb_west.put_item(
            TableName=table_name,
            Item=item
        )
        print("Elemento creado exitosamente en us-west-2:",response)
    except ClientError as e:
        print("Error al crear el elemento:",e)
    except Exception as e:
        print("Ocurrió un error inesperado:",e)
crear()
```

### Escribe un script en Python para insertar datos en la tabla y verificar la replicación entre regiones.

```
def actualizar():  # UPDATE
    key = {
        "Id":{"S":"EstoesotrapruebaGLOBAL2"},
        "Fecha":{"S":"2024-01-01"}
    }
    update_expression="SET Nombre = :n, Edad = :e, Correo = :c"
    expression_attribute_values={
        ":n":{"S":"Nuevo Ejemplo"},
        ":e":{"N":"31"},
        ":c":{"S":"nuevo_ejemplo@example.com"}
    }
    
    try:
        response=dynamodb_west.update_item(
            TableName=table_name,
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        print("Elemento actualizado exitosamente en us-west-2:",response)
    except ClientError as e:
        print("Error al actualizar el elemento:",e)
    except Exception as e:
        print("Ocurrió un error inesperado:",e)
actualizar()

```

El código inserta y actualiza datos en una de las regiones y, automáticamente, la replica en la otra región asociada como réplica

### Analiza el impacto de la replicación en el rendimiento y la consistencia de los datos

La replicación impactó de ran manera el rendimiento y la consistencia de datos ya que la redundancia de datos en múltiples regiones infliuye en que los usuarios, independientemente de su ubicación geográfica tengan acceso con baja latencia a diferentes tablas de dynamodb

Esta latencia reducida para usuarios ayuda también a que ellos trabajen en sus propias regiones, encargándose la base de datos misma de su replicación, mejorando la eficiencia y el flujo de trabajo ya que los desarolladores solo se encargan de realizar sus actividades sin pensar en crear réplicas manuales en las regiones donde trabaje el resto de su equipo
El procesamiento distribuido globalmente que propone una tabla global es inmensamente apreciado por los equipos de trabajo, pues mejora en gran medida su rendimiento. Sin embargo, también puede implicar un mayor costo en la red pues el tráfico adicional generado es tomado en cuenta por el modelo de pago por uso, también se considera que esta replicación no es instantánea y estos retrasos pueden afectar la consistencia de datos de manera temporal al sobreescribirse cambios, pero finalmente, se llega a un estado de consistencia eventual.

Existen diferentes formas de gestionar la inconsistencia, como la política "last writer wins" mencionada anteriormente, evitando así las escrituras concurrentes que aparecen mientras una actualización no ha sido propagada completamente.


