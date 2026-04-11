param(
    [string]$ProjectId = "tekforge-attend",
    [string]$ProjectNumber = "772785199121",
    [string]$BillingAccount = "018CCA-9AF2D4-93B4FA",
    [string]$Region = "us-central1",
    [string]$GithubOwner = "pedrocnf",
    [string]$GithubRepo = "tekforge-attend",
    [string]$GithubBranch = "main",
    [string]$Environment = "prod",
    [switch]$CreateGithubVariables,
    [switch]$SkipProjectCreation
)

$ErrorActionPreference = "Stop"

function Write-Step($message) {
    Write-Host ""
    Write-Host "==> $message" -ForegroundColor Cyan
}

function Ensure-Command($name) {
    if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
        throw "Comando '$name' não encontrado. Instale e tente novamente."
    }
}

Ensure-Command gcloud

Write-Step "Definindo configurações iniciais"
$RepoFull = "$GithubOwner/$GithubRepo"
$ProjectName = $ProjectId
$Location = $Region
$ArtifactRepoName = "tekattend-artifacts"
$AssetsBucket = "$ProjectId-assets"
$ExportsBucket = "$ProjectId-exports"
$WifPoolId = "github-pool"
$WifProviderId = "github-provider"
$GithubDeploySa = "github-actions-deployer"
$RuntimeSa = "tekattend-runtime"
$GithubDeploySaEmail = "$GithubDeploySa@$ProjectId.iam.gserviceaccount.com"
$RuntimeSaEmail = "$RuntimeSa@$ProjectId.iam.gserviceaccount.com"
$WorkloadIdentityPoolResource = "projects/$ProjectNumber/locations/global/workloadIdentityPools/$WifPoolId"
$WorkloadIdentityProviderResource = "$WorkloadIdentityPoolResource/providers/$WifProviderId"
$ImageName = "tekattend-api"
$CloudRunService = "tekattend-api"
$Secrets = @(
    "tekattend-jwt-secret",
    "tekattend-admin-bootstrap-password"
)

if (-not $SkipProjectCreation) {
    Write-Step "Criando projeto (se ainda não existir)"
    try {
        gcloud projects describe $ProjectId | Out-Null
        Write-Host "Projeto já existe: $ProjectId"
    } catch {
        gcloud projects create $ProjectId --name=$ProjectName
    }

    Write-Step "Associando billing account"
    gcloud beta billing projects link $ProjectId --billing-account $BillingAccount
}

Write-Step "Configurando projeto padrão"
gcloud config set project $ProjectId | Out-Null

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
gcloud services enable $apis

Write-Step "Criando service accounts"
try {
    gcloud iam service-accounts describe $GithubDeploySaEmail | Out-Null
    Write-Host "Service account já existe: $GithubDeploySaEmail"
} catch {
    gcloud iam service-accounts create $GithubDeploySa `
        --display-name "GitHub Actions Deployer"
}

try {
    gcloud iam service-accounts describe $RuntimeSaEmail | Out-Null
    Write-Host "Service account já existe: $RuntimeSaEmail"
} catch {
    gcloud iam service-accounts create $RuntimeSa `
        --display-name "TekAttend Runtime"
}

Write-Step "Concedendo papéis ao deployer"
$roles = @(
    "roles/run.admin",
    "roles/iam.serviceAccountUser",
    "roles/iam.workloadIdentityUser",
    "roles/artifactregistry.writer",
    "roles/storage.admin",
    "roles/secretmanager.admin",
    "roles/datastore.user",
    "roles/serviceusage.serviceUsageConsumer"
)
foreach ($role in $roles) {
    gcloud projects add-iam-policy-binding $ProjectId `
        --member="serviceAccount:$GithubDeploySaEmail" `
        --role=$role | Out-Null
}

Write-Step "Concedendo papéis ao runtime"
$runtimeRoles = @(
    "roles/datastore.user",
    "roles/secretmanager.secretAccessor",
    "roles/storage.objectAdmin"
)
foreach ($role in $runtimeRoles) {
    gcloud projects add-iam-policy-binding $ProjectId `
        --member="serviceAccount:$RuntimeSaEmail" `
        --role=$role | Out-Null
}

