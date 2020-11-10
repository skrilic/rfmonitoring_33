
# README
## Python Django project
RFmonitor project - RF from administratory perspective.



## Description
  
  RFmonitor is a Django web framework project with three applications named: "Asset", "Base stations" and "RFdjango". This is the long-term project of developing software for taking care of different aspects of managing information about infrastructures and tasks involved in day-to-day administratory work.

* "Asset" - Handling inventory data about measurement equipment, software, and instruments used for administrative tasks. Besides that, it is used for recording data about fixed measurement locations and instruments in a journaling form.

* "RFDjango" -  Handling data about TV and FM broadcasting transmitters in a form requested by regulatory bodies and suitable to use with prediction software such as ATDI ICS Telecom for instance. It is also useful for journaling and documenting on-site measurements.
 
* "Base Stations" - Handling data provided by mobile operators about installed base stations in the format suitable for import in ATDI ICS Telecom for further analysis and prediction.




### What is this repository for?

- Quick summary
- Version
- [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)



## Administration manual

### How do I get set up?

- Summary of set up
- Configuration
- Dependencies



#### Database configuration

##### Reset database migration without loosing data

This method I've found at the https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html

1.  Make sure your models fits the current database schema by trying to create new migrations:  
    `python manage.py makemigrations`
    If there is any pending migration then apply it, must be replied with `No changes detected`

2.  Clear the migration history:
    `python manage.py showmigrations`

3.  Make a fake migration:
    `python manage.py migrate --fake <app> zero`
    You can check the migration status by issuing showmigrations again.

4.  Remove all files inside the migration subfolder in the application folder except `__init__.py`. You can check the migration status by issuing showmigrations again.

5.  Create initial migration `python manage.py makemigrations`

6.  Since the database tables already exist We must apply fake initial migration `python manage.py migrate --fake-initial` or `python manage.py migrate --fake`. Issuing showmigrations is going to show what is the situation with migrations now.


## User manual

### Who do I talk to?

- Repo owner or admin
- Other community or team contact
