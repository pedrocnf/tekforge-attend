param(
    [string]$GithubOwner = "pedrocnf",
    [string]$GithubRepo = "tekforge-attend",
    [string]$ProjectId = "tekforge-attend",
    [string]$ProjectNumber = "772785199121",
    [string]$Region = "us-central1"
)

$ErrorActionPreference = "Stop"

function Ensure-Command($name) {
    if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
        throw "Comando '$name' não encontrado. Instale e tente novamente."
    }
}

Ensure-Command gh

$RepoFull = "$GithubOwner/$GithubRepo"

Write-Host "Gravando GitHub Variables em $RepoFull" -ForegroundColor Cyan
gh variable set GCP_PROJECT_ID --repo $RepoFull --body $ProjectId
gh variable set GCP_PROJECT_NUMBER --repo $RepoFull --body $ProjectNumber
gh variable set GCP_REGION --repo $RepoFull --body $Region
gh variable set APP_DOMAIN --repo $RepoFull --body "www.tekattend.tekforge.com.br"
gh variable set API_DOMAIN --repo $RepoFull --body "api.tekattend.tekforge.com.br"

Write-Host "Concluído." -ForegroundColor Green
