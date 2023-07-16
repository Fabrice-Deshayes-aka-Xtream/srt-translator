# srt-translator
batch translate subtitles srt files using deepL api

## installation

### prerequisites 

- miniconda
- git

You can check that all is ok by checking conda, python and git version
```powershell
conda --version
conda 23.5.2

python --version
Python 3.10.12

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

## Usage

### only the first time

as mention at the end of setup, edit srt-translator.py file to insert your deepL api key here

```python
auth_key = "<here>"
```

you can request a free deepL api key on the [deepL web-site](https://www.deepl.com/fr/pro-api?cta=header-pro-api/)

You can also change the target language for translation which is FR by default

```python
targetLang = "FR"
```

### normal usage

put your .srt files to translate  into the batch/toto folder

using powershell on Windows terminal, go inside `srt-translator` folder and execute run script

```powershell
cd srt-translator
./run.ps1
```

After execution, processed files have be moved to batch/done folder, and the translation result files are in batch/result folder.