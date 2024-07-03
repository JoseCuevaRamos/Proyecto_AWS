<p align="left""><img src="https://semanadelcannabis.cayetano.edu.pe/assets/img/logo-upch.png" width="150">
<h1 align="center">Ejercicio 8: Operaciones básicas con tablas DynamoDB</h1>

<h3>Operaciones CRUD</h3>
<ul>
<li>Implementa scripts para realizar operaciones de creación, lectura, actualización y eliminación en la tabla DynamoDB.</li>
</ul>
<h2>Respuesta</h2>

CRUD es acrónimo de Create, Read, Update y Delete, indicando la creación, lectura, actualización y borrado de elementos de una tabla de DynamoDB mediante las diferentes funciones que ofrece el cliente dynamodb con el SDK boto3:

* Operación Crear:
  * Definiremos los atributos que añadiremos a nuestra tabla (Id, Fecha, Etc.)

```
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

```

vemos como se crean los elementos incluso cuando no siguen la estructura del primer elemento de la tabla, función característica de las bases de datos no relacionales
![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/26f76363-8d3c-4625-8327-af56e8faf2f5)

* Operación Leer
  * Buscaremos el elemento que tenga los atributos que definimos (en este caso Id y Fecha), si es encontrado en la tabla, dará el mensaje de encontrado junto al elemento, sino, explicará cuál es el error
```
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
```
![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/44f2a263-4b92-4ebb-a373-c88d0cc775c1)



* Operación Actualizar
   * Nos encargamos de la búsqueda de un elemento que contenga los atributos definidos (Id y Fecha), si es encontrado, se actualizará con los valores de la variable expression_attribute_values.

```
def actualizar():  #UPDATE
    key={
        "Id":{"S":"Estoesotraprueba"}, 
        "Fecha":{"S":"2024-01-01"}
        }
    # Definimos los valores a actualiar
    update_expression="SET Nombre = :n, Edad = :e, Correo = :c"
    expression_attribute_values={# damos valores a los atributos que actualizaremos
        ":n":{"S":"Nuevo Ejemplo"},
        ":e":{"N":"31"},
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

```
![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/5b33f992-d93d-41fd-9e8a-7fa63c67fa7c)

* Operación Eliminar
  *Verificamos que exista un elemento con los atributos y, si es así, lo eliminamos
```
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
```
![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/3bacc527-e4d0-4ad6-b389-e1ff8ef464de)
