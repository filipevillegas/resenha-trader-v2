# 🏗️ ARQUITETURA ATUAL - Resenha Trader v2

**Versão:** 2.0  
**Data:** 16/10/2025  
**Status:** Produção (MVP Funcional)

---

## 📊 VISÃO GERAL DO SISTEMA
```
┌─────────────────────────────────────────────────────────┐
│                    RESENHA TRADER v2                    │
│                                                         │
│  [GitHub Actions] → [Railway API] → [Frontend Web]     │
│         ↓               ↓                  ↓            │
│    Automação        Cache             Dashboard         │
│    (Coleta)        (Dados)           (Visualização)     │
└─────────────────────────────────────────────────────────┘
```

---

## 🗂️ ESTRUTURA DE DIRETÓRIOS
```
resenha-trader-v2/
├── backend/                    # API FastAPI
│   ├── main.py                 # Entry point da aplicação
│   ├── modules/                # Módulos da aplicação
│   │   ├── sinais_trading/     # Módulo de sinais técnicos
│   │   │   ├── __init__.py     # Cache + exports
│   │   │   └── routes.py       # Endpoints FastAPI
│   │   └── assimetria/         # Módulo de Z-Score
│   │       ├── __init__.py     # Cache + exports
│   │       ├── models.py       # Modelos Pydantic
│   │       └── routes.py       # Endpoints FastAPI
│   └── __pycache__/            # Cache Python (ignorar)
│
├── frontend/                   # Interface Web
│   └── public/                 # Arquivos públicos
│       ├── index.html          # Landing page (legado)
│       └── dashboard.html      # Dashboard principal (SPA)
│
├── venv/                       # Ambiente virtual Python
├── .git/                       # Controle de versão
├── .gitignore                  # Arquivos ignorados
├── Procfile                    # Config Railway (deploy)
├── railway.json                # Config Railway (deploy)
├── requirements.txt            # Dependências Python
│
├── ESTADO_ATUAL.md             # Estado e tarefas atuais
├── PROGRESSO.md                # Histórico do projeto
├── PROXIMOS_PASSOS.md          # Roadmap futuro
└── ARQUITETURA_ATUAL.md        # Este arquivo
```

---

## 🔧 TECNOLOGIAS E STACK

### **Backend**
- **Framework:** FastAPI 0.104+
- **Linguagem:** Python 3.11+
- **Deploy:** Railway (PaaS)
- **CORS:** Habilitado para todos domínios
- **Docs:** Swagger UI automático (`/docs`)

### **Frontend**
- **HTML5** - Estrutura
- **Tailwind CSS** (via CDN) - Estilização
- **Vanilla JavaScript** - Lógica
- **Chart.js** (via CDN) - Gráficos
- **Font Awesome** (via CDN) - Ícones
- **Arquitetura:** SPA (Single Page Application)

### **Automação**
- **GitHub Actions** - CI/CD
- **Python 3.11** - Script de coleta
- **yfinance** - Dados financeiros
- **pandas/numpy** - Processamento

### **Deploy**
- **Railway** - Backend API
- **Neocities** - Frontend estático (legado)

---

## 🌐 FLUXO DE DADOS

### **1. Coleta Automática (GitHub Actions)**
```
┌─────────────────────────────────────────┐
│     GitHub Actions (resenha-trader)     │
│                                         │
│  Cron: Segunda a Sexta, 05h UTC-3      │
└─────────────────┬───────────────────────┘
                  ↓
        ┌─────────────────┐
        │ resenha-trader.py│
        └─────────┬─────────┘
                  ↓
    ┌─────────────────────────┐
    │  Download via yfinance  │
    │  (377 ativos)           │
    └────────┬────────────────┘
             ↓
    ┌────────────────────────────┐
    │  Processamento:            │
    │  ├─ Indicadores técnicos   │
    │  ├─ 5 Setups de Trading    │
    │  └─ Z-Score (Assimetria)   │
    └────────┬───────────────────┘
             ↓
    ┌────────────────────────────┐
    │  Output:                   │
    │  ├─ 39 sinais trading      │
    │  └─ 34 sinais assimetria   │
    └────────┬───────────────────┘
             ↓
    ┌────────────────────────────┐
    │  Upload para:              │
    │  ├─ Neocities (JSON)       │
    │  └─ Railway (POST /upload) │
    └────────────────────────────┘
```

---

