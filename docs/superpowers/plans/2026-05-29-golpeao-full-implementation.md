# GolPeão — Plano de Implementação Completo (Sprints 1–3)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementar o sistema de bolão gamificado GolPeão para a Copa do Mundo 2026 — backend FastAPI + SQLite + frontend Streamlit, com auth JWT, motor de pontuação, achievements e ranking em tempo real.

**Architecture:** Backend FastAPI com SQLAlchemy 2.0 (async-style mas sync para SQLite), Alembic para migrações, seed de 48 times e 104 jogos já estruturado em `data/fixtures.py`. Frontend Streamlit multi-página com CSS gamificado consumindo a API via `requests`.

**Tech Stack:** FastAPI 0.111, SQLAlchemy 2.0, Alembic 1.13, SQLite (dev), python-jose + passlib (JWT/bcrypt), Streamlit 1.35, flagcdn.com (bandeiras gratuitas)

---

## Mapa de Arquivos

### Sprint 1 — Core Backend
| Arquivo | Ação | Responsabilidade |
|---------|------|-----------------|
| `app/config.py` | Criar | Settings via pydantic-settings + .env |
| `app/database.py` | Criar | Engine SQLite, SessionLocal, Base |
| `app/models/user.py` | Criar | User model |
| `app/models/match.py` | Criar | Team + Match models |
| `app/models/prediction.py` | Criar | Prediction model |
| `app/models/__init__.py` | Modificar | Exportar todos os models |
| `app/dependencies.py` | Criar | get_db, get_current_user |
| `app/schemas/auth.py` | Criar | UserCreate, UserLogin, Token |
| `app/schemas/match.py` | Criar | TeamOut, MatchOut |
| `app/schemas/prediction.py` | Criar | PredictionCreate, PredictionOut |
| `app/routers/auth.py` | Criar | POST /auth/register, /auth/login, GET /auth/me |
| `app/routers/matches.py` | Criar | GET /matches/, /matches/{id}, /matches/upcoming |
| `app/routers/predictions.py` | Criar | POST/GET/PUT /predictions/ |
| `app/services/scoring.py` | Criar | Motor de pontuação |
| `app/main.py` | Criar | FastAPI app + routers |
| `alembic/env.py` | Modificar | Conectar ao app.database |
| `alembic.ini` | Criar | Config Alembic |
| `scripts/seed_db.py` | Modificar | Seed real com modelos |
| `scripts/create_admin.py` | Criar | Script de criação de admin |
| `.env` | Criar | Variáveis de ambiente |
| `tests/test_auth.py` | Criar | Testes de auth |
| `tests/test_scoring.py` | Criar | Testes do motor de pontuação |
| `tests/conftest.py` | Criar | Fixtures pytest |

### Sprint 2 — Grupos, Ranking, Achievements, Admin
| Arquivo | Ação | Responsabilidade |
|---------|------|-----------------|
| `app/models/group.py` | Criar | BolaoGroup + GroupMember |
| `app/models/achievement.py` | Criar | Achievement + UserAchievement |
| `app/schemas/group.py` | Criar | GroupCreate, GroupOut, MemberOut |
| `app/schemas/ranking.py` | Criar | RankingEntry, StatsOut |
| `app/routers/groups.py` | Criar | CRUD bolões + convites |
| `app/routers/ranking.py` | Criar | GET ranking + stats |
| `app/routers/admin.py` | Criar | POST resultado real |
| `app/services/achievements.py` | Criar | ACHIEVEMENTS list + check logic |
| `app/services/notifications.py` | Criar | Feed de atividade (in-memory) |
| `tests/test_groups.py` | Criar | Testes de grupos e ranking |

### Sprint 3 — Frontend Streamlit
| Arquivo | Ação | Responsabilidade |
|---------|------|-----------------|
| `frontend/app.py` | Criar | Entrypoint Streamlit + config |
| `frontend/style.css` | Criar | CSS gamificado Copa do Mundo |
| `frontend/api_client.py` | Criar | Wrapper requests para a API |
| `frontend/components/match_card.py` | Criar | Card de jogo com bandeiras |
| `frontend/components/ranking_table.py` | Criar | Tabela de ranking |
| `frontend/components/achievement_badge.py` | Criar | Badge de conquista |
| `frontend/components/prediction_form.py` | Criar | Formulário de palpite |
| `frontend/pages/1_🏠_Inicio.py` | Criar | Dashboard inicial |
| `frontend/pages/2_⚽_Jogos.py` | Criar | Lista de jogos |
| `frontend/pages/3_🎯_Meus_Palpites.py` | Criar | Formulário de palpites |
| `frontend/pages/4_🏆_Ranking.py` | Criar | Tabela de ranking |
| `frontend/pages/5_🏅_Conquistas.py` | Criar | Badges de achievement |
| `frontend/pages/7_⚙️_Admin.py` | Criar | Painel admin |

---

## SPRINT 1 — Core Backend

---

### Task 1: Configuração base (config, database, .env)

**Files:**
- Create: `app/config.py`
- Create: `app/database.py`
- Create: `.env`

- [ ] **Step 1: Criar .env**

```env
DATABASE_URL=sqlite:///./golpeao.db
SECRET_KEY=golpeao-secret-key-copa-2026-256bits-mude-em-prod
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ADMIN_SECRET=admin-secret-golpeao
ENVIRONMENT=development
API_BASE_URL=http://localhost:8000
DISPLAY_TIMEZONE=America/Recife
```

- [ ] **Step 2: Criar app/config.py**

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./golpeao.db"
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ADMIN_SECRET: str = "admin-secret"
    ENVIRONMENT: str = "development"
    API_BASE_URL: str = "http://localhost:8000"
    DISPLAY_TIMEZONE: str = "America/Recife"

    model_config = {"env_file": ".env"}


settings = Settings()
```

- [ ] **Step 3: Criar app/database.py**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings

connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
```

- [ ] **Step 4: Instalar dependências**

```bash
pip install -r requirements.txt
```

Esperado: sem erros de instalação.

- [ ] **Step 5: Verificar que config importa**

```bash
python -c "from app.config import settings; print(settings.DATABASE_URL)"
```

Esperado: `sqlite:///./golpeao.db`

---

### Task 2: Models — User, Team, Match

**Files:**
- Create: `app/models/user.py`
- Create: `app/models/match.py`
- Modify: `app/models/__init__.py`

- [ ] **Step 1: Escrever teste para User model**

Criar `tests/conftest.py`:

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import User, Team, Match, Prediction, BolaoGroup, GroupMember, Achievement, UserAchievement


@pytest.fixture(scope="function")
def db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
```

Criar `tests/__init__.py` (vazio).

- [ ] **Step 2: Criar app/models/user.py**

```python
from datetime import datetime
from sqlalchemy import String, Boolean, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    avatar_emoji: Mapped[str] = mapped_column(String(10), default="⚽")
    tier: Mapped[str] = mapped_column(String(20), default="bronze")
    total_points: Mapped[int] = mapped_column(Integer, default=0)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

- [ ] **Step 3: Criar app/models/match.py**

```python
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    iso_code: Mapped[str] = mapped_column(String(10), nullable=False)
    group_name: Mapped[str] = mapped_column(String(5), nullable=False)
    flag_url: Mapped[str] = mapped_column(String(255), nullable=False)
    confederation: Mapped[str] = mapped_column(String(20), nullable=False)


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    match_number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    home_team_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("teams.id"), nullable=True)
    away_team_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("teams.id"), nullable=True)
    stage: Mapped[str] = mapped_column(String(20), nullable=False)  # group/round32/round16/qf/sf/third/final
    group_name: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    venue: Mapped[str] = mapped_column(String(255), nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    is_played: Mapped[bool] = mapped_column(Boolean, default=False)
    home_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    away_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    home_score_et: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    away_score_et: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    winner_team_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("teams.id"), nullable=True)
    match_label: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    home_team: Mapped[Optional["Team"]] = relationship("Team", foreign_keys=[home_team_id])
    away_team: Mapped[Optional["Team"]] = relationship("Team", foreign_keys=[away_team_id])
    winner_team: Mapped[Optional["Team"]] = relationship("Team", foreign_keys=[winner_team_id])
```

- [ ] **Step 4: Criar app/models/prediction.py**

```python
from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, ForeignKey, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Prediction(Base):
    __tablename__ = "predictions"
    __table_args__ = (
        UniqueConstraint("user_id", "match_id", "bolao_group_id", name="uq_prediction"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    match_id: Mapped[int] = mapped_column(Integer, ForeignKey("matches.id"), nullable=False)
    bolao_group_id: Mapped[int] = mapped_column(Integer, ForeignKey("bolao_groups.id"), nullable=False)
    home_score: Mapped[int] = mapped_column(Integer, nullable=False)
    away_score: Mapped[int] = mapped_column(Integer, nullable=False)
    predicted_winner_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("teams.id"), nullable=True)
    points_earned: Mapped[int] = mapped_column(Integer, default=0)
    is_exact: Mapped[bool] = mapped_column(Boolean, default=False)
    is_winner_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

- [ ] **Step 5: Criar app/models/group.py**

```python
from datetime import datetime
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class BolaoGroup(Base):
    __tablename__ = "bolao_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    invite_code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    members: Mapped[list["GroupMember"]] = relationship("GroupMember", back_populates="group")


class GroupMember(Base):
    __tablename__ = "group_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("bolao_groups.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    group: Mapped["BolaoGroup"] = relationship("BolaoGroup", back_populates="members")
    user: Mapped["User"] = relationship("User")
