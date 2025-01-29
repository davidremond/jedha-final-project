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
docker rm jedha-final-project-api -f
docker image rm jedha-final-project-api
docker build . -t jedha-final-project-api
docker run --name jedha-final-project-api `
    --detach `
    --volume ./src:/app `
    --env DEFAULT_PORT=$env:DEFAULT_PORT `
    --env MLOPS_SERVER_URI=$env:MLOPS_SERVER_URI `
    --env MODEL_PATH=$env:MODEL_PATH `
    --publish $env:PORT`:$env:DEFAULT_PORT `
    jedha-final-project-api
