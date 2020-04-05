#!/usr/bin/python
import sys
from datetime import datetime
from glob import glob
import os
import json
import pandas as pd
from datetime import timedelta
import os


BASE_DATA_REPO = "/app/data/"



def main():
    # 1. first open JHU and NYT to produce "Truth" key and use JHU and NYT to produce "Truth" matrix
    # 2. Then forloop over predictions to measure "Truth" matrix to prediction matrix
    # 3. add to final_dict to go to leaderboard which is format: 
    #        'predictions':
    #              'prediction1': 
    #                       'meta_data': [],
    #                       'scores': [
    #                                 'place1':score,
    #                                 'place2':score,
    #                                  ....
    #                                 ]
    #                       'dates': [YYYY-MM-DD,YYYY-MM-DD...] 
    #                       'predictions':
    #                              'place1': [v1,v2,v3...],
    #                              'place2': [v1,v2,v3...],
    #              'prediction2': 
    #                       'meta_data': [],
    #                       'scores': [
    #                                 'place1':score,
    #                                 'place2':score,
    #                                  ....
    #                                 ]
    #                       'dates': [YYYY-MM-DD,YYYY-MM-DD...] 
    #                       'predictions':
    #                              'place1': [v1,v2,v3...],
    #                              'place2': [v1,v2,v3...],
    # .... 
    #      'truth': 
    #                   'dates': [YYYY-MM-DD,YYYY-MM-DD...] 
    #                   'timeseries':
    #                          'place1': [v1,v2,v3...],
    #                          'place2': [v1,v2,v3...],

    final_dict = {}


    # 1. first open JHU and NYT to produce "Truth" key and use JHU and NYT to produce "Truth" matrix
    JHU = os.path.join(BASE_DATA_REPO, 'covid_truth/jhu/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    NYT_states = os.path.join(BASE_DATA_REPO, 'covid_truth/nyt/us-states.csv')
    NYT_counties = os.path.join(BASE_DATA_REPO, 'covid_truth/nyt/us-counties.csv')

    #---

    df_jhu = pd.read_csv(JHU)
    df_nyt_states = pd.read_csv(NYT_states)
    df_nyt_counties = pd.read_csv(NYT_counties)

    #---

    # JHU to canonical: get correct columns and add World
    df_country_level = df_jhu.groupby("Country/Region", as_index=True).sum().reset_index()
    df_country_level = df_country_level.drop(["Lat","Long"],axis=1)

    global_stats = df_country_level.sum(axis=0)
    df_global_level = global_stats[3:]
    df_global_level = df_global_level.to_frame()
    global_dict = df_global_level.to_dict()[0]
    global_dict["Country/Region"]="World"


    country_stats = df_country_level.loc[df_country_level["Country/Region"] == "US"]
    dates = country_stats.columns[4:]
    data = country_stats.values[:,4:][0].astype('float')
    truth_matrix = df_country_level.values[:,1:]
    country_dict = {d:v for d,v in zip(dates,data)}


    df_country_level = df_country_level.append(global_dict,ignore_index=True)
    df_country_level = df_country_level.set_index('Country/Region')
    df_country_level = df_country_level.sort_index()
    df_country_level.columns = [str(datetime.strptime(i, '%m/%d/%y').date()) for i in df_country_level.columns]
    df_country_level

    df_jhu=df_country_level.copy()
    df_jhu.index.name = "Place"

    # ---
    # NYT states to canonical
    df_nyt_states.rename(columns={"date":"Date","deaths":"Deaths"}, inplace=True)
    df_nyt_states = df_nyt_states.drop(columns=["fips","cases"])

    df_nyt_states = df_nyt_states.pivot_table(index="state", columns="Date")
    df_nyt_states.columns = df_nyt_states.columns.droplevel(level=0)
    df_nyt_states.index.name = "Place"
    df_nyt_states = df_nyt_states.rename(index={'Georgia': 'Georgia_State'})

    #---
    # NYT county to canonical
    df_nyt_counties['Place'] = df_nyt_counties[["state","county"]].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
    df_nyt_counties.rename(columns={"date":"Date","deaths":"Deaths"}, inplace=True)
    df_nyt_counties = df_nyt_counties.drop(columns=["county","state","fips","cases"])
    df_nyt_counties = df_nyt_counties.pivot_table(index="Place", columns="Date")
    df_nyt_counties.columns = df_nyt_counties.columns.droplevel(level=0)
    #---

    df_truth = pd.concat([df_nyt_states, df_nyt_counties,df_jhu], axis=0,join="inner").sort_index()

    final_dict["Truth"] = {}
    for index, row in df_truth.iterrows():
        final_dict["Truth"][row.name] = list(row)
    final_dict["Truth"]["Dates"] = list(df_truth.columns)


    # 2. Then forloop over predictions to measure "Truth" matrix to prediction matrix

    PREDICTIONS_ROOT_FOLDER = os.path.join(BASE_DATA_REPO, "google_storage_data/predictions/")

    final_scores = {}
    submission_df = None
    print("Starting update at:",str(datetime.now()),PREDICTIONS_ROOT_FOLDER)
    for f in glob(PREDICTIONS_ROOT_FOLDER+"/*"):
        try:
            print("Calculating results for:",str(datetime.now()),f)
            
            meta_file = os.path.join(f,"metadata.json")
            meta_dict = json.load(open(meta_file))
            submission_id = f.split("/")[-1]
            final_scores[submission_id] = meta_dict
            

            submission_datetime = datetime.strptime(meta_dict['submitted_at_datetime'], '%Y-%m-%d %H:%M:%S.%f')
            submission_valid_beginning = submission_datetime.date()+timedelta(days=7)
            submission_file = os.path.join(f,"predictions.csv")
            
            submission_df = pd.read_csv(submission_file)
            submission_df = submission_df.set_index("Place")

        #     submission_df = submission_df.set_index("Place").sort_index()
        #     submission_df = submission_df.reset_index().groupby(['Place','Date'])['Deaths'].aggregate('first').unstack()
            
        #     # remove dates from columns before 7 days after submission and anything after today
            most_current_date = datetime.strptime(df_truth.columns[-1], '%Y-%m-%d').date()
            valid_columns = set([c for c in submission_df.columns[1:] if datetime.strptime(c, '%Y-%m-%d').date()>=submission_valid_beginning and datetime.strptime(c, '%Y-%m-%d').date()<=most_current_date])
            valid_rows = set(submission_df.index)&set(df_truth.index)
            print("submission: we can start evaluating at "+str(submission_valid_beginning) + " and will end at " + str(most_current_date) + " with valid countries "+str(len(valid_rows)) + "with valid dates "+str(len(valid_columns)))
            
            truth = df_truth.loc[valid_rows,valid_columns].sort_index()
            pred = submission_df.loc[valid_rows,valid_columns].sort_index()
            print(truth.shape,pred.shape)
            residual = (truth-pred).abs()
            scores = residual.sum(axis=1)/len(valid_columns)
            final_scores[submission_id]["scores"] = scores.to_dict()
            final_scores[submission_id]["days_scored"] = len(valid_columns)
            final_scores[submission_id]["dates_scored"] = list(valid_columns)
        except Exception as e:
            print("ERROR ",f , e)

    final_dict["Predictions"] = final_scores

    final_dict["LastUpdatedAt"] = str(datetime.now())


    with open(os.path.join(BASE_DATA_REPO,'leaderboard.json'), 'w') as json_file:
        json.dump(final_dict, json_file, indent=4)
    
    df_truth.to_csv(os.path.join(BASE_DATA_REPO,'all_data.csv'))

    print("Updated leaderboard!")


if __name__ == "__main__":
    main()
