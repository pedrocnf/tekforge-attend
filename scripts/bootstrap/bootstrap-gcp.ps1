[CmdletBinding()]
param(
    [string]$ProjectId = "tekforge-attend",
    [string]$ProjectNumber = "772785199121",
    [string]$BillingAccount = "018CCA-9AF2D4-93B4FA",
    [string]$Region = "us-central1",
    [string]$GithubOwner = "pedrocnf",
    [string]$GithubRepo = "tekforge-attend",
    [switch]$CreateGithubVariables,
    [switch]$SkipProjectCreation,
    [switch]$SkipBillingLink
)

$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$RepoFull = "$GithubOwner/$GithubRepo"
$ArtifactRepoName = "tekattend-artifacts"
$AssetsBucket = "$ProjectId-assets"
$ExportsBucket = "$ProjectId-exports"
$WifPoolId = "github-pool"
$WifProviderId = "github-provider"
$CloudRunService = "tekattend-api"
$ImageName = "tekattend-api"

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Ensure-Command {
    param([string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Comando '$Name' não encontrado."
    }
}

function Invoke-Gcloud {
    param(
        [Parameter(Mandatory = $true)][string[]]$Args,
        [switch]$Quiet
    )

    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "gcloud.cmd"
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true

    foreach ($arg in $Args) {
        [void]$psi.ArgumentList.Add($arg)
    }

    $proc = New-Object System.Diagnostics.Process
    $proc.StartInfo = $psi
    [void]$proc.Start()
    $stdout = $proc.StandardOutput.ReadToEnd()
    $stderr = $proc.StandardError.ReadToEnd()
    $proc.WaitForExit()

    if (-not $Quiet) {
        if ($stdout) { Write-Host $stdout.TrimEnd() }
        if ($stderr) { Write-Host $stderr.TrimEnd() }
    }

    return [PSCustomObject]@{
        ExitCode = $proc.ExitCode
        StdOut   = $stdout
        StdErr   = $stderr
    }
}

function Assert-Gcloud {
    param(
        [Parameter(Mandatory = $true)][string[]]$Args,
        [Parameter(Mandatory = $true)][string]$FriendlyName
    )

    $result = Invoke-Gcloud -Args $Args
    if ($result.ExitCode -ne 0) {
        throw "Falha ao executar: $FriendlyName"
    }
    return $result
}

function Test-Gcloud {
    param(
        [Parameter(Mandatory = $true)][string[]]$Args
    )
    $result = Invoke-Gcloud -Args $Args -Quiet
    return ($result.ExitCode -eq 0)
}

function Ensure-ProjectExists {
    if (Test-Gcloud @("projects","describe",$ProjectId)) {
        Write-Host "Projeto já existe: $ProjectId"
    } else {
        Assert-Gcloud @("projects","create",$ProjectId,"--name",$ProjectId) -FriendlyName "criação do projeto"
    }
}

function Ensure-BillingLinked {
    Assert-Gcloud @("beta","billing","projects","link",$ProjectId,"--billing-account",$BillingAccount) -FriendlyName "associação do billing account"
}

function Ensure-ProjectService {
    param([string]$ServiceName)
    $check = Invoke-Gcloud -Args @("services","list","--enabled","--project",$ProjectId,"--filter","config.name=$ServiceName","--format","value(config.name)") -Quiet
    if ($check.ExitCode -eq 0 -and $check.StdOut.Trim() -eq $ServiceName) {
        Write-Host "API já habilitada: $ServiceName"
    } else {
        Assert-Gcloud @("services","enable",$ServiceName,"--project",$ProjectId) -FriendlyName "ativação da API $ServiceName"
    }
}

function Ensure-ServiceAccount {
    param(
        [string]$AccountId,
        [string]$DisplayName
    )
    $email = "$AccountId@$ProjectId.iam.gserviceaccount.com"
    if (Test-Gcloud @("iam","service-accounts","describe",$email,"--project",$ProjectId)) {
        Write-Host "Service account já existe: $email"
    } else {
        Assert-Gcloud @("iam","service-accounts","create",$AccountId,"--display-name",$DisplayName,"--project",$ProjectId) -FriendlyName "criação da service account $email"
    }
    return $email
}

function Add-ProjectBinding {
    param(
        [string]$Member,
        [string]$Role
    )
    Assert-Gcloud @("projects","add-iam-policy-binding",$ProjectId,"--member",$Member,"--role",$Role) -FriendlyName "binding $Role para $Member"
}

function Ensure-ArtifactRegistry {
    if (Test-Gcloud @("artifacts","repositories","describe",$ArtifactRepoName,"--location",$Region,"--project",$ProjectId)) {
        Write-Host "Artifact Registry já existe: $ArtifactRepoName"
    } else {
        Assert-Gcloud @("artifacts","repositories","create",$ArtifactRepoName,"--repository-format","docker","--location",$Region,"--description","Docker images do TekAttend","--project",$ProjectId) -FriendlyName "criação do Artifact Registry"
    }
}

function Ensure-Bucket {
    param([string]$BucketName)
    $bucketUrl = "gs://$BucketName"
    if (Test-Gcloud @("storage","buckets","describe",$bucketUrl,"--project",$ProjectId)) {
        Write-Host "Bucket já existe: $BucketName"
    } else {
        Assert-Gcloud @("storage","buckets","create",$bucketUrl,"--location",$Region,"--uniform-bucket-level-access","--project",$ProjectId) -FriendlyName "criação do bucket $BucketName"
    }
}

function Ensure-Secret {
    param([string]$SecretName)
    if (Test-Gcloud @("secrets","describe",$SecretName,"--project",$ProjectId)) {
        Write-Host "Secret já existe: $SecretName"
    } else {
        Assert-Gcloud @("secrets","create",$SecretName,"--replication-policy","automatic","--project",$ProjectId) -FriendlyName "criação do secret $SecretName"
    }
}

function Ensure-WifPool {
    if (Test-Gcloud @("iam","workload-identity-pools","describe",$WifPoolId,"--project",$ProjectNumber,"--location","global")) {
        Write-Host "Workload Identity Pool já existe: $WifPoolId"
    } else {
        Assert-Gcloud @("iam","workload-identity-pools","create",$WifPoolId,"--project",$ProjectNumber,"--location","global","--display-name","GitHub Actions Pool") -FriendlyName "criação do Workload Identity Pool"
    }
}

function Ensure-WifProvider {
    if (Test-Gcloud @("iam","workload-identity-pools","providers","describe",$WifProviderId,"--project",$ProjectNumber,"--location","global","--workload-identity-pool",$WifPoolId)) {
        Write-Host "Provider já existe: $WifProviderId"
    } else {
        Assert-Gcloud @(
            "iam","workload-identity-pools","providers","create-oidc",$WifProviderId,
            "--project",$ProjectNumber,
            "--location","global",
            "--workload-identity-pool",$WifPoolId,
            "--display-name","GitHub Provider",
            "--issuer-uri","https://token.actions.githubusercontent.com",
            "--attribute-mapping","google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner,attribute.ref=assertion.ref",
            "--attribute-condition","assertion.repository=='$RepoFull'"
        ) -FriendlyName "criação do Workload Identity Provider"
    }
}

function Set-GithubVariables {
    Ensure-Command "gh"
    & gh variable set GCP_PROJECT_ID --repo $RepoFull --body $ProjectId
    & gh variable set GCP_PROJECT_NUMBER --repo $RepoFull --body $ProjectNumber
    & gh variable set GCP_REGION --repo $RepoFull --body $Region
    & gh variable set GCP_ARTIFACT_REGISTRY --repo $RepoFull --body $ArtifactRepoName
    & gh variable set GCP_WIF_PROVIDER --repo $RepoFull --body $WorkloadIdentityProviderResource
    & gh variable set GCP_DEPLOYER_SA --repo $RepoFull --body $GithubDeploySaEmail
    & gh variable set GCP_RUNTIME_SA --repo $RepoFull --body $RuntimeSaEmail
    & gh variable set GCP_ASSETS_BUCKET --repo $RepoFull --body $AssetsBucket
    & gh variable set GCP_EXPORTS_BUCKET --repo $RepoFull --body $ExportsBucket
    & gh variable set CLOUD_RUN_SERVICE --repo $RepoFull --body $CloudRunService
    & gh variable set DOCKER_IMAGE_NAME --repo $RepoFull --body $ImageName
    & gh variable set APP_DOMAIN --repo $RepoFull --body "www.tekattend.tekforge.com.br"
    & gh variable set API_DOMAIN --repo $RepoFull --body "api.tekattend.tekforge.com.br"
    & gh variable set FIRESTORE_DATABASE --repo $RepoFull --body "(default)"
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao gravar GitHub Variables."
    }
}

