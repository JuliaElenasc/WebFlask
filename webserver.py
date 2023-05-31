from flask import Flask, render_template, request, redirect, url_for,flash
from flask_mysqldb import MySQL



app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='flaskregistro'
mysql=MySQL(app)


#listaUtenti = []

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM registro WHERE user = %s AND password = %s', (user, password))
        data = cur.fetchone()
        cur.close()

        if data:
            dettaglioUtente = {
                "username": data[1],
                "password": data[2],
                "nascita": data[3],
                "corso": data[4]
            }
            return render_template('dettaglio.html', dettaglioUtente=dettaglioUtente)
        else:
            flash('Credenziali errate, prova di nuovo')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route ('/registro')
def registro():
    return render_template ('registro.html')

@app.route('/addregistro', methods=['POST'])
def add_registro():    
    if request.method =='POST':
        user=request.form['user']
        password=request.form['password']
        nascita=request.form['nascita']
        corso=request.form['corso']
        cur= mysql.connection.cursor()
        print(cur)
        cur.execute('INSERT INTO registro (user, password, nascita, corso) VALUES(%s,%s,%s,%s)',
                    (user, password, nascita, corso))
        mysql.connection.commit()

        dettaglioUtente = {"username": user, "password": password, "nascita": nascita, "corso": corso}
        #listaUtenti.append(dictUtente)

        #flash('Ti sei registrato')
        return render_template ('dettaglio.html', dettaglioUtente=dettaglioUtente)
        #return redirect(url_for('/detaglio'))
    

@app.route('/detaglio')
def dettaglio():
    cur = mysql.conection.cursor()
    cur.execute('SELECT*FROM registro')
    data=cur.fetchall()
    cur.close()
    return render_template ('dettaglio.html',dettaglioUtente=data)


if __name__ == '__main__':
    app.run(debug=True)
