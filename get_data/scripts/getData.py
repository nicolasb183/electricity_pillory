import json
import pandas as pd
import requests
import time
from datetime import datetime, timedelta
from influxdb import DataFrameClient
from influxdb import InfluxDBClient
import logging

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

time.sleep(30)
class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

#define client stuff
host='db'
port=8086
user = 'admin'
password = 'user123'
dbname = 'db_0'
protocol = 'line'
old_users=pd.DataFrame()
client1 = InfluxDBClient(host, port, user, password, dbname)
client2 = DataFrameClient(host, port, user, password, dbname)


while(True):
    q = 'select * from "users"'
    all_users = pd.DataFrame(client1.query(q).get_points())
    now = datetime.now()
    if (not(old_users.equals(all_users)) or now==now.replace(hour=4, minute=7)):

        for index, row in all_users.iterrows():

            token = row['token']
            meter=row['meter']
            consumer=row['name']
            departement=row['departement']
            #get the correct dates
            today = datetime.today().date()
            url = 'https://api.eloverblik.dk/CustomerApi/api'

            #get the refresh token from api
            #response = requests.get(url, headers = {"Authorization":"Bearer " + token})
            response = requests.get(url+'/Token',auth=BearerAuth(token))

            #extract the token
            json_response = response.json()
            refresh_token=json_response["result"]

            #If a meeteringmoint is defined, use it
            if meter:
                mp_list=json.dumps({"meteringPoints": {"meteringPoint":[meter]}})
                headers = {'Content-type': 'application/json'}
                response = requests.post(url+'/MeterData/GetTimeSeries/'+str(today.year)+'-01-01'+'/'+str(today)+'/'+'Hour',auth=BearerAuth(refresh_token), data=mp_list,headers=headers)

            #Else find the existing meetering points and take the first
            else:

                #Get the meetering point
                response = requests.get(url+'/MeteringPoints/MeteringPoints?includeAll=true',auth=BearerAuth(refresh_token))
                metering_points = response.json()

                #get the relevant meetering points (E17)
                mp=[]
                for x in (range(len(metering_points['result']))):
                    if metering_points['result'][x]['typeOfMP']=='E17':
                        mp.append(metering_points['result'][x]['meteringPointId'])

                #create a body for data request
                mp_list=json.dumps({"meteringPoints": {"meteringPoint":[mp[0]]}})


                #get the data
                headers = {'Content-type': 'application/json'}
                response = requests.post(url+'/MeterData/GetTimeSeries/'+str(today.year)+'-01-01'+'/'+str(today)+'/'+'Hour',auth=BearerAuth(refresh_token), data=mp_list,headers=headers)

            measurements = response.json()

            data=(pd.json_normalize(measurements['result'][0]["MyEnergyData_MarketDocument"]["TimeSeries"][0]["Period"], ['Point']))
            time1=(pd.json_normalize(measurements['result'][0]["MyEnergyData_MarketDocument"]["TimeSeries"][0]["Period"]))

            start=(time1['timeInterval.start'][0])
            end=(time1['timeInterval.end'][(len(time1)-1)])

            date_range=(pd.date_range(start=start, end=end, freq='1H'))

            data['Date']=date_range[:-1]

            data=data.drop(columns=['out_Quantity.quality', 'position'])

            data[['User']]=consumer
            data[['Departement']]=departement

            data['out_Quantity.quantity'] = data['out_Quantity.quantity'].astype(float)

            data['out_Quantity.quantity.per.person'] = data['out_Quantity.quantity']/row['persons']


            datatags=['User','Departement']

            data=data.set_index('Date')




            client2.write_points(data, 'electricity', protocol=protocol, tag_columns=datatags)

    else:
        pass

    old_users=all_users

    time.sleep( 5 )
