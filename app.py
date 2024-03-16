from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from AutoScout24 import AutoScout24

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/scrape', methods=['POST'])
def scrape():
    # Parse JSON data from the request
    data = request.get_json()
    
    # Extract necessary parameters
    url = data.get('url')
    startPage = data.get('startPage')
    offersNumber = data.get('offersNumber')
    waitingTime = data.get('waitingTime')

    # Call your scraping function with the provided parameters
    autoscout = AutoScout24(url,offersNumber, startPage, waitingTime)
    return Response(autoscout.format_articles_data(), content_type='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