```

- [ ] **Step 6: Criar app/models/achievement.py**

```python
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    icon: Mapped[str] = mapped_column(String(10), nullable=False)
    points_bonus: Mapped[int] = mapped_column(Integer, default=0)


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id: Mapped[int] = mapped_column(Integer, ForeignKey("achievements.id"), nullable=False)
    bolao_group_id: Mapped[int] = mapped_column(Integer, ForeignKey("bolao_groups.id"), nullable=False)
    unlocked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

- [ ] **Step 7: Atualizar app/models/__init__.py**

```python
from app.models.user import User
from app.models.match import Team, Match
from app.models.prediction import Prediction
from app.models.group import BolaoGroup, GroupMember
from app.models.achievement import Achievement, UserAchievement

__all__ = [
    "User", "Team", "Match", "Prediction",
    "BolaoGroup", "GroupMember", "Achievement", "UserAchievement",
]
```

- [ ] **Step 8: Rodar teste de modelos**

```bash
python -c "
from sqlalchemy import create_engine
from app.database import Base
from app.models import User, Team, Match, Prediction, BolaoGroup, GroupMember, Achievement, UserAchievement
engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)
print('Tabelas criadas:', list(Base.metadata.tables.keys()))
"
```

Esperado: lista com 8 tabelas.

---

### Task 3: Alembic — Migrações

**Files:**
- Create: `alembic.ini`
- Modify: `alembic/env.py`

- [ ] **Step 1: Criar alembic.ini**

```ini
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os
sqlalchemy.url = sqlite:///./golpeao.db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

- [ ] **Step 2: Criar alembic/env.py**

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.database import Base
from app.models import User, Team, Match, Prediction, BolaoGroup, GroupMember, Achievement, UserAchievement

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True,
                      dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(config.get_section(config.config_ini_section, {}),
                                     prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

- [ ] **Step 3: Criar alembic/versions/ e script/__init__.py**

```bash
mkdir -p alembic/versions
touch alembic/__init__.py
```

- [ ] **Step 4: Gerar primeira migração**

```bash
alembic revision --autogenerate -m "initial schema"
```

Esperado: arquivo criado em `alembic/versions/`.

- [ ] **Step 5: Aplicar migração**

```bash
alembic upgrade head
```

Esperado: `golpeao.db` criado com todas as tabelas.

---

### Task 4: Motor de Pontuação (TDD)

**Files:**
- Create: `app/services/scoring.py`
- Create: `tests/test_scoring.py`

- [ ] **Step 1: Escrever testes de pontuação**

Criar `tests/test_scoring.py`:

```python
import pytest
from unittest.mock import MagicMock
from app.services.scoring import calculate_points, get_tier, SCORING_RULES


def make_match(home_score, away_score, stage="group", home_score_et=None, away_score_et=None):
    m = MagicMock()
    m.home_score = home_score
    m.away_score = away_score
    m.stage = stage
    m.home_score_et = home_score_et
    m.away_score_et = away_score_et
    return m


def make_prediction(home_score, away_score, predicted_winner_id=None):
    p = MagicMock()
    p.home_score = home_score
    p.away_score = away_score
    p.predicted_winner_id = predicted_winner_id
    return p


def test_exact_score_group():
    result = calculate_points(make_prediction(2, 1), make_match(2, 1, "group"))
    assert result["points"] == SCORING_RULES["exact_score"]
    assert result["is_exact"] is True
    assert result["is_winner_correct"] is True


def test_exact_draw_group():
    result = calculate_points(make_prediction(1, 1), make_match(1, 1, "group"))
    assert result["points"] == SCORING_RULES["exact_score_draw"]
    assert result["is_exact"] is True


def test_correct_winner_group():
    result = calculate_points(make_prediction(3, 0), make_match(2, 0, "group"))
    assert result["points"] == SCORING_RULES["correct_winner"]
    assert result["is_winner_correct"] is True
    assert result["is_exact"] is False


def test_correct_winner_with_goal_diff():
    result = calculate_points(make_prediction(3, 1), make_match(2, 0, "group"))
    assert result["points"] == SCORING_RULES["correct_winner"] + SCORING_RULES["correct_goal_diff"]


def test_correct_draw_group():
    result = calculate_points(make_prediction(0, 0), make_match(1, 1, "group"))
    assert result["points"] == SCORING_RULES["correct_draw"]


def test_wrong_prediction():
    result = calculate_points(make_prediction(2, 0), make_match(0, 1, "group"))
    assert result["points"] == 0
    assert result["is_exact"] is False
    assert result["is_winner_correct"] is False


def test_exact_score_knockout():
    result = calculate_points(make_prediction(1, 0), make_match(1, 0, "qf"))
    assert result["points"] == SCORING_RULES["ko_exact_score"]
    assert result["is_exact"] is True


def test_correct_winner_knockout():
    result = calculate_points(make_prediction(2, 0), make_match(1, 0, "sf"))
    assert result["points"] == SCORING_RULES["ko_correct_winner"]


def test_get_tier_bronze():
    tier = get_tier(0)
    assert tier["name"] == "Bronze"


def test_get_tier_silver():
    tier = get_tier(50)
    assert tier["name"] == "Prata"


def test_get_tier_gold():
    tier = get_tier(150)
    assert tier["name"] == "Ouro"


def test_get_tier_legend():
    tier = get_tier(500)
    assert tier["name"] == "Lenda"
```

- [ ] **Step 2: Rodar testes — verificar falha**

```bash
python -m pytest tests/test_scoring.py -v 2>&1 | head -20
```

Esperado: `ModuleNotFoundError` ou `ImportError`.

- [ ] **Step 3: Criar app/services/scoring.py**

```python
from typing import Optional

SCORING_RULES = {
    "exact_score": 10,
    "exact_score_draw": 12,
    "correct_winner": 3,
    "correct_draw": 4,
    "correct_goal_diff": 2,
    "ko_exact_score": 15,
    "ko_correct_winner": 5,
    "ko_correct_winner_extra": 8,
    "champion_correct": 50,
    "top_scorer_correct": 20,
    "finalist_correct": 15,
}

TIERS = [
    {"name": "Bronze",  "min_points": 0,   "icon": "🥉", "color": "#CD7F32"},
    {"name": "Prata",   "min_points": 50,  "icon": "🥈", "color": "#C0C0C0"},
    {"name": "Ouro",    "min_points": 150, "icon": "🥇", "color": "#FFD700"},
    {"name": "Platina", "min_points": 300, "icon": "💎", "color": "#E5E4E2"},
    {"name": "Lenda",   "min_points": 500, "icon": "👑", "color": "#FF6B35"},
]


def get_tier(points: int) -> dict:
    for tier in reversed(TIERS):
        if points >= tier["min_points"]:
            return tier
    return TIERS[0]


def calculate_points(prediction, match) -> dict:
    points = 0
    breakdown = []

    pred_home = prediction.home_score
    pred_away = prediction.away_score
    real_home = match.home_score
    real_away = match.away_score
    is_group = match.stage == "group"

    # Placar exato
    if pred_home == real_home and pred_away == real_away:
        if pred_home == pred_away and is_group:
            rule = "exact_score_draw"
        else:
            rule = "exact_score" if is_group else "ko_exact_score"
        pts = SCORING_RULES[rule]
        points += pts
        breakdown.append((rule, pts, "Placar exato! 🎯"))
        return {"points": points, "breakdown": breakdown, "is_exact": True, "is_winner_correct": True}

    pred_result = "H" if pred_home > pred_away else ("A" if pred_away > pred_home else "D")
    real_result = "H" if real_home > real_away else ("A" if real_away > real_home else "D")

    if pred_result == real_result:
        if real_result == "D" and is_group:
            pts = SCORING_RULES["correct_draw"]
            breakdown.append(("correct_draw", pts, "Acertou o empate 🤝"))
        else:
            rule = "correct_winner" if is_group else "ko_correct_winner"
            pts = SCORING_RULES[rule]
            breakdown.append((rule, pts, "Acertou o vencedor ⚽"))
        points += pts

        if abs(pred_home - pred_away) == abs(real_home - real_away):
            pts_diff = SCORING_RULES["correct_goal_diff"]
            points += pts_diff
            breakdown.append(("correct_goal_diff", pts_diff, "Diferença de gols exata 📐"))

    return {
        "points": points,
        "breakdown": breakdown,
        "is_exact": False,
        "is_winner_correct": pred_result == real_result,
    }
```

- [ ] **Step 4: Rodar testes — verificar aprovação**

```bash
python -m pytest tests/test_scoring.py -v
```

Esperado: todos os testes passando.

---

### Task 5: Auth — Register, Login, JWT

**Files:**
- Create: `app/schemas/auth.py`
- Create: `app/dependencies.py`
- Create: `app/routers/auth.py`
- Create: `tests/test_auth.py`

- [ ] **Step 1: Criar app/schemas/auth.py**

```python
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    display_name: str
    avatar_emoji: str = "⚽"


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    display_name: str
    avatar_emoji: str
    tier: str
    total_points: int
    is_admin: bool
    created_at: datetime

    model_config = {"from_attributes": True}
```

- [ ] **Step 2: Criar app/dependencies.py**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return current_user
```

- [ ] **Step 3: Criar app/routers/auth.py**