Ensure-Command "gcloud.cmd"

if (-not $SkipProjectCreation) {
    Write-Step "Criando projeto (se ainda não existir)"
    Ensure-ProjectExists

    if (-not $SkipBillingLink) {
        Write-Step "Associando billing account"
        Ensure-BillingLinked
    }
}

Write-Step "Configurando projeto padrão"
Assert-Gcloud @("config","set","project",$ProjectId) -FriendlyName "configuração do projeto padrão"

Write-Step "Ativando APIs essenciais"
$apis = @(
    "run.googleapis.com",
    "artifactregistry.googleapis.com",
    "secretmanager.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "sts.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "firebase.googleapis.com",
    "firestore.googleapis.com",
    "storage.googleapis.com",
    "cloudbuild.googleapis.com",
    "compute.googleapis.com"
)
foreach ($api in $apis) { Ensure-ProjectService -ServiceName $api }

Write-Step "Criando service accounts"
$GithubDeploySaEmail = Ensure-ServiceAccount -AccountId "github-actions-deployer" -DisplayName "GitHub Actions Deployer"
$RuntimeSaEmail = Ensure-ServiceAccount -AccountId "tekattend-runtime" -DisplayName "TekAttend Runtime"

Write-Step "Concedendo papéis ao deployer"
$deployerRoles = @(
    "roles/run.admin",
    "roles/iam.serviceAccountUser",
    "roles/artifactregistry.writer",
    "roles/storage.admin",
    "roles/secretmanager.admin",
    "roles/datastore.user",
    "roles/serviceusage.serviceUsageConsumer"
)
foreach ($role in $deployerRoles) {
    Add-ProjectBinding -Member "serviceAccount:$GithubDeploySaEmail" -Role $role
}