### **2. Backend API (Railway)**
```
┌──────────────────────────────────────────┐
│         Railway FastAPI Server           │
│                                          │
│  URL: resenha-trader-v2-production...   │
└───────────────┬──────────────────────────┘
                ↓
        ┌───────────────┐
        │   main.py     │
        │   (FastAPI)   │
        └───────┬───────┘
                ↓
    ┌───────────────────────┐
    │   CORS Middleware     │
    │   (Allow all origins) │
    └───────────┬───────────┘
                ↓
    ┌───────────────────────────────┐
    │   Routers:                    │
    │   ├─ /api/sinais/*            │
    │   └─ /api/assimetria/*        │
    └───────────┬───────────────────┘
                ↓
    ┌───────────────────────────────┐
    │   Cache em Memória:           │
    │   ├─ sinais_cache{}           │
    │   └─ assimetria_cache{}       │
    └───────────────────────────────┘
```

**Endpoints Disponíveis:**

| Método | Rota                               | Descrição                         |
|--------|-----------------------------------|-----------------------------------|
| GET    | `/`                               | Serve frontend (dashboard.html)   |
| GET    | `/api/health`                     | Health check                      |
| GET    | `/api/sinais/`                    | Lista sinais trading              |
| GET    | `/api/sinais/resumo`              | Resumo trading                    |
| POST   | `/api/sinais/upload`              | Recebe dados (GitHub Actions)     |
| GET    | `/api/assimetria/`                | Lista sinais assimetria           |
| GET    | `/api/assimetria/resumo`          | Resumo assimetria                 |
| GET    | `/api/assimetria/ticker/{ticker}` | Busca ticker específico           |
| GET    | `/api/assimetria/oportunidades`   | Filtra por nível                  |
| GET    | `/docs`                           | Swagger UI                        |

---

### **3. Frontend (Dashboard SPA)**
```
┌────────────────────────────────────────┐
│       dashboard.html (SPA)             │
│                                        │
│  Sistema de Navegação via JavaScript  │
└────────────┬───────────────────────────┘
             ↓
    ┌────────────────────┐
    │   Menu Lateral     │
    │   (Navegação)      │
    └────────┬───────────┘
             ↓
    ┌──────────────────────────────┐
    │   Páginas (divs):            │
    │   ├─ #page-home              │
    │   ├─ #page-sinais            │
    │   ├─ #page-assimetria        │
    │   ├─ #page-ciclo             │
    │   └─ #page-blog              │
    └────────┬─────────────────────┘
             ↓
    ┌──────────────────────────────┐
    │   Funções JavaScript:        │
    │   ├─ showPage()              │
    │   ├─ loadSinaisData()        │
    │   ├─ loadAssimetriaData()    │
    │   ├─ renderTable()           │
    │   └─ createChart()           │
    └────────┬─────────────────────┘
             ↓
    ┌──────────────────────────────┐
    │   Fetch API:                 │
    │   ├─ GET /api/sinais/        │
    │   └─ GET /api/assimetria/    │
    └──────────────────────────────┘
```

---

## 🗄️ ESTRUTURA DE DADOS

### **Sinal de Trading**
```json
{
  "ticker": "PETR4",
  "setup": "Larry Williams 9.1",
  "signal": "Compra",
  "score": 85,
  "ultimo": 38.45,
  "gain1": "40.20 (+4.5%)",
  "gain2": "42.10 (+9.5%)",
  "loss1": "37.10 (-3.5%)",
  "loss2": "35.80 (-6.9%)",
  "quality": "BOM",
  "premium": true,
  "tags": ["ALTA", "VOL+", "RSI52", "Ação", "EXP"]
}
```

### **Sinal de Assimetria**
```json
{
  "ticker": "VALE3",
  "valor_atual": 60.86,
  "media_6m": 58.20,
  "z_score": 2.3,
  "volatilidade_anualizada": 0.35,
  "status": "Sobrecomprado",
  "nivel_oportunidade": "Alta"
}
```

### **Cache em Memória**

**sinais_cache:**
```python
{
  "data": "16/10/2025",
  "total": 39,
  "compras": 24,
  "vendas": 15,
  "premium": 4,
  "signals": [...]  # Lista de sinais
}
```

**assimetria_cache:**
```python
{
  "data": "16/10/2025",
  "total": 34,
  "sobrecomprados": 20,
  "sobrevendidos": 14,
  "signals": [...],  # Lista de sinais
  "updated_at": "2025-10-16T05:30:00"
}
```

