# -*- coding:utf-8 -*-
import json
from flask import Flask, request, Response

app = Flask(__name__)


# [POST] http://127.0.0.1:5000/chat
@app.route('/chat', methods=['POST'])
def generation():
    req_data = request.json
    result = req_data["requestContent"]

    responseContent = "responseContent"

    result = json.dumps(responseContent)
    return Response(result, mimetype='application/json')



if __name__ == '__main__':
    app.run(debug=False, threaded=True, host='0.0.0.0', port='5000')
