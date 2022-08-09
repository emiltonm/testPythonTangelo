import hashlib
import json
from models.RqObjects import RqObjects
from models.database import Databases

def hash_SHA1(value):
    return hashlib.sha1(value.encode('utf-8')).hexdigest()

def set_Zero(value):
    return value*0

def add_plus(value):
    return '+'+value


if __name__ == '__main__':

    #lectura de archivo de configuracion
    configuration=".env"
    with open(configuration,"r") as fl:
        file=fl.read()
    cfg=json.loads(file)
    
    #creacion de objeto de base de datos
    db=Databases(cfg["db_name"])
    #creo un diccionario con la lista name_columns (llave) y la lista path_data (valor)
    data_request=dict(zip(cfg["name_columns"],cfg["path_data"]))

    data_db=[cfg["db_name"],cfg["table_name"],cfg["index_column"]]
    
    #creacion de objeto rq para la realizacion de peticiones
    rq=RqObjects(cfg["url"],data_request,data_db)
    
    #columnas que quiero afectar, con la funcion...
    rq.set_alter_field("Language",hash_SHA1)
    print("")
    #leo lista de consultas
    with open(cfg["query_file"],"r") as fl:
        file=fl.read()
    list_query=json.loads(file)
    for q in list_query["query"]:
        rq.get_data(q)
    print("")
    print(rq.get_data_frame())
    print("")
    print("el tiempo total en crearse la tabla fue de "+str(rq.get_total_time())+" milisegundos")
    print("el tiempo promedio de cada renglon fue de "+str(rq.get_average_time())+" milisegundos")
    print("el tiempo de la peticion mas lenta fue de "+str(rq.get_max_time())+" milisegundos")
    print("el tiempo de la peticion mas rapida fue de "+str(rq.get_min_time())+" milisegundos")
    print("")
    rq.sendTo_JSON("data.json")