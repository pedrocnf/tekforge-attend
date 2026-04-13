# Attend infra compatibility patch

Este patch ajusta o código para a infra que já existe, sem retroceder o modo de deploy.

## Preserva
- projeto GCP: `tekforge-attend`
- buckets: `tekforge-attend-assets`, `tekforge-attend-exports`
- serviço técnico web: `tekattend-web`
- pipeline GitHub Actions atual
- Cloud Run e Artifact Registry atuais

## Nome público
- app público: `Attend`
- web pública: `www.attend.tekforge.com.br`
- api pública: `api.attend.tekforge.com.br`

## Observação
O serviço técnico continua com nomes `tek*` para não quebrar a esteira já montada.
