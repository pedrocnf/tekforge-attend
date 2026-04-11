# TekAttend bootstrap

Bootstrap inicial do projeto **TekAttend** para o repositório **pedrocnf/tekforge-attend**.

## Valores pré-configurados
- Projeto GCP: `tekforge-attend`
- Número do projeto: `772785199121`
- Billing account: `018CCA-9AF2D4-93B4FA`
- Região padrão: `us-central1`
- Repositório GitHub: `pedrocnf/tekforge-attend`

## Scripts principais
- `scripts/bootstrap/bootstrap-gcp.ps1`
- `scripts/bootstrap/bootstrap-github.ps1`

## Uso rápido

```powershell
./scripts/bootstrap/bootstrap-gcp.ps1 -CreateGithubVariables
```

## O que o bootstrap faz
- ativa APIs
- cria service accounts
- cria Artifact Registry
- cria buckets
- cria secrets
- cria Workload Identity Federation para GitHub Actions
- opcionalmente grava GitHub Variables

## Secrets que ainda precisam de valor
```powershell
echo 'SEU_JWT_AQUI' | gcloud secrets versions add tekattend-jwt-secret --data-file=-
echo 'SENHA_ADMIN_INICIAL' | gcloud secrets versions add tekattend-admin-bootstrap-password --data-file=-
```
