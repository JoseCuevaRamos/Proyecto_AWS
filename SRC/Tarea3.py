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

def leer(region):  # READ
    key={
        "Id":{"S":"EstoesotrapruebaGLOBAL2"},
        "Fecha":{"S":"2024-01-01"}
    }
    
    dynamodb=dynamodb_west if region=='us-west-2' else dynamodb_east
    try:
        response=dynamodb.get_item(
            TableName=table_name,
            Key=key
        )
        
        if 'Item' in response:
            item=response['Item']
            print(f"Elemento encontrado en {region}:",item)
        else:
            print(f"Elemento no encontrado en {region}.")
    except ClientError as e:
        print(f"Error al leer el elemento en {region}:",e)
    except Exception as e:
        print(f"Ocurrió un error inesperado en {region}:",e)

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

def eliminar():  # DELETE
    key = {
        "Id":{"S":"EstoesotrapruebaGLOBAL2"},
        "Fecha":{"S":"2024-01-01"}
    }
    
    try:
        response = dynamodb_west.delete_item(
            TableName=table_name,
            Key=key
        )
        print("Elemento eliminado exitosamente en us-west-2.")
    except ClientError as e:
        print("Error al eliminar el elemento:",e)
    except Exception as e:
        print("Ocurrió un error inesperado:",e)

# Ejecutar las operaciones en us-west-2
crear()

# Verificar la replicación leyendo en ambas regiones
leer('us-west-2')
leer('us-east-1')

# Puedes descomentar las siguientes líneas para actualizar o eliminar el elemento
# actualizar()
# leer('us-west-2')
# leer('us-east-1')
# eliminar()
# leer('us-west-2')
# leer('us-east-1'