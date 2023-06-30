#configurazione nel server # Patron DAO (Data Acces Object, per mantenere la persistenza dei dati)
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__) # Crea una instancia de la aplicación Flask con el nombre app para el modulo actual
app.config['MYSQL_HOST'] = 'localhost' #Establece la configuración para el host de la base de datos MySQL
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
mysql = MySQL(app)

class DevelopmentConfig:
    DEBUG=True # Para mostrar mensajes detallados y reiniciar automáticamente la aplicación cuando se detectan cambios.

class User: 
    def __init__(self, username, password, nascita, corso,id,is_admin): # Se ejecuta automáticamente cuando se crea una nueva instancia de la clase.
        self.username = username #atributos de la clase (publicos por defecto)
        self.password = password
        self.nascita = nascita
        self.corso = corso
        self.id=id
        self.is_admin=is_admin

class Device:
    def __init__(self, id,device, stanza):
        self.id=id
        self.device = device
        self.stanza = stanza

class Action:
    def __init__(self, value_state, intensity, battery, date, id_Dev, id_user):
        self.value_state = value_state
        self.intensity = intensity
        self.battery = battery
        self.date = date
        self.id_Dev = id_Dev
        self.id_user = id_user
       

class DataBase:
    @staticmethod # es independiente y se puede llamar directamente desde la clase sin necesidad de crear una instancia
    def insert_user(user):
        sql = 'INSERT INTO user (user, password, nascita, corso) VALUES (%s, %s, %s, %s)'#insertar con marcadores de posicion
        values = (user.username, user.password, user.nascita, user.corso) # valores a insertar
        DataBase.execute_query(sql, values)# ejecuta la consulta
    
    @staticmethod # Falta definir la logica de negocio (considerar casos: quien, cuando, como)
    def delete_user(username):
        sql = 'DELETE FROM user WHERE user = %s'
        values = (username,)
        DataBase.execute_query(sql, values)

    @staticmethod 
    def obtain_user(username, password):
        sql = 'SELECT * FROM user WHERE user = %s AND password = %s'
        values = (username, password)
        return DataBase.execute_query(sql, values, fetch_one=True)
    
    @staticmethod
    def obtain_device():
        sql = 'SELECT * FROM device'
        devices = DataBase.execute_query(sql, fetch_one=False)
        return devices
    
    @staticmethod
    def control_device(device):
        sql = "INSERT INTO actions(value_state, intensity, battery,id_Dev,id_user) VALUES (%s, %s, %s,%s,%s)"
        values = (device.value_state, device.intensity, device.battery,device.id_Dev, device.id_user)
        return DataBase.execute_query(sql, values, fetch_one=True)

    @staticmethod
    def getDeviceById(id):
        sql= "SELECT * FROM device WHERE id = %s"
        values=(id,)
        result= DataBase.execute_query(sql,values,fetch_one=True)
        if result is not None:
            device = {
                'id': result[0],
                'device': result[1],
                'stanza': result[2]
             }
            return device
        else:
            
            return None
    
    @staticmethod
    def getDevice():
        sql= "SELECT device FROM device"
        return DataBase.execute_query(sql,fetch_one=False)
    
    @staticmethod
    def postprogram(time, brightness, status, id_Dev, id_user):
        sql= "INSERT INTO program (time, brightness, status, id_Dev, id_user) VALUES (%s, %s, %s, %s, %s)"
        values = (time, brightness, status, id_Dev, id_user)
        return DataBase.execute_query(sql,values,fetch_one=False)
        

    @staticmethod
    def request_graphic(selected_drop_down_value):
        sql = "SELECT a.date, a.intensity, d.%s FROM actions AS a JOIN device AS d ON a.id_Dev = d.id;"
        column_name = "device"
        sql = sql % column_name
        result = DataBase.execute_query(sql, fetch_one=False)
        return result
    
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
        cur = DataBase.connect() #poner un get?--> revisar bibliografia
        cur.execute(sql)# ejecuta la consulta
        mysql.connection.commit()#guarda la consulta --> revisar
        DataBase.close(cur)
    
    @staticmethod
    def connect():
        return mysql.connection.cursor()
    
    @staticmethod
    def close(cursor):
        cursor.close()




