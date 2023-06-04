from flask import Flask, render_template, request, redirect, url_for, flash
from config_ws import app, controloDB, Utente

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        data = controloDB.ottenere_utente(user, password)

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
        user = request.form['user']
        password = request.form['password']
        nascita = request.form['nascita']
        corso = request.form['corso']
        usuario = Utente(user, password, nascita, corso)
        controloDB.inserire_utente(usuario)
        #dettaglioUtente = {"username": user, "password": password, "nascita": nascita, "corso": corso}
        return render_template('dettaglio.html', dettaglioUtente=usuario)
        #listaUtenti.append(dictUtente)
        #flash('Ti sei registrato')
                #return redirect(url_for('/detaglio'))
    

@app.route('/detaglio')
def dettaglio():
    data = controloDB.restituire_dati()
    return render_template('dettaglio.html', dettaglioUtente=data)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        controloDB.chiudere()
