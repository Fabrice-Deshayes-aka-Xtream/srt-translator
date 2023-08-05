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
import datetime

import colorama

import config
import functions
import deepl_translator


def main():
    # check that there are files to process in todoPath, throws warning otherwise
    nb_files_to_process = sum(1 for dummy in Path(config.todoPath).glob(config.fileExt))
    if nb_files_to_process == 0:
        print(
            colorama.Fore.YELLOW + "WARNING: no file with extension {} present in {} folder. nothing todo".format(config.fileExt, config.todoPath))
        colorama.deinit()
        exit(0)

    print(colorama.Fore.GREEN + "start to process {} file(s)".format(nb_files_to_process))
    print()

    todo_files = Path(config.todoPath).glob(config.fileExt)

    # for each file to process
    current_file = 1
    for todo_filepath in todo_files:
        start = datetime.datetime.now()

        # compute the result file path (same filename as file to process with targetLang as suffix)
        result_filepath = Path(config.resultPath + "/" + todo_filepath.stem + "-" + config.targetLang + todo_filepath.suffix)
        # compute the done file path (were file processed will be moved after translation)
        done_filepath = Path(config.donePath + "/" + todo_filepath.stem + todo_filepath.suffix)

        # translate file
        print(colorama.Fore.GREEN + "translate file {}/{} [{}] to [{}]".format(current_file, nb_files_to_process, todo_filepath, result_filepath))
        with open(result_filepath, "w", encoding=config.result_encoding) as result_file:
            # translate in one call to preserve full context
            translate_srt(todo_filepath, result_file)

            end = datetime.datetime.now()
            elapsed = end - start
            print(colorama.Fore.GREEN + "file [{}] translated in {} s".format(todo_filepath, elapsed.total_seconds()))

            # translation is done, move processed file to the done folder
            print()
            print(colorama.Fore.GREEN + "move [{}] to [{}]".format(todo_filepath, done_filepath))
            print()
            Path(todo_filepath).rename(done_filepath)

            current_file += 1

    # exit program
    colorama.deinit()
    exit(0)


def translate_srt(todo_filepath, result_file):
    # split technical info (sequence, timecode) and subtitles text (which will be separate with a <BR/> tag by removing line feed)
    result = functions.split_srt(todo_filepath)

    # merge all subtitles items in one big string to translate it in one time to preserve context and improve translation quality and speed
    subtitles_to_translate_as_str = ''.join(result[1])

    # translate all subtitles with deepl
    subtitles_translated_as_str = deepl_translator.translate_text(subtitles_to_translate_as_str)

    # rebuild subtitles arrays using <BR/> delimiter
    subtitles_translated = subtitles_translated_as_str.split('<BR/>')

    # fix some punctuation anomaly caused by translation
    subtitles_translated = functions.fix_anomaly(subtitles_translated)

    # generate translated SRT file with technical info (sequence, timecode) and translated subtitles
    functions.merge_srt(result_file, result[0], subtitles_translated)


if __name__ == "__main__":
    main()
