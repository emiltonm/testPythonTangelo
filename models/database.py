import sqlite3 as sql
from pathlib import Path

class Databases:
    __path_name: str = '<unknown>'

    def __init__(self,path_name):
        self.__path_name = path_name

        if(not Path(self.__path_name).exists()):
            print("Creando Base de Datos")
            conn = sql.connect(str(Path(self.__path_name)))
            conn.commit()
            conn.close()
        else:
            print("La Base de Datos ya existe")
    
    def get_path_name(self):
        return self.__path_name

