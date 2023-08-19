# srt-translator

> Batch translate subtitles srt files using deepL api
> - minimise number of characters to translate by removing sequence number, timecode and can optionally remove HTML tags and hearing impaired annotations
> - translation is done on concatenated packet of subtitles (1000 lines). It preserves context by avoiding line by line translation, improve translation execution time and avoid
    exceeding deepl text length limit
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

using powershell on Windows terminal, go inside `srt-translator` folder and execute `setup.ps1` script.
you can also right-click "execute with powershell".
```powershell
cd srt-translator
./setup.ps1
```

that's all folks! this setup script has created a dedicated conda environment for this project and install all required libraries using pip. No need to activate the environment, it
will be done automatically by using the run script.

## usage

put your .srt files to translate into the batch/todo folder

using powershell on Windows terminal, go inside `srt-translator` folder and execute `run.ps1` script.
you can also right-click "execute with powershell".

```powershell
cd srt-translator
./run.ps1
```

Example of execution output

![image](https://github.com/Fabrice-Deshayes-aka-Xtream/srt-translator/assets/7294270/2f36d9da-b3c9-4397-9f5d-bc4f7eba9b7c)

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
formality = "prefer_less"
```
