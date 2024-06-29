<p align="left""><img src="https://semanadelcannabis.cayetano.edu.pe/assets/img/logo-upch.png" width="150">
<h1 align="center">Familiarizándonos con LabLearner y la creación de tablas de bases de datos DynamoDB</h1>
</p>


Para este ejercicio de familiarización, usremos AWS Academy Learner Lab [82339], iniciando el laboratorio, de manera que tengamos acceso a los servicios de AWS

<p aling="center"><img src="https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/4848bc44-c66e-4247-98dc-8c81dabc79d1"></p>


## Elegiremos el servicio de DynamoDB 
<p aling="center"><img src="https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/881b0774-4d2e-45a0-9a93-4dc08cf5024d"></p>

# Creamos una tabla nueva con un nombre y clave de partición en Número, manteniendo la configuración de la tabla en predeterminada sin añadir etiquetas de momento
![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/5476f9f3-ffcf-421d-af4b-cbc06aab75be)


<p>Una vez tenemos la tabla creada, <img src="https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/0dac26ec-44de-4be8-968b-dc098edb87fe" width="150"> podemos comenzar a añadir elementos</p>

![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/dbc303b5-ba94-4826-8af9-23602e314d78)



En este caso hemos creado los elementos "Departamento" y "Nombre" 
teniendo cuidado del uso de mayúsculas, pues pueden representar variables distintas

Luego, para realizar búsquedas sencillas, haremos click en filtros y añadiremos los necesarios para encontra la información requerida

![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/6fd97041-d62e-4d49-aee3-baaf544b9ead)

Es así como obtenemos el resultado de la persona con identiciador 2 y Nombre "Ricardo"


Podemos obtener, también, métricas de uso de nuestra tabla:
![image](https://github.com/JoseCuevaRamos/Proyecto_AWS/assets/150297452/2d63eeaa-3a45-47d3-8618-f6dd41811c9e)













<br>
Casos de uso de DynamoDB:

- Seguimiento de inventario o carros de compra para tiendas de venta en linea
  
- Marketing, almacenando información como perfiles de usuarios, enlaces recientemente visitados, etc.
  
- Almacenamiento de información de puntajes y estados en videojuegos
  
- Transacciones bancarias, detección de fraudes, etc.



## Aprendimos a crear una tabla de DynamoDB a través de la interfaz gráfica de AWS, pero también podemos hacerlo a base de código usando el Software Developer Kit de boto3 a través de un script creado por nosotros
