$exclude = @("venv", "ProjetoFinalCompass.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "ProjetoFinalCompass.zip" -Force