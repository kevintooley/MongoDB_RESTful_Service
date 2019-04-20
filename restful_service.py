#!/usr/bin/python
#
# Author:  Kevin Tooley
#
# License: GPL
#
# Subject: RESTful Service
#
# Date:    2/10/2019
# Update:  2/23/2019 Code reuse
#
######

import json
import bson
import datetime
import pymongo
import pprint
from bson import json_util
import bottle
from bottle import route, run, request, abort, get, put
from pymongo import MongoClient

import restful_api

##connection = MongoClient('localhost', 27017)
##db = connection['market']
##collection = db['stocks']

# Set up URI paths for REST service
@route('/currentTime', method='GET')
def get_currentTime():
    dateString = datetime.datetime.now().strftime("%Y-%m-%d")
    timeString = datetime.datetime.now().strftime("%H:%M:%S")
    string = "{\"date\":" + dateString + ",\"time\":" + timeString + "}\n"
    return json.loads(json.dumps(string, indent=4, default=json_util.default))

@get('/hello')
def get_hello():
    arg1 = request.query.name
    string = "{ hello: \"" + arg1 + "\"}\n"
    return json.loads(json.dumps(string, indent=4, default=json_util.default))
  
@route('/strings', method='POST')
def post_strings():
    request.json.get
    first = request.json.get("string1")
    second = request.json.get("string2")
    string = "{ first: \"" + first + "\", second: \"" + second + "\" }\n"
    return json.loads(json.dumps(string, indent=4, default=json_util.default))

# This is the CREATE method of the basic GRUD
# This method requires a complete json input from the curl command  
@route('/create', method='POST')
def post_create():
    try:
        document = request.json
        post_result = restful_api.insert_document(document)
        return json.loads(json.dumps(document, indent=4, default=json_util.default))
    except Exception as e:
        print("Exception occurred: %s" % e)

# This is the READ method of the basic GRUD
# This method requires a ticker input from the curl command
@get('/read', method='GET')
def get_read():
    try:
        arg1 = request.query.ticker
        #query = { "Ticker" : arg1 }
        result = restful_api.find_document("Ticker", arg1)
        return json.loads(json.dumps(result, indent=4, default=json_util.default))
    except Exception as e:
        print("Exception occurred: %s" % e)

# This is the UPDATE method of the basic GRUD
# This method requires a ticker and volume input from the curl command        
@route('/update')
def put_update():
    try:
        arg1 = request.query.ticker
        arg2 = request.query.volume
        
        result = restful_service.update_document("Ticker", arg1, "Volume", arg2)
        
        return json.loads(json.dumps(result, indent=4, default=json_util.default))
      
    except Exception as e:
        print("Exception occurred: %s" % e)

# This is the DELETE method of the basic GRUD
# This method requires a ticker input from the curl command        
@route('/delete')
def delete():
    try:
        arg1 = request.query.ticker
        #query = { "Ticker" : arg1 }
        result = restful_api.delete_document("Ticker", arg1)
        return "Item successfully deleted\n"
    except Exception as e:
        print("Exception occurred: %s" % e)

# This method returns summary information for a list of ticker symbols
@get('/list', method='GET')
def get_list():
    try:
        arg1 = request.query.tickers
        ticker_list = arg1.split(',')

        result = restful_api.get_list(ticker_list)

        return json.dumps(result, indent=4, default=json_util.default)
    except Exception as e:
        print("Exception occurred: %s" % e)

# This method returns the top 5 stocks for a given industry
# The industry is input via the curl command
@get('/top', method='GET')
def get_top():
    try:
        arg1 = request.query.industry
        #print arg1

        result = restful_api.get_top(arg1)

        return json.dumps(result, indent=4, default=json_util.default)
    except Exception as e:
        print("Exception occurred: %s" % e)

if __name__ == '__main__':
    #app.run(debug=True)
    run(host='localhost', port=8080)
