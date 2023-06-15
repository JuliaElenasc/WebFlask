from flask import Flask, render_template, request, redirect, url_for, flash
from config_ws import User, app, DevelopmentConfig , DataBase

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        data = DataBase.obtain_user(user, password)

        if data:
            dettaglioUtente = {
                "username": data[1],
                "password": data[2],
                "nascita": data[3],
                "corso": data[4]
            }
            return render_template('dettaglio.html', dettaglioUtente=dettaglioUtente)
            #return redirect("/detaglio") --> respuesta 302
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
        user = request.form['user']
        password = request.form['password']
        nascita = request.form['nascita']
        corso = request.form['corso']
        usuario = User(user, password, nascita, corso)
        DataBase.insert_user(usuario)
        return render_template('dettaglio.html', dettaglioUtente=usuario)
        
@app.route('/detaglio')
def dettaglio():
    data = DataBase.obtain_user()
    return render_template('dettaglio.html', dettaglioUtente=data)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        DataBase.close()
