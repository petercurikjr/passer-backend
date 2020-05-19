#view.py
#this file handles POST requests from iOS Passer app.
#after recieving a sixdigit code with uuid of the user's device, Flask builds a dict out of it and writes it to in memory cache in json format for a limited time (2 min)

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from datetime import datetime
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__) #create a flask app
cors = CORS(app) #enables javascript to GET from this server. for more, see enable-cors.org/server_flask.html

cache = SimpleCache()

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
    
    dic[sixdigitCode] = [passwordItems, bankCardItems, otherItems, dateStr]
    cache.set(sixdigitCode,dic,timeout=2*60) #identifier, value, timeout
    return 'ok'

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
    return 'ok'

@app.route('/verifySixDigitfromwebsite', methods=['POST'])
def processDataFromWeb():
    incomingData = request.get_json()
    sixdigitTyped = incomingData['sixdigitTyped']
    data = cache.get(sixdigitTyped)
    if data != None:
        return data
    return 'Wrong code'
    
@app.route('/verifyQRfromwebsite')
def yieldQRresult():
    def checkSessionID():
        yield "lol"
    return Response(checkSessionID(), mimetype = 'text/plain')

if __name__ == '__main__':
    app.run(threaded=False, processes=1)
