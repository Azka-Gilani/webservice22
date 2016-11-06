#!/usr/bin/env python

import urllib
import json
import os
import re

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    city_names=processlocation(req)
    sector_names=processSector(req)
    property_type=processPropertyType(req)
    unit_property=processUnit(req)
    area_property=processArea(req)
    NoOfDays=processDate(req)
    DateUnit=processDateUnit(req)
    school=processSchool(req)
    malls=processMalls(req)
    transport=processTransport(req)
    security=processSecurity(req)
    airport=processAirport(req)
    fuel=processFuel(req)
    minimum_value=processMinimum(req)
    maximum_value=processMaximum(req)
    latest=processLatestProperties(req)
    if minimum_value > maximum_value:
        minimum_value,maximum_value=maximum_value,minimum_value
    else:
        minimum_value,maximum_value=minimum_value,maximum_value    
    baseurl = "https://fazendanatureza.com/bot/botarz.php?city_name="+city_names+"&sector_name="+sector_names+"&minPrice="+minimum_value+"&maxPrice="+maximum_value+"&type="+property_type+"&LatestProperties="+latest+"&UnitArea="+area_property+"&Unit="+unit_property+"&context_type="+NoOfDays+"&context_num="+DateUnit+"&school="+school+"&airport="+airport+"&transport="+transport+"&security="+security+"&shopping_mall="+malls+"&fuel="+fuel
    result = urllib.urlopen(baseurl).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

def processlocation(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("city")
    return city

def processSector(req):
    result = req.get("result")
    parameters = result.get("parameters")
    sector = parameters.get("Location")
    return sector

def processMinimum(req):
    result = req.get("result")
    parameters = result.get("parameters")
    minimum = parameters.get("number")
    return minimum

def processMaximum(req):
    result = req.get("result")
    parameters = result.get("parameters")
    maximum = parameters.get("number1")
    return maximum


def processPropertyType(req):
    result = req.get("result")
    parameters = result.get("parameters")
    propertyType = parameters.get("PropertyType")
    return propertyType

def processLatestProperties(req):
    result = req.get("result")
    parameters = result.get("parameters")
    latest = parameters.get("LatestProperties")
    return latest

def processUnit(req):
    result = req.get("result")
    parameters = result.get("parameters")
    unit = parameters.get("Unit")
    return unit

def processArea(req):
    result = req.get("result")
    parameters = result.get("parameters")
    area = parameters.get("AreaNumber")
    return area

def processDate(req):
    result = req.get("result")
    parameters = result.get("parameters")
    days = parameters.get("NoOfDays")
    return days

def processDateUnit(req):
    result = req.get("result")
    parameters = result.get("parameters")
    dayUnit = parameters.get("DayUnit")
    return dayUnit

def processSchool(req):
    result = req.get("result")
    parameters = result.get("parameters")
    school = parameters.get("school")
    return school

def processMalls(req):
    result = req.get("result")
    parameters = result.get("parameters")
    malls = parameters.get("malls")
    return malls

def processTransport(req):
    result = req.get("result")
    parameters = result.get("parameters")
    transport = parameters.get("transport")
    return transport

def processSecurity(req):
    result = req.get("result")
    parameters = result.get("parameters")
    security = parameters.get("security")
    return security

def processAirport(req):
    result = req.get("result")
    parameters = result.get("parameters")
    airport = parameters.get("airport")
    return airport

def processFuel(req):
    result = req.get("result")
    parameters = result.get("parameters")
    fuel = parameters.get("fuelstation")
    return fuel

def makeWebhookResult(data):
    row1_id=data[0]['p_id']
    row1_title = data[0]['title']
    row1_location=data[0]['address']
    row1_price = data[0]['price']
    row2_id=data[1]['p_id']
    row2_title = data[1]['title']
    row2_location=data[1]['address']
    row2_price = data[1]['price']
    
    # print(json.dumps(item, indent=4))
    speech = "This is the response from server."+ row1_title +"Location-1"+row1_location+"...."+row2_title +"Location-2"+row2_location
    print("Response:")
    print(speech)
    if "unable" in row1_title:
        message={
         "text":row1_title
    }
    else:
        message= {
         "attachment": {
           "type": "template",
             "payload": {
               "template_type": "generic",
               "elements": [{
               "title": row1_title,
               "subtitle": row1_location,
               "item_url": "http://www.aarz.pk/property-detail?id="+row1_id,               
               "image_url": "http://www.aarz.pk/assets/images/properties/"+row1_id+"/"+row1_id+".actual.1.jpg" ,
                "buttons": [{
                "type": "web_url",
                "url": "www.aarz.pk",
                "title": "Open Web URL"
            }, 
                   ],
          }, 
                   {
                "title": row2_title,
                "subtitle": row2_location,
                "item_url":  "http://www.aarz.pk/property-detail?id="+row2_id,               
                "image_url": "http://www.aarz.pk/assets/images/properties/"+row2_id+"/"+row2_id+".actual.1.jpg",
                "buttons": [{
                "type": "web_url",
                "url": "www.aarz.pk",
                "title": "Open Web URL"
            },
                   ]
          }]
        }
      }
    }

    return {
        "speech": speech,
        "displayText": speech
        #"originalRequest":{"source":"facebook","data": {"facebook": message}}
        #"data": {"facebook": message},
        # "contextOut": [],
        #"source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
