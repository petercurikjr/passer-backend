#view.py
#this file handles POST requests from iOS Passer app.
#after recieving a sixdigit code with uuid of the user's device, Flask builds a dict out of it and writes it to in memory cache in json format for a limited time (2 min)

from flask import Flask, request, jsonify
from flask_cors import CORS
#from flask_caching import Cache
from datetime import datetime
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__) #create a flask app
cors = CORS(app) #enables my website to GET from this server. for more, see enable-cors.org/server_flask.html

#cache = Cache(app, config = {'CACHE_TYPE': 'simple'})  #COFIGURATE cache and create Cache instance
cache = SimpleCache()

@app.route('/', methods=['POST']) #requests to allow
#@cache.cached(timeout=0.001)
def processDataFromApp():
    #dic = {}
    incomingData = request.get_json()
    deviceID = incomingData['deviceID']
    sixdigitCode = incomingData['sixdigitCode']
    dateStr = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    passwordItems = incomingData.get('passwordItems')
    bankCardItems = incomingData.get('bankCardItems')
    otherItems = incomingData.get('otherItems')
    #cacheVal = [sixdigitCode, passwordItems, bankCardItems, otherItems]
    #print(cache.set('key', 'cacheVal', timeout=50))
    #dic[deviceID] = [sixdigitCode, dateStr, passwordItems, bankCardItems, otherItems]
    
    arr = [sixdigitCode, dateStr, passwordItems, bankCardItems, otherItems]
    cache.set(deviceID,arr,timeout=5)
    #verifyTimeStamps(datetime.now());
    #return jsonify(dic)
    return cache.get(deviceID)

@app.route('/verify_from_website', methods=['POST'])
def processDataFromWeb():
    verifyTimeStamps(datetime.now());
    incomingData = request.get_json()
    sixdigitTyped = incomingData['sixdigitTyped']
    key = verify(sixdigitTyped)
    if key != None:
        return jsonify(dic[key])
    return 'Wrong code'

def verify(sixdigitTyped):
    for deviceID in dic.keys():
        if dic[deviceID][0] == sixdigitTyped:
            return deviceID
    return None

def verifyTimeStamps(currentDate):
    for item in list(dic.keys()):
        dateFromCache = datetime.strptime(dic[item][1], '%d/%m/%Y %H:%M:%S')
        delta = currentDate - dateFromCache
        minutesDelta = delta.seconds / 60
        if minutesDelta > 1.99:
            del dic[item]


if __name__ == '__main__':
    app.run(threaded=False, processes=1)
