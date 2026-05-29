# GolPeão — Bolão Gamificado da Copa do Mundo 2026
## Instruções para o Claude Code

---

## VISÃO GERAL DO PROJETO

GolPeão é um sistema de bolão gamificado para a Copa do Mundo FIFA 2026 (EUA/Canadá/México).
Grupos de amigos e família criam bolões privados, apostam nos resultados de todos os 104 jogos
e acumulam pontos por acertos. O sistema gamifica a experiência com achievements, badges,
ranking em tempo real, sistema de tiers e um feed de atividade social.

**Público-alvo:** Grupos privados (5–50 pessoas), foco em Brasil.
**Idioma da interface:** Português Brasileiro (pt-BR).

---

## STACK TECNOLÓGICA

```
Backend:   FastAPI 0.111+ | Python 3.11+
ORM:       SQLAlchemy 2.0 (async) + Alembic (migrações)
Banco:     SQLite (desenvolvimento) → PostgreSQL (produção)
Frontend:  Streamlit 1.35+ (com CSS customizado para visual gamificado)
Auth:      JWT (python-jose) + bcrypt (passlib)
Agendamento: APScheduler (fechar palpites antes dos jogos)
Bandeiras: flagcdn.com/{codigo_iso_2}.svg — sem API key, gratuito
Testes:    pytest + pytest-asyncio
```

**NUNCA use:** Flask, Django, SQLite em modo síncrono para produção.

---

## ARQUITETURA DE ARQUIVOS

```
golpeao/
├── CLAUDE.md                     # Este arquivo
├── README.md
├── requirements.txt
├── .env.example
├── alembic.ini
├── alembic/
│   └── versions/
├── app/
│   ├── main.py                   # FastAPI app + routers
│   ├── database.py               # Engine, SessionLocal, Base
│   ├── config.py                 # Settings via pydantic-settings
│   ├── dependencies.py           # get_db, get_current_user
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py               # User, UserProfile
│   │   ├── group.py              # BolaoGroup, GroupMember
│   │   ├── match.py              # Match, Team, Stage
│   │   ├── prediction.py         # Prediction
│   │   └── achievement.py        # Achievement, UserAchievement
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py               # POST /auth/register, /auth/login
│   │   ├── groups.py             # CRUD de bolões + convites
│   │   ├── matches.py            # GET jogos por fase/grupo
│   │   ├── predictions.py        # POST/GET palpites
│   │   ├── ranking.py            # GET ranking do bolão
│   │   └── admin.py              # POST resultado real (protegido)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── scoring.py            # Motor de pontuação (CRÍTICO)
│   │   ├── bracket.py            # Avanço de fases, habilita jogos
│   │   ├── achievements.py       # Verificação e unlock de badges
│   │   └── notifications.py      # Feed de atividade
│   └── schemas/
│       ├── __init__.py
│       ├── auth.py
│       ├── group.py
│       ├── match.py
│       ├── prediction.py
│       └── ranking.py
├── data/
│   ├── teams.py                  # 48 seleções com códigos ISO
│   ├── groups.py                 # 12 grupos A–L com seleções
│   └── fixtures.py               # 104 jogos da Copa 2026
├── scripts/
│   ├── seed_db.py                # Popula banco com times e jogos
│   └── create_admin.py           # Cria usuário admin
└── frontend/
    ├── app.py                    # Streamlit entrypoint
    ├── style.css                 # CSS gamificado
    ├── components/
    │   ├── match_card.py         # Card de jogo com bandeiras
    │   ├── ranking_table.py      # Tabela de ranking animada
    │   ├── achievement_badge.py  # Badge de conquista
    │   ├── prediction_form.py    # Formulário de palpite
    │   └── bracket_view.py       # Visualização do chaveamento
    └── pages/
        ├── 1_🏠_Inicio.py
        ├── 2_⚽_Jogos.py
        ├── 3_🎯_Meus_Palpites.py
        ├── 4_🏆_Ranking.py
        ├── 5_🏅_Conquistas.py
        ├── 6_🔢_Chaveamento.py
        └── 7_⚙️_Admin.py
```

---

## MODELOS DE DADOS (SQLAlchemy)

