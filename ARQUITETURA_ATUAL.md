# 🏗️ ARQUITETURA ATUAL - Resenha Trader v2

**Data:** 15/10/2025

## 📂 Estrutura de Diretórios
```
resenha-trader-v2/           (Repositório NOVO)
├── backend/
│   ├── main.py              ← Ponto de entrada da API
│   └── modules/
│       └── sinais_trading/
│           ├── __init__.py
│           └── routes.py    ← Endpoints de sinais
├── frontend/
│   └── public/
│       ├── index.html       ← Dashboard original (integrado com API)
│       └── dashboard.html   ← Dashboard profissional (menu lateral)
├── Procfile                 ← Configuração Railway
├── railway.json             ← Configuração Railway
├── requirements.txt         ← Dependências Python
├── PROGRESSO.md            ← Este histórico
├── PROXIMOS_PASSOS.md      ← Próximas implementações
└── ARQUITETURA_ATUAL.md    ← Este documento
```
```
resenha-trader/              (Repositório ANTIGO)
├── resenha-trader.py        ← Script principal (MODIFICADO)
├── index.html               ← HTML para Neocities
├── data.json
├── requirements.txt
└── .github/workflows/
    └── update.yml           ← GitHub Actions (MODIFICADO)
```

## 🔌 Endpoints da API

**Base URL:** `https://[sua-url].up.railway.app`

### Sistema
- `GET /` → Frontend (index.html)
- `GET /dashboard` → Dashboard profissional
- `GET /api/health` → Health check
- `GET /docs` → Documentação Swagger

### Sinais Trading
- `GET /api/sinais/` → Lista todos os sinais
- `POST /api/sinais/upload` → Recebe sinais do GitHub Actions
- `GET /api/sinais/resumo` → Estatísticas (total, compras, vendas, premium)
- `GET /api/sinais/teste` → Endpoint de teste

## 🔄 Fluxo de Dados

### Produção de Sinais (Diário)
```
1. GitHub Actions dispara (seg-sex 05h)
2. Executa resenha-trader.py
3. Baixa dados de 377 ativos (yfinance)
4. Calcula 5 setups de análise técnica
5. Gera score 0-100 para cada sinal
6. Salva index.html + data.json
7. Upload para Neocities (mantém site atual)
8. POST para Railway API /api/sinais/upload ← NOVO!
```

### Consumo de Sinais
```
1. Usuário acessa frontend
2. Frontend faz GET /api/sinais/
3. API retorna sinais do cache (memória)
4. Frontend renderiza cards e listas
```

## 🧩 Módulos Implementados

### 1. Sinais Trading ✅
**Localização:** `backend/modules/sinais_trading/`

**Responsabilidades:**
- Receber sinais do GitHub Actions
- Armazenar em cache (memória)
- Servir sinais via API
- Calcular estatísticas

**Cache:**
```python
sinais_cache = {
    "data": "DD/MM/YYYY",
    "total": 25,
    "compras": 14,
    "vendas": 11,
    "signals": [...],
    "updated_at": "ISO datetime"
}
```

## 🎨 Frontend

### index.html (Original)
- Dashboard com cards de estatísticas
- Grid de sinais (PETR4, VALE3, etc.)
- Integrado com Railway API
- Design: Tema escuro, gradientes dourados

### dashboard.html (Profissional) ⭐
- **Menu lateral:** 5 páginas navegáveis
- **Páginas:**
  1. Home → Cards de stats + sinais recentes
  2. Sinais Trading → Lista completa com filtros
  3. Distância da Média → Placeholder (TODO)
  4. Ciclo Fundamentalista → Placeholder (TODO)
  5. Blog/Documentação → Guias e explicações
- **Filtros:** Ticker, tipo de sinal, qualidade
- **Design:** Dark premium, animações suaves

## 🔐 Variáveis de Ambiente

**GitHub Secrets (resenha-trader):**
- `NEOCITIES_API_KEY` → Para upload Neocities
- `RAILWAY_API_URL` → URL da API Railway

**Railway (resenha-trader-v2):**
- Nenhuma variável necessária atualmente
- PORT é fornecido automaticamente pelo Railway

## 🚀 Deploy

### Railway
- **Trigger:** Push para `main` branch
- **Build:** Nixpacks (detecta Python automaticamente)
- **Start:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Health check:** GET /api/health

### GitHub Actions (Neocities)
- **Trigger:** Cron (seg-sex 05h) ou manual
- **Executa:** resenha-trader.py
- **Outputs:** index.html, data.json
- **Deploy:** Neocities API + Railway API

## 🧪 Testar Localmente
```bash
# Backend
cd backend
uvicorn main:app --reload
# http://localhost:8000

# Frontend (servir arquivos)
cd frontend/public
python -m http.server 8080
# http://localhost:8080
```

## 📊 Stack Tecnológico

**Backend:**
- Python 3.10
- FastAPI
- Uvicorn
- yfinance (no repo antigo)
- pandas, numpy (no repo antigo)

**Frontend:**
- HTML5
- Tailwind CSS (via CDN)
- Vanilla JavaScript
- Font Awesome icons

**Infraestrutura:**
- Railway (API hosting)
- GitHub Actions (automação)
- Neocities (site estático)

## ⚠️ Pontos de Atenção

### main.py - ORDEM CRÍTICA
```python
# ✅ CORRETO (ordem atual):
# 1. Rotas da API (/api/*)
# 2. Rotas de páginas HTML (/dashboard)
# 3. app.mount("/", StaticFiles) ← POR ÚLTIMO!

# ❌ ERRADO:
# app.mount antes das rotas = 404 em tudo!
```

### Cache de Sinais
- Armazenado em **memória** (não persiste entre restarts)
- TODO futuro: Migrar para banco de dados (PostgreSQL?)

### CORS
- Atualmente: `allow_origins=["*"]` (aberto para todos)
- TODO futuro: Restringir para domínios específicos

## 🔄 Atualizações Futuras Planejadas

1. **Banco de Dados:**
   - PostgreSQL no Railway
   - Histórico de sinais
   - Análise de performance

2. **Autenticação:**
   - Login/registro
   - API keys para acesso

3. **Notificações:**
   - Email quando sinal premium
   - Telegram bot
   - Webhooks

4. **Módulos Adicionais:**
   - Distância da Média
   - Ciclo Fundamentalista
   - Análise de volume
   - Screener personalizado