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
            colorama.Fore.LIGHTRED_EX + "WARNING: no file with extension {} present in {} folder. nothing todo".format(config.fileExt, config.todoPath))
        colorama.deinit()
        exit(0)

    print(
        colorama.Fore.LIGHTWHITE_EX + "start to batch process " +
        colorama.Fore.LIGHTGREEN_EX + "{}".format(nb_files_to_process) +
        colorama.Fore.LIGHTWHITE_EX + " file(s)"
    )
    print()

    todo_files = Path(config.todoPath).glob(config.fileExt)

    # for each file to process
    current_file = 1
    for todo_filepath in todo_files:
        start = datetime.datetime.now()

        nb_chars_to_translate = functions.count_chars_to_translate(todo_filepath)
        nb_chars_left_on_deepl_account = deepl_translator.get_character_usage_info().count

        if nb_chars_to_translate > nb_chars_left_on_deepl_account:
            print(
                colorama.Fore.LIGHTRED_EX + "Skip file" +
                colorama.Fore.LIGHTBLUE_EX + "{}".format(todo_filepath) +
                colorama.Fore.LIGHTWHITE_EX + " because theres is not enough credits left on deepl account. Need " +
                colorama.Fore.LIGHTGREEN_EX + "{}".format(nb_chars_to_translate) +
                colorama.Fore.LIGHTWHITE_EX + " but only " +
                colorama.Fore.LIGHTGREEN_EX + "{}".format(nb_chars_left_on_deepl_account) +
                colorama.Fore.LIGHTWHITE_EX + " left."
            )
            continue

        # compute the result file path (same filename as file to process with targetLang as suffix)
        if config.suffixResultWithTargetLang:
            result_filepath = Path(config.resultPath + "/" + todo_filepath.stem + "_" + config.targetLang + todo_filepath.suffix)
        else:
            result_filepath = Path(config.resultPath + "/" + todo_filepath.stem + todo_filepath.suffix)

        # translate file
        print(
            colorama.Fore.LIGHTGREEN_EX + "{}".format(current_file) +
            colorama.Fore.LIGHTWHITE_EX + "/" +
            colorama.Fore.LIGHTGREEN_EX + "{}: ".format(nb_files_to_process) +
            colorama.Fore.LIGHTWHITE_EX + "translate file " +
            colorama.Fore.LIGHTBLUE_EX + "{}".format(todo_filepath) +
            colorama.Fore.LIGHTWHITE_EX + " to " +
            colorama.Fore.LIGHTBLUE_EX + "{}".format(result_filepath) +
            colorama.Fore.LIGHTWHITE_EX + " (" +
            colorama.Fore.LIGHTGREEN_EX + "{}".format(nb_chars_to_translate) +
            colorama.Fore.LIGHTWHITE_EX + " characters)"
        )

        with open(result_filepath, "w", encoding=config.result_encoding) as result_file:
            # translate in one call to preserve full context
            detected_source_lang = translate_srt_in_packets(todo_filepath, result_file)

            # compute the done file path (were file processed will be moved after translation)
            if config.suffixDoneFileWithDetectedLang:
                done_filepath = Path(config.donePath + "/" + todo_filepath.stem + "_" + detected_source_lang + todo_filepath.suffix)
            else:
                done_filepath = Path(config.donePath + "/" + todo_filepath.stem + todo_filepath.suffix)

            # translation is done, move processed file to the done folder
            end = datetime.datetime.now()
            elapsed = end - start
            print(
                colorama.Fore.LIGHTWHITE_EX + "\nfile " +
                colorama.Fore.LIGHTBLUE_EX + "{}".format(todo_filepath) +
                colorama.Fore.LIGHTWHITE_EX + " translated in " +
                colorama.Fore.LIGHTGREEN_EX + "{}".format(elapsed.total_seconds()) +
                colorama.Fore.LIGHTWHITE_EX + " seconds and moved to " +
                colorama.Fore.LIGHTBLUE_EX + "{}".format(done_filepath)
            )
            print()
            Path(todo_filepath).rename(done_filepath)
            current_file += 1

    apikey_infos = deepl_translator.get_best_api_key()
    print(
        colorama.Fore.LIGHTGREEN_EX + "{}".format(apikey_infos[1]) +
        colorama.Fore.LIGHTWHITE_EX + " characters left on you deepl subscription for this billing period"
    )

    # exit program
    colorama.deinit()
    exit(0)


def translate_srt_in_packets(todo_filepath, result_file):
    # split technical info (sequence, timecode) and subtitles text
    result = functions.split_srt(todo_filepath)

    nb_subtitles = len(result[1])
    current_index_subtitle = 0
    subtitles_translated_as_str = ""

    # subtitles are concatenate, removing line feed to preserve context and translate by packet (to not reach deepl limit per api call)
    # functions.subtitle_separator is used to keep sequence and subtitle line separation, mandatory to rebuild the final SRT file
    while current_index_subtitle + functions.packets_size < nb_subtitles:
        functions.progressbar(current_index_subtitle, nb_subtitles)

        # merge subtitles items by packets_size
        subtitles_to_translate_as_str = ''.join(result[1][current_index_subtitle:current_index_subtitle + functions.packets_size])

        # translate subtitles packet with deepl
        translate_result = deepl_translator.translate_text(subtitles_to_translate_as_str)
        subtitles_translated_as_str += translate_result.text

        current_index_subtitle += functions.packets_size

    # process the last packet
    functions.progressbar(current_index_subtitle, nb_subtitles)
    subtitles_to_translate_as_str = ''.join(result[1][current_index_subtitle:])
    translate_result = deepl_translator.translate_text(subtitles_to_translate_as_str)
    subtitles_translated_as_str += translate_result.text
    functions.progressbar(nb_subtitles, nb_subtitles)  # 100%

    # rebuild subtitles arrays using functions.subtitle_separator delimiter
    subtitles_translated = subtitles_translated_as_str.split(functions.subtitle_separator)

    # fix some punctuation anomaly caused by translation
    subtitles_translated = functions.fix_anomaly(subtitles_translated)

    # generate translated SRT file with technical info (sequence, timecode) and translated subtitles
    functions.merge_srt(result_file, result[0], subtitles_translated)

    return translate_result.detected_source_lang


if __name__ == "__main__":
    main()
