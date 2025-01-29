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

docker rm jedha-final-project-app -f
docker image rm jedha-final-project-app -f
docker build . -t jedha-final-project-app
docker run --name jedha-final-project-app `
    --detach `
    --volume ./src:/app `
    --env PORT=$env:DEFAULT_PORT `
    --publish $env:PORT`:$env:DEFAULT_PORT `
    jedha-final-project-app