#!/usr/bin/python
#
# Author: Kevin Tooley
#
# License: GPL
#
# Subject: RESTful Scaffolding
#
# Date: 2/23/2019
#
######

import restful_api

# Create a menu for the application
menu = {}
menu['1']="Add Company" 
menu['2']="Update Volume"
menu['3']="Delete Company"
menu['4']="Find Company"
menu['5']="Find 50-Day Count"
menu['6']="Find Industry Tickers"
menu['7']="Aggregate Sector"
menu['9']="Exit"
while True:
    options=menu.keys()
    options.sort()
    for entry in options: 
        print entry, menu[entry]

    selection = raw_input("Please Select: ") 
    if selection =='1': 
        #print "Add"

        # Read the inputs
        company_name = raw_input("Enter the company name: ")
        ticker_symbol = raw_input("Enter the company ticker: ")
        volume = int(raw_input("Enter the Volume: "))

        #print company_name
        #print ticker_symbol
        #print sector_name
        
        result = restful_api.insert_document(
            {"Company" : company_name,
             "Ticker" : ticker_symbol,
             "Volume" : volume}
            )

        # clear items for additional use
        company_name = ""
        ticker_symbol = ""
        volume = None

        print str(result)
             
    elif selection == '2': 
        #print "Update"

        # Read the inputs
        ticker_symbol = raw_input("Enter the company ticker: ")
        volume = int(raw_input("Enter the new volume: "))

        result = restful_api.update_document(
            "Ticker",
            ticker_symbol,
            "Volume",
            volume)

        # clear items for additional use
        ticker_symbol = ""
        volume = None

        print str(result)
        
    elif selection == '3':
        #print "Delete"

        # Read the inputs
        ticker_symbol = raw_input("Enter the company ticker: ")
        
        result = restful_api.delete_document("Ticker", ticker_symbol)

        # clear item for additional use
        ticker_symbol = ""
        
        print "Item Deleted"
            
    elif selection == '4':
        #print "Find"

        # Read the inputs
        ticker_symbol = raw_input("Enter the company ticker: ")

        result = restful_api.find_document("Ticker", ticker_symbol)

        # clear item for additional use
        ticker_symbol = ""
        print str(result)

    elif selection == '5':
        #print "Find 50-Day average between ranges"

        # Read the inputs
        min_value = float(raw_input("Enter the minimum 50-Day Moving Avg value: "))
        max_value = float(raw_input("Enter the maximum 50-Day Moving Avg value: "))

        result = restful_api.find_50_day(min_value, max_value)


        # clear items for additional use
        min_value = None
        max_value = None
        
        print("The number of companies within the min and max is %s" % result)

    elif selection == '6':
        #print "Find ticker for industry"

        # Read the inputs
        industry_name = raw_input("Enter the industry name: ")

        result = restful_api.find_industry(industry_name)

        # clear items for additional use
        industry_name = ""

        print ""
        print "The following ticker symbols are associated with the industry:"

        for document in result:
            print(document["Ticker"])

        print ""

    elif selection == '7':
        #print "Aggregate on Sector field"

        # Read the inputs
        sector_name = raw_input("Enter a sector name: ")

        result = restful_api.aggregate_sector(sector_name)

        # clear items for additional use
        sector_name = ""

        print ""
        print "The following are Total OutStanding Shares, grouped by Industry:"

        for document in result:
            print(document)

        print ""
        
    elif selection == '9': 
        break
    else: 
        print "Unknown Option Selected!"