Write-Step "Concedendo papéis ao runtime"
$runtimeRoles = @(
    "roles/datastore.user",
    "roles/secretmanager.secretAccessor",
    "roles/storage.objectAdmin"
)
foreach ($role in $runtimeRoles) {
    Add-ProjectBinding -Member "serviceAccount:$RuntimeSaEmail" -Role $role
}

Write-Step "Criando Artifact Registry"
Ensure-ArtifactRegistry

Write-Step "Criando buckets"
Ensure-Bucket -BucketName $AssetsBucket
Ensure-Bucket -BucketName $ExportsBucket

Write-Step "Criando secrets iniciais"
Ensure-Secret -SecretName "tekattend-jwt-secret"
Ensure-Secret -SecretName "tekattend-admin-bootstrap-password"

Write-Step "Criando Workload Identity Pool"
Ensure-WifPool
$WorkloadIdentityPoolResource = "projects/$ProjectNumber/locations/global/workloadIdentityPools/$WifPoolId"

Write-Step "Criando Workload Identity Provider"
Ensure-WifProvider
$WorkloadIdentityProviderResource = "$WorkloadIdentityPoolResource/providers/$WifProviderId"

Write-Step "Permitindo que o GitHub use a service account deployer"
Assert-Gcloud @(
    "iam","service-accounts","add-iam-policy-binding",$GithubDeploySaEmail,
    "--project",$ProjectId,
    "--role","roles/iam.workloadIdentityUser",
    "--member","principalSet://iam.googleapis.com/$WorkloadIdentityPoolResource/attribute.repository/$RepoFull"
) -FriendlyName "binding do Workload Identity User"

if ($CreateGithubVariables) {
    Write-Step "Gravando GitHub Variables no repositório"
    Set-GithubVariables
}

Write-Step "Bootstrap concluído"
Write-Host "Projeto: $ProjectId"
Write-Host "Repo GitHub: $RepoFull"
Write-Host "WIF Provider: $WorkloadIdentityProviderResource"
Write-Host "Deployer SA: $GithubDeploySaEmail"
Write-Host "Runtime SA: $RuntimeSaEmail"
Write-Host "Buckets: gs://$AssetsBucket | gs://$ExportsBucket"
Write-Host ""
Write-Host "Próximos passos:"
Write-Host "1. Adicione valores aos secrets:"
Write-Host "   echo 'SEU_JWT_AQUI' | gcloud secrets versions add tekattend-jwt-secret --data-file=-"
Write-Host "   echo 'SENHA_ADMIN_INICIAL' | gcloud secrets versions add tekattend-admin-bootstrap-password --data-file=-"
Write-Host "2. Faça push das workflows."
