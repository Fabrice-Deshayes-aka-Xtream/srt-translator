# --------------------------------------------------------------------
# srt-translator
# Copyright (C) 2023  Fabrice Deshayes aka Xtream
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# --------------------------------------------------------------------
import os
import re
import sys
from pathlib import Path

import colorama
import deepl
from colorama import Fore

# todoPath is the place where your text files which need to be translated are located
todoPath = "batch/todo"

# each files in todoPath will be translated using the defined targetLang and the result will be put in resultPath
# result files have the same name as input file with targetLang suffix
resultPath = "batch/result"

# files found in todoPath are moved to donePath after translation
donePath = "batch/done"

# process only files with this extension
fileExt = "*.srt"

# target lang for translation (source lang is automatically detected)
targetLang = "FR"

# define encoding for input files (see https://docs.python.org/3/library/codecs.html#standard-encodings)
input_encoding = "utf_8_sig"  # default is utf_8_sig (utf-8 with BOM)

# define encoding for result files (see https://docs.python.org/3/library/codecs.html#standard-encodings)
result_encoding = "utf_8_sig"  # default is utf_8_sig (utf-8 with BOM)

# remove deaf annotations from translated result (text inside parenthesis (...) or hooks [...])
removeDeafAnnotations = True

# the file where is deepL apikey will be stored
path_to_deepl_apikey = "deepl_apikey.txt"


# function used to display a progress bar
def progressbar(count_value, total, suffix=''):
    bar_length = 100
    filled_up_length = int(round(bar_length * count_value / float(total)))
    percentage = round(100.0 * count_value / float(total), 1)
    bar = '=' * filled_up_length + '-' * (bar_length - filled_up_length)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percentage, '%', suffix))
    sys.stdout.flush()


def clean_sentence(sentence=""):
    sentence = re.sub("(?:\(.+?\))", "", sentence)  # remove (...)
    sentence = re.sub("(?:\[.+?\])", "", sentence)  # remove [...]
    sentence = re.sub("\ {1,}", " ", sentence)  # replace multiple spaces by on space
    return sentence


# load deepL apikey from file or ask it for the first time
auth_key = ""
if os.path.isfile(path_to_deepl_apikey):
    with open(path_to_deepl_apikey, "r") as apikey:
        auth_key = apikey.readlines().pop()

if len(auth_key) == 0:
    auth_key = input("Enter your deepL api key: ")
    with open(path_to_deepl_apikey, "w") as apikey:
        apikey.write(auth_key)
        apikey.close()

# check that there are files to process in todoPath, throws warning otherwise
nbFilesToProcess = sum(1 for dummy in Path(todoPath).glob(fileExt))
if nbFilesToProcess == 0:
    print(
        Fore.YELLOW + "WARNING: no file with extension {} present in {} folder. nothing todo".format(fileExt, todoPath))
    colorama.deinit()
    exit(0)

# init deepl translator
translator = deepl.Translator(auth_key)

print(Fore.GREEN + "start to process {} file(s)".format(nbFilesToProcess))
print()

todo_files = Path(todoPath).glob(fileExt)

# for each file to process
currentFile = 1
for todo_filepath in todo_files:
    # compute the result file path (same filename as file to process with targetLang as suffix)
    result_filepath = Path(resultPath + "/" + todo_filepath.stem + "-" + targetLang + todo_filepath.suffix)
    # compute the done file path (were file processed will be moved after translation)
    done_filepath = Path(donePath + "/" + todo_filepath.stem + todo_filepath.suffix)

    # translate file
    print(Fore.GREEN + "translate file {}/{} [{}] to [{}]".format(currentFile, nbFilesToProcess, todo_filepath,
                                                                  result_filepath))
    with open(result_filepath, "w", encoding=result_encoding) as result_file:

        with open(todo_filepath, "rb") as f:
            nbLines = sum(1 for _ in f)

        with open(todo_filepath, "r", encoding=input_encoding) as todo_file:
            i = 0
            for line in todo_file:
                if any(c.isalpha() for c in line):
                    # line which contain letters must be translated
                    # remove deaf annotations if asked
                    if removeDeafAnnotations:
                        line = clean_sentence(line)
                    result_file.write(translator.translate_text(line, target_lang=targetLang).text)
                else:
                    # line which doesn't contain letters are copied as is (sequence number, time code, empty line)
                    # this help to reduce the number of characters send to deepl (free subscription is limiter to 500 000 characters per month)
                    result_file.write(line)
                i += 1
                # display a progress bar, it's useful specially for big file
                progressbar(i, nbLines)

        # translation is done, move processed file to the done folder
        print()
        print(Fore.GREEN + "move [{}] to [{}]".format(todo_filepath, done_filepath))
        print()
        Path(todo_filepath).rename(done_filepath)

# exit program
colorama.deinit()
exit(0)
