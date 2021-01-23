from flask import Flask, render_template, request
from influxdb import InfluxDBClient

host='db'
port=8086
user = 'admin'
password = 'user123'
dbname = 'db_0'
client = InfluxDBClient(host, port, user, password, dbname)


app = Flask(__name__)
@app.route('/')
def user():
   return render_template('user.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      new_user= request.form.to_dict()
      json_body = [
      
        {"measurement": "users",
            "fields": {
                "name": new_user['Navn'],
                "token": new_user['Token'],
                "meter": new_user['Maalepunkt'],
                "persons": int(new_user['Persons']),
                "departement": new_user['Afdeling']
            }
        }
    ]
      client.write_points(json_body, time_precision ='s')
      return render_template("result.html",result = result)


if __name__ == '__main__':
   app.run(host='0.0.0.0',port='5000')
