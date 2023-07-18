Write-Host "activate conda dedicated environnent" -foregroundcolor "green"
conda activate srt-translator
Write-Host "execute srt-count-chars" -foregroundcolor "green"
python srt-count-chars.py
Write-Host -NoNewLine 'Press any key to continue...';
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');