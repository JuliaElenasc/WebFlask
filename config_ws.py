#configurazione nel server # Patron DAO (Data Acces Object, per mantenere la persistenza dei dati)

from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__) # Crea una instancia de la aplicación Flask con el nombre app para el modulo actual
app.config['MYSQL_HOST'] = 'localhost' #Establece la configuración para el host de la base de datos MySQL
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskregistro'
mysql = MySQL(app)

class DevelopmentConfig:
    DEBUG=True # Para mostrar mensajes detallados y reiniciar automáticamente la aplicación cuando se detectan cambios.

class User: 
    def __init__(self, username, password, nascita, corso): # Se ejecuta automáticamente cuando se crea una nueva instancia de la clase.
        self.username = username #atributos de la clase
        self.password = password
        self.nascita = nascita
        self.corso = corso

class DataBase:
    @staticmethod # es independiente y se puede llamar directamente desde la clase sin necesidad de crear una instancia
    def insert_user(user):
        sql = 'INSERT INTO registro (user, password, nascita, corso) VALUES (%s, %s, %s, %s)'#insertar con marcadores de posicion
        values = (user.username, user.password, user.nascita, user.corso) # valores a insertar
        DataBase.execute_query(sql, values)# ejecuta la consulta
    
    @staticmethod # Falta definir la logica de negocio (considerar casos: quien, cuando, como)
    def delete_user(username):
        sql = 'DELETE FROM registro WHERE user = %s'
        values = (username,)
        DataBase.execute_query(sql, values)

    @staticmethod 
    def obtain_user(username, password):
        sql = 'SELECT * FROM registro WHERE user = %s AND password = %s'
        values = (username, password)
        return DataBase.execute_query(sql, values, fetch_one=True)
    
    @staticmethod
    def execute_query(sql, values=None, fetch_one=False):
        cur = mysql.connection.cursor() #crea un cursor, para ejecutar comandos y recuperar info de la BD
        if values:
            cur.execute(sql, values) # para ejecutar la consulta con los datos proporcionados
        else:
            cur.execute(sql) # Si no se proporcionan valores, la consulta SQL se ejecuta sin argumentos adicionales.
        mysql.connection.commit() #Guardo los cambios en la base de datos
        data = cur.fetchone() if fetch_one else cur.fetchall() #fetch=obtener, obtiene la linea en la bd de la consulta, u obtener todas las filas segun la query y lo guardo en data
        cur.close()# cierro el cursor para liberar conecciones (buena practica).
        return data
    
    @staticmethod
    def query(sql):
        cur = DataBase.conect() #poner un get?--> revisar bibliografia
        cur.execute(sql)# ejecuta la consulta
        mysql.connection.commit()#guarda la consulta --> revisar
        DataBase.close(cur)
    
    @staticmethod
    def conect():
        return mysql.connection.cursor()
    
    @staticmethod
    def close(cursor):
        cursor.close()




