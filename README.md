# Music Garden Backend

This is the Flask web server that provides APIs to browse the music library for our android application. </br>
The server handles user authentication and data entry as well. </br>

Instructions
1.) Create a file under the root folder with the name information.py which should contain the following string variables: DB_USER, DB_PASSWORD, DB_INSTANCE, DB_DATABASE pertaining to your database. </br>

2.) Create virtual env.

>virtualenv venv

3.) Activate virtual env

>venv/Scripts/activate

4.) Install libraries from requirement.txt

>pip install -r requirement.txt

5.) Set-up the DB connections

>python manage.py db init
>python manage.py db migrate
>python manage.py db upgrade

6.) Run the app using following command

>python manage.py runserver
