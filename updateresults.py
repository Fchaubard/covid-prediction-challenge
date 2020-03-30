#!/usr/bin/python
import sys
from datetime import datetime
from glob import glob
import os
import json
import sys
from datetime import datetime
from glob import glob
import os
import json
import pandas as pd
from datetime import timedelta
import json 


# LEADERBOARD_SAVE_PATH = '/Users/francoischaubard/Desktop/leaderboard.json'
LEADERBOARD_SAVE_PATH = '/app/data/leaderboard.json'

def main():
    # print command line arguments
    print(sys.argv)
    SUBMISSION_FOLDER_PATH = sys.argv[1]
    COVID_REPO_PATH = sys.argv[2]
    RELATIVE_TIME_SERIES_DATA_PATH = 'csse_covid_19_data/csse_covid_19_time_series/'
    RELATIVE_DAILY_SERIES_DATA_PATH = 'csse_covid_19_data/csse_covid_19_daily_reports/'

    TRUTH_DATA_PATH = os.path.join(COVID_REPO_PATH,RELATIVE_TIME_SERIES_DATA_PATH)
    TRUTH_DATA_PATH = os.path.join(TRUTH_DATA_PATH,"time_series_covid19_deaths_global.csv")

    # produce the truth data
    df = pd.read_csv(TRUTH_DATA_PATH)
    df_country_level = df.groupby("Country/Region", as_index=True).sum().reset_index()
    df_country_level = df_country_level.drop(["Lat","Long"],axis=1)

    global_stats = df_country_level.sum(axis=0)
    df_global_level = global_stats[3:]
    df_global_level = df_global_level.to_frame()
    # df_global_level.columns = ["Deaths"]
    global_dict = df_global_level.to_dict()[0]
    global_dict["Country/Region"]="World"
    df_country_level = df_country_level.append(global_dict,ignore_index=True)
    df_country_level = df_country_level.set_index('Country/Region')
    df_country_level = df_country_level.sort_index()
    df_country_level.columns = [str(datetime.strptime(i, '%m/%d/%y').date()) for i in df_country_level.columns]

    final_scores = {}

    print("Starting update at:",str(datetime.now()),SUBMISSION_FOLDER_PATH)
    for f in glob(SUBMISSION_FOLDER_PATH+"predictions/*"):
        if not os.path.isdir(f):
            continue
        print("Calculating results for:",str(datetime.now()),f)
        meta_file = os.path.join(f,"metadata.json")
        meta_dict = json.load(open(meta_file))
        submission_id = f.split("/")[-1]
        final_scores[submission_id] = meta_dict

        submission_datetime = datetime.strptime(meta_dict['submitted_at_datetime'], '%Y-%m-%d %H:%M:%S.%f')
        submission_valid_beginning = submission_datetime.date()+timedelta(days=7)
        submission_file = os.path.join(f,"predictions.csv")
        
        
        submission_df = pd.read_csv(submission_file)
        submission_df = submission_df.set_index("Place").sort_index()
        submission_df = submission_df.reset_index().groupby(['Place','Date'])['Deaths'].aggregate('first').unstack()
        
        # remove dates from columns before 7 days after submission and anything after today
        most_current_date = datetime.strptime(df_country_level.columns[-1], '%Y-%m-%d').date()
        valid_columns = [c for c in submission_df.columns if datetime.strptime(c, '%Y-%m-%d').date()>=submission_valid_beginning and datetime.strptime(c, '%Y-%m-%d').date()<=most_current_date] 
        valid_countries = set(submission_df.index)&set(df_country_level.index)
        print("submission: we can start evaluating at "+str(submission_valid_beginning) + " and will end at " + str(most_current_date) + " with valid countries "+str(len(valid_countries)))
        
        truth = df_country_level.loc[valid_countries,valid_columns].sort_index()
        pred = submission_df.loc[valid_countries,valid_columns].sort_index()
        print(truth.shape,pred.shape)
        residual = (truth-pred).abs()
        scores = residual.sum(axis=1)/len(valid_columns)
        final_scores[submission_id]["scores"] = scores.to_dict()

    with open(LEADERBOARD_SAVE_PATH, 'w') as json_file:
        json.dump(final_scores, json_file,indent=4)




if __name__ == "__main__":
    main()
#This script updates the records 
