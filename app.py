import os
from flask import Flask,Response,render_template,request, url_for, redirect, abort, send_file,send_from_directory
from flask_bootstrap import Bootstrap
import pandas as pd
import json
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import random
import string
from glob import glob

import copy

#----- setup
# os.system("bash /app/task.sh") # I can not figure out any other way to do this!! :(
app = Flask(__name__)
Bootstrap(app)
#-----



#----- for uploading
UPLOAD_FOLDER = '/app/data/google_storage_data/predictions/'
if not os.path.exists(UPLOAD_FOLDER):
    print("ERROR! NO UPLOAD_FOLDER: ", UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = set(['txt', 'csv'])
#-----



def get_subset_of_lb_for_place(data, place):
    data_smaller = copy.deepcopy(data)

    for place_ in data["Truth"].keys():
        if not (place_==place or place_=="Dates"):
            data_smaller["Truth"][place_]=[]

    for submission_id in data["Predictions"].keys():
        if place in data["Predictions"][submission_id]['TimeSeries']:
            for place_ in data["Predictions"][submission_id]['TimeSeries'].keys():
                if not (place_==place or place_=="Dates"):
                    try:
                        del data_smaller["Predictions"][submission_id]['TimeSeries'][place_]
                    except Exception:
                        pass
            data_smaller["Predictions"][submission_id]["scores"] = {place:data["Predictions"][submission_id]["scores"][place]}
        else:
            del data_smaller["Predictions"][submission_id]

    return data_smaller


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/submit_form', methods=[ 'GET', 'POST'])
def submit_form():
    print("submit_form ")
    print(request.form)
    print(request.files)
    print(request)
    if request.method == 'POST':

        if 'file' not in request.files:
            print('No file part')
            return 'No file selected'

        file = request.files['file']

        if file.filename == '':
            print('No selected file')
            return 'No file selected'
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("filename",filename)

            now = datetime.now()
            form_data = request.form.to_dict(flat=False)
            email = None
            if "email" in form_data:
                email = form_data["email"]
                print(email)
            source = None
            if "source" in form_data:
                source = form_data["source"]
                print(source)
            # grab the data 
            meta_dict = { 
                          "submitted_at_datetime": str(now),
                          "submission_name": form_data['email'][0],
                          "source": form_data['source'][0],
                        }

            print("meta_dict" , meta_dict)
            folder_name =  str(now.date()).replace("/","_") +"_"+ randomString(10)
            print("folder_name",folder_name)
            os.system("mkdir "+UPLOAD_FOLDER + folder_name)
            file_path = UPLOAD_FOLDER + folder_name +"/"+ filename
            file.save(file_path)
            with open(UPLOAD_FOLDER + folder_name +"/"+ "metadata.json", 'w') as json_file:
                json.dump(meta_dict, json_file, indent=4)

            # TODO: validate the csv file better than this!
            try:
                df = pd.read_csv(file_path)
            except Exception as e:
                print("wrong format!")
                return 'Wrong csv format. please see example predictions.csv file'
                os.system("rm -rf "+UPLOAD_FOLDER +folder_name)
            # TODO: load the data to gcp?

            print("DONE with file_path",file_path)
            return "OK"
        else:
            print("bad input", file.filename)
            return "Not a valid filetype or just bad input"


def get_files(req_path):

    BASE_DIR = '/app/data/covid_truth/jhu/csse_covid_19_data/csse_covid_19_daily_reports/'

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

@app.route("/submit")
def submit():
    return render_template('submit.html')

@app.route("/about")
def about():
    return render_template('about.html')

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
    return json.dumps(json.load(open("/app/data/leaderboard.json",'r')),sort_keys=True, indent=4)

@app.route('/see_predictions')
def see_predictions():
    d = [f for f in os.listdir(UPLOAD_FOLDER)]
    return str(len(d)) +" <br/><br/><br/><br/> "+ str(d)


@app.route('/get/leaderboard', methods=[ 'GET'])
def get_leaderboard():
    with open('/app/data/leaderboard.json') as f:
        data = json.load(f)
    place = "World"
    if request.method == 'GET':
        try:
            place = request.args.get('place')
            print("GET place ", place)
        except Exception as e:
            print(place,e)

    data = get_subset_of_lb_for_place(data, place)
    return json.dumps(data,sort_keys=True)


# @app.route("/get/files", defaults={'req_path': ''})
# def serve_files(req_path):
#     files = get_files(req_path)
#     return json.dumps({'files':files}, indent=2)

@app.route('/get_data/<path:filename>')
def download_file(filename):
    print("HIT",filename)
    return send_from_directory("/app/",
                               filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
