from flask import Flask, render_template, redirect, request, session
import time
import requests
from models.EventsModel import EventsModel
from db import DB
from models.UsersModel import UsersModel
import os
from werkzeug.utils import secure_filename

db = DB()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = './static'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/login', methods=['POST', 'GET'])
def login():
        if request.method == 'GET':
            return render_template('login.html', title='Please fill in this form to sign in an account:')
        elif request.method == 'POST':
            um = UsersModel(db.get_connection())
            um.init_table()
            if um.exists(request.form['email'], request.form['pswd']):
                session['username'] = request.form['email']
                return redirect('/main')
            else:
                return render_template('login.html', title='Wrong email or password')


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html')
    elif request.method == 'POST':
        um = UsersModel(db.get_connection())
        um.init_table()
        um.insert(request.form['email'], request.form['pswd'], request.form['surname'],
                  request.form['name'], request.form['fname'], request.form['date'],
                  request.form.get('city'), request.form.get('school'), request.form['doc_id'])
        session['username'] = request.form['email']
        print(um.get_all())
        return redirect('/main')

        # return render_template('sign_up', title='Specified account already exists. Log in with it or create new one')


@app.route('/logout')
def logout():
    session.pop('username', 0)
    return redirect('/login')


@app.route('/my_page')
def my_page():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'GET':
        nm = EventsModel(db.get_connection())
        nm.init_table()
        um = UsersModel(db.get_connection())
        um.init_table()
        em = um.get_email(session['username'])
        uname = session['username']
        image = um.get_avatar(uname)
        return render_template('account.html', username=uname, news=nm.get_all(uname),
                               email=em, own="True", image=image)


@app.route('/about')
def about():
    if request.method == 'GET':
        return render_template('about.html')


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = EventsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/index")


@app.route('/uploader', methods=['GET', 'POST'])
def change_img():
    if request.method == 'POST':
        f = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(file_path)
        um = UsersModel(db.get_connection())
        um.init_table()
        um.change_avatar(session['username'], f.filename)
        return redirect('/my_page')


@app.route('/', methods=['POST', 'GET'])
@app.route('/main', methods=['POST', 'GET'])
def main():
    em = EventsModel(db.get_connection())
    em.init_table()
    um = UsersModel(db.get_connection())
    um.init_table()
    if request.method == "POST":
        name, date, volnum, city, loc, description = request.form["name"], request.form["evdate"], \
                                               request.form["volnum"], request.form.get("cityselect"), \
                                               request.form["location"], request.form["description"]
        status = "Ведется набор"
        em.insert(date, status, name, volnum, description, city, loc)
        return redirect("/main")
    else:
        return render_template('home.html',  events=em.get_all())


@app.route('/user/<uname>', methods=['GET'])
def show_user(uname):
    if 'username' not in session:
        return redirect('/login')
    em = EventsModel(db.get_connection())
    em.init_table()
    um = UsersModel(db.get_connection())
    um.init_table()
    email = um.get_email(session['username'])
    image = um.get_avatar(uname)
    if uname == session['username']:
        owning = 'True'
    else:
        owning = 'False'
    if request.method == "GET":
        print(um.get_all(uname))
        return render_template('account.html', username=uname, news=um.get_all(uname), email=email,
                               own=owning, image=image)


def check_if_avatar_exists(item):
    if item[4]:
        print(item[4])
    else:
        print('f')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
