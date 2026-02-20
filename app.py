from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from AutoScout24 import AutoScout24
import json
import time
import os

app = Flask(__name__)
CORS(app)

# #region agent log
_DEBUG_LOG = '/home/znajdaou/goinfre/repos/autoscout24/.cursor/debug-ed8a46.log'
def _dbg(loc, msg, data, hid, run_id='run1'):
    os.makedirs(os.path.dirname(_DEBUG_LOG), exist_ok=True)
    with open(_DEBUG_LOG, 'a') as f:
        f.write(json.dumps({"sessionId": "ed8a46", "location": loc, "message": msg, "data": data, "timestamp": int(time.time() * 1000), "hypothesisId": hid, "runId": run_id}) + '\n')
# #endregion

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/ilorez')
def helloFromIlorez():
    return 'ilorez was here!'

@app.route('/scrape', methods=['POST'])
def scrape():
    # Parse JSON data from the request (silent=True so invalid/empty body gives None, not 400 HTML)
    data = request.get_json(silent=True)
    # #region agent log
    _dbg('app.py:scrape', 'after get_json', {'data_is_none': data is None, 'content_type': request.content_type}, 'A')
    # #endregion

    if data is None:
        return jsonify({'error': 'Invalid or missing JSON body. Send JSON with at least "url".'}), 400

    url = data.get('url')
    if not url or not str(url).strip():
        return jsonify({'error': 'Missing required field "url".'}), 400

    # Optional parameters with defaults
    startPage = data.get('startPage', 1)
    offersNumber = data.get('offersNumber', 19)
    waitingTime = data.get('waitingTime', 30)
    businessType = data.get('businessType', 'b2b')

    # #region agent log
    _dbg('app.py:scrape', 'params extracted', {'url': url, 'startPage': startPage, 'offersNumber': offersNumber, 'waitingTime': waitingTime, 'businessType': businessType}, 'B')
    # #endregion

    return Response(
        AutoScout24(url, offersNumber, startPage, waitingTime, businessType).format_articles_data(),
        content_type='application/json'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
