Write-Host "Start installation" -foregroundcolor "green"
conda create --name srt-translator
conda activate srt-translator
pip install -r requirements.txt
Write-Host "Installation done" -foregroundcolor "green"
Write-Host "Put your srt files into batch/todo and execute run powershell script. Type your deepl api key on first launch. Have fun!" -foregroundcolor "yellow"