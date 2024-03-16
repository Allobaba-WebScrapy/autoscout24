from flask import Flask, Response
import time

app = Flask(__name__)

def generate_json_data():
    for i in range(5):
        if i == 3:
            break
        time.sleep(1)  # Simulate some processing time
        yield '{"counter": ' + str(i+1) + '}'

@app.route('/stream_json_data')
def stream_json_data():
    return Response(generate_json_data(), content_type='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
