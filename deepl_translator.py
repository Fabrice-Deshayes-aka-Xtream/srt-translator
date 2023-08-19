import config
import os
import deepl

translator = None
init_done = False
path_to_deepl_apikey = "deepl_apikey.txt"


def get_character_usage_info(apikey=None):
    if apikey is None:
        return translator.get_usage().character
    else:
        t = deepl.Translator(apikey)
        return t.get_usage().character


def get_api_key():
    auth_key = None
    max_remain_chars = 0

    if os.path.isfile(path_to_deepl_apikey):
        with open(path_to_deepl_apikey, "r") as apikey_file:
            apikeys = apikey_file.readlines()
            for apikey in apikeys:
                apikey = apikey.strip()
                if apikey.startswith("#") or len(apikey) == 0:
                    continue

                usage = get_character_usage_info(apikey)
                remain_chars = usage.limit - usage.count
                print("apikey {} is allowed to translate {} chars".format(apikey, remain_chars))
                if remain_chars > max_remain_chars:
                    auth_key = apikey
                    max_remain_chars = remain_chars

                print("will finally used {} as it's the more loaded ones".format(auth_key))

    return auth_key


def ask_and_store_api_key():
    auth_key = input("Enter your deepL api key: ")
    with open(path_to_deepl_apikey, "a") as apikey_file:
        apikey_file.write('\n' + auth_key)
        apikey_file.close()

    return auth_key


def init():
    global init_done
    global translator

    auth_key = get_api_key()

    if auth_key is None:
        auth_key = ask_and_store_api_key()

    # init deepl translator
    translator = deepl.Translator(auth_key)
    init_done = True


def translate_text(text_to_translate):
    if not init_done:
        init()

    return translator.translate_text(
        text_to_translate,
        source_lang=config.sourceLang,
        target_lang=config.targetLang,
        formality=config.formality,
        tag_handling="xml",
        split_sentences='nonewlines'
    )
