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

todo_files = Path(config.plannedPath).glob(config.fileExt)
totalNbChars = 0

# for each file to process
for todo_filepath in todo_files:
    with open(todo_filepath, "r", encoding=config.input_encoding) as todo_file:
        nbChars = 0
        for line in todo_file:
            if any(c.isalpha() for c in line):
                if config.removeDeafAnnotations:
                    line = functions.clean_sentence(line)
                nbChars += len(line)
        print(colorama.Fore.GREEN + "File {} contains ".format(todo_filepath) + colorama.Fore.RED + "{}".format(nbChars) + colorama.Fore.GREEN + " chars to translate")
        totalNbChars += nbChars

print()
print(colorama.Fore.LIGHTMAGENTA_EX + "total chars count for all files : {}".format(totalNbChars))

# exit program
colorama.deinit()
exit(0)
