import boto3

#crear un cliente de DynamoDB
dynamodb = boto3.client('dynamodb', region_name='us-west-2')

#ARN de la copia de seguridad a restaurar
backup_arn = 'arn:aws:dynamodb:us-west-2:123456789012:table/Tablaprueba/backup/01534567891011-1234abcd'

#Nombre de la nueva tabla a crear desde la copia de seguridad
new_table_name = 'Tablaprueba_Restored'

try:
    response = dynamodb.restore_table_from_backup(
        TargetTableName=new_table_name,
        BackupArn=backup_arn
    )
    print(f"EXITO: {response['TableDescription']['TableArn']}")
except Exception as e:
    print(f"Error: {e}")
