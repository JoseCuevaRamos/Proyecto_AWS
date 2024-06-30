import boto3
from botocore.exceptions import ClientError

# Creamos un cliente de DynamoDB
dynamodb=boto3.client('dynamodb', region_name='us-west-2')


table_name='Tablaprueba'


def crear():  #CREATE
    item={ # Definimos el elemento que insertaremos en la tabla 
        "Id":{"S":"Estoesotraprueba"},
        "Fecha":{"S":"2024-01-01"},
        "Estado":{"S":"Activo"},
        "Nombre":{"S":"Ejemplo"}, #con atributos extra que no seguirán la estructura del elemento anteriormente creado
        "Edad":{"N":"25"},
        "Correo":{"S":"ejemplo@example.com"}
        }
    
    try:
        response=dynamodb.put_item( #la función put_item agrtegará el elemento con los atributos definidos
            TableName=table_name,
            Item=item
            )
        print("Elemento creado exitosamente:",response)
    except ClientError as e:
        print("Error al crear el elemento:",e)
    except Exception as e:
        print("Ocurrió un error inesperado:",e)


def leer():  #READ
    key={# El elemento que creamos en nuestra tabla será buscado por sus atributos de ID y Fecha
        "Id":{"S":"Estoesotraprueba"},
        "Fecha":{"S":"2024-01-01"}
        }
    
    try:
        response=dynamodb.get_item( # get_item nos dará el elemento con las características introducidas
            TableName=table_name,
            Key=key
            )
        
        if 'Item' in response: # Si el item existe en la lista de elementos
            item=response['Item']
            print("Elemento encontrado:",item)
        else:
            print("Elemento no encontrado.")
    except ClientError as e:
        print("Error al leer el elemento:",e)
    except Exception as e:
        print("Ocurrió un error inesperado:",e)


def actualizar():  #UPDATE
    key={
        "Id":{"S":"Estoesotraprueba"}, 
        "Fecha":{"S":"2024-01-01"}
        }
    # Definimos los valores a actualiar
    update_expression="SET Nombre = :n, Edad = :e, Correo = :c"
    expression_attribute_values={# damos valores a los atributos que actualizaremos
        ":n":{"S":"Nuevo Ejemplo"},
        ":e":{"N":"30"},
        ":c":{"S":"nuevo_ejemplo@example.com"}
        }
    
    try:
        response=dynamodb.update_item(
            TableName=table_name,
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
            )
        print("Elemento actualizado exitosamente:",response)
    except ClientError as e:
        print("Error al actualizar el elemento:",e)
    except Exception as e:
        print("Ocurrió un error inesperado:",e)


def eliminar():  #DELETE
    key={
        "Id":{"S":"Estoesotraprueba"},
        "Fecha":{"S":"2024-01-01"}
        }
    
    try:
        response=dynamodb.delete_item( # Buscamos el item a eliminar por su Id y Fecha
            TableName=table_name,
            Key=key
            )
        print("Elemento eliminado exitosamente.")
    except ClientError as e:
        print("Error al eliminar el elemento:",e)
    except Exception as e:
        print("Ocurrió un error inesperado:",e)

# Ejecutar las operaciones
crear()
leer()
actualizar()
eliminar()
