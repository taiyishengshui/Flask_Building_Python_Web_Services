from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request
import json
import dateparser
import datetime
import string

import dbconfig

if dbconfig.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper

app = Flask(__name__)
DB = DBHelper()

categories = ['mugging', 'break-in']


@app.route("/")
def home(error_massage=None):
    crimes = DB.get_all_crimes()
    crimes = json.dumps(crimes)
    # print("crimes:", crimes)
    return render_template("home.html", crimes=crimes, categories=categories,error_massage=error_massage)


@app.route("/add", methods=["post"])
def add():
    try:
        data = request.form.get("userinput")
        DB.add_input(data)
    except Exception as e:
        print('Exception is:', e)
    return home()


@app.route("/clear")
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print('Exception is:', e)
    return home()


@app.route("/submitcrime", methods=['POST'])
def submitcrime():
    category = request.form.get("category")
    if category not in categories:
        return home()
    date = format_date(request.form.get("date"))
    if not date:
        print("error date",date)
        return home("Invalid date. Please use yyyy-mm-dd format")
    try:
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
    except ValueError:
        return home()
    # description = request.form.get("description")
    # print("date", date)
    ddd = sanitize_string(request.form.get("description"))
    #官方版本中在此处有bug
    #description =sanitize_string(request.form.get("description"))
    #原因，list无法保存传给mysql
    #需要转换成string使用 "".join方法将 list转换为string
    description = "".join(sanitize_string(request.form.get("description")))
    DB.add_crime(category, date, latitude, longitude, description)
    return home()

def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None


def sanitize_string(userinput):
    whilelist = string.ascii_letters + string.digits + " !?$.,;:-'()&"
    return filter(lambda x: x in whilelist, userinput)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