```python
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext

from app.config import settings
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, Token, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": str(user_id), "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@router.post("/register", response_model=UserOut, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(400, "Username já em uso")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email já em uso")
    user = User(
        username=data.username,
        email=data.email,
        password_hash=pwd_context.hash(data.password),
        display_name=data.display_name,
        avatar_emoji=data.avatar_emoji,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not pwd_context.verify(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    return Token(access_token=create_access_token(user.id))


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
```

- [ ] **Step 4: Escrever testes de auth**

Criar `tests/test_auth.py`:

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base
from app.dependencies import get_db


@pytest.fixture(scope="function")
def client():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


def test_register_user(client):
    r = client.post("/auth/register", json={
        "username": "joao", "email": "joao@test.com",
        "password": "senha123", "display_name": "João"
    })
    assert r.status_code == 201
    data = r.json()
    assert data["username"] == "joao"
    assert "password_hash" not in data


def test_register_duplicate_username(client):
    payload = {"username": "joao", "email": "joao@test.com", "password": "senha123", "display_name": "João"}
    client.post("/auth/register", json=payload)
    r = client.post("/auth/register", json={**payload, "email": "outro@test.com"})
    assert r.status_code == 400


def test_login(client):
    client.post("/auth/register", json={
        "username": "joao", "email": "joao@test.com",
        "password": "senha123", "display_name": "João"
    })
    r = client.post("/auth/login", json={"username": "joao", "password": "senha123"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "username": "joao", "email": "joao@test.com",
        "password": "senha123", "display_name": "João"
    })
    r = client.post("/auth/login", json={"username": "joao", "password": "errada"})
    assert r.status_code == 401


def test_me(client):
    client.post("/auth/register", json={
        "username": "joao", "email": "joao@test.com",
        "password": "senha123", "display_name": "João"
    })
    token = client.post("/auth/login", json={"username": "joao", "password": "senha123"}).json()["access_token"]
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["username"] == "joao"
```

---

### Task 6: app/main.py — FastAPI App

**Files:**
- Create: `app/main.py`

- [ ] **Step 1: Criar app/main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth, matches, predictions, groups, ranking, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="GolPeão API", version="1.0.0", description="Bolão Copa do Mundo 2026")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(matches.router)
app.include_router(predictions.router)
app.include_router(groups.router)
app.include_router(ranking.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "GolPeão API ⚽ Copa do Mundo 2026"}
```

- [ ] **Step 2: Criar stubs para os routers faltantes (temporário)**

Criar `app/routers/matches.py` (stub):

```python
from fastapi import APIRouter
router = APIRouter(prefix="/matches", tags=["matches"])
```

Criar `app/routers/predictions.py` (stub):

```python
from fastapi import APIRouter
router = APIRouter(prefix="/predictions", tags=["predictions"])
```

Criar `app/routers/groups.py` (stub):

```python
from fastapi import APIRouter
router = APIRouter(prefix="/groups", tags=["groups"])
```

Criar `app/routers/ranking.py` (stub):

```python
from fastapi import APIRouter
router = APIRouter(prefix="/ranking", tags=["ranking"])
```

Criar `app/routers/admin.py` (stub):

```python
from fastapi import APIRouter
router = APIRouter(prefix="/admin", tags=["admin"])
```

- [ ] **Step 3: Rodar testes de auth**

```bash
python -m pytest tests/test_auth.py -v
```

Esperado: 5 testes passando.

- [ ] **Step 4: Testar API manualmente**

```bash
uvicorn app.main:app --reload --port 8000 &
sleep 3
curl http://localhost:8000/
```

Esperado: `{"message": "GolPeão API ⚽ Copa do Mundo 2026"}`

---

### Task 7: Matches Router

**Files:**
- Create: `app/schemas/match.py`
- Modify: `app/routers/matches.py`

- [ ] **Step 1: Criar app/schemas/match.py**

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TeamOut(BaseModel):
    id: int
    name: str
    name_en: str
    iso_code: str
    group_name: str
    flag_url: str
    confederation: str

    model_config = {"from_attributes": True}


class MatchOut(BaseModel):
    id: int
    match_number: int
    stage: str
    group_name: Optional[str]
    venue: str
    scheduled_at: datetime
    is_locked: bool
    is_played: bool
    home_score: Optional[int]
    away_score: Optional[int]
    match_label: Optional[str]
    home_team: Optional[TeamOut]
    away_team: Optional[TeamOut]

    model_config = {"from_attributes": True}
```

- [ ] **Step 2: Implementar app/routers/matches.py**

```python
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.dependencies import get_db
from app.models.match import Match
from app.schemas.match import MatchOut

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/", response_model=List[MatchOut])
def list_matches(
    stage: Optional[str] = None,
    group: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Match)
    if stage:
        query = query.filter(Match.stage == stage)
    if group:
        query = query.filter(Match.group_name == group)
    return query.order_by(Match.scheduled_at).all()


