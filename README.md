# TekAttend

Monorepo inicial do **TekAttend by Tekforge**.

## Estrutura
- `backend/` API FastAPI
- `web/` frontend React + Vite
- `infra/` OpenTofu
- `.github/workflows/` CI/CD
- `docs/` documentação funcional e técnica

## Primeiros passos

### Backend
```bash
cd backend
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Web
```bash
cd web
npm install
npm run dev
```

## Deploy
O deploy do backend usa GitHub Actions + Workload Identity Federation + Cloud Run.
