Write-Host "start installation" -foregroundcolor "green"
conda create --name srt-translator
conda activate srt-translator
pip install -r requirements.txt
Write-Host "installation done" -foregroundcolor "green"
Write-Host "insert your deepl api key in the beginning of srt-translator.py, put your srt files to batch/todo and execute run powershell script. Have fun!" -foregroundcolor "yellow"