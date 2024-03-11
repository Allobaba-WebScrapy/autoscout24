from flask import Flask, jsonify
from Scrape import Url
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/scrape')
def scrape():
    url = Url('https://www.autoscout24.fr/lst/volkswagen/amarok?atype=C&cy=F&desc=0&page=1&powertype=kw&search_id=2fe1dqq1j4q&sort=standard&source=listpage_pagination&ustate=N%2CU')
    return jsonify(url.format_articles_data())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)