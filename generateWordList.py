import requests,json,string
from urllib.parse import urlparse

#this api has many public api url
APIdatabaseURL = "http://apis.io/api/apis?limit=1000"

words = []
while True:
    response = requests.get(APIdatabaseURL)
    jsonResponse = json.loads(response.content)

    #if there's no data then finish
    if(len(jsonResponse['data'])==0):
        break
    
    #get look at data
    for data in jsonResponse['data']:
        if('baseURL' in data):
            #get the url path component
            path = urlparse(data['baseURL']).path
            #slipt it
            paths = path.split("/")
            #add all the path to the list
            for i in range(1,len(paths)):
                # print(paths[i])
                if(paths[i] not in words):
                    words.append(paths[i])

    #go to next page
    APIdatabaseURL = jsonResponse[' paging']['next']

#remove the word that is too long in the result list
for word in words:
    if len(word)>20:
        words.remove(word)

#write it to the file
with open('wordList', 'w') as f:
    for item in words:
        f.write("%s\n" % item)