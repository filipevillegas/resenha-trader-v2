# 🚀 PRÓXIMOS PASSOS - Resenha Trader v2

**Status:** Pronto para adicionar módulos

## 📋 FALTAM IMPLEMENTAR (OPCIONAL)

### 🧩 Módulo B: Distância da Média

**O que faz:**
- Calcula distância dos ativos em relação às médias móveis (9, 21, 50, 200)
- Identifica oportunidades de entrada/saída
- Mostra ativos esticados (muito acima) ou comprimidos (muito abaixo)

**Estrutura a criar:**
```
backend/modules/distancia_media/
├── __init__.py
└── routes.py
```

**Endpoints a criar:**
- `GET /api/distancia/` → Lista todos os ativos com distâncias
- `GET /api/distancia/oportunidades` → Filtra oportunidades
- `GET /api/distancia/ticker/{ticker}` → Análise individual

**Frontend:**
- Atualizar página "Distância da Média" no dashboard.html
- Adicionar tabela com ativos
- Adicionar filtros (% distância, média escolhida)

**Tempo estimado:** 40-60 minutos

---

### 🧩 Módulo C: Ciclo Fundamentalista

**O que faz:**
- Análise de indicadores fundamentalistas
- Identifica fase do ciclo (acumulação, alta, distribuição, baixa)
- Combina múltiplos indicadores

**Estrutura a criar:**
```
backend/modules/ciclo_fundamentalista/
├── __init__.py
└── routes.py
```

**Endpoints a criar:**
- `GET /api/ciclo/` → Análise geral do mercado
- `GET /api/ciclo/ticker/{ticker}` → Análise individual
- `GET /api/ciclo/fase` → Fase atual do ciclo

**Frontend:**
- Atualizar página "Ciclo Fundamentalista" no dashboard.html
- Adicionar gráficos de ciclo
- Mostrar indicadores fundamentalistas

**Tempo estimado:** 40-60 minutos

---

## ⚠️ IMPORTANTE ANTES DE IMPLEMENTAR

### Para Distância da Média:
1. **Revisar código Python original** (se existir)
2. Testar localmente antes de integrar
3. Definir quais médias usar (9, 21, 50, 200)
4. Definir thresholds (ex: >5% = esticado, <-5% = comprimido)

### Para Ciclo Fundamentalista:
1. **Revisar código Python original** (se existir)
2. Definir indicadores fundamentalistas a usar
3. Definir critérios de cada fase
4. Fonte de dados fundamentalistas (API? Manual?)

---

## 🔄 PROCESSO RECOMENDADO

**Para adicionar qualquer módulo novo:**

1. **Criar estrutura:**
```bash
   mkdir backend/modules/nome_modulo
   touch backend/modules/nome_modulo/__init__.py
   touch backend/modules/nome_modulo/routes.py
```

2. **Implementar lógica em routes.py:**
   - Criar router
   - Adicionar endpoints
   - Testar localmente

3. **Registrar no main.py:**
```python
   from modules.nome_modulo.routes import router as nome_router
   app.include_router(nome_router, prefix="/api/nome", tags=["Nome"])
```

4. **Testar:**
```bash
   cd backend
   uvicorn main:app --reload
   # Acessar: http://localhost:8000/docs
```

5. **Deploy:**
```bash
   git add .
   git commit -m "Add módulo X"
   git push
   railway up
```

---

## 📝 PERGUNTAS PARA PRÓXIMA CONVERSA

**Sobre Distância da Média:**
- [ ] Você já tem código Python deste módulo?
- [ ] Onde está? (repositório antigo? outro arquivo?)
- [ ] Quais médias usar? (9, 21, 50, 200 ou outras?)
- [ ] Como calcular distância? (% ou pontos?)

**Sobre Ciclo Fundamentalista:**
- [ ] Você já tem código Python deste módulo?
- [ ] Quais indicadores usar? (P/L, ROE, Dividend Yield?)
- [ ] De onde vêm os dados fundamentalistas?
- [ ] Como definir as 4 fases do ciclo?

---

## 🎯 ORDEM RECOMENDADA

1. **PRIMEIRO:** Revisar código Python dos módulos (se existir)
2. **DEPOIS:** Adaptar para FastAPI (criar routes.py)
3. **ENTÃO:** Integrar no backend
4. **POR FIM:** Atualizar frontend

**Não implementar sem antes revisar o código!** ✅