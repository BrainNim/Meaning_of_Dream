# -*- coding:utf-8 -*-
import json
import time

from flask import Flask, request, Response

from service.chat import ChatService
from service.illust import IllustrateService

app = Flask(__name__)
chat_service = ChatService()

# [POST] http://127.0.0.1:5000/chat
@app.route('/chat', methods=['POST'])
def chat():
    req_data = request.json
    question = req_data["requestContent"]
    response = chat_service.interpret_dream(question)
    # time.sleep(2)
    # response = " <Response>\n    <Title>심리적 불안</Title>\n    <Interpret>꿈에서 결혼반지를 잃어버리는 것은 현재의 결혼생활에 대한 심리적 불안이나 결혼 생활의 문제를 시사합니다. </Interpret>\n    <Score>3</Score>\n    <Summary>You lost your wedding ring in your dream.</Summary>\n</Response>"

    result = json.dumps(response)
    return Response(result, mimetype='application/json')

@app.route('/illustrate', methods=['POST'])
def illustrate():
    params = request.json
    result = IllustrateService().get_image(params)
    # time.sleep(10)
    # result = "https://mblogthumb-phinf.pstatic.net/MjAyMDA2MDFfNzQg/MDAxNTkwOTkzODU4MTg1.MbMtqBLDTWrZabpkQs3UQtXwtyTBL2PD3Hf9ndaP72sg.5YUAeus3aYY3GjhF6vIQimSAXulR1UalevOWPaF4tVcg.PNG.leekywood/0001.png?type=w420"

    return Response(result, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port='5000')
