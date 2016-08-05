# it will search taipei every restaurant placeID
# Example: placeID

import json
import time
from urllib.request import urlopen

def getNearBySearching(lat,lng,radius):
    the_url = "https://maps.googleapis.com/maps/api/place/"\
            +"radarsearch/json?location="+str(lat)+","+str(lng)\
            +"&radius="+str(radius)+"&types=food|restauran"\
            +"|meal_takeaway|meal_delivery|bakery|cafe&"\
            +"key=AIzaSyCdFvZIlyrwnINnppc19vgsZcdqmmoabDo"
    print(the_url) 
    
    response = urlopen( the_url ).read().decode('utf-8')
    responseJSON =  json.loads(response)
     
    while (responseJSON.get("status") != "OK" and \
          responseJSON.get("status") != "ZERO_RESULTS"):
        #maybe OVER_QUERY_LIMIT 
        time.sleep(60) #sleep 1 min
        response = urlopen( the_url ).read().decode('utf-8')
        responseJSON =  json.loads(response)
    
    place_set = set()
    for x in responseJSON.get("results"):
        place_set.add(x.get("place_id"))
   
    print("place_set = " + str( len(place_set) ))

    if len(place_set) >= 200:
        radius_meter = (radius/2)/1.41421 #Circle to rectangle
        radius_cod = radius_meter * 0.0000089937
        radius_meter = radius / 2 * 1.1 #for safe
        place_set_2 = set()
        place_set_2|= getNearBySearching(lat+radius_cod \
                ,lng+radius_cod,radius_meter) 
        place_set_2|= getNearBySearching(lat+radius_cod \
                ,lng-radius_cod,radius_meter) 
        place_set_2|= getNearBySearching(lat-radius_cod \
                ,lng+radius_cod,radius_meter) 
        place_set_2|= getNearBySearching(lat-radius_cod \
                ,lng-radius_cod,radius_meter) 

        print("place_set_2 = " + str( len(place_set_2) ))

        return place_set_2
    else:
        return place_set

north = 25.209887
south = 24.961148
east = 121.663415
west = 121.462099
lat = south
lng = west

northDisSouth = (north-south)/27.657
eastDisWest = (east-west)/20.252

all_place_set = set()
fout = open("exception.txt","wt")
while lat <= north:
    while lng <= east :
        try:
            all_place_set|= getNearBySearching(lat,lng,1000)
        except Exception as err:
            print(str(lat)+","+str(lng)+" "+err, file=fout)
        lng += (eastDisWest * 1.8) # it should radius*2 for safe*1.8
    lat += (northDisSouth *1.8)
    lng = west

fout.close()
print("all_place_set = " + str(len(all_place_set)))

fout = open("all_place_set.txt","wt")
fout.write(str(all_place_set))
fout.close()

#for i in getNearBySearching("25.023601","121.528552"):
#    print(i)

