Write-Host "start installation" -foregroundcolor "green"
conda create --name XtrTranslator
conda activate XtrTranslator
pip install -r requirements.txt
Write-Host "installation done" -foregroundcolor "geen"
Write-Host "insert your deepl api key in the beginning of XtrTranslator.py, put your srt files to batch/todo and execute run powershell script. Have fun!" -foregroundcolor "yellow"