### User
```python
id: int (PK)
username: str (unique)
email: str (unique)
password_hash: str
display_name: str
avatar_emoji: str (default: "⚽")  # escolhido no cadastro
tier: str (default: "bronze")       # bronze/silver/gold/platinum/legend
total_points: int (default: 0)
created_at: datetime
is_admin: bool (default: False)
```

### Team
```python
id: int (PK)
name: str                    # "Brasil"
name_en: str                 # "Brazil"
iso_code: str                # "br" (para flagcdn.com)
group_name: str              # "A", "B", ..., "L"
flag_url: str                # gerado: f"https://flagcdn.com/64x48/{iso_code}.png"
confederation: str           # "CONMEBOL", "UEFA", etc.
```

### Match
```python
id: int (PK)
match_number: int            # 1 a 104
home_team_id: int (FK)       # NULL em fases avançadas até definição
away_team_id: int (FK)
stage: str                   # "group", "round32", "round16", "qf", "sf", "third", "final"
group_name: str              # "A"..."L" (NULL para mata-mata)
venue: str                   # "Estádio Azteca, Cidade do México"
scheduled_at: datetime       # horário UTC
is_locked: bool              # True quando palpites fecham (5min antes)
is_played: bool              # True quando resultado inserido
home_score: int              # NULL até jogar
away_score: int
home_score_et: int           # prorrogação
away_score_et: int
winner_team_id: int (FK)     # vencedor (inclui pênaltis)
match_label: str             # "Vencedor Grupo A vs 2º Grupo B" (mata-mata)
```

### Prediction
```python
id: int (PK)
user_id: int (FK)
match_id: int (FK)
bolao_group_id: int (FK)
home_score: int              # palpite do placar casa
away_score: int              # palpite do placar visitante
predicted_winner_id: int (FK)  # obrigatório em mata-mata
points_earned: int           # calculado após jogo
is_exact: bool               # acertou placar exato?
is_winner_correct: bool      # acertou o vencedor?
created_at: datetime
updated_at: datetime
# CONSTRAINT: unique(user_id, match_id, bolao_group_id)
```

### BolaoGroup
```python
id: int (PK)
name: str                    # "Família Pereira"
invite_code: str (unique)    # 6 chars alfanumérico gerado
owner_id: int (FK)
is_active: bool
created_at: datetime
members: relationship → GroupMember
```

### Achievement
```python
id: int (PK)
slug: str (unique)           # "em_chamas", "polvo", etc.
name: str                    # "Em Chamas 🔥"
description: str
icon: str                    # emoji
points_bonus: int            # pontos extras ao desbloquear
```

### UserAchievement
```python
id: int (PK)
user_id: int (FK)
achievement_id: int (FK)
bolao_group_id: int (FK)
unlocked_at: datetime
```

---

## MOTOR DE PONTUAÇÃO (services/scoring.py)

### Regras de Pontuação

```python
SCORING_RULES = {
    # Fase de Grupos
    "exact_score": 10,           # Placar exato (ex: 2x1 = 2x1) ✨ OURO
    "exact_score_draw": 12,      # Placar exato em empate          👑 LENDA
    "correct_winner": 3,         # Acertou o vencedor              ⚽ OK
    "correct_draw": 4,           # Acertou que seria empate        🤝 BOM
    "correct_goal_diff": 2,      # Diferença de gols correta (+bônus) 📐
    
    # Mata-mata (pontuação maior, tensão maior)
    "ko_exact_score": 15,        # Placar exato em mata-mata       🎯
    "ko_correct_winner": 5,      # Acertou classificado            🏅
    "ko_correct_winner_extra": 8, # Acertou via prorrogação/pênalti (bônus)
    
    # Palpites especiais (feitos antes do torneio)
    "champion_correct": 50,      # Acertou o campeão               🏆
    "top_scorer_correct": 20,    # Acertou artilheiro do torneio   🥇
    "finalist_correct": 15,      # Acertou os dois finalistas      🎭
}
```

### Função de Cálculo

