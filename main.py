# import flask dependencies 
from flask import Flask, request, make_response, jsonify
import requests 
import json
from datetime import datetime

# initialize the flask app 
app = Flask(__name__) 

# api to make the post request
api = "https://orderstatusapi-dot-organization-project-311520.uc.r.appspot.com/api/getOrderStatus"

# downloaded postman collection 
f = open("OrderStatusAPI.json")
orderstatus_json = json.load(f)

def index(): 
	return 'Hello World!' 

# function for responses 
def results(): 
	# build a request object 
	req = request.get_json(force=True) 

	# fetch parameters from json 
	orderId = req.get('queryResult').get('parameters')['order_id']
	
	# making post request to get the shipment date
	r = requests.post(url = api, json = orderstatus_json, data = {"orderId" : str(orderId)}).json()

	# converting shipment date to human readable form: dddd, dd mmm yyyy
	shipmentDate = r['shipmentDate']
	shipmentDate = datetime.strptime(shipmentDate, "%Y-%m-%dT%H:%M:%S.%fZ")
	shipmentDate = shipmentDate.strftime("%A, %d %b %Y")

	# sending webhookresponse to the agent
	return {'fulfillmentText': 'Your order ' + orderId + ' will be shipped on ' + shipmentDate} 

# create a route for webhook 
@app.route('/webhook', methods=['GET', 'POST']) 

def webhook(): 
	# return response 
	return make_response(jsonify(results())) 

# run the app 
if __name__ == '__main__': 
	app.run()