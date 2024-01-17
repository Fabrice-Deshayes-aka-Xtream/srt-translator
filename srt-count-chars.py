# --------------------------------------------------------------------
# srt-count-char
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

todo_files = Path(config.plannedPath).glob(config.fileExt)
totalNbChars = 0

# for each file to process
for todo_filepath in todo_files:
    nbChars = functions.count_chars_to_translate(todo_filepath)
    print(
        colorama.Fore.LIGHTWHITE_EX + "File " + colorama.Fore.LIGHTBLUE_EX + "{}".format(todo_filepath) +
        colorama.Fore.LIGHTWHITE_EX + " contains " + colorama.Fore.LIGHTGREEN_EX + "{}".format(nbChars) + colorama.Fore.LIGHTWHITE_EX + " chars to translate"
    )
    totalNbChars += nbChars

print()
print(colorama.Fore.LIGHTWHITE_EX + "Total chars count for all files : " + colorama.Fore.LIGHTGREEN_EX + "{}".format(totalNbChars))

print()
apikey, remain_chars, total_remain_chars = deepl_translator.get_best_api_key(True)
print(colorama.Fore.LIGHTGREEN_EX + "{}".format(total_remain_chars) + colorama.Fore.LIGHTWHITE_EX + " cumulated characters left for all apiKeys")

# exit program
colorama.deinit()
exit(0)
