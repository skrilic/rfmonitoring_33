
# README
## rfmonitoring_33 - Python Django project
RFmonitor project - RF from administratory perspective.



## Description
  
  RFmonitor is a Django web framework project with three applications named: "Asset", "Base stations" and "RFdjango". This is the long-term project of developing software for taking care of different aspects of managing information about infrastructures and tasks involved in day-to-day administratory work.

* "Asset" - Handling inventory data about measurement equipment, software, and instruments used for administrative tasks. Besides that, it is used for recording data about fixed measurement locations and instruments in a journaling form.

* "RFDjango" -  Handling data about TV and FM broadcasting transmitters in a form requested by regulatory bodies and suitable to use with prediction software such as ATDI ICS Telecom for instance. It is also useful for journaling and documenting on-site measurements.
 
* "Base Stations" - Handling data provided by mobile operators about installed base stations in the format suitable for import in ATDI ICS Telecom for further analysis and prediction.


## INSTALL

  The project was developed for Python3.x and Django3.x. Initially the SQLite has been chosen for the database backend. Pipfile is included in the project tree and to use it you must have ```pipenv``` installed then you can start with installing and activating the environment in the base ```rfmonitoring_33``` folder:
* ```pipenv install```
* ```pipenv shell```

When the environment is activated go to the ```project_root``` folder and initiate creating database infrastructure:
* ```python manage.py makemigrations admin asset rfdjango base_stations```
* ```python manage.py migrate```

Crate super user for Web site and for further settings.
* ```python manage.py createsuperuser```


### CHANGE SETTINGS

Initially project use development settings with ```DEBUG=True```. The secret key is inside the file but for production it is needful to switch ```DEBUG=False``` and to set environment variable ```RFMONITORING_SECRET_KEY``` so the django can find it in production. The selection between development and production is made by editing file ```project_root/RFmonitor/settings/__init__.py```

### SETTING HOME PAGE MAP
Navigate to the ```Map definitions``` on the admin site inside ```RFdjango``` application. Add ```name``` as __home_page__, set the center point of your map and zoom you want. The map should appear on the front page of the site.
![Admin site -> RFdjango -> Map definitions](https://github.com/skrilic/rfmonitoring_33/tree/master/images/map_definitions.png?raw=true)
