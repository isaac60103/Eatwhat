# give a Coordinates it will return near radius = 500m restauran
# because Google API restrict  The maximum number of results 
# that can be returned is 60.
# Example: [ ("name"),("rating"),("price_level")]

import json
import time
from urllib.request import urlopen

def getNearBySearching(lat,lng,next_page_token):
    the_url = "https://maps.googleapis.com/maps/api/place/"\
            +"nearbysearch/json?location="+lat+","+lng\
            +"&radius=500&types=food|restauran|meal_takeaway"\
            +"|meal_delivery|bakery|cafe&"\
            +"key=AIzaSyBBvjvN65VDFxYVMP5_Y_5GiU-USs3sMrQ"
    if next_page_token != None :
        the_url = the_url + "&pagetoken=" + next_page_token
   
    response = urlopen( the_url ).read().decode('utf-8')
    responseJSON =  json.loads(response)

    while responseJSON.get("status") == "INVALID_REQUEST":
        time.sleep(3) # wait for next_page_token be vailed
        response = urlopen( the_url ).read().decode('utf-8')
        responseJSON =  json.loads(response)
     
    place_list = []
    for x in responseJSON.get("results"):
        place_list.append([x.get("name"),x.get("rating"),\
                          x.get("price_level")])
  
    if responseJSON.get("next_page_token") != None :
        place_list += getNearBySearching(lat,lng,\
                responseJSON.get("next_page_token"))

    
    return place_list

for i in getNearBySearching("25.023601","121.528552",None):
    print(i)