```python
def calculate_points(prediction: Prediction, match: Match) -> dict:
    """
    Retorna dict com:
    - points: int total de pontos
    - breakdown: list de (rule_name, points, description)
    - is_exact: bool
    - is_winner_correct: bool
    """
    points = 0
    breakdown = []
    
    pred_home = prediction.home_score
    pred_away = prediction.away_score
    real_home = match.home_score
    real_away = match.away_score
    
    is_group = match.stage == "group"
    
    # 1. Placar exato
    if pred_home == real_home and pred_away == real_away:
        if pred_home == pred_away:  # empate exato
            rule = "exact_score_draw" if is_group else "ko_exact_score"
        else:
            rule = "exact_score" if is_group else "ko_exact_score"
        pts = SCORING_RULES[rule]
        points += pts
        breakdown.append((rule, pts, "Placar exato! 🎯"))
        return {"points": points, "breakdown": breakdown, 
                "is_exact": True, "is_winner_correct": True}
    
    # 2. Acertou vencedor (sem placar exato)
    pred_result = "H" if pred_home > pred_away else ("A" if pred_away > pred_home else "D")
    real_result = "H" if real_home > real_away else ("A" if real_away > real_home else "D")
    
    if pred_result == real_result:
        if real_result == "D" and is_group:
            pts = SCORING_RULES["correct_draw"]
            breakdown.append(("correct_draw", pts, "Acertou o empate 🤝"))
        elif real_result != "D":
            rule = "correct_winner" if is_group else "ko_correct_winner"
            pts = SCORING_RULES[rule]
            breakdown.append((rule, pts, "Acertou o vencedor ⚽"))
        points += pts
        
        # Bônus: diferença de gols correta
        if abs(pred_home - pred_away) == abs(real_home - real_away):
            pts_diff = SCORING_RULES["correct_goal_diff"]
            points += pts_diff
            breakdown.append(("correct_goal_diff", pts_diff, "Diferença de gols exata 📐"))
    
    return {
        "points": points, 
        "breakdown": breakdown,
        "is_exact": False,
        "is_winner_correct": pred_result == real_result
    }
```

---

## SISTEMA DE ACHIEVEMENTS (services/achievements.py)

```python
ACHIEVEMENTS = [
    {
        "slug": "primeiro_gol",
        "name": "Primeiro Gol ⚽",
        "description": "Fez seu primeiro palpite",
        "icon": "⚽",
        "points_bonus": 5,
        "check": lambda stats: stats["total_predictions"] >= 1,
    },
    {
        "slug": "em_chamas",
        "name": "Em Chamas 🔥",
        "description": "3 acertos de vencedor consecutivos",
        "icon": "🔥",
        "points_bonus": 15,
        "check": lambda stats: stats["consecutive_winner_hits"] >= 3,
    },
    {
        "slug": "craque_do_bolao",
        "name": "Craque do Bolão 🎯",
        "description": "5 placares exatos no torneio",
        "icon": "🎯",
        "points_bonus": 25,
        "check": lambda stats: stats["exact_scores"] >= 5,
    },
    {
        "slug": "polvo",
        "name": "Polvo 🐙",
        "description": "Acertou todos os jogos de uma rodada",
        "icon": "🐙",
        "points_bonus": 30,
        "check": lambda stats: stats["perfect_round"] is True,
    },
    {
        "slug": "aguia",
        "name": "Águia 🦅",
        "description": "Previu eliminação de um dos 5 favoritos",
        "icon": "🦅",
        "points_bonus": 20,
        "check": lambda stats: stats["upset_predicted"] is True,
    },
    {
        "slug": "lenda",
        "name": "Lenda 👑",
        "description": "Acertou placar exato de empate",
        "icon": "👑",
        "points_bonus": 10,
        "check": lambda stats: stats["exact_draw_score"] is True,
    },
    {
        "slug": "sortudo",
        "name": "Sortudo 🎪",
        "description": "Placar exato no jogo de abertura",
        "icon": "🎪",
        "points_bonus": 15,
        "check": lambda stats: stats["opening_match_exact"] is True,
    },
    {
        "slug": "fantasma",
        "name": "Fantasma 👻",
        "description": "Não apostou em 5 jogos seguidos (cuidado!)",
        "icon": "👻",
        "points_bonus": 0,
        "check": lambda stats: stats["missed_predictions"] >= 5,
    },
    {
        "slug": "rei",
        "name": "O Rei 🏆",
        "description": "Acertou o campeão da Copa",
        "icon": "🏆",
        "points_bonus": 50,
        "check": lambda stats: stats["champion_correct"] is True,
    },
    {
        "slug": "100pts",
        "name": "Centenário 💯",
        "description": "Atingiu 100 pontos no bolão",
        "icon": "💯",
        "points_bonus": 20,
        "check": lambda stats: stats["total_points"] >= 100,
    },
]
```

