import boto3
from time import sleep
from botocore.exceptions import ClientError

#creamos un cliente en la región usada 
dynamodb=boto3.client("dynamodb",region_name="us-west-2")

table_name="Tablaprueba"

try:
    response= dynamodb.update_table(
        TableName=table_name,
        StreamSpecification={
            "StreamEnabled":True, # Cambiamos el estado del stream a Activado
            "StreamViewType":"NEW_AND_OLD_IMAGES" #especificamos el tipo de dato usado
        }
    )
    print(f"streams habilitados en ´{table_name}´")
    print("Detalles de la tabla", response)

except ClientError as e:
    print(f"Error al habilitar streams: {e}")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
    

dynamodbstreams = boto3.client('dynamodbstreams', region_name='us-west-2') #creamos un cliente de dynamostreams

try:
    # Obtenemos el ARN del Stream de la tabla
    response = dynamodb.describe_table(TableName=table_name)
    stream_arn = response['Table']['LatestStreamArn']
    print(f"Stream ARN: {stream_arn}")

    # Obtenemos la descripción del Stream
    response = dynamodbstreams.describe_stream(StreamArn=stream_arn)
    stream_description = response['StreamDescription']

    print("Stream Description:", stream_description)

    # Obtenemos el shard ID del primer shard
    shards = stream_description['Shards']
    shard_id = shards[0]['ShardId']

    # Obtenemos un iterador para el shard
    shard_iterator = dynamodbstreams.get_shard_iterator(
        StreamArn=stream_arn,
        ShardId=shard_id,
        ShardIteratorType='TRIM_HORIZON'
    )['ShardIterator']

    # Leemos y procesamos registros del stream
    while True:
        response = dynamodbstreams.get_records(ShardIterator=shard_iterator)
        records = response['Records']
        if records:
            print("Records:")
            for record in records:
                print(record)

        # Obtenemos el siguiente iterador
        shard_iterator = response['NextShardIterator']

        # Pausamos un poco antes de la próxima lectura
        sleep(30)

except ClientError as e:
    print(f"Error al procesar Streams: {e}")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
