Write-Host "activate conda dedicated environnent" -foregroundcolor "green"
conda activate srt-translator
Write-Host "execute srt-count-chars" -foregroundcolor "green"
python srt-count-chars.py