---

## SISTEMA DE TIERS

```python
TIERS = [
    {"name": "Bronze",   "min_points": 0,    "icon": "🥉", "color": "#CD7F32"},
    {"name": "Prata",    "min_points": 50,   "icon": "🥈", "color": "#C0C0C0"},
    {"name": "Ouro",     "min_points": 150,  "icon": "🥇", "color": "#FFD700"},
    {"name": "Platina",  "min_points": 300,  "icon": "💎", "color": "#E5E4E2"},
    {"name": "Lenda",    "min_points": 500,  "icon": "👑", "color": "#FF6B35"},
]

def get_tier(points: int) -> dict:
    for tier in reversed(TIERS):
        if points >= tier["min_points"]:
            return tier
    return TIERS[0]
```

---

## BRACKET ENGINE (services/bracket.py)

### Lógica de Avanço de Fases

```python
def advance_group_stage(db: Session):
    """
    Após todos os jogos de grupos:
    1. Calcula classificação de cada grupo (A–L)
    2. Identifica os 8 melhores 3os colocados
    3. Cria/atualiza os matches do Round of 32 com os times classificados
    4. Desbloqueia palpites para o Round of 32
    """

def advance_knockout_round(db: Session, stage: str):
    """
    Após completar um round knockout:
    1. Identifica vencedores dos jogos da fase
    2. Popula home_team/away_team nos jogos da próxima fase
    3. Atualiza match_label (ex: "Brasil vs Argentina")
    4. Desbloqueia palpites da próxima fase
    5. Dispara notificação no feed de atividade
    """

STAGE_ORDER = ["group", "round32", "round16", "qf", "sf", "third", "final"]

BRACKET_MATCHUPS_ROUND32 = [
    # (match_number, "Vencedor Grupo X", "2º Grupo Y")
    (73, "1A", "2B"),
    (74, "1E", "3ABCDF"),
    (75, "1F", "2C"),
    (76, "1C", "2F"),
    (77, "1I", "3CDFGH"),
    (78, "2E", "2I"),
    (79, "1A_host", "3CEFHI"),  # Azteca
    (80, "1L", "3EHIJK"),
    (81, "1D", "3BEFIJ"),
    (82, "1G", "3AEHIJ"),
    (83, "2K", "2L"),
    (84, "1H", "2J"),
    (85, "1B", "3EFGIJ"),
    (86, "1J", "2H"),
    (87, "1K", "3DEIJL"),
    (88, "2D", "2G"),
]
```

---

## FRONTEND STREAMLIT (frontend/app.py)

### Configuração Base

```python
import streamlit as st

st.set_page_config(
    page_title="GolPeão ⚽",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Carregar CSS gamificado
with open("frontend/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
```

### CSS Gamificado (frontend/style.css)

