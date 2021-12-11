import numpy as np
import pandas as pd
from flask import Flask,request,jsonify,render_template
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "ALUYp8thDVqnl1eQflTpQUv3lua7T2TTriUcszVh3m4k"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)
#model = pickle.load(open('weather_prediction.pickle','rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == "POST":
        ds = request.form["date"]
        a = {"ds":[ds]}
        ds=pd.DataFrame(a)
        ds['year'] = pd.DatetimeIndex(ds['ds']).year
        ds['month'] = pd.DatetimeIndex(ds['ds']).month
        ds['day'] = pd.DatetimeIndex(ds['ds']).day
        #print(ds)
        year= ds['year']
        #print(year)
        y=year.values.tolist()
        #print(y[0])
        month= ds['month']
        #print(month)
        m=month.values.tolist()
        day= ds['day']
        d=day.values.tolist()
        #print(m[0])
        payload_scoring = {"input_data": [{"fields": [["year", "month","date"]], "values": [[y[0],m[0],d[0]]]}]}
        #prediction = model.predict(ds)
        #output = round(prediction.iloc[0,18],2)
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/94703e4c-9b51-486e-a636-1bdaa6ed93da/predictions?version=2021-12-11', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        pred= response_scoring.json()
        print(pred)
        output= pred['predictions'][0]['values'][0][0]

        print(output)
        return render_template('home.html',output="Temperature on selected date is. {} degree celsius".format(output))
        #return "<h1>Temperature on selected date is. {} degree celsius</h1>".format(output)
    return render_template("home.html")
        


if __name__ == "__main__":
    app.run(port=5000,debug=False)