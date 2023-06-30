from flask import Flask, render_template, request, redirect, url_for, flash
from config_ws import User, app, DataBase,Device,Action, mysql
from datetime import datetime
import time
import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.graph_objects as go

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
            
            if bool(data[6]): # 6 es el ultimo elemento en la lista resultante de la query
                return redirect('/report/')
            else:
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

    elif request.method=='POST':
       date= datetime.now()
       id_Dev = request.form.get('deviceId')
       intensity = request.form.get('brightness')
       battery= 100-(int(intensity)* 2)
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
    
@app.route('/logout')
def logout():
    return redirect(('/'))

@app.route('/program', methods=['GET', 'POST'])
def program():
    if request.method == 'POST':
        return render_template('program.html')

    

app_d = dash.Dash(__name__, server=app, url_base_pathname='/report/')

app_d.layout = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options = [],
        value=None
    ),
    dcc.Graph(id='my-graph')
], style={'width': '500px'})

@app_d.callback( Output('my-dropdown', 'options'), Output('my-dropdown', 'value'), [Input('my-dropdown', 'search')])
def update_dropdown(search_value):
    results = DataBase.getDevice()
    options = [{'label': device[0], 'value': device[0]} for device in results]
    value=None
    return options, value

@app_d.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_drop_down_value):
    result = DataBase.request_graphic(selected_drop_down_value)
    result_list = [result]  # Convertir el resultado en una lista de una tupla
    df = pd.DataFrame(result_list, columns=['date', 'intensity', 'device'])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['intensity'], mode='lines'))

    layout = {'margin': {'l': 40, 'r': 10, 't': 20, 'b': 30}}
    fig.update_layout(layout)

    return fig

if __name__ == '__main__':
    try:
        app.run(debug=True,host="0.0.0.0")
    except KeyboardInterrupt:
        DataBase.close()

#Unir registro y add registro
#Crear en vez de flash un otro html else reurn redirect al endpoint return(redirect"/passerror")