Write-Step "Criando Artifact Registry"
try {
    gcloud artifacts repositories describe $ArtifactRepoName --location=$Location | Out-Null
    Write-Host "Artifact Registry já existe: $ArtifactRepoName"
} catch {
    gcloud artifacts repositories create $ArtifactRepoName `
        --repository-format=docker `
        --location=$Location `
        --description="Docker images do TekAttend"
}

Write-Step "Criando buckets"
try {
    gcloud storage buckets describe "gs://$AssetsBucket" | Out-Null
    Write-Host "Bucket já existe: $AssetsBucket"
} catch {
    gcloud storage buckets create "gs://$AssetsBucket" --location=$Location --uniform-bucket-level-access
}

try {
    gcloud storage buckets describe "gs://$ExportsBucket" | Out-Null
    Write-Host "Bucket já existe: $ExportsBucket"
} catch {
    gcloud storage buckets create "gs://$ExportsBucket" --location=$Location --uniform-bucket-level-access
}

Write-Step "Criando secrets iniciais"
foreach ($secretName in $Secrets) {
    try {
        gcloud secrets describe $secretName | Out-Null
        Write-Host "Secret já existe: $secretName"
    } catch {
        gcloud secrets create $secretName --replication-policy="automatic" | Out-Null
        Write-Host "Secret criado: $secretName"
    }
}

Write-Step "Criando Workload Identity Pool"
try {
    gcloud iam workload-identity-pools describe $WifPoolId `
        --project=$ProjectNumber `
        --location="global" | Out-Null
    Write-Host "Workload Identity Pool já existe: $WifPoolId"
} catch {
    gcloud iam workload-identity-pools create $WifPoolId `
        --project=$ProjectNumber `
        --location="global" `
        --display-name="GitHub Actions Pool"
}

Write-Step "Criando Workload Identity Provider"
try {
    gcloud iam workload-identity-pools providers describe $WifProviderId `
        --project=$ProjectNumber `
        --location="global" `
        --workload-identity-pool=$WifPoolId | Out-Null
    Write-Host "Provider já existe: $WifProviderId"
} catch {
    gcloud iam workload-identity-pools providers create-oidc $WifProviderId `
        --project=$ProjectNumber `
        --location="global" `
        --workload-identity-pool=$WifPoolId `
        --display-name="GitHub Provider" `
        --issuer-uri="https://token.actions.githubusercontent.com" `
        --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner,attribute.ref=assertion.ref" `
        --attribute-condition="assertion.repository=='$RepoFull'"
}

Write-Step "Permitindo que o GitHub use a service account deployer"
gcloud iam service-accounts add-iam-policy-binding $GithubDeploySaEmail `
    --role="roles/iam.workloadIdentityUser" `
    --member="principalSet://iam.googleapis.com/$WorkloadIdentityPoolResource/attribute.repository/$RepoFull" | Out-Null

if ($CreateGithubVariables) {
    Ensure-Command gh
    Write-Step "Gravando GitHub Variables no repositório"
    gh variable set GCP_PROJECT_ID --repo $RepoFull --body $ProjectId
    gh variable set GCP_PROJECT_NUMBER --repo $RepoFull --body $ProjectNumber
    gh variable set GCP_REGION --repo $RepoFull --body $Region
    gh variable set GCP_ARTIFACT_REGISTRY --repo $RepoFull --body $ArtifactRepoName
    gh variable set GCP_WIF_PROVIDER --repo $RepoFull --body $WorkloadIdentityProviderResource
    gh variable set GCP_DEPLOYER_SA --repo $RepoFull --body $GithubDeploySaEmail
    gh variable set GCP_RUNTIME_SA --repo $RepoFull --body $RuntimeSaEmail
    gh variable set GCP_ASSETS_BUCKET --repo $RepoFull --body $AssetsBucket
    gh variable set GCP_EXPORTS_BUCKET --repo $RepoFull --body $ExportsBucket
    gh variable set CLOUD_RUN_SERVICE --repo $RepoFull --body $CloudRunService
    gh variable set DOCKER_IMAGE_NAME --repo $RepoFull --body $ImageName
    gh variable set APP_DOMAIN --repo $RepoFull --body "www.tekattend.tekforge.com.br"
    gh variable set API_DOMAIN --repo $RepoFull --body "api.tekattend.tekforge.com.br"
    gh variable set FIRESTORE_DATABASE --repo $RepoFull --body "(default)"
}

Write-Step "Bootstrap concluído"
Write-Host "Projeto: $ProjectId"
Write-Host "Repo GitHub: $RepoFull"
Write-Host "WIF Provider: $WorkloadIdentityProviderResource"
Write-Host "Deployer SA: $GithubDeploySaEmail"
Write-Host "Runtime SA: $RuntimeSaEmail"
Write-Host "Buckets: gs://$AssetsBucket | gs://$ExportsBucket"
Write-Host ""
Write-Host "Próximos passos sugeridos:"
Write-Host "1. Criar versões para os secrets:"
Write-Host "   echo 'SEU_JWT_AQUI' | gcloud secrets versions add tekattend-jwt-secret --data-file=-"
Write-Host "   echo 'SENHA_ADMIN_INICIAL' | gcloud secrets versions add tekattend-admin-bootstrap-password --data-file=-"
Write-Host "2. Confirmar se as GitHub Variables foram criadas."
Write-Host "3. Fazer o primeiro push das workflows."
