# ⚽ GolPeão — Bolão Gamificado da Copa do Mundo 2026

> *"O bolão que te faz rei da Copa"*

Sistema de bolão gamificado para a Copa do Mundo FIFA 2026 (EUA / Canadá / México).
Crie um grupo privado, convide amigos e família, apostem em todos os 104 jogos e
disputem o título de **GolPeão** da sua galera.

---

## 🎮 Funcionalidades

- **Bolões privados** com código de convite (6 dígitos)
- **104 jogos** da Copa 2026 pré-carregados com bandeiras e horários
- **Sistema de pontuação gamificado** (placar exato, vencedor, empate, diferença de gols)
- **Achievements / Badges** desbloqueáveis (🔥 Em Chamas, 🎯 Craque do Bolão, 🐙 Polvo...)
- **Sistema de Tiers** (Bronze → Prata → Ouro → Platina → 👑 Lenda)
- **Ranking em tempo real** com feed de atividade
- **Avanço automático de fases** (times se preenchem conforme classificação real)
- **Painel Admin** para inserir resultados reais
- **Interface em Português** com visual gamificado estilo Copa

---

## 🏆 Sistema de Pontuação

| Acerto | Pontos |
|---|---|
| ✅ Vencedor correto | 3 pts |
| 🤝 Empate previsto | 4 pts |
| 📐 Diferença de gols certa (bônus) | +2 pts |
| 🎯 Placar exato | 10 pts |
| 👑 Placar exato em empate | 12 pts |
| 🏅 Classificado correto (mata-mata) | 5 pts |
| 🎯 Placar exato no mata-mata | 15 pts |
| 🏆 Campeão correto | 50 pts |

---

## 🛠️ Tecnologia

- **Backend:** FastAPI + SQLAlchemy + SQLite/PostgreSQL
- **Frontend:** Streamlit (visual gamificado com CSS customizado)
- **Auth:** JWT + bcrypt
- **Bandeiras:** flagcdn.com (gratuito, sem API key)
- **Agendamento:** APScheduler (fechar palpites automático)

---

## 🚀 Instalação

```bash
# 1. Clonar e entrar na pasta
git clone https://github.com/seu-usuario/golpeao.git
cd golpeao

# 2. Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações

# 5. Criar banco e rodar migrações
alembic upgrade head

# 6. Popular banco com dados da Copa 2026
python scripts/seed_db.py

# 7. Criar usuário admin
python scripts/create_admin.py --username admin --password SuaSenha123

# 8. Rodar backend (terminal 1)
uvicorn app.main:app --reload --port 8000

# 9. Rodar frontend (terminal 2)
streamlit run frontend/app.py --server.port 8501
```

Abrir no navegador: **http://localhost:8501**

---

## 📁 Estrutura do Projeto

```
golpeao/
├── CLAUDE.md          # Instruções para o Claude Code
├── README.md
├── requirements.txt
├── .env.example
├── alembic/           # Migrações de banco
├── app/
│   ├── main.py        # FastAPI app
│   ├── models/        # SQLAlchemy models
│   ├── routers/       # Endpoints da API
│   ├── services/      # Lógica de negócio (scoring, bracket, achievements)
│   └── schemas/       # Pydantic schemas
├── data/
│   └── fixtures.py    # 48 times + 104 jogos da Copa 2026
├── scripts/
│   └── seed_db.py     # Popula o banco
└── frontend/
    ├── app.py         # Streamlit entrypoint
    ├── style.css      # CSS gamificado
    ├── components/    # Componentes reutilizáveis
    └── pages/         # Telas do Streamlit
```

---

## 🎯 Regras do Bolão

1. Palpites fecham **5 minutos antes** de cada jogo
2. Cada palpite pode ser editado até fechar
3. **Sem palpite = 0 pontos** (sem penalidade extra)
4. No mata-mata, é obrigatório indicar quem avança
5. Ranking é sempre **por bolão** (grupos privados)
6. Admin insere resultado → sistema recalcula pontos automaticamente

---

## 🏅 Achievements

| Badge | Conquista |
|---|---|
| ⚽ Primeiro Gol | Fez o primeiro palpite |
| 🔥 Em Chamas | 3 acertos de vencedor seguidos |
| 🎯 Craque do Bolão | 5 placares exatos |
| 🐙 Polvo | Acertou todos os jogos de uma rodada |
| 🦅 Águia | Previu eliminação de favorito |
| 👑 Lenda | Placar exato em empate |
| 🎪 Sortudo | Placar exato no jogo de abertura |
| 🏆 O Rei | Acertou o campeão |
| 💯 Centenário | 100 pontos no bolão |
| 👻 Fantasma | Não apostou em 5 jogos seguidos |

---

## 📅 Copa do Mundo 2026

- **Início:** 11 de junho de 2026 (México vs África do Sul)
- **Final:** 19 de julho de 2026 (MetLife Stadium, New Jersey)
- **Times:** 48 seleções
- **Grupos:** 12 grupos (A–L)
- **Jogos:** 104 partidas

---

## 📄 Licença

MIT License — Uso livre para fins pessoais e de grupo.

---

*Desenvolvido com ❤️ e Claude Code — Copa do Mundo 2026 🏆*
