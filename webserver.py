from flask import Flask, render_template, request, redirect, url_for, flash
from config_ws import User, app, DataBase,Device,Action
from datetime import datetime

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        data = DataBase.obtain_user(user, password)
        dataDev = DataBase.obtain_device()

        listDevice = []
        for itemDev in dataDev:
            listDevice.append(Device(itemDev[0], itemDev[1], itemDev[2]))

        if data:
            dettaglioUtente = {
                "username": data[1],
                "password": data[2],
                "nascita": data[3],
                "corso": data[4]
            }
            print("WebServer login", dataDev)

            return render_template('dettaglio.html', dettaglioUtente=dettaglioUtente, listDevice = listDevice)
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

@app.route('/dettaglio')
def dettaglio():
    data = DataBase.obtain_user()
    return render_template('dettaglio.html', dettaglioUtente=data)
    

@app.route('/device', methods=['GET','POST'])
def add_action():
    if request.method == 'GET':
        device_id = request.args.get('deviceId')
        
        if device_id is not None: 
            id = int(device_id)
        else: id = None
        
        device = DataBase.getDeviceById(id)
        if device:
            objDevice = Device(device.get('id'), device.get('device'), device.get('stanza'))
            
            return render_template("device.html", device=objDevice)
        else:
            
            return "Device not found"
            #creare istanza della classe device in base ai dati ottenuti dal DB (come fatto in listDevice di Login)

    elif request.method=='POST':
       
       date= datetime.now()
       id_Dev = request.form.get('deviceId')
       intensity = request.form.get('brightness')
       battery= 100-(intensity* 2)
       id_user = 1
       value_state = request.form.get('check')
       
       if value_state is None:
            value_state = "0"
       else: value_state="1"
       data=Action(value_state,intensity,battery,date, id_Dev, id_user)
       DataBase.control_device(data)
       return redirect('/device?deviceId='+str(id_Dev))
    else:
        return render_template("device.html")
    

if __name__ == '__main__':
    try:
        app.run(debug=True,host="0.0.0.0")
    except KeyboardInterrupt:
        DataBase.close()


# app.route(/get reg",methods post)
#def post registrazione()
#nome=request.form[user]
#Unir registro y add registro
#Crear en vez de flash un otro html else reurn redirect al endpoint return(redirect"/passerror")
# 