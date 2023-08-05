# plannedPath is the place where your srt files planned to be processed are located to count number of chars
plannedPath = "batch/planned"

# todoPath is the place where your srt files which need to be translated are located
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

# remove deaf annotations from subtitles before translation (text inside parenthesis (...) or hooks [...])
removeDeafAnnotations = True

# remove HTML/XML tags from subtitles before translation (text like <...>)
removeTags = True

# formality possible values
# default (default)
# more - for a more formal language
# less - for a more informal language
# prefer_more - for a more formal language if available, otherwise fallback to default formality
# prefer_less - for a more informal language if available, otherwise fallback to default formality
formality = "prefer_more"

# Sets which kind of tags should be handled. Options currently available:
# None: dont try to translate text inside tags
# xml: Enable XML tag handling; see [XML Handling](https://www.deepl.com/fr/docs-api/xml/).
# html: Enable HTML tag handling; see [HTML Handling](https://www.deepl.com/fr/docs-api/html/).
# please note that deepl tag handling is currently buggy, if start tag is not on the same line as end tag.
# So removing tags before translation seem to produce better result than activate tag handling
tag_handling = None
