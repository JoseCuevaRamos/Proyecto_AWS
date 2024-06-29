<p align="left""><img src="https://semanadelcannabis.cayetano.edu.pe/assets/img/logo-upch.png" width="150">
<h1 align="center">Base de datos conceptos</h1>
</p>

## ¿Qué es una base de datos?

A diferencia de un simple contenedor de información, una base de datos recopila los datos ingresados de manera sistemática, no importa el formato de la información, sean números, imágenes, documentos de texto, etc.

### Sobre el Sistema de Administración de Bases de Datos (DBMS)
Se refiere un software dedicado a almacenar, recuperar y editar los datos, en los sistemas informáticos, es normal referirse a un DBMS como una base de datos.

### Ventajas de usar una base de datos:
- **Escalamiento eficiente:** Se pueden manejar grandes cantidades de información, aumentando a millones, billones o más. Para manejar y tener un uso eficiente de la información, es trascendental el uso de una base de datos
- **Integridad de la información:** Las reglas de las bases de datos permiten que la información se mantenga en su estado original sin pérdida o corrupción de datos
- **Seguridad de la información:** Mediante la integración con otros servicios como IAM, nos aseguramos que la información sea solo accesible por usuarios IAM con roles específicos y que solo miembros de grupos específicos tengan acceso a la modificación, manteniendo segura nuestra data.
  
### Modelos de base de datos:
Los modelos de bases de datos define las relaciones y reglas que determinan el modo en que los datos se pueden almacenar, organizar y manipular.

Las bases de datos han tenido un trayecto a través del cuál fueron evolucionando, comenzando con **bases de datos jerárquicas**, pasando por las **bases de datos de red** y, una especialmente interesante para este proyecto, la **Base de Datos Relacional**

## Sobre las Bases de Datos Relacionales:
Surgió en los años 80, ayudando a mejoras en la productividad, flexibilidad y compatibilidad con hardware más rápido. 
<br>
Usamos tablas para organizar los registros en lugar de listas enlazadas.
<br>
En estos modelos, cada categoría tiene una tabla  donde los atributos son columnas y los datos, filas. 
| Número de habitación | Nombre de la habitación          |
|---|---------------------|
| 1 | Dormitorio          |
| 2 | Habitación Infantil |

En esta estructura, las columnas son denominadas claves principales 

## Sobre el Lenguaje de Consulta Estructurada (SQL)
SQL es un lenguaje de consulta utilizado para recuperar, acceder y editar datos en bases de datos relacionales. Mediante una serie de consultas o instrucciones podemos tener control de la información almacenada en nuestras bases de datos relacionales.

* **Componentes de SQL**
  - **DDL (Data Definition Language): ** se refiere a comandos SQL para diseñar la estructura de la base de datos con comandos como CREATE-ALTER-DROP
  - **DML (Data Manipulation Language):** estas instrucciones escriben información nueva o modifican los registros existentes con comandos como INSERT-SELECT-UPDATE-DELETE
  - **DCL (Data Control Language):** este lenguaje de control administra o autoriza el acceso a la base de datos con comandos como GRANT-REVOKE para dar o quitar permisos
  - **TCL (Transaction Control Language):** ayuda a realizar cambios en la base de datos de manera automática con comandos como COMMIT-ROLLBACK-SAVEPOINT
  
* Operaciones ACID:
El acrónimo ACID significa Atomicidad, Consistencia, Aislamiento y Durabilidad.


## Sobre las Bases de Datos No Relacionales (NoSQL)