```css
/* Paleta Copa do Mundo */
:root {
    --copa-green: #0A5C36;
    --copa-gold: #FFD700;
    --copa-dark: #020F2A;
    --copa-red: #FF2A00;
    --copa-white: #FFFFFF;
    --tier-bronze: #CD7F32;
    --tier-silver: #C0C0C0;
    --tier-gold: #FFD700;
    --tier-platinum: #E5E4E2;
    --tier-legend: #FF6B35;
}

/* Background principal */
.stApp {
    background: linear-gradient(135deg, var(--copa-dark) 0%, #0D1B2A 100%);
    color: var(--copa-white);
}

/* Cards de jogos */
.match-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,215,0,0.2);
    border-radius: 16px;
    padding: 20px;
    margin: 10px 0;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.match-card:hover {
    border-color: var(--copa-gold);
    box-shadow: 0 0 20px rgba(255,215,0,0.3);
    transform: translateY(-2px);
}

/* Bandeiras */
.flag-img {
    width: 64px;
    height: 48px;
    border-radius: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
}

/* Ranking */
.rank-1 { color: var(--copa-gold); font-size: 1.4em; }
.rank-2 { color: var(--tier-silver); font-size: 1.2em; }
.rank-3 { color: var(--tier-bronze); font-size: 1.1em; }

/* Badges de achievement */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.85em;
    font-weight: bold;
    margin: 2px;
}

.badge-unlocked {
    background: linear-gradient(135deg, var(--copa-gold), #FF8C00);
    color: var(--copa-dark);
}

.badge-locked {
    background: rgba(255,255,255,0.1);
    color: rgba(255,255,255,0.3);
}

/* Tier badges */
.tier-bronze   { background: linear-gradient(135deg, #CD7F32, #8B4513); color: white; }
.tier-silver   { background: linear-gradient(135deg, #C0C0C0, #808080); color: white; }
.tier-gold     { background: linear-gradient(135deg, #FFD700, #FF8C00); color: #020F2A; }
.tier-platinum { background: linear-gradient(135deg, #E5E4E2, #BCC0C4); color: #020F2A; }
.tier-legend   { background: linear-gradient(135deg, #FF6B35, #FF2A00); color: white; }

/* Feed de atividade */
.activity-item {
    padding: 8px 12px;
    border-left: 3px solid var(--copa-gold);
    margin: 6px 0;
    background: rgba(255,215,0,0.05);
    border-radius: 0 8px 8px 0;
    font-size: 0.9em;
}

/* Countdown */
.countdown {
    font-size: 2em;
    font-weight: 900;
    color: var(--copa-gold);
    text-align: center;
    letter-spacing: 4px;
    font-family: monospace;
}

/* Score input */
.score-input {
    font-size: 2em;
    text-align: center;
    width: 60px;
    background: rgba(255,255,255,0.1);
    border: 2px solid var(--copa-gold);
    border-radius: 8px;
    color: white;
}

/* Botão principal */
.stButton > button {
    background: linear-gradient(135deg, var(--copa-green), #0D7A4A) !important;
    color: white !important;
    border: 2px solid var(--copa-gold) !important;
    border-radius: 12px !important;
    font-weight: bold !important;
    transition: all 0.3s !important;
}

.stButton > button:hover {
    box-shadow: 0 0 15px rgba(255,215,0,0.5) !important;
    transform: translateY(-1px) !important;
}

/* Barra de XP */
.xp-bar-bg {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    height: 12px;
    overflow: hidden;
}

.xp-bar-fill {
    background: linear-gradient(90deg, var(--copa-gold), #FF8C00);
    height: 100%;
    border-radius: 10px;
    transition: width 1s ease;
}
```

### Tela de Palpites (components/prediction_form.py)

```python
def render_match_card(match: dict, existing_prediction: dict = None):
    """
    Renderiza card de jogo com:
    - Bandeiras dos times (flagcdn.com)
    - Input de placar (dois números)
    - Countdown até fechar palpites
    - Indicador se jogo está bloqueado
    - Resultado real (se já jogou)
    """
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.markdown(f"""
        <div style="text-align:center">
            <img src="https://flagcdn.com/64x48/{match['home_iso']}.png" 
                 class="flag-img"><br>
            <b>{match['home_name']}</b>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if match['is_played']:
            st.markdown(f"<h2 style='text-align:center;color:#FFD700'>"
                       f"{match['home_score']} × {match['away_score']}</h2>", 
                       unsafe_allow_html=True)
        elif match['is_locked']:
            st.markdown("<p style='text-align:center'>🔒 Fechado</p>", 
                       unsafe_allow_html=True)
        else:
            home_pred = st.number_input("", min_value=0, max_value=20,
                                         value=existing_prediction.get('home_score', 0),
                                         key=f"home_{match['id']}")
            st.markdown("<h3 style='text-align:center'>×</h3>", 
                       unsafe_allow_html=True)
            away_pred = st.number_input("", min_value=0, max_value=20,
                                         value=existing_prediction.get('away_score', 0),
                                         key=f"away_{match['id']}")
    
    with col3:
        st.markdown(f"""
        <div style="text-align:center">
            <img src="https://flagcdn.com/64x48/{match['away_iso']}.png" 
                 class="flag-img"><br>
            <b>{match['away_name']}</b>
        </div>
        """, unsafe_allow_html=True)
```

