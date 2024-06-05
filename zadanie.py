from threading import Lock
from flask import Flask, render_template, session, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit, disconnect
import MySQLdb
import serial
import time
import configparser as ConfigParser
import random
import math
import json


async_mode = None

app = Flask(__name__)

config = ConfigParser.ConfigParser()
config.read('config.cfg')
myhost = config.get('mysqlDB', 'host')
myuser = config.get('mysqlDB', 'user')
mypasswd = config.get('mysqlDB', 'passwd')
mydb = config.get('mysqlDB', 'db')
print(myhost)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

#ser = None

def background_thread(args):
    count = 0
    dataCounter = 0
    dataList = []
    db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)          
    while True:
        if args:
          #A = dict(args).get('A')
          #btnV = dict(args).get('btn_value')
          dbV = dict(args).get('db_value')
        else:
          #A = 1
          #btnV = 'null'
          dbV = 'nieco'  
        socketio.sleep(1)
        dataCounter +=1
        count += 1
        print("button value: ", dbV)
        ser = serial.Serial("/dev/ttyACM0", 9600)
        if ser:
            fo = open("static/files/sensors.txt","a+")
            read_ser = ser.readline().decode().strip()
            print("Sensor value: ", read_ser)
            sensor_values = read_ser.split(',')
           # Convert values to floats
            gas_value, light_value, temperature_value, rain_value = map(float, sensor_values)
            if dbV == 'start':    
                # Create JSON object
                dataDict = {
                    "Count": count,
                    "Gas": gas_value,
                    "Light": light_value,
                    "Temperature": temperature_value,
                    "Rain": rain_value
                }
                dataList.append(dataDict)                
                socketio.emit('my_response',
                              {'data': dataDict, 'count': count},
                              namespace='/test')

            else:
                if len(dataList)>0:
                   
                    print("Data List:::::: ",str(dataList))
                    val = str(dataList).replace("'", "\"")
                    print("data:::::", val)
                    cursor = db.cursor()
                    cursor.execute("SELECT MAX(id) FROM sensors")
                    maxid = cursor.fetchone()
#                     if maxid[0] is None:
#                         max_id = 0
#                     else:
#                         max_id = maxid[0]
                    #for data in dataList:
                        #data_str = json.dumps(data)
                    cursor.execute("INSERT INTO sensors (id, hodnoty) VALUES (%s, %s)", (maxid[0] + 1, val))
                   # max_id+=1
                    db.commit()
                   
                    fo.write("%s\r\n" %val)
                dataList = []
                dataCounter = 0
        
    
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/start', methods=['GET', 'POST'])
def start():
    return render_template('start.html', async_mode=socketio.async_mode)

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    return render_template('graph.html', async_mode=socketio.async_mode)

@app.route('/gauge', methods=['GET', 'POST'])
def gauge():
    return render_template('gauge.html', async_mode=socketio.async_mode)

@app.route('/rest', methods=['GET', 'POST'])
def rest():
    return render_template('getdb.html', async_mode=socketio.async_mode)

@app.route('/graphdb', methods=['GET', 'POST'])
def dbGraph():
    return render_template('showidDB.html', async_mode=socketio.async_mode)

@app.route('/readfile', methods=['GET', 'POST'])
def fileGrah():
    return render_template('writeFile.html', async_mode=socketio.async_mode)


@app.route('/db', methods=['GET', 'POST'])
def db():
    db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
    cursor = db.cursor()
    cursor.execute('''SELECT  hodnoty FROM  sensors''')
    rv = cursor.fetchall()
    # Extract JSON strings from the result
    json_data = [row[0] for row in rv]
    return render_template('showAllDB.html',data=json_data)    

@app.route('/dbdata/<string:num>', methods=['GET', 'POST'])
def dbdata(num):
    db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
    cursor = db.cursor()
    print(num)
    cursor.execute("SELECT hodnoty FROM  sensors WHERE id=%s", num)
    rv = cursor.fetchone()
    return str(rv[0])

@app.route('/read', methods=['GET', 'POST'])
def readmyfile():
    fo = open("static/files/sensors.txt","r")
    data = fo.readlines()
    #return data
    return render_template('readFile.html',data=data) 


@app.route('/read/<string:num>', methods=['GET', 'POST'])
def readmyfileID(num):
    fo = open("static/files/sensors.txt","r")
    rows = fo.readlines()
    return rows[int(num)-1]

@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['db_value'] = message['value']     
 
@socketio.on('db_event', namespace='/test')
def test_message(message):
    session['db_value'] = message['value']   

@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    ser = None
    #thread = None
    #session['btn_value'] = 'null'
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())


@socketio.on('click_event', namespace='/test')
def db_message(message):
    session['btn_value'] = message['value']


# @socketio.on('slider_event', namespace='/test')
# def slider_message(message):
#     session['slider_value'] = message['value']


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

@app.route('/close', methods=['POST'])
def close_server():
    socketio.stop()  # Stop the SocketIO server
    return redirect('/')  # Redirect to the home page

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)
