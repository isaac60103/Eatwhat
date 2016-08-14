# give placeID list (.txt) it will return every place information
# input:    all_taipeiPlaceID_set.txt
# output:   all_taipeiPlaceInfo_set.txt (place information)
#           exception.txt (Error messsage)
# Example:  ["name","rating","lat","lng"]

import json
from urllib.request import urlopen

def getRating(placeID):
    url = "https://maps.googleapis.com/maps/api/place/"\
          +"details/json?placeid="+placeID+"&key="\
          +"AIzaSyBBvjvN65VDFxYVMP5_Y_5GiU-USs3sMrQ"
          
    print(url)

    response = urlopen(url).read().decode('utf-8')
    responseJSON =  json.loads(response)
    responseResult = responseJSON.get("result")
    return [responseResult.get("name"),\
            responseResult.get("rating"),\
            responseResult.get("geometry").get("location").get("lat"),\
            responseResult.get("geometry").get("location").get("lng")]
            #responseResult.get("formatted_address"),\
            #responseResult.get("formatted_phone_number"),\
            #responseResult.get("permanently_closed"),\
            #responseResult.get("url"),\
            #responseResult.get("types") ]

fout = open("all_taipeiPlaceInfo_set.txt","wt")
fErrOut = open("exception.txt","wt")
fin = open("all_taipeiPlaceID_set.txt","rt")

placeIDList = set(fin.read().split( "\'"))
exception_num = 0

for i in placeIDList:
    #so I need to cut some part
    # or i[2:29] but they are not good
    # maybe split shoud add something like '
    print(i)
    try:
        print(getRating(i),file=fout)
    except Exception as err:
        print(i+"\nError: ",file=fErrOut)
        print(err,file=fErrOut)
        exception_num+=1
fin.close()
fout.close()
fErrOut.close()
if exception_num != 0:
    print("ERROR!!! Please see exception.txt!!!")
