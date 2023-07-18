import re
import sys


# function used to display a progress bar
def progressbar(count_value, total, suffix=''):
    bar_length = 100
    filled_up_length = int(round(bar_length * count_value / float(total)))
    percentage = round(100.0 * count_value / float(total), 1)
    bar = '=' * filled_up_length + '-' * (bar_length - filled_up_length)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percentage, '%', suffix))
    sys.stdout.flush()


# remove annotation (...) or [...] from string
def clean_sentence(sentence=""):
    sentence = re.sub("(?:\(.+?\))", "", sentence)  # remove (...)
    sentence = re.sub("(?:\[.+?\])", "", sentence)  # remove [...]
    sentence = re.sub("\ {1,}", " ", sentence)  # replace multiple spaces by on space
    return sentence
