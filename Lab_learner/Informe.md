# Informe Detallado del Proceso de Desarrollo
## 1.- Introducción

Elegimos usar AWS Cloud9 como entorno de desarrollo por sobre alternativas como VSCode, ya que integra mejor los servicios de AWS a través del SDK Boto3 al extraer nuestras credenciales directamente de la sesión iniciada al crear el entorno de Cloud9. Esta decisión nos ayudó a desarrollar los scripts de cada actividad que propone el proyecto, para, finalmente, juntarlos en un único documento llamado “Proyecto-Final.py” a través de una interfaz de texto con python, facilitando la interacción de todas las funciones que creamos.

## 2- Desarrollo del Proyecto

### Implementación y desafíos técnicos:

El Software Developer Kit Boto3 representó un desafío para el equipo, pues no estábamos familiarizados con este SDK, a través de la investigación en la documentación oficial hallada en internet y múltiples pruebas, logramos superar esta dificultad. Otra mayor dificultad fue la elección de las regiones en las que trabajar, pues las cuentas de AWS con las que contamos tienen algunos permisos limitados en ciertas regiones, logramos la mayor cantidad de permisos y funcionalidades en la región us-west-2, que fue elegida finalmente como región principal a lo largo de todo este proyecto.
### Integración y pruebas
Los scripts individuales fueron convertidos a funciones para el ejercicio final, donde integramos todos estos códigos en uno solo, sumado a la interfaz de comandos, junto a las pruebas exhaustivas que garantizaron la interacción correcta con los servicios de Amazon por parte de nuestro script final 

## 3.-  Soluciones implementadas:
### Aprendizaje del SDK Boto3:
Se realizó una inversión de tiempo en el estudio de la documentación y aplicación de ejemplos 
### Selección de modelos:
Algunos de los ejercicios requerían el cambio de región o modelo de pago, para, por ejemplo, crear réplicas, cambiando a otra región con el modelo de pago PAY-PER-REQUEST

## 4.- Análisis de resultados:
Los scripts proporcionados por el equipo logran interactuar eficientemente con los servicios AWS mediante la creación de tablas, elementos, streams, registros, eventos y backups. La naturaleza NoSQL de DynamoDB nos fue útil para la creación de elementos variados a lo largo del script y las pruebas por su mayor flexibilidad en cuanto a los datos y sus estructuras 
Métricas Relevantes

### **Latencia**: Gracias a las capacidades de lectura y escritura proporcionadas, tanto como la replicación en regiones distintas, los datos fueron accedidos de manera rápida con una latencia consistentemente baja

### **Escalabilidad**:
La capacidad de escalar horizontalmente al crear más tablas para asegurar la disponibilidad y redundancia de datos fue validada mediante la creación de los scripts, al poder ser accedidas mediante funciones de lectura sin problemas

### **Costo-Eficiencia**:
A lo largo del desarrollo del proyecto, los precios y gastos que implica la creación y lectura de estas tablas se mantuvo en un valor mínimo, ya que las consultas y creaciones fueron puntuales gracias a las funciones y su implementación eficiente para evitar un uso excesivo de las consultas o creaciones y, por ende, un gasto mayor del capital proporcionado.

<br>
Las decisiones tomadas y estrategias de resoluciones por las que optamos culminaron en un sistema robusto y eficiente que cumple con los objetivos propuestos con una interacción fluida con los servicios de AWS gracias a las soluciones implementadas.
