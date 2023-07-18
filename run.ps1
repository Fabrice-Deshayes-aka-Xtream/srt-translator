Write-Host "activate conda dedicated environnent" -foregroundcolor "green"
conda activate srt-translator
Write-Host "execute srt-translator" -foregroundcolor "green"
python srt-translator.py
Write-Host -NoNewLine 'Press any key to continue...';
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');