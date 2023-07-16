# srt-translator

> Batch translate subtitles srt files using deepL api

/!\ **you must request a free or paid deepL api key on the [deepL web-site](https://www.deepl.com/fr/pro-api?cta=header-pro-api/)** /!\

Developed by Fabrice Deshayes for my friend Didier Martini  

## installation

### prerequisites 

- miniconda (conda, python, pip)
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

put your .srt files to translate into the batch/todo folder

using powershell on Windows terminal, go inside `srt-translator` folder and execute run script

```powershell
cd srt-translator
./run.ps1
```

you can request a free deepL api key on the [deepL web-site](https://www.deepl.com/fr/pro-api?cta=header-pro-api/)

After execution, processed files have be moved to batch/done folder, and the translation result files are in
batch/result folder.