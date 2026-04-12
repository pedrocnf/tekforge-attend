# TekAttend frontend deploy patch

## Inclui
- `web/Dockerfile`
- `web/.dockerignore`
- workflow `.github/workflows/web-deploy.yml`

## Como usar
1. Copie os arquivos para o repositório.
2. Faça commit e push na `main`.
3. Aguarde a action `web-deploy`.
4. O serviço web será publicado como `tekattend-web` no Cloud Run.
