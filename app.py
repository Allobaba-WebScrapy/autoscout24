from flask import Flask, jsonify
from Scrape import Url
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/scrape')
def scrape():
    url = Url('https://www.autoscout24.fr/lst/bmw/i3?atype=C&cy=F&damaged_listing=exclude&desc=0&powertype=kw&search_id=majrm8ivsv&sort=standard&source=listpage_pagination&ustate=N%2CU',40,1,30)
    return jsonify(url.format_articles_data())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)