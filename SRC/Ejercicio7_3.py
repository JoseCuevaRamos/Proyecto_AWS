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
        print(f"Exito: {response['BackupDetails']['BackupArn']}")
    except Exception as e:
        print(f"Error: {e}")