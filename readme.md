## Prueba Python - Emilton Mendoza Ojeda
---
# Descripción de la prueba
![tabla](images/tabla.jpg)

Desarrolle una aplicación en python que genere la tabla anterior teniendo las siguientes consideraciones:

- De https://restcountries.com/ obtenga el nombre del idioma que habla el pais y encriptelo con SHA1
- En la columna Time ponga el tiempo que tardo en armar la fila (debe ser automatico)
- La tabla debe ser creada en un DataFrame con la libreria PANDAS
- Con funciones de la libreria pandas muestre el tiempo total, el tiempo promedio, el tiempo minimo y el maximo que tardo en procesar toda las filas de la tabla.
- Guarde el resultado en sqlite.
- Genere un Json de la tabla creada y guardelo como data.json
- La prueba debe ser entregada en un repositorio git.

Es un plus si:

- No usa famework
- Entrega Test Unitarios
- Presenta un diseño de su solucion.

---
# Diseño de la solución
ademas de los requerimientos propuestos en la prueba, la solución fue desarrollada de manera que pueda cumplir con los siguientes requisitos:  
- Con el fin de que el código realizado en esta solución pueda ser aprovechado y ampliado en otras soluciones,se desarrollo con un enfoque orientado a objetos.  
- Realizar la peticion de datos a **cualquier restapi** que no solicite key y no solamente a la api de restcountries, ejemplo:\
  https://pokeapi.co/api/v2/pokemon/  
  https://randomuser.me/api/  
  https://catfact.ninja/fact  
- Extraer cualquier cantidad de campos deseados del json **sin reescribir el codigo**  
- Implementar una manera de modificar los datos de una columna de forma que no implique reescribir codigo, por ejemplo encriptar el lenguaje del pais en SHA1

la solucion puede ser configurada a traves del archivo **.env** que tiene formato json con los siguientes campos: 
>{  
        **"url"**: "url de la apiRest",  
        **"name_columns"**: ["Label Columna 1","Label Columna 2",...,"Label Columna n"],  
        **"path_data"**: ["ruta del registro a extraer 1","ruta del registro a extraer 2",...,"ruta del registro a extraer n"],  
        **"db_name"**: "ruta y nombre de la base de datos",  
        **"table_name"**: "nombre de la tabla en la que se almacenara el dataframe",  
        **"index_column"**:"nombre de la columna por la cual se realizaran las busquedas",  
        **"query_file"**:"ruta y nombre del archivo json que contiene las consultas a realizar en la api (peticiones)"  
        }  

Cabe señalar que el numero valores contenidos en **name_columns** debe ser igual al numero de valores contenidos en **path_data**.  
para dar solucion a la prueba propuesta el archivo de configuración .env estaria configurado con los siguientes valores:
>{  
        **"url"**: "https://restcountries.com/v2/name/",  
        **"name_columns"**: ["Region","Country","Language"],  
        **"path_data"**: ["[0].region","[0].name","[0].languages[0].name"],  
        **"db_name"**: "db/cache.db",  
        **"table_name"**: "countries",  
        **"index_column"**:"Country",  
        **"query_file"**:"countries.json"  
        }  

El archivo de registros de consultas a la api tiene el siguiente formato:  
>{**"query"**:[  
"peticion 1",  
"peticion 2",  
...  
"peticion n"  
]}

para dar solución a la prueba propuesta el archivo de consulta **countries.json** (nombre que se encuentra en .env.query_file) estaria configurado con los siguientes valores:

>{"query":[  
"Angola",  
"Spain",  
"France",  
"Germany",  
"Italy",  
"Mexico",  
"Colombia",  
"Argentina",  
]}  
  

---
# Ejecución de la solución
Instalar la libreria **virtualenv**
```virtualenv
pip install virtualenv
```  
Creamos el entorno virtual
```virtualenvcreate
virtualenv -p python3 venv
```  
Ejecutamos el entorno virtual
```virtualenvactivate
.\venv\Scripts\activate
```  
Instalamos las librerias necesarias para la ejecucion de la prueba
```requierements
pip install -r .\requirements.txt
```  
Ejecutamos la prueba a traves del script *main.py*
```main.py
python .\main.py
```
las salida de los datos sera visualizada a traves de la consola  y del fichero data.json