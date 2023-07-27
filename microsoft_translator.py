import requests
import os
import config

auth_key = None
init_done = False


def init():
    global init_done
    global auth_key

    path_to_microsoft_apikey = "microsoft_apikey.txt"

    if os.path.isfile(path_to_microsoft_apikey):
        with open(path_to_microsoft_apikey, "r") as apikey:
            auth_key = apikey.readlines().pop()

    if len(auth_key) == 0:
        auth_key = input("Enter your Microsoft api key: ")
        with open(path_to_microsoft_apikey, "w") as apikey:
            apikey.write(auth_key)
            apikey.close()

    init_done = True


def translate_text(text_to_translate):
    if not init_done:
        init()

    headers = {
        "Ocp-Apim-Subscription-Key": auth_key,
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Region": config.region
    }

    body = [
        {
            "text": text_to_translate
        }
    ]

    response = requests.post(f"{config.base_url}{config.endpoint}?api-version=3.0&to={config.targetLang}", headers=headers, json=body)

    if response.status_code == 200:
        translated_text = response.json()[0]['translations'][0]['text']
        return translated_text
    else:
        print("Microsoft translation problem. response.status_code={}".format(response.status_code))
        return None
