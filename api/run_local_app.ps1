$envFilePath = ".env"
Get-Content $envFilePath | ForEach-Object {
    if ($_ -match '^\s*#' -or $_ -match '^\s*$') { 
        continue 
    }
    $key, $value = $_ -split '=', 2
    $key = $key.Trim()
    $value = $value.Trim()
    [System.Environment]::SetEnvironmentVariable($key, $value, [System.EnvironmentVariableTarget]::Process)
}

fastapi run src/app.py --host localhost --reload