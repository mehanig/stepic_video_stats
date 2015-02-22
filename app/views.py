from app import app
from flask import Blueprint, request, redirect, render_template, url_for, make_response
from flask.views import MethodView
from app import mongo_db_collection
import requests
import json
import copy
from datetime import datetime, timedelta
from bson.json_util import dumps
from app import jinja_filters
import pymongo

stats = Blueprint('tasks', __name__, template_folder='templates')


class StatView(MethodView):

    def get(self):
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

        return render_template('main_page.html', data=data_arr)


class SendPostRequest(MethodView):

    def get(self):
        payload = {'key1': 'value1', 'key2': 'value2'}
        r = requests.post("http://127.0.0.1:5000/newVideo", data=payload)
        return redirect('/')


class AddNewStat(MethodView):

    def post(self):
            data_dict = request.data
            print(type(request.data))
            print(data_dict)
            data_dict = json.loads(data_dict.decode("utf-8"))
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