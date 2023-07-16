Write-Host "activate conda dedicated environnent" -foregroundcolor "green"
conda activate srt-translator
Write-Host "execute XtrTranslator" -foregroundcolor "green"
python srt-translator.py