---

## 🔐 SEGURANÇA E CONFIGURAÇÃO

### **Secrets (GitHub)**
- `NEOCITIES_API_KEY` - Upload para Neocities
- `RAILWAY_API_URL` - URL da API Railway

### **CORS**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restringir em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Rate Limiting**
- GitHub Actions: 1x por dia útil
- yfinance: Respeitado automaticamente
- Railway: Sem limite configurado

---

## 📈 PERFORMANCE

### **Tempos de Execução**
- GitHub Actions completo: ~120 segundos
- Coleta de dados (377 ativos): ~90 segundos
- Processamento de sinais: ~20 segundos
- Upload para Railway: ~2 segundos

### **Uptime**
- Railway API: 99.9%
- GitHub Actions: 100% (execuções bem-sucedidas)

### **Cache**
- Tipo: Memória (dicionários Python)
- Persistência: Até restart do servidor
- Atualização: Via POST do GitHub Actions

---

## 🔄 CICLO DE ATUALIZAÇÃO
```
05:00 (UTC-3) - GitHub Actions dispara
    ↓
05:01 - Download de dados iniciado
    ↓
05:03 - Análise técnica completa
    ↓
05:03 - Cálculo de assimetria completo
    ↓
05:03 - Upload para Railway
    ↓
05:03 - Cache atualizado
    ↓
05:04 - Dashboard exibe novos dados
```

---

## 🐛 PROBLEMAS CONHECIDOS

### **1. Cache Volátil**
**Problema:** Reiniciar servidor = perde dados  
**Solução Temporária:** Re-executar GitHub Actions  
**Solução Futura:** Banco de dados persistente

### **2. CORS Permissivo**
**Problema:** `allow_origins=["*"]` aceita todos  
**Risco:** Baixo (API pública)  
**Solução Futura:** Restringir domínios específicos

### **3. Sem Autenticação**
**Problema:** API aberta para todos  
**Risco:** Baixo (dados públicos)  
**Solução Futura:** JWT tokens

### **4. Responsividade Mobile Incompleta**
**Problema:** Dashboard não testado em mobile  
**Status:** Em desenvolvimento (Tarefa 6)  
**Solução:** Implementar na fase de polimento

---

## 🔮 ROADMAP TÉCNICO

### **v2.1 - Polimento (Atual)**
- Frontend premium
- Animações e transições
- Responsividade mobile

### **v2.2 - Persistência**
- PostgreSQL/MongoDB
- Histórico de sinais
- Tracking de performance

### **v2.3 - Autenticação**
- Login/cadastro
- JWT tokens
- Perfis de usuário

### **v2.4 - Notificações**
- Email alerts
- Telegram bot
- Push notifications

### **v3.0 - Expansão**
- Ciclo Fundamentalista
- API pública
- Webhooks

---

## 📚 DEPENDÊNCIAS

### **Backend (requirements.txt)**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.4.2
python-multipart==0.0.6
```

### **Frontend (via CDN)**
```
Tailwind CSS 3.3+
Chart.js 4.4+
Font Awesome 6.0+
```

### **Automação (requirements no resenha-trader)**
```
yfinance
pandas
numpy
requests
```

---

## 🔧 COMANDOS ÚTEIS

### **Desenvolvimento Local**
```powershell
# Ativar venv
.\venv\Scripts\Activate

# Rodar servidor
cd backend
uvicorn main:app --reload

# Acessar
http://localhost:8000/dashboard
```

### **Deploy**
```bash
# Commit e push (deploy automático Railway)
git add .
git commit -m "Feature: descrição"
git push origin main
```

### **GitHub Actions**
```bash
# Disparar manualmente
# Ir em: https://github.com/filipevillegas/resenha-trader/actions
# Clicar em "Run workflow"
```

---

## 📊 MONITORAMENTO

### **Logs**
- **Railway:** Dashboard > Deployments > Logs
- **GitHub Actions:** Actions tab > Workflow runs

### **Health Check**
```bash
curl https://resenha-trader-v2-production.up.railway.app/api/health
```

### **Métricas**
- Total de requisições: Não configurado
- Tempo de resposta: ~50-200ms
- Taxa de erro: <1%

---

**Última Atualização:** 16/10/2025  
**Versão da Arquitetura:** 2.0  
**Autor:** Filipe Villegas