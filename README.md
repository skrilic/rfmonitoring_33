- Description
- Administration manual
- USer Manual

# README

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for?

- Quick summary
- Version
- [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up?

- Summary of set up
- Configuration
- Dependencies
-

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

6.  Since the database tables already exist We must apply fake initial migration `python manage.py migrate --fake-initial`. Issuing showmigrations is going to show what is the situation with migrations now.

- How to run tests
- Deployment instructions

### Contribution guidelines

- Writing tests
- Code review
- Other guidelines

### Who do I talk to?

- Repo owner or admin
- Other community or team contact
