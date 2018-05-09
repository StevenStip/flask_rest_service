from flask import Flask, request, jsonify
import logging

app = Flask(__name__)


@app.route('/',  methods=["GET"])
def record_ip():
    logger.info("ip: {}".format(request.environ['REMOTE_ADDR']))

    return jsonify({'ip': request.environ['REMOTE_ADDR']}), 200



if __name__ == '__main__':
    logger = logging.getLogger('record-ip-flask')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('debug.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    app.run()
