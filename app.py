#this server script handles POST requests from iOS Passer app and website passer.netlify.app.
#all data is saved to SimpleCache valid for 2 minutes. no filesystem interaction is used for security and performance reasons.

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__) #create a flask app
cors = CORS(app) #enables javascript to interact with this server. for more, see enable-cors.org/server_flask.html

cache = SimpleCache()

#Passer - six digit code
@app.route('/sixdigit', methods=['POST']) #requests to allow
def processSixDigitFromApp():
    dic = {}
    incomingData = request.get_json()
    
    deviceID = incomingData['deviceID']
    sixdigitCode = incomingData['sixdigitCode']
    dateStr = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    passwordItems = incomingData.get('passwordItems')
    bankCardItems = incomingData.get('bankCardItems')
    otherItems = incomingData.get('otherItems')
    
    if cache.has(sixdigitCode):
        return 409 #conflict - this six digit code is already in the cache
        
    if cache.has(deviceID): #check if the same user has already some data in the cache
        userOldVerifData = cache.get(deviceID)
        cache.delete(deviceID)
        cache.delete(userOldVerifData)
        
    dic[sixdigitCode] = [passwordItems, bankCardItems, otherItems, dateStr, deviceID]
    cache.set(deviceID,sixdigitCode,timeout=2*60) #map deviceID to sixdigitCode
    cache.set(sixdigitCode,dic,timeout=2*60) #map sixdigitCode to passer items data
    return 'server: ok', 201

#Passer - QR code
@app.route('/qr', methods=['POST'])
def processQRFromApp():
    dic = {}
    incomingData = request.get_json()
    
    sessionID = incomingData['sessionID']
    dateStr = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    passwordItems = incomingData.get('passwordItems')
    bankCardItems = incomingData.get('bankCardItems')
    otherItems = incomingData.get('otherItems')
    
    dic[sessionID] = [passwordItems, bankCardItems, otherItems, dateStr]
    cache.set(sessionID,dic,timeout=2*60)
    return 'server: ok', 201

#website - six digit code
@app.route('/verifySixDigitfromwebsite', methods=['POST'])
def processDataFromWeb():
    incomingData = request.get_json()
    sixdigitTyped = incomingData['sixdigitTyped']
    data = cache.get(sixdigitTyped)
    if data != None:
        cache.delete(sixdigitTyped)
        cache.delete(data[-1]) #last element of data list (deviceID)
        return data
    return 'Wrong code'
    
#website - QR code
@app.route('/verifyQRfromwebsite', methods=['POST'])
def processSessionIDFromWeb():
    incomingData = request.get_json()
    sessionID = incomingData['sessionID']
    data = cache.get(sessionID)
    if data != None:
        cache.delete(sessionID)
        return data
    return 'Nothing'

if __name__ == '__main__':
    app.run(threaded=False, processes=1)
