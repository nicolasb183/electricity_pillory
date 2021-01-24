
# Electricity Pillory
Electricity Pillory is a docker-compose that is based on python, grafana and an influxDB. The Electricity Pillory pulls electricity metering data from the Danish TSO's (Energinet) platform eloverblik.dk and visualizes it in a grafana dashboard. After adding a user to the pillory the software pulls the data automatically and updates it once a day. Thus it is easily possible to build your own electricity dashboard and follow your own consumption/production on the dash. 

## Available features
- Add a user without specifying a meteringID (leave it blank) will pull the data on the first metering point the eloverblik API sends
- Specify a meteringID will pull the measurements on this specific meteringID. Thus it is for example possible to pull data on a specific metering point, for example your summerhouse or your rooftop installed solar panels
- Add usernames for visualizing multiple users data. This can also be used to visualize different locations measurements ("summerhouse"/"home")
- Add categories in order to distinguish between different measurements (e.g. "production"/"consumption" or "metering1"/"metering2"
- As it uses grafana as dashboard you can freely change the appearance of the dashboard and also add/remove panels
## Installation
The Electricity Pillory is a docker-compose that was developed to use it on a raspberry pi (raspberry pi os, earlier raspbian). It also runs on ubunut (20.04), other operating systems weren't tested yet. 
In order to install it download the repository or do a simple 
```
git clone https://github.com/nicolasb183/electricity_pillory.git
```

As it is a docker compose you will both need the docker software and docker-compose installed on your system. Find a guide to install this on a search engine of your choice. 
Next issue the following commands:
```##cd into the electricity pillory folder
cd electricity_pillory
##build the containers
docker-compose build
##After the build process is done (it may take a while) start the docker-compose
docker-compose up
##If you would like to start it as a daemon ad a hyphen d to the command
docker-compose up -d
```
## Add a user
The Electricity Pillory exposes a simple web form on port 5000 to add new users to the database. to access it simply go to your browser and type  
```localhost:5000```
- Navn: Your name/your companies name
- Token: A token in order to access data from ELOverblik. In order to receive a token see the guide below. 
- Maalepunkt: Your meteringpointID (optional, if you leave it blank the first consumption meteringpointId will be chosen)
- Personer i husholdning : The number of persons living together with you
- Afdeling: Optional to add an additional tag - e.g. "Production"/"Consumption" or "IT Department"/"Accounting"

### Add a metering point to Eloverblik
Before you can access the data from Eloverblik you need to make sure that you added your metering points to portal. In order to do so read the following from Energinet. 

[Read the guide](https://energinet.dk/-/media/1C8ECDF4A59C4568A5C05798E4D2B5BD.pdf)
### Get a token

[Get a token](https://energinet.dk/-/media/89C11ABC00C84D4CA8B3B96819169A44.pdf)
## The grafana dashboard
The grafana dashboard can be accessed on port 3000. To access it simply type ```localhost:3000```. The default username and password for grafana is admin/admin. After the first login you will have to provide a new password for the admin user. 
### Add the influxDB data source to grafana
Go to the gearwheel icon and click on "Data Source". Then click on "Add data source" and choose "influxDB". Enter the following configurations:
- url: db:8086
- Database: db_0
- user:admin
- password:user123

click on "Save and Test". If everything went right you now added your influxDB data source to grafana. 
#### Add your first dashboard
A default dashboard is added to the repository and can be used in order to do some initial checks. Feel free to modify/change the dashboard in whatever way you like. In order to add the dashboard go to the plus sign (+) and click on "import". Next click on "Upload JSON file". Choose the "Solar_dashboard.json" file from the Electricity Pillory. For the "Solar_dashjson.json" you need to specify production/consumption (produktion/forbrug) in the "Afdeling" field when adding a users, as the dash is filtering the data based on those attributes. 
## Default settings
### Add a user
```localhost:5000```
### Grafana
```localhost:3000```  
username:admin  
password:admin  
### Database
network address (inside the compose): db  
port: 8086  
database:db_0  
username:admin  
password:user123 
## ToDo
- Add correct volumes to grafana in the docker-compose file so settings will be kept
- Probably better error handling would be nice - the pillory crashes, when something goes wrong
- A better user interface to the database would be useful. Currently you have to edit the database directly from within the container
## Disclaimer
I'm either a python programmer or a granary specialist. I built this dashboard for my private use and offer it to others without any warranty or support. Feel free to use it if you like. I would be happy for any contributions to the project. 