@router.get("/upcoming", response_model=List[MatchOut])
def upcoming_matches(db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    return (
        db.query(Match)
        .filter(Match.scheduled_at >= now, Match.is_played == False)
        .order_by(Match.scheduled_at)
        .limit(5)
        .all()
    )


@router.get("/{match_id}", response_model=MatchOut)
def get_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(404, "Jogo não encontrado")
    return match
```

---

### Task 8: Predictions Router

**Files:**
- Create: `app/schemas/prediction.py`
- Modify: `app/routers/predictions.py`

- [ ] **Step 1: Criar app/schemas/prediction.py**

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PredictionCreate(BaseModel):
    match_id: int
    bolao_group_id: int
    home_score: int
    away_score: int
    predicted_winner_id: Optional[int] = None


class PredictionOut(BaseModel):
    id: int
    match_id: int
    bolao_group_id: int
    home_score: int
    away_score: int
    predicted_winner_id: Optional[int]
    points_earned: int
    is_exact: bool
    is_winner_correct: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
```

- [ ] **Step 2: Implementar app/routers/predictions.py**

```python
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.match import Match
from app.models.prediction import Prediction
from app.models.group import GroupMember
from app.schemas.prediction import PredictionCreate, PredictionOut

router = APIRouter(prefix="/predictions", tags=["predictions"])


def _check_match_open(match: Match):
    if match.is_locked:
        raise HTTPException(400, "Palpites fechados para este jogo")
    if match.is_played:
        raise HTTPException(400, "Jogo já realizado")


@router.post("/", response_model=PredictionOut, status_code=201)
def create_prediction(
    data: PredictionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    match = db.query(Match).filter(Match.id == data.match_id).first()
    if not match:
        raise HTTPException(404, "Jogo não encontrado")
    _check_match_open(match)

    member = db.query(GroupMember).filter(
        GroupMember.group_id == data.bolao_group_id,
        GroupMember.user_id == current_user.id,
    ).first()
    if not member:
        raise HTTPException(403, "Você não é membro deste bolão")

    existing = db.query(Prediction).filter(
        Prediction.user_id == current_user.id,
        Prediction.match_id == data.match_id,
        Prediction.bolao_group_id == data.bolao_group_id,
    ).first()
    if existing:
        raise HTTPException(400, "Palpite já registrado. Use PUT para atualizar.")

    pred = Prediction(
        user_id=current_user.id,
        match_id=data.match_id,
        bolao_group_id=data.bolao_group_id,
        home_score=data.home_score,
        away_score=data.away_score,
        predicted_winner_id=data.predicted_winner_id,
    )
    db.add(pred)
    db.commit()
    db.refresh(pred)
    return pred


@router.get("/", response_model=List[PredictionOut])
def list_predictions(
    bolao_group_id: Optional[int] = None,
    match_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Prediction).filter(Prediction.user_id == current_user.id)
    if bolao_group_id:
        query = query.filter(Prediction.bolao_group_id == bolao_group_id)
    if match_id:
        query = query.filter(Prediction.match_id == match_id)
    return query.all()


@router.put("/{prediction_id}", response_model=PredictionOut)
def update_prediction(
    prediction_id: int,
    data: PredictionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pred = db.query(Prediction).filter(
        Prediction.id == prediction_id,
        Prediction.user_id == current_user.id,
    ).first()
    if not pred:
        raise HTTPException(404, "Palpite não encontrado")

    match = db.query(Match).filter(Match.id == pred.match_id).first()
    _check_match_open(match)

    pred.home_score = data.home_score
    pred.away_score = data.away_score
    pred.predicted_winner_id = data.predicted_winner_id
    pred.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(pred)
    return pred
```

---

### Task 9: Seed Real do Banco

**Files:**
- Modify: `scripts/seed_db.py`

- [ ] **Step 1: Reescrever scripts/seed_db.py com models reais**

```python
"""
GolPeão — seed_db.py
Popula o banco com times, jogos e achievements.
Uso: python scripts/seed_db.py [--reset]
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Team, Match, Achievement
from app.config import settings
from data.fixtures import (
    TEAMS, GROUP_STAGE_FIXTURES, ROUND_OF_32_FIXTURES,
    ROUND_OF_16_FIXTURES, QUARTERFINAL_FIXTURES, SEMIFINAL_FIXTURES, FINAL_FIXTURES,
)

ACHIEVEMENTS_DATA = [
    {"slug": "primeiro_gol", "name": "Primeiro Gol ⚽", "description": "Fez seu primeiro palpite", "icon": "⚽", "points_bonus": 5},
    {"slug": "em_chamas", "name": "Em Chamas 🔥", "description": "3 acertos de vencedor consecutivos", "icon": "🔥", "points_bonus": 15},
    {"slug": "craque_do_bolao", "name": "Craque do Bolão 🎯", "description": "5 placares exatos no torneio", "icon": "🎯", "points_bonus": 25},
    {"slug": "polvo", "name": "Polvo 🐙", "description": "Acertou todos os jogos de uma rodada", "icon": "🐙", "points_bonus": 30},
    {"slug": "aguia", "name": "Águia 🦅", "description": "Previu eliminação de um dos 5 favoritos", "icon": "🦅", "points_bonus": 20},
    {"slug": "lenda", "name": "Lenda 👑", "description": "Acertou placar exato de empate", "icon": "👑", "points_bonus": 10},
    {"slug": "sortudo", "name": "Sortudo 🎪", "description": "Placar exato no jogo de abertura", "icon": "🎪", "points_bonus": 15},
    {"slug": "fantasma", "name": "Fantasma 👻", "description": "Não apostou em 5 jogos seguidos", "icon": "👻", "points_bonus": 0},
    {"slug": "rei", "name": "O Rei 🏆", "description": "Acertou o campeão da Copa", "icon": "🏆", "points_bonus": 50},
    {"slug": "100pts", "name": "Centenário 💯", "description": "Atingiu 100 pontos no bolão", "icon": "💯", "points_bonus": 20},
]


def run_seed(reset: bool = False):
    engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})
    if reset:
        print("⚠️  RESET: Recriando todas as tabelas...")
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    try:
        # Times
        print(f"\n📌 Inserindo {len(TEAMS)} times...")
        team_map = {}
        for t in TEAMS:
            tid, name_pt, name_en, iso_code, group, confederation = t
            existing = db.query(Team).filter(Team.name == name_pt, Team.group_name == group).first()
            if existing:
                team_map[tid] = existing
                continue
            team = Team(name=name_pt, name_en=name_en, iso_code=iso_code, group_name=group,
                        flag_url=f"https://flagcdn.com/64x48/{iso_code}.png", confederation=confederation)
            db.add(team)
            db.flush()
            team_map[tid] = team
            print(f"  ✅ {name_pt} ({iso_code}) — Grupo {group}")

        # Fase de grupos
        print(f"\n⚽ Inserindo {len(GROUP_STAGE_FIXTURES)} jogos da fase de grupos...")
        for f in GROUP_STAGE_FIXTURES:
            match_number, home_id, away_id, group, venue, scheduled_at = f
            if db.query(Match).filter(Match.match_number == match_number).first():
                continue
            match = Match(match_number=match_number, home_team_id=team_map[home_id].id,
                          away_team_id=team_map[away_id].id, stage="group", group_name=group,
                          venue=venue, scheduled_at=scheduled_at.replace(tzinfo=None), is_locked=False, is_played=False)
            db.add(match)

        # Mata-mata
        knockout_stages = [
            (ROUND_OF_32_FIXTURES, "round32"), (ROUND_OF_16_FIXTURES, "round16"),
            (QUARTERFINAL_FIXTURES, "qf"), (SEMIFINAL_FIXTURES, "sf"),
        ]
        for fixtures, stage in knockout_stages:
            print(f"\n🏅 Inserindo {len(fixtures)} jogos — {stage}...")
            for f in fixtures:
                match_number, match_label, venue, scheduled_at = f
                if db.query(Match).filter(Match.match_number == match_number).first():
                    continue
                match = Match(match_number=match_number, stage=stage, venue=venue,
                              scheduled_at=scheduled_at.replace(tzinfo=None),
                              match_label=match_label, is_locked=True, is_played=False)
                db.add(match)

        # Final + 3º lugar
        for f in FINAL_FIXTURES:
            match_number, match_label, venue, scheduled_at = f
            stage = "third" if "3º" in match_label else "final"
            if db.query(Match).filter(Match.match_number == match_number).first():
                continue
            match = Match(match_number=match_number, stage=stage, venue=venue,
                          scheduled_at=scheduled_at.replace(tzinfo=None),
                          match_label=match_label, is_locked=True, is_played=False)
            db.add(match)

        # Achievements
        print("\n🏅 Inserindo achievements...")
        for ach in ACHIEVEMENTS_DATA:
            if db.query(Achievement).filter(Achievement.slug == ach["slug"]).first():
                continue
            db.add(Achievement(**ach))
            print(f"  ✅ {ach['icon']} {ach['name']}")

        db.commit()
        total_matches = db.query(Match).count()
        print(f"\n✅ Seed concluído! Times: {len(TEAMS)} | Jogos: {total_matches} | Achievements: {len(ACHIEVEMENTS_DATA)}")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro no seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()
    run_seed(reset=args.reset)
```

- [ ] **Step 2: Rodar seed**

```bash
python scripts/seed_db.py --reset
```

Esperado: `✅ Seed concluído! Times: 48 | Jogos: 104 | Achievements: 10`

---

### Task 10: Script create_admin.py

**Files:**
- Create: `scripts/create_admin.py`

- [ ] **Step 1: Criar scripts/create_admin.py**

```python
"""
Cria um usuário admin.
Uso: python scripts/create_admin.py --username admin --password SenhaForte123
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

from app.database import Base
from app.models.user import User
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_admin(username: str, password: str, email: str):
    engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    try:
        if db.query(User).filter(User.username == username).first():
            print(f"⚠️  Usuário '{username}' já existe.")
            return
        admin = User(username=username, email=email, password_hash=pwd_context.hash(password),
                     display_name=username.capitalize(), is_admin=True)
        db.add(admin)
        db.commit()
        print(f"✅ Admin '{username}' criado com sucesso!")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--email", default="admin@golpeao.local")
    args = parser.parse_args()
    create_admin(args.username, args.password, args.email)
```

- [ ] **Step 2: Criar admin de teste**

```bash
python scripts/create_admin.py --username admin --password Admin@123 --email admin@golpeao.local
```

Esperado: `✅ Admin 'admin' criado com sucesso!`

- [ ] **Step 3: Rodar todos os testes do Sprint 1**

```bash
python -m pytest tests/ -v
```

Esperado: todos passando.

---

## SPRINT 2 — Grupos, Ranking, Achievements, Admin

---

### Task 11: Groups Router

**Files:**
- Create: `app/schemas/group.py`
- Modify: `app/routers/groups.py`

- [ ] **Step 1: Criar app/schemas/group.py**

```python
from pydantic import BaseModel
from datetime import datetime
from typing import List


class GroupCreate(BaseModel):
    name: str


class MemberOut(BaseModel):
    user_id: int
    username: str
    display_name: str
    avatar_emoji: str
    tier: str
    total_points: int
    joined_at: datetime

    model_config = {"from_attributes": True}


class GroupOut(BaseModel):
    id: int
    name: str
    invite_code: str
    owner_id: int
    is_active: bool
    created_at: datetime
    member_count: int = 0

    model_config = {"from_attributes": True}


class GroupDetail(GroupOut):
    members: List[MemberOut] = []
```

- [ ] **Step 2: Implementar app/routers/groups.py**

```python
import random
import string
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.group import BolaoGroup, GroupMember
from app.schemas.group import GroupCreate, GroupOut, GroupDetail, MemberOut

router = APIRouter(prefix="/groups", tags=["groups"])


def generate_invite_code(db: Session) -> str:
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not db.query(BolaoGroup).filter(BolaoGroup.invite_code == code).first():
            return code


@router.post("/", response_model=GroupOut, status_code=201)
def create_group(data: GroupCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    group = BolaoGroup(name=data.name, invite_code=generate_invite_code(db), owner_id=current_user.id)
    db.add(group)
    db.flush()
    member = GroupMember(group_id=group.id, user_id=current_user.id)
    db.add(member)
    db.commit()
    db.refresh(group)
    group.member_count = len(group.members)
    return group


@router.post("/join", response_model=GroupOut)
def join_group(invite_code: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    group = db.query(BolaoGroup).filter(BolaoGroup.invite_code == invite_code.upper()).first()
    if not group:
        raise HTTPException(404, "Código de convite inválido")
    if db.query(GroupMember).filter(GroupMember.group_id == group.id, GroupMember.user_id == current_user.id).first():
        raise HTTPException(400, "Você já é membro deste bolão")
    db.add(GroupMember(group_id=group.id, user_id=current_user.id))
    db.commit()
    db.refresh(group)
    group.member_count = len(group.members)
    return group


@router.get("/{group_id}", response_model=GroupDetail)
def get_group(group_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    group = db.query(BolaoGroup).options(joinedload(BolaoGroup.members)).filter(BolaoGroup.id == group_id).first()
    if not group:
        raise HTTPException(404, "Bolão não encontrado")
    return group


@router.get("/", response_model=List[GroupOut])
def my_groups(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    memberships = db.query(GroupMember).filter(GroupMember.user_id == current_user.id).all()
    groups = []
    for m in memberships:
        g = db.query(BolaoGroup).filter(BolaoGroup.id == m.group_id).first()
        if g:
            g.member_count = db.query(GroupMember).filter(GroupMember.group_id == g.id).count()
            groups.append(g)
    return groups
```

---

### Task 12: Achievements Service

**Files:**
- Create: `app/services/achievements.py`

- [ ] **Step 1: Criar app/services/achievements.py**

```python
from sqlalchemy.orm import Session
from app.models.achievement import Achievement, UserAchievement
from app.models.prediction import Prediction
from app.models.user import User


ACHIEVEMENTS = [
    {"slug": "primeiro_gol",    "check": lambda s: s["total_predictions"] >= 1},
    {"slug": "em_chamas",       "check": lambda s: s["consecutive_winner_hits"] >= 3},
    {"slug": "craque_do_bolao", "check": lambda s: s["exact_scores"] >= 5},
    {"slug": "polvo",           "check": lambda s: s.get("perfect_round") is True},
    {"slug": "aguia",           "check": lambda s: s.get("upset_predicted") is True},
    {"slug": "lenda",           "check": lambda s: s.get("exact_draw_score") is True},
    {"slug": "sortudo",         "check": lambda s: s.get("opening_match_exact") is True},
    {"slug": "fantasma",        "check": lambda s: s["missed_predictions"] >= 5},
    {"slug": "rei",             "check": lambda s: s.get("champion_correct") is True},
    {"slug": "100pts",          "check": lambda s: s["total_points"] >= 100},
]


def build_stats(db: Session, user_id: int, bolao_group_id: int) -> dict:
    preds = db.query(Prediction).filter(
        Prediction.user_id == user_id,
        Prediction.bolao_group_id == bolao_group_id,
    ).order_by(Prediction.created_at).all()

    total_points = sum(p.points_earned for p in preds)
    exact_scores = sum(1 for p in preds if p.is_exact)
    total_predictions = len(preds)

    # Acertos consecutivos
    max_consecutive = 0
    current = 0
    for p in preds:
        if p.is_winner_correct:
            current += 1
            max_consecutive = max(max_consecutive, current)
        else:
            current = 0

    # Placar exato de empate
    from app.models.match import Match
    exact_draw = False
    for p in preds:
        if p.is_exact:
            match = db.query(Match).filter(Match.id == p.match_id).first()
            if match and match.home_score == match.away_score:
                exact_draw = True

    # Jogo de abertura (match_number=1)
    opening_exact = False
    for p in preds:
        match = db.query(Match).filter(Match.id == p.match_id, Match.match_number == 1).first()
        if match and p.is_exact:
            opening_exact = True

    return {
        "total_predictions": total_predictions,
        "total_points": total_points,
        "exact_scores": exact_scores,
        "consecutive_winner_hits": max_consecutive,
        "missed_predictions": 0,
        "perfect_round": False,
        "upset_predicted": False,
        "exact_draw_score": exact_draw,
        "opening_match_exact": opening_exact,
        "champion_correct": False,
    }


def check_and_unlock(db: Session, user_id: int, bolao_group_id: int) -> list:
    stats = build_stats(db, user_id, bolao_group_id)
    unlocked = []

    for ach_def in ACHIEVEMENTS:
        if not ach_def["check"](stats):
            continue

        ach = db.query(Achievement).filter(Achievement.slug == ach_def["slug"]).first()
        if not ach:
            continue

        already = db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id,
            UserAchievement.achievement_id == ach.id,
            UserAchievement.bolao_group_id == bolao_group_id,
        ).first()
        if already:
            continue

        ua = UserAchievement(user_id=user_id, achievement_id=ach.id, bolao_group_id=bolao_group_id)
        db.add(ua)

        user = db.query(User).filter(User.id == user_id).first()
        user.total_points += ach.points_bonus

        unlocked.append(ach)

    if unlocked:
        db.commit()
    return unlocked
```

---

### Task 13: Ranking Router

**Files:**
- Create: `app/schemas/ranking.py`
- Modify: `app/routers/ranking.py`

- [ ] **Step 1: Criar app/schemas/ranking.py**

```python
from pydantic import BaseModel
from typing import List


class RankingEntry(BaseModel):
    position: int
    user_id: int
    username: str
    display_name: str
    avatar_emoji: str
    tier: str
    total_points: int
    exact_scores: int
    correct_winners: int

    model_config = {"from_attributes": True}


class RankingOut(BaseModel):
    group_id: int
    group_name: str
    entries: List[RankingEntry]
```

- [ ] **Step 2: Implementar app/routers/ranking.py**

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.group import BolaoGroup, GroupMember
from app.models.prediction import Prediction
from app.schemas.ranking import RankingOut, RankingEntry

router = APIRouter(prefix="/ranking", tags=["ranking"])


@router.get("/{group_id}", response_model=RankingOut)
def get_ranking(group_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    group = db.query(BolaoGroup).filter(BolaoGroup.id == group_id).first()
    if not group:
        raise HTTPException(404, "Bolão não encontrado")

    members = db.query(GroupMember).filter(GroupMember.group_id == group_id).all()

    entries = []
    for m in members:
        user = db.query(User).filter(User.id == m.user_id).first()
        preds = db.query(Prediction).filter(
            Prediction.user_id == m.user_id,
            Prediction.bolao_group_id == group_id,
        ).all()
        total_points = sum(p.points_earned for p in preds)
        exact_scores = sum(1 for p in preds if p.is_exact)
        correct_winners = sum(1 for p in preds if p.is_winner_correct)

        entries.append(RankingEntry(
            position=0,
            user_id=user.id,
            username=user.username,
            display_name=user.display_name,
            avatar_emoji=user.avatar_emoji,
            tier=user.tier,
            total_points=total_points,
            exact_scores=exact_scores,
            correct_winners=correct_winners,
        ))

    entries.sort(key=lambda x: (-x.total_points, -x.exact_scores))
    for i, e in enumerate(entries):
        e.position = i + 1

    return RankingOut(group_id=group_id, group_name=group.name, entries=entries)
```

---

### Task 14: Admin Router — Inserir Resultados

**Files:**
- Modify: `app/routers/admin.py`

- [ ] **Step 1: Implementar app/routers/admin.py**

```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from app.dependencies import get_db, get_admin_user
from app.models.user import User
from app.models.match import Match
from app.models.prediction import Prediction
from app.models.group import GroupMember
from app.services.scoring import calculate_points, get_tier
from app.services.achievements import check_and_unlock

router = APIRouter(prefix="/admin", tags=["admin"])


class MatchResult(BaseModel):
    home_score: int
    away_score: int
    winner_team_id: int = None


@router.post("/matches/{match_id}/result")
def set_match_result(
    match_id: int,
    result: MatchResult,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(404, "Jogo não encontrado")

    match.home_score = result.home_score
    match.away_score = result.away_score
    match.winner_team_id = result.winner_team_id
    match.is_played = True
    match.is_locked = True

    # Recalcular todos os palpites
    preds = db.query(Prediction).filter(Prediction.match_id == match_id).all()
    updated = 0
    for pred in preds:
        calc = calculate_points(pred, match)
        pred.points_earned = calc["points"]
        pred.is_exact = calc["is_exact"]
        pred.is_winner_correct = calc["is_winner_correct"]

        # Atualizar tier do usuário
        user = db.query(User).filter(User.id == pred.user_id).first()
        if user:
            all_preds = db.query(Prediction).filter(Prediction.user_id == user.id).all()
            user.total_points = sum(p.points_earned for p in all_preds)
            tier = get_tier(user.total_points)
            user.tier = tier["name"].lower()

        updated += 1

    db.commit()

    # Verificar achievements para cada usuário
    group_ids = {pred.bolao_group_id for pred in preds}
    user_ids = {pred.user_id for pred in preds}
    for uid in user_ids:
        for gid in group_ids:
            check_and_unlock(db, uid, gid)

    return {"message": f"Resultado registrado. {updated} palpites recalculados."}


@router.get("/matches/pending-results", response_model=List[dict])
def pending_results(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    matches = db.query(Match).filter(Match.is_played == False, Match.is_locked == True).all()
    return [{"id": m.id, "match_number": m.match_number, "stage": m.stage,
             "scheduled_at": str(m.scheduled_at), "match_label": m.match_label} for m in matches]
```

---

### Task 15: Notifications Service (Feed de Atividade)

**Files:**
- Create: `app/services/notifications.py`

- [ ] **Step 1: Criar app/services/notifications.py**

```python
from datetime import datetime
from typing import List

_feed: List[dict] = []
MAX_FEED_SIZE = 100


def add_event(event_type: str, message: str, user_display: str = None, icon: str = "⚽"):
    _feed.insert(0, {
        "type": event_type,
        "message": message,
        "user": user_display,
        "icon": icon,
        "at": datetime.utcnow().isoformat(),
    })
    if len(_feed) > MAX_FEED_SIZE:
        _feed.pop()


def get_feed(limit: int = 20) -> List[dict]:
    return _feed[:limit]
```

---

## SPRINT 3 — Frontend Streamlit

---

### Task 16: API Client + Style CSS

**Files:**
- Create: `frontend/api_client.py`
- Create: `frontend/style.css`

- [ ] **Step 1: Criar frontend/api_client.py**

```python
import requests
import streamlit as st

API_BASE = "http://localhost:8000"


def _headers():
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}


def register(username, email, password, display_name, avatar_emoji="⚽"):
    r = requests.post(f"{API_BASE}/auth/register", json={
        "username": username, "email": email, "password": password,
        "display_name": display_name, "avatar_emoji": avatar_emoji,
    })
    return r.json(), r.status_code


def login(username, password):
    r = requests.post(f"{API_BASE}/auth/login", json={"username": username, "password": password})
    if r.status_code == 200:
        return r.json()["access_token"], None
    return None, r.json().get("detail", "Erro")


def me():
    r = requests.get(f"{API_BASE}/auth/me", headers=_headers())
    return r.json() if r.status_code == 200 else None


def get_matches(stage=None, group=None):
    params = {}
    if stage:
        params["stage"] = stage
    if group:
        params["group"] = group
    r = requests.get(f"{API_BASE}/matches/", params=params, headers=_headers())
    return r.json() if r.status_code == 200 else []


def get_upcoming():
    r = requests.get(f"{API_BASE}/matches/upcoming", headers=_headers())
    return r.json() if r.status_code == 200 else []


def get_predictions(bolao_group_id=None, match_id=None):
    params = {}
    if bolao_group_id:
        params["bolao_group_id"] = bolao_group_id
    if match_id:
        params["match_id"] = match_id
    r = requests.get(f"{API_BASE}/predictions/", params=params, headers=_headers())
    return r.json() if r.status_code == 200 else []


def create_prediction(match_id, bolao_group_id, home_score, away_score, predicted_winner_id=None):
    r = requests.post(f"{API_BASE}/predictions/", json={
        "match_id": match_id, "bolao_group_id": bolao_group_id,
        "home_score": home_score, "away_score": away_score,
        "predicted_winner_id": predicted_winner_id,
    }, headers=_headers())
    return r.json(), r.status_code


def update_prediction(pred_id, match_id, bolao_group_id, home_score, away_score):
    r = requests.put(f"{API_BASE}/predictions/{pred_id}", json={
        "match_id": match_id, "bolao_group_id": bolao_group_id,
        "home_score": home_score, "away_score": away_score,
    }, headers=_headers())
    return r.json(), r.status_code


def get_my_groups():
    r = requests.get(f"{API_BASE}/groups/", headers=_headers())
    return r.json() if r.status_code == 200 else []


def create_group(name):
    r = requests.post(f"{API_BASE}/groups/", json={"name": name}, headers=_headers())
    return r.json(), r.status_code


def join_group(invite_code):
    r = requests.post(f"{API_BASE}/groups/join", params={"invite_code": invite_code}, headers=_headers())
    return r.json(), r.status_code


def get_ranking(group_id):
    r = requests.get(f"{API_BASE}/ranking/{group_id}", headers=_headers())
    return r.json() if r.status_code == 200 else None


def set_match_result(match_id, home_score, away_score):
    r = requests.post(f"{API_BASE}/admin/matches/{match_id}/result",
                      json={"home_score": home_score, "away_score": away_score}, headers=_headers())
    return r.json(), r.status_code
```

- [ ] **Step 2: Criar frontend/style.css**

```css
/* GolPeão — CSS Gamificado Copa 2026 */
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

.stApp { background: linear-gradient(135deg, var(--copa-dark) 0%, #0D1B2A 100%); color: var(--copa-white); }
.stSidebar { background: rgba(10, 92, 54, 0.15) !important; border-right: 1px solid rgba(255,215,0,0.2); }

.match-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,215,0,0.2);
    border-radius: 16px;
    padding: 20px;
    margin: 10px 0;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}
.match-card:hover { border-color: var(--copa-gold); box-shadow: 0 0 20px rgba(255,215,0,0.3); transform: translateY(-2px); }

.flag-img { width: 64px; height: 48px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.4); }
.team-name { font-size: 1.1em; font-weight: bold; margin-top: 6px; text-align: center; }
.score-display { font-size: 2.5em; font-weight: 900; color: var(--copa-gold); text-align: center; font-family: monospace; }
.vs-text { font-size: 1.4em; text-align: center; color: rgba(255,255,255,0.4); }

.rank-1 { color: var(--copa-gold); font-size: 1.4em; font-weight: 900; }
.rank-2 { color: var(--tier-silver); font-size: 1.2em; font-weight: bold; }
.rank-3 { color: var(--tier-bronze); font-size: 1.1em; font-weight: bold; }

.badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.85em; font-weight: bold; margin: 2px; }
.badge-unlocked { background: linear-gradient(135deg, var(--copa-gold), #FF8C00); color: var(--copa-dark); }
.badge-locked { background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.3); border: 1px solid rgba(255,255,255,0.1); }

.tier-badge { padding: 3px 10px; border-radius: 12px; font-size: 0.8em; font-weight: bold; }
.tier-bronze   { background: linear-gradient(135deg, #CD7F32, #8B4513); color: white; }
.tier-silver   { background: linear-gradient(135deg, #C0C0C0, #808080); color: white; }
.tier-ouro     { background: linear-gradient(135deg, #FFD700, #FF8C00); color: #020F2A; }
.tier-platina  { background: linear-gradient(135deg, #E5E4E2, #BCC0C4); color: #020F2A; }
.tier-lenda    { background: linear-gradient(135deg, #FF6B35, #FF2A00); color: white; }

.activity-item { padding: 8px 12px; border-left: 3px solid var(--copa-gold); margin: 6px 0; background: rgba(255,215,0,0.05); border-radius: 0 8px 8px 0; font-size: 0.9em; }

.stButton > button { background: linear-gradient(135deg, var(--copa-green), #0D7A4A) !important; color: white !important; border: 2px solid var(--copa-gold) !important; border-radius: 12px !important; font-weight: bold !important; transition: all 0.3s !important; }
.stButton > button:hover { box-shadow: 0 0 15px rgba(255,215,0,0.5) !important; transform: translateY(-1px) !important; }

.stTextInput input, .stNumberInput input { background: rgba(255,255,255,0.08) !important; border: 1px solid rgba(255,215,0,0.3) !important; color: white !important; border-radius: 8px !important; }
.stSelectbox select { background: rgba(10,92,54,0.3) !important; color: white !important; }

h1, h2, h3 { color: var(--copa-gold) !important; }

.invite-code { font-family: monospace; font-size: 2em; font-weight: 900; color: var(--copa-gold); letter-spacing: 8px; text-align: center; padding: 10px; border: 2px dashed rgba(255,215,0,0.5); border-radius: 12px; }

.xp-bar-bg { background: rgba(255,255,255,0.1); border-radius: 10px; height: 12px; overflow: hidden; }
.xp-bar-fill { background: linear-gradient(90deg, var(--copa-gold), #FF8C00); height: 100%; border-radius: 10px; }
```

---

### Task 17: Streamlit App + Página de Login

**Files:**
- Create: `frontend/app.py`

- [ ] **Step 1: Criar frontend/app.py**

```python
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.api_client import login, register, me

st.set_page_config(
    page_title="GolPeão ⚽",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

css_path = os.path.join(os.path.dirname(__file__), "style.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "active_group" not in st.session_state:
    st.session_state.active_group = None


def render_login():
    st.markdown("<h1 style='text-align:center'>⚽ GolPeão</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:rgba(255,255,255,0.6)'>Bolão Gamificado — Copa do Mundo 2026</p>", unsafe_allow_html=True)
    st.markdown("---")

    tab_login, tab_register = st.tabs(["Entrar", "Criar Conta"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("🔑 Entrar", use_container_width=True)
            if submitted:
                token, err = login(username, password)
                if token:
                    st.session_state.token = token
                    st.session_state.user = me()
                    st.rerun()
                else:
                    st.error(f"❌ {err}")

    with tab_register:
        with st.form("register_form"):
            new_username = st.text_input("Nome de usuário")
            new_email = st.text_input("Email")
            new_display = st.text_input("Nome de exibição")
            new_avatar = st.selectbox("Avatar", ["⚽", "🏆", "🎯", "🔥", "⚡", "🦅", "🐙", "👑"])
            new_password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("🎉 Criar Conta", use_container_width=True)
            if submitted:
                data, code = register(new_username, new_email, new_password, new_display, new_avatar)
                if code == 201:
                    st.success("✅ Conta criada! Faça login.")
                else:
                    st.error(f"❌ {data.get('detail', 'Erro')}")


def render_sidebar():
    user = st.session_state.user
    if not user:
        return

    with st.sidebar:
        tier_class = f"tier-{user['tier']}"
        st.markdown(f"""
        <div style="text-align:center;padding:10px">
            <div style="font-size:3em">{user['avatar_emoji']}</div>
            <div style="font-weight:bold;font-size:1.1em">{user['display_name']}</div>
            <span class="tier-badge {tier_class}">{user['tier'].capitalize()}</span>
            <div style="margin-top:8px;color:var(--copa-gold);font-weight:bold">{user['total_points']} pts</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.active_group = None
            st.rerun()


if not st.session_state.token:
    render_login()
else:
    render_sidebar()
    st.markdown("<h2>🏠 Bem-vindo ao GolPeão!</h2>", unsafe_allow_html=True)
    st.markdown(f"Olá, **{st.session_state.user['display_name']}**! Use o menu lateral para navegar.")
    st.info("🏆 Copa do Mundo FIFA 2026 — EUA/Canadá/México")
```

---

### Task 18: Página Início (Dashboard)

**Files:**
- Create: `frontend/pages/1_🏠_Inicio.py`

- [ ] **Step 1: Criar frontend/pages/1_🏠_Inicio.py**

```python
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from frontend.api_client import get_upcoming, get_my_groups, get_ranking
from datetime import datetime, timezone

if not st.session_state.get("token"):
    st.warning("⚠️ Faça login primeiro.")
    st.stop()

user = st.session_state.user
st.markdown(f"<h1>🏠 Início</h1>", unsafe_allow_html=True)

# Próximos jogos
st.markdown("### ⏰ Próximos Jogos")
upcoming = get_upcoming()
if upcoming:
    for m in upcoming[:3]:
        home = m.get("home_team", {}) or {}
        away = m.get("away_team", {}) or {}
        home_iso = home.get("iso_code", "xx")
        away_iso = away.get("iso_code", "xx")
        home_name = home.get("name", m.get("match_label", "A definir"))
        away_name = away.get("name", "A definir")
        sched = m.get("scheduled_at", "")[:16].replace("T", " ")

        st.markdown(f"""
        <div class="match-card">
            <div style="display:flex;align-items:center;justify-content:space-around">
                <div style="text-align:center">
                    <img src="https://flagcdn.com/64x48/{home_iso}.png" class="flag-img"><br>
                    <span class="team-name">{home_name}</span>
                </div>
                <div style="text-align:center">
                    <div class="vs-text">⚽ vs ⚽</div>
                    <div style="font-size:0.8em;color:rgba(255,255,255,0.5)">{sched} UTC</div>
                </div>
                <div style="text-align:center">
                    <img src="https://flagcdn.com/64x48/{away_iso}.png" class="flag-img"><br>
                    <span class="team-name">{away_name}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Nenhum jogo programado em breve.")

# Meus bolões
st.markdown("### 🏆 Meus Bolões")
groups = get_my_groups()
if groups:
    for g in groups:
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.markdown(f"**{g['name']}**")
        col2.markdown(f"👥 {g.get('member_count', '?')}")
        if col3.button("Ver Ranking", key=f"rank_{g['id']}"):
            st.session_state.active_group = g
            st.switch_page("pages/4_🏆_Ranking.py")
else:
    st.info("Você ainda não participa de nenhum bolão. Crie ou entre em um na aba Grupos.")
```

---

### Task 19: Página Jogos

**Files:**
- Create: `frontend/pages/2_⚽_Jogos.py`

- [ ] **Step 1: Criar frontend/pages/2_⚽_Jogos.py**

```python
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from frontend.api_client import get_matches

if not st.session_state.get("token"):
    st.warning("⚠️ Faça login primeiro.")
    st.stop()

st.markdown("<h1>⚽ Jogos</h1>", unsafe_allow_html=True)

STAGES = {
    "group": "Fase de Grupos",
    "round32": "Oitavas de Final (Round of 32)",
    "round16": "Round of 16",
    "qf": "Quartas de Final",
    "sf": "Semifinais",
    "third": "Disputa de 3º Lugar",
    "final": "Final",
}

stage = st.selectbox("Fase", list(STAGES.keys()), format_func=lambda x: STAGES[x])

if stage == "group":
    group_filter = st.selectbox("Grupo", ["Todos"] + list("ABCDEFGHIJKL"))
    matches = get_matches(stage=stage, group=group_filter if group_filter != "Todos" else None)
else:
    matches = get_matches(stage=stage)

if not matches:
    st.info("Nenhum jogo encontrado.")
else:
    for m in matches:
        home = m.get("home_team") or {}
        away = m.get("away_team") or {}
        home_iso = home.get("iso_code", "xx")
        away_iso = away.get("iso_code", "xx")
        home_name = home.get("name", "A definir")
        away_name = away.get("name", "A definir")
        sched = m.get("scheduled_at", "")[:16].replace("T", " ")

        if m.get("is_played"):
            score = f"{m['home_score']} × {m['away_score']}"
            status_html = f'<div class="score-display">{score}</div>'
        elif m.get("is_locked"):
            status_html = '<div style="text-align:center;color:#FF6B35">🔒 Fechado</div>'
        else:
            status_html = '<div style="text-align:center;color:#7FFF00">🟢 Aberto</div>'

        st.markdown(f"""
        <div class="match-card">
            <div style="font-size:0.75em;color:rgba(255,255,255,0.4);text-align:right">Jogo #{m['match_number']} | {sched} UTC</div>
            <div style="display:flex;align-items:center;justify-content:space-around;margin-top:10px">
                <div style="text-align:center;width:35%">
                    <img src="https://flagcdn.com/64x48/{home_iso}.png" class="flag-img"><br>
                    <span class="team-name">{home_name}</span>
                </div>
                <div style="width:30%">{status_html}</div>
                <div style="text-align:center;width:35%">
                    <img src="https://flagcdn.com/64x48/{away_iso}.png" class="flag-img"><br>
                    <span class="team-name">{away_name}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
```

---

### Task 20: Página Meus Palpites

**Files:**
- Create: `frontend/pages/3_🎯_Meus_Palpites.py`

- [ ] **Step 1: Criar frontend/pages/3_🎯_Meus_Palpites.py**

```python
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from frontend.api_client import get_my_groups, get_matches, get_predictions, create_prediction, update_prediction

if not st.session_state.get("token"):
    st.warning("⚠️ Faça login primeiro.")
    st.stop()

st.markdown("<h1>🎯 Meus Palpites</h1>", unsafe_allow_html=True)

groups = get_my_groups()
if not groups:
    st.info("Entre em um bolão primeiro!")
    st.stop()

group_names = {g["id"]: g["name"] for g in groups}
selected_group_id = st.selectbox("Bolão", list(group_names.keys()), format_func=lambda x: group_names[x])

stage = st.selectbox("Fase", ["group", "round32", "round16", "qf", "sf", "third", "final"],
                     format_func=lambda x: {"group": "Fase de Grupos", "round32": "Oitavas (R32)",
                     "round16": "Round of 16", "qf": "Quartas", "sf": "Semis", "third": "3º Lugar", "final": "Final"}[x])

matches = get_matches(stage=stage)
my_preds = get_predictions(bolao_group_id=selected_group_id)
pred_map = {p["match_id"]: p for p in my_preds}

st.markdown("---")

for m in matches:
    if m.get("is_played"):
        continue

    home = m.get("home_team") or {}
    away = m.get("away_team") or {}
    home_iso = home.get("iso_code", "xx")
    away_iso = away.get("iso_code", "xx")
    home_name = home.get("name", m.get("match_label", "A definir"))
    away_name = away.get("name", "A definir")
    sched = m.get("scheduled_at", "")[:16].replace("T", " ")
    existing = pred_map.get(m["id"])

    with st.expander(f"{'🔒' if m['is_locked'] else '🟢'} Jogo #{m['match_number']} — {home_name} vs {away_name} | {sched}", expanded=not m["is_locked"]):
        if m.get("is_locked"):
            if existing:
                st.info(f"Palpite: {existing['home_score']} × {existing['away_score']}")
            else:
                st.warning("Palpites fechados — sem palpite registrado.")
        else:
            col1, col2, col3 = st.columns([2, 1, 2])
            with col1:
                st.markdown(f'<div style="text-align:center"><img src="https://flagcdn.com/64x48/{home_iso}.png" class="flag-img"><br><b>{home_name}</b></div>', unsafe_allow_html=True)
            with col2:
                h_val = existing["home_score"] if existing else 0
                a_val = existing["away_score"] if existing else 0
                h = st.number_input("Casa", 0, 20, h_val, key=f"h_{m['id']}")
                st.markdown("<div style='text-align:center;font-size:1.5em'>×</div>", unsafe_allow_html=True)
                a = st.number_input("Fora", 0, 20, a_val, key=f"a_{m['id']}")
            with col3:
                st.markdown(f'<div style="text-align:center"><img src="https://flagcdn.com/64x48/{away_iso}.png" class="flag-img"><br><b>{away_name}</b></div>', unsafe_allow_html=True)

            if existing:
                if st.button("✏️ Atualizar", key=f"upd_{m['id']}"):
                    data, code = update_prediction(existing["id"], m["id"], selected_group_id, h, a)
                    st.success("✅ Palpite atualizado!") if code == 200 else st.error(f"❌ {data.get('detail')}")
            else:
                if st.button("💾 Salvar", key=f"save_{m['id']}"):
                    data, code = create_prediction(m["id"], selected_group_id, h, a)
                    st.success("✅ Palpite salvo!") if code == 201 else st.error(f"❌ {data.get('detail')}")
```

---

### Task 21: Página Ranking + Grupos

**Files:**
- Create: `frontend/pages/4_🏆_Ranking.py`

- [ ] **Step 1: Criar frontend/pages/4_🏆_Ranking.py**

```python
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from frontend.api_client import get_my_groups, get_ranking, create_group, join_group

if not st.session_state.get("token"):
    st.warning("⚠️ Faça login primeiro.")
    st.stop()

st.markdown("<h1>🏆 Ranking & Grupos</h1>", unsafe_allow_html=True)

tab_ranking, tab_groups = st.tabs(["📊 Ranking", "👥 Meus Grupos"])

with tab_groups:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ➕ Criar Bolão")
        with st.form("new_group"):
            name = st.text_input("Nome do bolão")
            if st.form_submit_button("Criar", use_container_width=True):
                data, code = create_group(name)
                if code == 201:
                    st.success(f"✅ Bolão criado!")
                    st.markdown(f'<div class="invite-code">{data["invite_code"]}</div>', unsafe_allow_html=True)
                    st.caption("Compartilhe este código com seus amigos!")
                else:
                    st.error(f"❌ {data.get('detail')}")
    with col2:
        st.markdown("#### 🔗 Entrar em Bolão")
        with st.form("join_group"):
            code = st.text_input("Código de convite").upper()
            if st.form_submit_button("Entrar", use_container_width=True):
                data, status = join_group(code)
                if status == 200:
                    st.success(f"✅ Você entrou em **{data['name']}**!")
                else:
                    st.error(f"❌ {data.get('detail')}")

    st.markdown("---")
    st.markdown("#### 🏅 Meus Bolões")
    groups = get_my_groups()
    for g in groups:
        st.markdown(f"**{g['name']}** — Código: `{g['invite_code']}` — 👥 {g.get('member_count', '?')} membros")

with tab_ranking:
    groups = get_my_groups()
    if not groups:
        st.info("Entre em um bolão para ver o ranking!")
        st.stop()

    group_names = {g["id"]: g["name"] for g in groups}
    gid = st.selectbox("Bolão", list(group_names.keys()), format_func=lambda x: group_names[x])

    ranking = get_ranking(gid)
    if not ranking or not ranking.get("entries"):
        st.info("Sem dados de ranking ainda.")
    else:
        for e in ranking["entries"]:
            pos = e["position"]
            pos_class = f"rank-{pos}" if pos <= 3 else ""
            medal = ["🥇", "🥈", "🥉"][pos - 1] if pos <= 3 else f"#{pos}"
            tier_class = f"tier-{e['tier']}"

            st.markdown(f"""
            <div class="match-card" style="padding:12px 20px">
                <div style="display:flex;align-items:center;gap:16px">
                    <div class="{pos_class}" style="min-width:40px;font-size:1.5em">{medal}</div>
                    <div style="font-size:2em">{e['avatar_emoji']}</div>
                    <div style="flex:1">
                        <div style="font-weight:bold">{e['display_name']}</div>
                        <span class="tier-badge {tier_class}">{e['tier'].capitalize()}</span>
                    </div>
                    <div style="text-align:right">
                        <div style="color:var(--copa-gold);font-weight:900;font-size:1.3em">{e['total_points']} pts</div>
                        <div style="font-size:0.8em;color:rgba(255,255,255,0.5)">🎯 {e['exact_scores']} exatos | ✅ {e['correct_winners']} venc.</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
```

---

### Task 22: Página Conquistas

**Files:**
- Create: `frontend/pages/5_🏅_Conquistas.py`

- [ ] **Step 1: Criar frontend/pages/5_🏅_Conquistas.py**

```python
import streamlit as st
import requests
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from frontend.api_client import get_my_groups

if not st.session_state.get("token"):
    st.warning("⚠️ Faça login primeiro.")
    st.stop()

st.markdown("<h1>🏅 Conquistas</h1>", unsafe_allow_html=True)

API_BASE = "http://localhost:8000"
headers = {"Authorization": f"Bearer {st.session_state['token']}"}

ALL_ACHIEVEMENTS = [
    {"slug": "primeiro_gol", "name": "Primeiro Gol", "icon": "⚽", "description": "Fez seu primeiro palpite"},
    {"slug": "em_chamas", "name": "Em Chamas", "icon": "🔥", "description": "3 acertos de vencedor consecutivos"},
    {"slug": "craque_do_bolao", "name": "Craque do Bolão", "icon": "🎯", "description": "5 placares exatos"},
    {"slug": "polvo", "name": "Polvo", "icon": "🐙", "description": "Acertou todos os jogos de uma rodada"},
    {"slug": "aguia", "name": "Águia", "icon": "🦅", "description": "Previu eliminação de um favorito"},
    {"slug": "lenda", "name": "Lenda", "icon": "👑", "description": "Acertou placar exato de empate"},
    {"slug": "sortudo", "name": "Sortudo", "icon": "🎪", "description": "Placar exato no jogo de abertura"},
    {"slug": "rei", "name": "O Rei", "icon": "🏆", "description": "Acertou o campeão da Copa"},
    {"slug": "100pts", "name": "Centenário", "icon": "💯", "description": "Atingiu 100 pontos"},
]

groups = get_my_groups()
if not groups:
    st.info("Entre em um bolão para ver suas conquistas!")
    st.stop()

group_names = {g["id"]: g["name"] for g in groups}
gid = st.selectbox("Bolão", list(group_names.keys()), format_func=lambda x: group_names[x])

r = requests.get(f"{API_BASE}/ranking/{gid}", headers=headers)
if r.status_code != 200:
    st.error("Erro ao carregar dados.")
    st.stop()

# Achievements do user (simulado via total_points por enquanto)
user = st.session_state.user
unlocked_slugs = set()
if user["total_points"] >= 1:
    unlocked_slugs.add("primeiro_gol")
if user["total_points"] >= 100:
    unlocked_slugs.add("100pts")

st.markdown(f"### {user['avatar_emoji']} {user['display_name']} — {user['total_points']} pts")
st.markdown("---")

cols = st.columns(3)
for i, ach in enumerate(ALL_ACHIEVEMENTS):
    unlocked = ach["slug"] in unlocked_slugs
    badge_class = "badge-unlocked" if unlocked else "badge-locked"
    lock_overlay = "" if unlocked else "🔒 "
    with cols[i % 3]:
        st.markdown(f"""
        <div class="match-card" style="text-align:center;padding:15px">
            <div style="font-size:2.5em">{ach['icon']}</div>
            <div class="badge {badge_class}" style="margin:8px 0">{lock_overlay}{ach['name']}</div>
            <div style="font-size:0.8em;color:rgba(255,255,255,{'0.7' if unlocked else '0.3'})">{ach['description']}</div>
        </div>
        """, unsafe_allow_html=True)
```

---

### Task 23: Página Admin

**Files:**
- Create: `frontend/pages/7_⚙️_Admin.py`

- [ ] **Step 1: Criar frontend/pages/7_⚙️_Admin.py**

```python
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from frontend.api_client import get_matches, set_match_result

if not st.session_state.get("token"):
    st.warning("⚠️ Faça login primeiro.")
    st.stop()

user = st.session_state.user
if not user.get("is_admin"):
    st.error("⛔ Acesso restrito a administradores.")
    st.stop()

st.markdown("<h1>⚙️ Painel Admin</h1>", unsafe_allow_html=True)
st.warning("⚠️ Área restrita. Insira os resultados com atenção.")

STAGES = {"group": "Fase de Grupos", "round32": "R32", "round16": "R16", "qf": "Quartas", "sf": "Semis", "third": "3º", "final": "Final"}
stage = st.selectbox("Fase", list(STAGES.keys()), format_func=lambda x: STAGES[x])
matches = get_matches(stage=stage)

unplayed = [m for m in matches if not m.get("is_played")]
if not unplayed:
    st.success("✅ Todos os jogos desta fase já têm resultado!")
else:
    for m in unplayed:
        home = m.get("home_team") or {}
        away = m.get("away_team") or {}
        home_name = home.get("name", m.get("match_label", "A definir"))
        away_name = away.get("name", "A definir")

        with st.expander(f"Jogo #{m['match_number']} — {home_name} vs {away_name}"):
            col1, col2, col3 = st.columns(3)
            h = col1.number_input("Gols Casa", 0, 20, 0, key=f"ah_{m['id']}")
            col2.markdown("<div style='text-align:center;padding-top:28px;font-size:1.5em'>×</div>", unsafe_allow_html=True)
            a = col3.number_input("Gols Fora", 0, 20, 0, key=f"aa_{m['id']}")
            if st.button(f"✅ Registrar Resultado", key=f"res_{m['id']}"):
                data, code = set_match_result(m["id"], h, a)
                if code == 200:
                    st.success(f"✅ Resultado registrado! {data['message']}")
                    st.rerun()
                else:
                    st.error(f"❌ {data.get('detail', 'Erro')}")
```

---

### Task 24: Teste de Integração Final

- [ ] **Step 1: Verificar que todos os testes passam**

```bash
python -m pytest tests/ -v
```

Esperado: todos passando.

- [ ] **Step 2: Rodar backend**

```bash
uvicorn app.main:app --reload --port 8000
```

Esperado: servidor rodando em `http://localhost:8000`.

- [ ] **Step 3: Rodar seed (se banco não populado)**

```bash
python scripts/seed_db.py
```

- [ ] **Step 4: Rodar frontend**

Em outro terminal:

```bash
cd frontend && streamlit run app.py --server.port 8501
```

Esperado: interface abrindo em `http://localhost:8501`.

- [ ] **Step 5: Fluxo de smoke test**

1. Criar conta em `/auth/register`
2. Fazer login
3. Criar bolão
4. Ver jogos da fase de grupos
5. Registrar palpite
6. Verificar que aparece em "Meus Palpites"
7. (Como admin) Inserir resultado de um jogo
8. Verificar pontos no ranking

- [ ] **Step 6: Verificar docs da API**

Acessar `http://localhost:8000/docs` — verificar que todos os endpoints estão documentados.

---

## Self-Review

### Cobertura de Spec

| Requisito | Implementado em |
|-----------|----------------|
| 48 times com ISO codes | Task 9 (seed_db.py) |
| 104 jogos | Task 9 (seed_db.py) |
| Auth JWT (register/login/me) | Task 5 |
| Motor de pontuação | Task 4 |
| Bolões (criar/entrar) | Task 11 |
| Ranking por bolão | Task 13 |
| Achievements | Task 12 + Task 15 |
| Admin inserir resultados | Task 14 |
| Frontend Streamlit | Tasks 16–23 |
| CSS gamificado | Task 16 |
| Bandeiras flagcdn.com | Tasks 18–20 |
| Palpites fechar 5min antes | Regra: is_locked (APScheduler pendente) |
| Recalcular palpites ao inserir resultado | Task 14 |
| Tiers (Bronze→Lenda) | Task 4 + Task 14 |

### Gaps Conhecidos
- APScheduler para fechar palpites automaticamente: não implementado (admin fecha manualmente via is_locked). Pode ser adicionado em Sprint 4.
- Endpoint `/admin/advance-stage` (bracket engine): não implementado. Admin insere resultados manualmente.
- Paginação de ranking > 20 membros: não implementado.
- Tests para groups e ranking: não adicionados (apenas auth e scoring). Adicionar em Sprint 4.
