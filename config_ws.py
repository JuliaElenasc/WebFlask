#configurazione nel server

from flask import Flask, render_template, request, redirect, url_for,flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='flaskregistro'
mysql=MySQL(app)

class DevelopmentConfig:
    DEBUG=True


class Utente:
    def __init__(self,username,password,nascita,corso):
        self.username = username
        self.password = password
        self.nascita = nascita
        self.corso = corso

#listaUtenti = []

class controloDB:
    @staticmethod
    def collegare():
        return mysql.connection.cursor()
    
    @staticmethod
    def chiudere(cursor):
        cursor.close()

    @staticmethod
    def inserire_utente(usuario):
        cur = controloDB.collegare()
        cur.execute('INSERT INTO registro (user, password, nascita, corso) VALUES (%s, %s, %s, %s)',
                    (usuario.username, usuario.password, usuario.nascita, usuario.corso))
        mysql.connection.commit()
        controloDB.chiudere(cur)

    @staticmethod
    def ottenere_utente(user, password):
        cur = controloDB.collegare()
        cur.execute('SELECT * FROM registro WHERE user = %s AND password = %s', (user, password))
        data = cur.fetchone()
        controloDB.chiudere(cur)
        return data
    
    @staticmethod
    def eliminare_utente(user):
        cur = controloDB.collegare()
        cur.execute('DELETE FROM registro WHERE user = %s', (user,))
        mysql.connection.commit()
        controloDB.chiudere(cur)


    @staticmethod
    def restituire_dati():
        cur = controloDB.collegare()
        cur.execute('SELECT * FROM registro')
        data = cur.fetchall()
        controloDB.chiudere(cur)
        return data










