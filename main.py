# -*- coding:utf-8 -*-
import json
from flask import Flask, request, Response

from service.chat import ChatService

app = Flask(__name__)
chat_service = ChatService()

# [POST] http://127.0.0.1:5000/chat
@app.route('/chat', methods=['POST'])
def generation():
    req_data = request.json
    question = req_data["requestContent"]
    response = chat_service.interpret_dream(question)

    result = json.dumps(response)
    return Response(result, mimetype='application/json')



if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port='5000')
