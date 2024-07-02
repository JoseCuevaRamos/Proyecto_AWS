import boto3
from time import sleep
from botocore.exceptions import ClientError

# Configuración
region = 'us-west-2'
table_name = 'Tablaprueba3'

# Crear cliente de DynamoDB
dynamodb = boto3.client('dynamodb', region_name=region)

# Crear cliente de DynamoDB Streams
dynamodbstreams = boto3.client('dynamodbstreams', region_name=region)

def enable_streams():
    try:
        # Actualizar la tabla para habilitar streams
        response = dynamodb.update_table(
            TableName=table_name,
            StreamSpecification={
                "StreamEnabled": True,
                "StreamViewType": "NEW_AND_OLD_IMAGES"
            }
        )
        print(f"Streams habilitados en '{table_name}'")
        print("Detalles de la tabla", response)
    except ClientError as e:
        print(f"Error al habilitar streams: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def process_stream_events():
    try:
        # Esperar un poco para que los streams estén disponibles
        sleep(30)

        # Obtener el ARN del Stream de la tabla
        response = dynamodb.describe_table(TableName=table_name)
        stream_arn = response['Table']['LatestStreamArn']
        print(f"Stream ARN: {stream_arn}")

        # Obtener la descripción del Stream
        response = dynamodbstreams.describe_stream(StreamArn=stream_arn)
        stream_description = response['StreamDescription']

        print("Stream Description:", stream_description)

        shards = stream_description['Shards']

        if not shards:
            print("No hay shards disponibles. Asegúrate de que la tabla tenga datos y espera un poco.")
        else:
            shard_id = shards[0]['ShardId']

            # Obtener un iterador para el shard
            shard_iterator = dynamodbstreams.get_shard_iterator(
                StreamArn=stream_arn,
                ShardId=shard_id,
                ShardIteratorType='TRIM_HORIZON'
            )['ShardIterator']

            # Leer y procesar registros del stream
            while True:
                response = dynamodbstreams.get_records(ShardIterator=shard_iterator)
                records = response['Records']
                if records:
                    print("Records:")
                    for record in records:
                        print(record)

                # Obtener el siguiente iterador
                shard_iterator = response['NextShardIterator']

                # Pausar un poco antes de la próxima lectura
                sleep(5)

    except ClientError as e:
        print(f"Error al procesar Streams: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    enable_streams()
    process_stream_events()
