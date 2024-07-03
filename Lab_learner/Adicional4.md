<p align="left""><img src="https://semanadelcannabis.cayetano.edu.pe/assets/img/logo-upch.png" width="150">
<h1 align="center"> Uso de transacciones en dynamoDB </h1>
</p>

# Capacidades y Casos de Uso de Transacciones en DynamoDB
DynamoDB ofrece transacciones para garantizar que varias operaciones se completen de manera exitosa o no se realicen en absoluto. Esto es crucial en escenarios donde es necesario mantener la consistencia de múltiples elementos de datos, por ejemplo, al actualizar varios registros de manera simultánea.

## Capacidades Clave de Transacciones en DynamoDB:
**Atomicidad**: Todas las operaciones dentro de una transacción se completan de manera exitosa o se revierten en su totalidad.

**Consistencia**: Las transacciones en DynamoDB garantizan que los datos no se dejen en un estado inconsistente.

**Aislamiento**: Las transacciones se ejecutan de manera aislada de otras transacciones concurrentes, evitando problemas de concurrencia.

**Durabilidad**: Las transacciones completadas se guardan de manera duradera en DynamoDB, asegurando que no se pierdan debido a fallos del sistema.
# Script
En el siguiente script vamos a realizar una trascaccion en la que vamos a modificar varios items a la vez y en caso que uno de los elementos no pueda ser modificado todos los cambios se revierten y vuelven a su estado original

```
# Inicializar el cliente de DynamoDB
dynamodb = boto3.client('dynamodb', region_name='us-west-2')

# Definir las operaciones transaccionales
transact_items = [
    {
        'Update': {
            'TableName': 'Tablap',
            'Key': {
                'Id': {'S': '1'},
                'Fecha': {'S': '2'}
            },
            'UpdateExpression': 'SET Costo = :new_cost, Tipo = :new_type',
            'ExpressionAttributeValues': {
                ':new_cost': {'N': '3000'},
                ':new_type': {'S': 'F'}
            }
        }
    },
    {
        'Update': {
            'TableName': 'Tablaprueba',
            'Key': {
                'Id': {'S': '3'},
                'Fecha': {'S': '4'}
            },
            'UpdateExpression': 'SET Costo = :new_cost, Tipo = :new_type',
            'ExpressionAttributeValues': {
                ':new_cost': {'N': '300'},
                ':new_type': {'S': 'H'}
            }
        }
    }
]

# Ejecutar la transacción
try:
    response = dynamodb.transact_write_items(TransactItems=transact_items)
    print("Transacción completada con éxito")
except ClientError as e:
    print(f"Error en la transacción: {e.response['Error']['Message']}")


```




