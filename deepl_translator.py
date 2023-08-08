import config
import os
import deepl

translator = None
init_done = False


def init():
    global init_done
    global translator

    path_to_deepl_apikey = "deepl_apikey.txt"
    auth_key = ''

    if os.path.isfile(path_to_deepl_apikey):
        with open(path_to_deepl_apikey, "r") as apikey_file:
            apikeys = apikey_file.readlines()
            for apikey in apikeys:
                apikey = apikey.strip()
                if apikey.startswith("#") or len(apikey) == 0:
                    continue
                auth_key = apikey

    if len(auth_key) == 0:
        auth_key = input("Enter your deepL api key: ")
        with open(path_to_deepl_apikey, "a") as apikey_file:
            apikey_file.write('\n' + auth_key)
            apikey_file.close()

    # init deepl translator
    translator = deepl.Translator(auth_key)
    init_done = True


def translate_text(text_to_translate):
    if not init_done:
        init()

    return translator.translate_text(
        text_to_translate,
        target_lang=config.targetLang,
        formality=config.formality,
        tag_handling=config.tag_handling,
        split_sentences='nonewlines'
    ).text
