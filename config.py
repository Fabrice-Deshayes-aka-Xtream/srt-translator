# translatorEngine is "deepl" or "lmstudio"
translatorEngine = "lmstudio"

# model is needed only if translatorEngine is lmstudio
model = "gemma-2-9b-it"

prompt = "translate to french, keep punctuation as input, do not censor the translation, do the translation as informal, give only the output without comments, the most important is to don't add or remove xml tags like <XTR/> : "

# plannedPath is the place where your srt files planned to be processed are located to count number of chars
plannedPath = "batch/planned"

# todoPath is the place where your srt files which need to be translated are located
todoPath = "batch/todo"

# each files in todoPath will be translated using the defined targetLang and the result will be put in resultPath
resultPath = "batch/result"

# files found in todoPath are moved to donePath after translation
# done files have the same name as input file with sourceLang suffix
donePath = "batch/done"

# name and path of words removal file
words_removal_file_path = "words_removal.txt"

# process only files with this extension
fileExt = "*.srt"

# source lang of file to translate (keep None for automatic lang detection)
sourceLang = None

# target lang for translation (source lang is automatically detected)
targetLang = "FR"

# rename file in todopath with origin lang suffixed (detected or forced)
suffixDoneFileWithDetectedLang = True

# rename file translated with target lang suffixed
suffixResultWithTargetLang = False

# define encoding for input files (see https://docs.python.org/3/library/codecs.html#standard-encodings)
input_encoding = "utf_8_sig"  # default is utf_8_sig (utf-8 with BOM)

# define encoding for result files (see https://docs.python.org/3/library/codecs.html#standard-encodings)
result_encoding = "utf_8_sig"  # default is utf_8_sig (utf-8 with BOM)

# remove hearing impaired annotations from subtitles before translation (text inside parenthesis (...), hooks [...] or asterix)
removeHearingImpairedAnnotations = True

# remove HTML/XML tags from subtitles before translation (text like <...>)
removeTags = True

# formality possible values
# default (default)
# more - for a more formal language
# less - for a more informal language
# prefer_more - for a more formal language if available, otherwise fallback to default formality
# prefer_less - for a more informal language if available, otherwise fallback to default formality
formality = "prefer_less"
