#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 20:09:05 2018

@author: zihaoli
"""

import pandas as pd
import numpy as np
import plotly
plotly.tools.set_credentials_file(username='CaesarLee666', api_key='nhXkNfC3K3hntFJCGyuL')
import plotly.plotly as py
import plotly.graph_objs as go


df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

#Data Preparation

#Replacing spaces with null values in total charges column
df['TotalCharges'] = df["TotalCharges"].replace(" ",np.nan)

#replace values
df["SeniorCitizen"] = df["SeniorCitizen"].replace({1:"Yes",0:"No"})

#Dropping null values from total charges column which contain .15% missing data 
df = df[df["TotalCharges"].notnull()]
df = df.reset_index()[df.columns]

#convert to float type
df["TotalCharges"] = df["TotalCharges"].astype(float)

#replace 'No internet service' to No for the following columns
replace_cols = [ 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                'TechSupport','StreamingTV', 'StreamingMovies']
for i in replace_cols : 
    df[i]  = df[i].replace({'No internet service' : 'No'})

#available online services
df['available_online_services'] = (df[['OnlineSecurity', 'DeviceProtection', 'StreamingMovies', 
  'TechSupport', 'StreamingTV', 'OnlineBackup']] == 'Yes').sum(axis=1)

def col_bin(df) :
    
    if df["available_online_services"] == 0:
        return "NoServices"
    elif df['available_online_services'] == 2:
        return "DeviceProtection"
    elif df['available_online_services'] == 3:
        return "StreamingMovies"
    elif df['available_online_services'] == 4:
        return "TechSupport"
    elif df['available_online_services'] == 5:
        return "StreamingTV"
    elif df['available_online_services'] == 6:
        return "OnlineBackup"
    if df["available_online_services"] == 1:
        return "OnlineSecurity"
    
df["available_online_services"] = df.apply(lambda df:col_bin(df),
                                      axis = 1)

def tenure_bin(df) :
    
    if df["tenure"] <= 12 :
        return "0-1years"
    elif (df["tenure"] > 12) & (df["tenure"] <= 24 ):
        return "1-2years"
    elif (df["tenure"] > 24) & (df["tenure"] <= 36) :
        return "2-3years"
    elif (df["tenure"] > 36) & (df["tenure"] <= 48) :
        return "3-4years"
    elif (df["tenure"] > 48) & (df["tenure"] <= 60) :
        return "4-5years"
    elif df["tenure"] > 60 :
        return "over5years"
df["tenure_group"] = df.apply(lambda df:tenure_bin(df),
                                      axis = 1)

#Separating churn and non churn customers
churn     = df[df["Churn"] == "Yes"]
not_churn = df[df["Churn"] == "No"]

trace1 = go.Scatter3d(x = churn["MonthlyCharges"],
                      y = churn["TotalCharges"],
                      z = churn["tenure"],
                      mode = "markers",
                      name = "Churn customers",
                      text = "Id : " + churn["customerID"],
                      marker = dict(size = 1,color = "red")
                     )
trace2 = go.Scatter3d(x = not_churn["MonthlyCharges"],
                      y = not_churn["TotalCharges"],
                      z = not_churn["tenure"],
                      name = "Non churn customers",
                      text = "Id : " + not_churn["customerID"],
                      mode = "markers",
                      marker = dict(size = 1,color= "blue")
                     )



layout = go.Layout(dict(title = "Customer Attrition with Numeric Variables",
                        scene = dict(camera = dict(up=dict(x= 0 , y=0, z=0),
                                                   center=dict(x=0, y=0, z=0),
                                                   eye=dict(x=1.25, y=1.25, z=1.25)),
                                     xaxis  = dict(title = "monthly charges",
                                                   gridcolor='rgb(255, 255, 255)',
                                                   zerolinecolor='rgb(255, 255, 255)',
                                                   showbackground=True,
                                                   backgroundcolor='rgb(230, 230,230)'),
                                     yaxis  = dict(title = "total charges",
                                                   gridcolor='rgb(255, 255, 255)',
                                                   zerolinecolor='rgb(255, 255, 255)',
                                                   showbackground=True,
                                                   backgroundcolor='rgb(230, 230,230)'
                                                  ),
                                     zaxis  = dict(title = "tenure",
                                                   gridcolor='rgb(255, 255, 255)',
                                                   zerolinecolor='rgb(255, 255, 255)',
                                                   showbackground=True,
                                                   backgroundcolor='rgb(230, 230,230)'
                                                  )
                                    ),
                        height = 600,
                       )
                  )
                  
data = [trace1,trace2]
fig  = go.Figure(data = data,layout = layout)
py.iplot(fig)