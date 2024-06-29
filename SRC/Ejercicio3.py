import boto3

#Crear un cliente de DynamoDB en la region usada
dynamodb = boto3.client('dynamodb', region_name='us-west-2')

#tabla existente en DynamoDB
table_name = 'Tablaprueba'

# Claves de partición y ordenación de tu item
partition_key_value = '123'  #valor para la clave de partición 'Id'
sort_key_value = '2024-06-30'  # valor para la clave de ordenación 'Fecha'


# Crear el item que deseas insertar en la tabla
item = {
    'Id': {'S': partition_key_value},
    'Fecha': {'S': sort_key_value},
    'Estado': {'S': 'Activo'}  #añadir otros atributro a la tabla
}

#Insertar el item en la tabla
try:
    response = dynamodb.put_item(
        TableName=table_name,
        Item=item
    )
    print("se añadio con exito", response)
except Exception as e:
    print("Error :", e)
