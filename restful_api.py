#!/usr/bin/python
#
# Author:  Kevin Tooley
#
# License: GPL
#
# Subject: RESTful API
# 
# Date:    2/2/2019
# Update:  2/23/2019 Code reuse
#
######

import json
import bson
import datetime
import pymongo
import pprint
from bson import json_util
from pymongo import MongoClient

# This file is the base for all connections to the database
# Connection parameters are setup below
connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']

# This is the CREATE method of the basic CRUD
def insert_document(document):
    try:
        result = collection.insert_one(document)
        return result
    except Exception as e:
        print("Exception occurred: %s" % e)

# This is the READ method of the basic CRUD
# Any key,value pair can be used, but this app is setup to read ticker symbols by default
def find_document(key, value):
    try:
        result = collection.find_one({key : value})

        if not result:
            print('No document with %s: %s' % (key, value))
        else: 
            #print "\n"
            #print str(result)
            #print "\n"
            
            file = open("read_result.json", "w")
            file.write('[')
            file.write(str(result))
            file.write(',')
            file.write(']')
        
            print "JSON file 'read_result.json' has been saved"
            
        return result
    
    except Exception as e:
        print("Exception occurred: %s" % e)

# This is the UPDATE method of the basic CRUD
# Any key,value pair can be used, but this app is setup to read ticker symbols by default
# key/value are the search params; update_key/update_value are the fields to change
def update_document(key, value, update_key, update_value):
    try:
        collection.update_one({key : value}, 
                              { "$set" : 
                               {update_key : update_value}
                              } 
                             )

        result = collection.find_one({key : value})
        
        #print "\n"
        #print str(result)
        #print "\n"

        file = open("update_result.json", "w")
        file.write("[")
        file.write(str(result))
        file.write(",")
        file.write("]")

        print "JSON file 'update_result.json' has been saved"
        return result
    
    except Exception as e:
        print("Exception occurred: %s" % e)

# This is the DELETE method of the basic CRUD
# Any key,value pair can be used, but this app is setup to read ticker symbols by default        
def delete_document(key, value):
    try:
        collection.delete_one({key : value})
        
        result = collection.find_one({key : value})
        
        #print "\n"
        #print str(result)
        #print "\n"
        
        file = open("delete_result.json", "w")
        file.write("[")
        file.write(str(result))
        file.write(",")
        file.write("]")
        
        print "JSON file 'delete_result.json' has been saved"
        return result
        
    except Exception as e:
        print("Exception occurred: %s" % e)

# This method returns documents with 50-Day moving average within the min/max
# Values supplied by the operator
def find_50_day(min_val, max_val):
    try:
##        pipeline = [
##            {"$match" : {"50-Day Simple Moving Average" : { "$gte" : min_val , "$lte" : max_val }}},
##            {"$group" : {"_id" : "null", "count" : {"$sum" : 1}}}
##            ]
##        
##        result = list(collection.aggregate(pipeline))
##
##        num_items = result[0]["count"]
##
##        return num_items

        result = collection.find(
            {"50-Day Simple Moving Average" :
             { "$gte" : min_val, "$lte" : max_val}
             }).count()#.min({"50-Day Simple Moving Average" : min_val }).max({"50-Day Simple Moving Average" : max_val }).count()

        return result

    except Exception as e:
        print("Exception occurred: %s" % e)

# This method returns the ticker symbols for documents in the given industry
def find_industry(industry):
    try:
        result = list(collection.find({"Industry" : industry }, {"Ticker" : 1}))

        return result
    except Exception as e:
        print("Exception occurred: %s" % e)

# This is an aggregate method to count the number of outstanding shares for each industry within the sector
def aggregate_sector(sector_name):
    try:
        #db.stocks.aggregate([{ "$match" : { "Sector" : "Healthcare" }}, {"$group" : { "_id" : { "Industry" : "$Industry" }, "total outstanding shares" : { "$sum" : "$Shares Outstanding" }}}])
        pipeline = [
            { "$match" : { "Sector" : sector_name }},
            { "$group" : { "_id" : { "Industry" : "$Industry" }, "total outstanding shares" : { "$sum" : "$Shares Outstanding" }}}
            ]

        result = list(collection.aggregate(pipeline))

        return result

    except Exception as e:
        print("Exception occurred: %s" % e)

# The operator provides a list of ticker symbols, and this method returns summary of each
def get_list(ticker_list):
    try:
        result = list(collection.find({"Ticker" : { "$in" : ticker_list }}, {"Ticker" : 1, "Company" : 1, "Price" : 1, "52-Week Low" : 1, "52-Week High" : 1, "P/E" :1, "Volume" : 1}))
        
        return result

    except Exception as e:
        print("Exception occurred: %s" % e)

# The operator supplies and industry name, and this method returns the top 5 performers for that industry
def get_top(industry_name):
    try:
        #.find({"Industry" : "Medical Laboratories & Research"}, {"Ticker" : 1, "Change from Open" : 1}).sort({"Change from Open" : -1}).limit(5)
        pipeline = [
            {"$match" : { "Industry" : industry_name }},
            { "$sort" : { "Change from Open" : 1 }},
            { "$group" : { "_id" : { "Ticker" : "$Ticker", "Change from Open" : "$Change from Open" }}},
            {"$limit" : 5}
            ]
        #result = list(collection..find({"Industry" : "Medical Laboratories & Research"}, {"Ticker" : 1, "Change from Open" : 1}).sort({"Change from Open" : -1}).limit(5))
        result = list(collection.aggregate(pipeline))
                      
        return result
    except Exception as e:
        print("Exception occurred: %s" % e)
