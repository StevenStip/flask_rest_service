from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logger = logging.getLogger('record-ip-flask')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('debug.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

# counter to rate limit every N calls
limit_counter = 0


@app.route('/', methods=["GET"])
def record_ip():
    r = request

    global logger
    logger.info("""ip: {}, 
url: {}, 
headers:{}, 
data:{}
+++++++++++++++++++++++++++++""".format(r.environ['REMOTE_ADDR'], r.url, r.headers, r.data))

    return jsonify({'ip': request.environ['REMOTE_ADDR']}), 200


@app.route('/ratelimit', methods=["GET"])
def rate_limited_record_ip():
    global limit_counter
    limit_counter += 1
    # check for rate limit
    if limit_counter == 3:
        limit_counter = 0
        return '429 error', 429

    return record_ip()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
