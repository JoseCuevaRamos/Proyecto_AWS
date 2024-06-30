import boto3

def calculate_rcu(item_size_kb, read_rate_per_second, consistency='eventual'):
    #calcula las Unidades de Capacidad de Lectura(RCU) necesarias
    if consistency == 'fuerte':
        #Lectura consistente fuerte
        rcu_per_read = 1 if item_size_kb <= 4 else (item_size_kb // 4) + 1
    else:
        #lectura eventualmente consistente
        rcu_per_read = 0.5 if item_size_kb <= 4 else (item_size_kb // 4) / 2
    
    total_rcu = rcu_per_read * read_rate_per_second
    return total_rcu

def calculate_wcu(item_size_kb, write_rate_per_second):
    #Calcula las Unidades de Capacidad de Escritura (WCU) necesarias
    wcu_per_write = 1 if item_size_kb <= 1 else (item_size_kb // 1) + 1
    total_wcu = wcu_per_write * write_rate_per_second
    return total_wcu

#Datos de entrada
item_size_kb = 3  #tamaño promedio de los ítems en KB
read_rate_per_second = 10  #numero de lecturas por segundo
write_rate_per_second = 5  #numero de escrituras por segundo
consistency = 'eventual'  #tipo de consistencia de lectura: 'eventual' o 'fuerte'

#Calcular RCU y WCU
rcu = calculate_rcu(item_size_kb, read_rate_per_second, consistency)
wcu = calculate_wcu(item_size_kb, write_rate_per_second)

print(f"Unidades de Capacidad de Lectura (RCU) necesarias: {rcu}")
print(f"Unidades de Capacidad de Escritura (WCU) necesarias: {wcu}")

#crear un cliente de DynamoDB
dynamodb = boto3.client('dynamodb', region_name='us-west-2')

#configurar el autoescalado para la tabla
table_name = 'Tablaprueba'

#Ajustar las capacidades provisionadas segun los calculos
try:
    response = dynamodb.update_table(
        TableName=table_name,
        ProvisionedThroughput={
            'ReadCapacityUnits': int(rcu),
            'WriteCapacityUnits': int(wcu)
        }
    )
    print("Exito:", response)
except Exception as e:
    print("Error", e)
