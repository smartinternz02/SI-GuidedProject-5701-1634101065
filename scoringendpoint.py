import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "ALUYp8thDVqnl1eQflTpQUv3lua7T2TTriUcszVh3m4k"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields": [["year", "month","date"]], "values": [[1999,12,23]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/94703e4c-9b51-486e-a636-1bdaa6ed93da/predictions?version=2021-12-11', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
pred= response_scoring.json()
print(pred)
output= pred['predictions'][0]['values'][0][0]
print(output)