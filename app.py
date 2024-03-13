from flask import Flask, jsonify
# from Scrape import Url
from AutoScout24 import AutoScout24
app = Flask(__name__)

# generate yield data
def generate():
    for i in range(1, 100000000):
        yield f'Number: {i}\n'



@app.route('/stream')
def stream():
    return generate()


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/scrape')
def scrape():
    url = AutoScout24('https://www.autoscout24.fr/lst/bmw/i3?atype=C&cy=F&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU',20,6,10)
    return jsonify(url.format_articles_data())
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)