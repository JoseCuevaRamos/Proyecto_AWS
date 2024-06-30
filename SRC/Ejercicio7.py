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
