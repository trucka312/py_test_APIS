## Flask Tutorial Postgres + SocketIO App Chat + Ecomere
# install 
- python3. -m venv or install pycharm run flask
- pip install -r requirements.txt
# connect database postgres
- $ sudo su postgres 
- $ psql
- $ create database flask_tutorial encoding "UTF-8";
# set permission admin
- $ create user admin with password '123456abcA';
- $ grant all privileges on database flask_tutorial to admin;

# migrate test model to database
- $ Ctrl + D exit psql and Ctrl + D exit permission su
- $ export FLASK_APP=manage.py
- $ flask db init (first run)
- $ flask db migrate
- $ flask db upgrade

# run server 
- $ flask run or python manage.py run

