import boto3
import time

def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb', region_name='us-west-2')
    
    backup_arn = 'arn:aws:dynamodb:us-west-2:983477961749:table/Tablaprueba/backup/01719901842190-1c1f39de'
    new_table_name = 'Tablaprueba_Restored2223'
    
    # Verificar si el evento es una eliminación
    for record in event['Records']:
        if record['eventName'] == 'REMOVE':
            try:
                response = dynamodb.restore_table_from_backup(
                    TargetTableName=new_table_name,
                    BackupArn=backup_arn
                )
                
                new_table_arn = response['TableDescription']['TableArn']
                
                while True:
                    status_response = dynamodb.describe_table(TableName=new_table_name)
                    table_status = status_response['Table']['TableStatus']
                    if table_status == 'ACTIVE':
                        break
                    time.sleep(5)  # Esperar 5 segundos antes de verificar nuevamente
                
                return {
                    'statusCode': 200,
                    'body': f"EXITO: {new_table_arn}"
                }
            except Exception as e:
                return {
                    'statusCode': 500,
                    'body': f"Error: {e}"
                }
    
    return {
        'statusCode': 200,
        'body': "No se detectaron eliminaciones"
    }


