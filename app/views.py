from app import app
from flask import Blueprint, request, redirect, render_template, url_for, make_response
from flask.views import MethodView
from app import mongo_db_collection, mongo_db_users
import requests
import json
import copy
from datetime import datetime, timedelta
from bson.json_util import dumps
from app import jinja_filters
import pymongo
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, lm
from app.forms import LoginForm2Fields
from app.models import User
from flask import jsonify
from .crypto import AESCipher, isPassword, getDigest
# from config import OPENID_PROVIDERS

stats = Blueprint('tasks', __name__, template_folder='templates')


class StatView(MethodView):

    def get(self):
        print("%s THIS IS LOGGED USER!!" % g.user)
        ans = mongo_db_collection.find({"meta": "stepicStudioVideoObj"}).sort("data.Time", pymongo.DESCENDING)
        size = ans.count()
        to_dump = copy.copy(ans)
        print(size)
        data_arr = [a['data'] for a in json.loads(dumps(to_dump))]
        print(data_arr)
        for timeObj in data_arr:
            try:
                time_in_db = int(timedelta(seconds=int(timeObj['Time']['$date'])).total_seconds())
                y = datetime.utcfromtimestamp(time_in_db/1000)
                print("DATETIME:", y)
            except Exception as e:
                print(e)

        return render_template('list_element.html', data=data_arr)


class SendPostRequest(MethodView):

    def get(self):
        payload = {'key1': 'value1', 'key2': 'value2'}
        r = requests.post("http://127.0.0.1:5000/newVideo", data=payload)
        return redirect('/')

@app.before_request
def before_request():
    g.user = current_user



class AddNewStat(MethodView):

    def post(self):
            data_dict = request.form
            print(type(request.form))
            print(data_dict)
            try:
                username = data_dict['User']
                stepName = data_dict['Name']
                Duration = data_dict['Duration']
                priority = int(data_dict['priority'])
                status = int(data_dict['status'])

                _id = mongo_db_collection.insert({"meta": "stepicStudioVideoObj"})
                dt = datetime.now()
                mongo_db_collection.update({"_id": _id}, {'$set': {'data.User': username, 'data.Name': stepName,
                                                           'data.Time': dt, 'data.Duration': Duration,
                                                           'data.priority': priority, 'data.status': status}}, upsert=False, multi=False)
                return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
            except Exception as e:
                print('ERROR! Raised ', e)
                return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    def get(self):
        resp = make_response('{"Status": "ok"}')
        resp.headers['Content-Type'] = "application/json"
        return resp

stats.add_url_rule('/', view_func=StatView.as_view("list"))
stats.add_url_rule('/newVideo', methods=('GET', 'POST'), view_func=AddNewStat.as_view("addNew"))

@app.template_filter('datetime')
def filter_datetime(time_dict):
    return jinja_filters.format_datetime(int(time_dict['$date']/1000))

@app.template_filter('status_info')
def status_info_filter(status):
    return jinja_filters.status_info(status)

@lm.user_loader
def load_user(username):
    return User(username=username, passhash="LOL")

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if g.user is not None and g.user.is_authenticated():
    #     return redirect(url_for('index'))
    form = LoginForm2Fields()
    if form.validate_on_submit():
        user_exist = find_user(username=form.username.data, password=form.password.data)
        if user_exist:
            # user = User(form.username.data, form.password.data)
            login_user(user_exist)
            flash("Logged in successfully.")
            flash('Login requested for User="%s' % (form.username.data, ))
            # loger = User(form.username.data, form.password.data)
            print("VALID")
            return redirect('/')
        else:
            return redirect('/login')
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


###TODO: Add refresh page after AJAX
@app.route("/update", methods=['POST'])
def update():
    update_list = [value for key, value in request.form.items() if key == 'name']
    update_action = [value for key, value in request.form.items() if key == 'is_update']
    print("ALL DATA :", update_action)
    print("STEPS UPDATED :")
    print(update_list)
    for i, el in enumerate(update_list):
        _id = mongo_db_collection.find({"data.Name": el}).__getitem__(0)
        print(_id, el)
        upd_field = _id
        mongo_db_collection.update({"_id": _id["_id"]}, {'$set': {'data.status': update_action[i]}}, upsert=True, multi=False)
    print("FINISHED WITH NO ERRORS")
    return jsonify(status="OK")


###TODO: Find place for this function ###
###TODO replase
def find_user(username, password):
    ans = mongo_db_users.find({"name": username})
    if ans.count() == 1:
        user_passhash = ans.__getitem__(0)['password']
        if isPassword(password, user_passhash):
            return User(username=username, passhash=user_passhash)
        else:
            return False
    else:
        return False
