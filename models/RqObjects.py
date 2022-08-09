#from dataclasses import field
import requests
import time
import jmespath
import pandas as pd
import sqlite3 as sql

class RqObjects:
    __url: str = '<unknown>'
    __path: dict = {}
    __data: dict = {}
    __alter: dict = {}
    __df = None
    __df_cache = None
    __nameDB: str = '<unknown>'
    __tableName: str = '<unknown>'
    __index_columns: str = '<unknown>'

    def __init__(self,url,dict_data,db_data):
        self.__url = url
        self.__nameDB=db_data[0]
        self.__tableName=db_data[1]
        self.__index_columns=db_data[2]
        self.__path=dict_data
        columns_name = list(dict_data.keys())
        columns_name.append('time')
        self.__df=pd.DataFrame(columns=columns_name)
        self.__df_cache=pd.DataFrame(columns=columns_name)
        self.__load_cache()

    def get_data(self,field_name):
        #si el campo NO existe en el data frame cache
        if(self.__df_cache[self.__df_cache[self.__index_columns]==field_name].empty):
            print(field_name+" no existe en cache")
            #realizo peticion a la API y guarda en cache
            try:
                url = self.__url + field_name
                start_time = time.time()
                response = requests.get( url )
                if response.status_code == 200:
                    #recorro el diccionario path
                    for key,path in self.__path.items():
                        #obtengo el valor de la ruta json
                        raw_value=jmespath.search(path,response.json())
                        try:
                            #intento alterar el valor con la funcion del diccionario alter
                            self.__data[key]=self.__alter[key](raw_value)
                        except:
                            #si no es posible alterar asigno el valor original
                            self.__data[key]=raw_value
                    end_time = time.time()
                    time_row = (end_time - start_time) * 1000
                    self.__data['time'] = time_row
                    self.__df.loc[-1]=self.__data
                    self.__df.reset_index(drop=True,inplace=True)
                    self.__sendTo_DB()
                else:
                    print( 'Peticion a la url fallida' )
            except:
                print( 'la url no responde' )            
        else:
            print(field_name+" existe en cache")
            #recupera de cache
            start_time = time.time()
            #devuelvo los valores que cumplen la condicion cache[nombrecolumna]=="loquebusco"
            #cache["Country"]=="Colombia"
            self.__data=self.__df_cache[self.__df_cache[self.__index_columns]==field_name].iloc[0].to_dict()
            end_time = time.time()
            self.__df.loc[-1]=self.__data
            time_row = (end_time - start_time) * 1000
            #modifica el valor de la columna time
            self.__df.loc[-1,'time']=time_row
            self.__df.reset_index(drop=True,inplace=True)

    def get(self,key):
        return self.__data[key]

    def get_data_frame(self):
        return self.__df

    def get_total_time(self):
        return self.__df['time'].sum()
    
    def get_average_time(self):
        return self.__df['time'].mean()
    
    def get_max_time(self):
        return self.__df['time'].max()
    
    def get_min_time(self):
        return self.__df['time'].min()

    def set_alter_field(self,key,value):
        self.__alter[key]=value

    def __sendTo_DB(self):
        conn = sql.connect(self.__nameDB)
        registro=self.__df.tail(1)
        registro.to_sql(self.__tableName, conn, if_exists='append', index=False)
        conn.close()

    def __load_cache(self):
        try:
            conn = sql.connect(self.__nameDB)
            self.__df_cache=pd.read_sql_query("SELECT * FROM "+self.__tableName, conn)
            conn.close()
        except:
            print("No se pudo cargar la cache")
    
    def sendTo_JSON(self,name_file):
        self.__df.to_json(name_file,orient='records')
        print("Se guardo el archivo "+name_file)
        
