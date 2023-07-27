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
from pathlib import Path

import colorama

import config
import functions
import deepl_translator
import microsoft_translator

# check that there are files to process in todoPath, throws warning otherwise
nbFilesToProcess = sum(1 for dummy in Path(config.todoPath).glob(config.fileExt))
if nbFilesToProcess == 0:
    print(
        colorama.Fore.YELLOW + "WARNING: no file with extension {} present in {} folder. nothing todo".format(
            config.fileExt, config.todoPath))
    colorama.deinit()
    exit(0)

print(colorama.Fore.GREEN + "start to process {} file(s)".format(nbFilesToProcess))
print()

todo_files = Path(config.todoPath).glob(config.fileExt)

# for each file to process
currentFile = 1
for todo_filepath in todo_files:
    # compute the result file path (same filename as file to process with targetLang as suffix)
    result_filepath = Path(
        config.resultPath + "/" + todo_filepath.stem + "-" + config.targetLang + todo_filepath.suffix)
    # compute the done file path (were file processed will be moved after translation)
    done_filepath = Path(config.donePath + "/" + todo_filepath.stem + todo_filepath.suffix)

    # translate file
    print(colorama.Fore.GREEN + "translate file {}/{} [{}] to [{}]".format(currentFile, nbFilesToProcess, todo_filepath, result_filepath))
    with open(result_filepath, "w", encoding=config.result_encoding) as result_file:

        with open(todo_filepath, "rb") as f:
            nbLines = sum(1 for _ in f)

        with open(todo_filepath, "r", encoding=config.input_encoding) as todo_file:
            i = 0
            for line in todo_file:
                if any(c.isalpha() for c in line):
                    # line which contain letters must be translated
                    # remove deaf annotations if asked
                    if config.removeDeafAnnotations:
                        line = functions.clean_sentence(line)

                    # translate line using the configured translation engine
                    match config.translation_engine:
                        case "deepl":
                            translated_line = deepl_translator.translate_text(line)
                        case "microsoft":
                            translated_line = microsoft_translator.translate_text(line)

                    # write result to file
                    result_file.write(translated_line)
                else:
                    # line which doesn't contain letters are copied as is (sequence number, time code, empty line)
                    # this help to reduce the number of characters send to deepl (free subscription is limiter to 500 000 characters per month)
                    result_file.write(line)

                # display a progress bar, it's useful specially for big file
                i += 1
                functions.progressbar(i, nbLines)

        # translation is done, move processed file to the done folder
        print()
        print(colorama.Fore.GREEN + "move [{}] to [{}]".format(todo_filepath, done_filepath))
        print()
        Path(todo_filepath).rename(done_filepath)

# exit program
colorama.deinit()
exit(0)
