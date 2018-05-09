from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# counter to rate limit every N calls
limit_counter = 0


@app.route('/', methods=["GET"])
def record_ip():
    r = request

    app.logger.error("""ip: {}, 
url: {}, 
headers:{}, 
data:{}""".format(r.environ['REMOTE_ADDR'], r.url, r.headers, r.data))

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
    handler = logging.FileHandler('debug.log')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.run()
