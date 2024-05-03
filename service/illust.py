import json
import requests
from flask import abort


class IllustService:
    def __init__(self):
        with open("key/dalle-api-key.txt", "r") as f:
            key = f.readline()

        self.url = "https://api.openai.com/v1/images/generations"
        self.headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {key}'
        }
        self.body = {
            "model": "dall-e-3",
            "n": 1,
            # "prompt": prompt
            "size": "1024x1024"
        }
        self.mood_stage = {
            5:"Bright",
            4:"Cheerful",
            3:"Neutral",
            2:"Sad",
            1:"Dark and Gloomy"
        }

    def get_image(self, params):
        situation = params['situation']
        mood = self.mood_stage[params['mood_stage']]

        # prompt
        prompt = f"""Illustrate only one tarot card in the style of Art Nouveau, inspired by early 20th century artwork, featuring ({situation}). 
        The total mood is ({mood}).The card should embody the essence of elegance and intricate designs associated with this style, with the subject depicted in an elegant pose, wearing flowing garments typical of the period. 
        The background should be adorned with floral motifs and soft, creating a serene and artistic atmosphere. 
        The card's frame should have stylized borders that enhance the aesthetic of timelessness and sophistication."""

        # request params
        body = self.body.copy()
        body["prompt"] = prompt

        # request & response
        response = requests.post(url=self.url, headers=self.headers, data=json.dumps(body))
        if response.status_code != 200:
            abort(response.status_code, response.json()['error']['message'])

        image_url = response.json()['data'][0]['url']
        return image_url


# service = IllustService()
# params = {"situation": "I am a mother but I lost my son",
#           "mood_stage": 1,}
# response = service.get_image(params)