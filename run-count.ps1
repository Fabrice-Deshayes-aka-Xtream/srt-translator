conda activate srt-translator
python srt-count-chars.py
Write-Host -NoNewLine 'Press any key to continue...' -foregroundcolor "Yellow"
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')