---

## ROTAS DA API

```
# Auth
POST   /auth/register          Body: {username, email, password, display_name}
POST   /auth/login             Body: {username, password} → {access_token}
GET    /auth/me                → UserProfile

# Bolões
POST   /groups/                Criar bolão → {invite_code}
POST   /groups/join            Body: {invite_code} → entrar no bolão
GET    /groups/{id}            Detalhes do bolão
GET    /groups/{id}/members    Lista de membros

# Jogos
GET    /matches/               Query: stage=group&group=A
GET    /matches/{id}           Detalhes do jogo
GET    /matches/upcoming       Próximos 5 jogos

# Palpites
POST   /predictions/           Body: {match_id, bolao_group_id, home_score, away_score}
GET    /predictions/           Query: bolao_group_id&match_id
PUT    /predictions/{id}       Atualizar palpite (se não bloqueado)

# Ranking
GET    /ranking/{bolao_group_id}         Ranking completo do bolão
GET    /ranking/{bolao_group_id}/stats   Estatísticas detalhadas

# Admin (requer is_admin=True)
POST   /admin/matches/{id}/result        Body: {home_score, away_score}
POST   /admin/advance-stage             Body: {from_stage}
GET    /admin/matches/pending-results   Jogos sem resultado
```

---

## SEED DE DADOS (data/fixtures.py)

### Times (48 seleções com ISO 2 para bandeiras)

```python
# Formato: (name_pt, name_en, iso_code, group, confederation)
TEAMS = [
    # GRUPO A
    ("México",        "Mexico",       "mx", "A", "CONCACAF"),
    ("Coreia do Sul", "South Korea",  "kr", "A", "AFC"),
    ("África do Sul", "South Africa", "za", "A", "CAF"),
    ("Playoff UEFA D","UEFA PO D",    "xx", "A", "UEFA"),   # a definir
    # GRUPO B
    ("Canadá",        "Canada",       "ca", "B", "CONCACAF"),
    ("Qatar",         "Qatar",        "qa", "B", "AFC"),
    ("Suíça",         "Switzerland",  "ch", "B", "UEFA"),
    ("Playoff UEFA A","UEFA PO A",    "xx", "B", "UEFA"),   # a definir
    # GRUPO C
    ("Argentina",     "Argentina",    "ar", "C", "CONMEBOL"),  # ← VERIFICAR GRUPO FINAL
    # ... continuar para todos os 48
]
```

### IMPORTANTE: Grupos Confirmados até maio/2026

```
Grupo A: México, Coreia do Sul, África do Sul, + 1 UEFA
Grupo B: Canadá, Qatar, Suíça, + 1 UEFA  
Grupo C: Alemanha*, Escócia, + ... (verificar fonte oficial)
Grupo D: EUA, Paraguai, Austrália, + 1 UEFA
Grupo E: Alemanha, Curaçao, Costa do Marfim, Equador
Grupo F: Holanda, Japão, + 1 UEFA, Tunísia
Grupo G: Bélgica, Egito, Irã, Nova Zelândia
Grupo H: Espanha, Cabo Verde, Arábia Saudita, Uruguai
Grupo I: França, Senegal, Noruega, + 1 playoff
Grupo J: Argentina, Argélia, Áustria, Jordânia
Grupo K: Portugal, + ...
Grupo L: Inglaterra, Croácia, + ...

⚠️  AÇÃO OBRIGATÓRIA: Antes de criar o seed, buscar no site da FIFA
    (https://www.fifa.com/pt/tournaments/mens/worldcup/canadamexicousa2026)
    os grupos definitivos com todos os 48 times confirmados.
    Usar a ferramenta web_search/web_fetch para buscar dados atualizados.
```

---

## REGRAS DE NEGÓCIO CRÍTICAS

1. **Palpite fecha 5 minutos antes do kickoff** (`scheduled_at - 5min`)
2. **Um palpite por jogo por usuário por bolão** (unique constraint)
3. **Palpites podem ser editados** até fechar (PUT /predictions/{id})
4. **Mata-mata:** usuário DEVE informar quem passa (além do placar)
5. **Empates em mata-mata:** placar do tempo normal conta para pontuação,
   mas o vencedor (pênaltis/prorrogação) é o que importa para classificação
