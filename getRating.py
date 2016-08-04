import json
from urllib.request import urlopen

def getRating(placeID):
    response = urlopen("https://maps.googleapis.com/maps/api/place/"\
            +"details/json?placeid="+placeID+"&key="\
            +"AIzaSyBBvjvN65VDFxYVMP5_Y_5GiU-USs3sMrQ")\
            .read().decode('utf-8')
    responseJSON =  json.loads(response)
    return [responseJSON.get("result").get("name"),\
            responseJSON.get("result").get("rating")]

def getPlaceIDlist(lat,lng):
    response = urlopen("https://maps.googleapis.com/maps/api/place/"\
            +"radarsearch/json?location="+lat+","+lng\
            +"&radius=50&types=food&"\
            +"key=AIzaSyBBvjvN65VDFxYVMP5_Y_5GiU-USs3sMrQ")\
            .read().decode('utf-8')
    responseJSON =  json.loads(response)
    
    placeID_set = set()
    for x in responseJSON.get("results"):
        placeID_set.add(x.get("place_id"))
    
    return placeID_set

for i in getPlaceIDlist("25.0444189","121.523382"):
    print(getRating(i))
