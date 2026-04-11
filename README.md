# TekAttend backend auth patch

## Conteúdo
- signup de aluno
- login JWT
- `/auth/me`
- solicitação de perfil professor
- listagem/aprovação/negação por admin
- bootstrap opcional do primeiro admin

## Variáveis novas
- `JWT_ALGORITHM`
- `JWT_EXPIRE_MINUTES`
- `ADMIN_BOOTSTRAP_USERNAME`
- `ADMIN_BOOTSTRAP_EMAIL`
- `ENABLE_ADMIN_BOOTSTRAP`

## Fluxo sugerido
1. Copiar a pasta `backend/` para o repo
2. Commitar e dar push
3. Esperar deploy
4. Popular secrets/variáveis
5. Fazer bootstrap do admin temporariamente com:
   - `ENABLE_ADMIN_BOOTSTRAP=true`
   - `POST /admin/bootstrap?password=<ADMIN_BOOTSTRAP_PASSWORD>`
6. Desligar bootstrap depois