6. **Sem palpite = 0 pontos** (sem penalidade, mas fica sem badge)
7. **Ranking é por bolão** (não global — privacidade dos grupos)
8. **Admin** insere resultado real → sistema recalcula todos os palpites daquele jogo
9. **Fases desbloqueiam automaticamente** quando admin avança o stage

---

## ORDEM DE DESENVOLVIMENTO (prioridade)

### Sprint 1 — Core (3-4h)
- [ ] database.py + config.py
- [ ] models/user.py + models/match.py + models/prediction.py
- [ ] alembic init + primeira migração
- [ ] scripts/seed_db.py (times + grupos + 104 jogos fase de grupos)
- [ ] routers/auth.py (register + login + JWT)
- [ ] routers/matches.py (GET jogos)
- [ ] routers/predictions.py (POST/GET palpites)
- [ ] services/scoring.py (motor de pontuação)

### Sprint 2 — Grupos e Ranking (2-3h)
- [ ] models/group.py
- [ ] routers/groups.py (criar/entrar bolão)
- [ ] routers/ranking.py
- [ ] services/achievements.py
- [ ] routers/admin.py (inserir resultados)

### Sprint 3 — Frontend Streamlit (3-4h)
- [ ] frontend/app.py + style.css
- [ ] pages/1_Inicio.py (dashboard com próximos jogos + ranking snippet)
- [ ] pages/2_Jogos.py (lista por fase/grupo com bandeiras)
- [ ] pages/3_Meus_Palpites.py (formulário de palpites)
- [ ] pages/4_Ranking.py (tabela gamificada)
- [ ] pages/5_Conquistas.py (badges)

### Sprint 4 — Fases e Polimento (2-3h)
- [ ] services/bracket.py (avanço de fases)
- [ ] pages/6_Chaveamento.py (visualização do bracket)
- [ ] pages/7_Admin.py (painel admin)
- [ ] Testes pytest
- [ ] README.md com instruções de deploy

---

## COMANDOS DE DESENVOLVIMENTO

```bash
# Instalar dependências
pip install -r requirements.txt

# Criar banco e rodar migrações
alembic upgrade head

# Popular banco com dados da Copa
python scripts/seed_db.py

# Criar admin
python scripts/create_admin.py --username admin --password SuaSenha123

# Rodar backend
uvicorn app.main:app --reload --port 8000

# Rodar frontend (outro terminal)
streamlit run frontend/app.py --server.port 8501

# Rodar testes
pytest tests/ -v
```

---

## VARIÁVEIS DE AMBIENTE (.env)

```env
DATABASE_URL=sqlite:///./golpeao.db
SECRET_KEY=sua-chave-secreta-256bits-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ADMIN_SECRET=chave-para-criar-admins
ENVIRONMENT=development
```

---

## REQUISITOS (requirements.txt)

```
fastapi==0.111.0
uvicorn[standard]==0.29.0
sqlalchemy==2.0.30
alembic==1.13.1
pydantic==2.7.1
pydantic-settings==2.2.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
streamlit==1.35.0
requests==2.32.2
apscheduler==3.10.4
pytest==8.2.0
pytest-asyncio==0.23.6
httpx==0.27.0
```

---

## NOTAS FINAIS PARA O CLAUDE CODE

- **Bandeiras:** Sempre usar `https://flagcdn.com/64x48/{iso2}.png` (gratuito, sem key)
- **Timezones:** Armazenar em UTC, exibir em horário de Brasília (UTC-3)
- **ISO codes:** Para times "a definir" (playoffs), usar código `"xx"` e exibir emoji 🌍
- **Seed:** Buscar grupos finais na web antes de criar o seed — alguns ainda não confirmados
- **Streamlit state:** Usar `st.session_state` para auth token e seleção de bolão ativo
- **Segurança:** Nunca retornar password_hash nas respostas da API
- **Paginação:** Rankings com > 20 membros devem ter paginação
- **Mobile:** Streamlit é responsivo por padrão — priorizar layouts em colunas estreitas

---

*GolPeão v1.0 — Copa do Mundo FIFA 2026 🏆*
*Desenvolvido com Claude Code — Anthropic*
