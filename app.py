import os
from flask import Flask,render_template,request, url_for, redirect, abort, send_file
from flask_bootstrap import Bootstrap
import pandas as pd
import json
import os

app = Flask(__name__)

os.system("bash /app/task.sh") # I can not figure out any other way to do this!! :(

Bootstrap(app)


def get_files(req_path):

    BASE_DIR = '/app/data/csse_covid_19_data/csse_covid_19_daily_reports/'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    try:
        # Joining the base and the requested path
        abs_path = os.path.join(BASE_DIR, req_path)

        # Return 404 if path doesn't exist
        if not os.path.exists(abs_path):
            return abort(404)

        # Check if path is a file and serve
        if os.path.isfile(abs_path):
            return send_file(abs_path)

        # Show directory contents
        files = [i for i in os.listdir(abs_path) if i.endswith(".csv")]
        return sorted(files)
    except Exception as e:
        print(e)
        return []

@app.route("/", defaults={'req_path': ''})
def index(req_path):
    files = get_files(req_path)
    return render_template('index.html',files=files)

@app.route('/data/<path:req_path>')
def dir_listing(req_path):
    print('dir_listing',req_path)
    if req_path.endswith(".csv"):
        try:
            df=pd.read_csv('data/'+req_path)
            return df.to_html()
        except Exception as e:
            print(e)
            return "No such file."+req_path
    else:
        try:
            # os.system("bash /app/task.sh")
            return json.load(open('data/'+req_path,'r'))
        except Exception as e:
            print(e)
            return "No such file."+req_path



@app.route('/update_leaderboard')
def update_leaderboard():
    os.system("bash /app/task.sh")
    return "updated successfully"


@app.route("/get/files", defaults={'req_path': ''})
def serve_files(req_path):
    files = get_files(req_path)
    return json.dumps({'files':files}, indent=2)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
