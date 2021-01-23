# electricity_pillory
Electricity pillory is a docker-compose that is based on python, grafana and an influxdb. The electricity pillory pull electricity meetering data from the Danish TSO's (Energinet) platform eloverblik.dk and vizaulizes it in a grafana dashboard. After adding a user to the pillory the software pulls the data automatically and updates it once a day. Thus it is easily possible to build your own electricity dashboard and follow your own consumption/production on the dash. 

## Available features
- Add a user without specifying a meeteringID (leave it blank) will pull the data on the first meeteringpoint the eloverblik API sends
- Specify a meeteringID will pull the measurements on this specific meeteringID. Thus it is for example possible to pull data on a specific meetering point, forexample your summerhouse or your rooftop installed solar panels
-Add usernames for visualizing multiple users data. This can also be used to visualize different locations measurements ("summerhouse"/"home")
-Add cathegories in order to distinguish between different measurements (e.g. "production"/"conssumption" or "meetering1"/"meetering2"
-As it uses grafana as dashboard you can freely change the apperiance of the dahsboard and also add/remove panels
## Installation
The electricity pillory is a docker-compose that was developed to use it on a rasperry pi (raspberry pi os, earlier raspbian). It also runs on ubunut (20.04), other operating systems weren't tested yet. 
In order to install it 
