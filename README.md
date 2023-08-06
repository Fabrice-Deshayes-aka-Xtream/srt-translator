# srt-translator

> Batch translate subtitles srt files using deepL api
> - minimise number of characters to translate by removing sequence number, timecode and can optionally remove tags and hearing impaired annotations
> - translation is done with one big string. It preserves context by avoiding line by line translation and improve translation time.
> - automatically fix some punctuation glitch after translation

/!\ **you must request a free or paid deepL api key on the [deepL web-site](https://www.deepl.com/fr/pro-api?cta=header-pro-api/)** /!\

Developed by Fabrice Deshayes for my friend Didier Martini  

## installation

### prerequisites 

- miniconda (which install conda + python + pip)
- git

You can check that all is ok by checking conda, python, pip and git version
```powershell
conda --version
conda 23.5.2

python --version
Python 3.10.12

pip --version                                                                                                                                            ─╯
pip 23.1.2 from C:\Users\fabri\scoop\apps\miniconda3\current\lib\site-packages\pip (python 3.10)

git --version
git version 2.41.0.windows.2
```

### setup

clone project somewhere on you disk
```
git clone https://github.com/Fabrice-Deshayes-aka-Xtream/srt-translator.git
```

using powershell on Windows terminal, go inside `srt-translator` folder and execute setup script
```powershell
cd srt-translator
./setup.ps1
```

that's all folks! this setup scrip has created a conda environment dedicated for this project and install all required libraries using pip. No need to activate the environment, it will be done automatically by using the run script.

## usage

put your .srt files to translate into the batch/todo folder

using powershell on Windows terminal, go inside `srt-translator` folder and execute run script

```powershell
cd srt-translator
./run.ps1
```

you can request a free deepL api key on the [deepL web-site](https://www.deepl.com/fr/pro-api?cta=header-pro-api/)

After execution, processed files have be moved to batch/done folder, and the translation result files are in
batch/result folder.

You can also put your file in batch/planned and launch the program which count the number of chars to translate in
files

```powershell
cd srt-translator
./run-count.ps1
```

## configuration

some variables can be changed on config.py file if needed. **please note that only deepl translation_engine is working. Microsoft one's has not been tested yet.**

```python
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

# remove deaf annotations from translated result (text inside parenthesis (...) or hooks [...])
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
```