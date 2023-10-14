import time

import config
import os
import deepl
import colorama

path_to_deepl_apikey = "deepl_apikey.txt"


def get_character_usage_info(apikey=None):
    translator = init_translator(apikey)
    return translator.get_usage().character


def get_best_api_key(display_stats):
    apikey = None
    max_remain_chars = 0
    total_remain_chars = 0

    if os.path.isfile(path_to_deepl_apikey):
        with open(path_to_deepl_apikey, "r") as apikey_file:
            apikeys = apikey_file.readlines()
            for current_apikey in apikeys:
                current_apikey = current_apikey.strip()
                if current_apikey.startswith("#") or len(current_apikey) == 0:
                    continue

                usage = get_character_usage_info(current_apikey)
                remain_chars = usage.limit - usage.count
                total_remain_chars += remain_chars

                if display_stats:
                    print(
                        colorama.Fore.LIGHTGREEN_EX + "{}".format(remain_chars) +
                        colorama.Fore.LIGHTWHITE_EX + " characters left on your apikey " +
                        colorama.Fore.LIGHTGREEN_EX + "*****{}".format(current_apikey[-8:])
                    )

                if remain_chars > 0 and remain_chars > max_remain_chars:
                    apikey = current_apikey
                    max_remain_chars = remain_chars

    return apikey, remain_chars, total_remain_chars


def ask_and_store_api_key():
    apikey = input("Enter your deepL api key: ")
    file_already_exist = os.path.isfile(path_to_deepl_apikey)
    with open(path_to_deepl_apikey, "a") as apikey_file:
        if file_already_exist:
            apikey_file.write('\n' + apikey)
        else:
            apikey_file.write(apikey)
        apikey_file.close()

    return apikey


def init_translator(apikey=None):
    if apikey is None:
        # get api key from path_to_deepl_apikey file (choose the one with the most remaining chars allowed)
        apikey_infos = get_best_api_key(False)
        apikey = apikey_infos[0]

        # if there's no key configured or valid, ask a new one
        if apikey is None:
            apikey = ask_and_store_api_key()

    # init deepl translator
    return deepl.Translator(apikey)


def translate_text(text_to_translate):
    translator = init_translator()

    # uncomment for tests
    text_to_translate = "1"
    time.sleep(2)

    return translator.translate_text(
        text_to_translate,
        source_lang=config.sourceLang,
        target_lang=config.targetLang,
        formality=config.formality,
        tag_handling="xml",
        split_sentences='nonewlines'
    )
