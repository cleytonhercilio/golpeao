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
    {"slug": "primeiro_gol",    "name": "Primeiro Gol ⚽",    "description": "Fez seu primeiro palpite",                    "icon": "⚽", "points_bonus": 5},
    {"slug": "em_chamas",       "name": "Em Chamas 🔥",       "description": "3 acertos de vencedor consecutivos",           "icon": "🔥", "points_bonus": 15},
    {"slug": "craque_do_bolao", "name": "Craque do Bolão 🎯", "description": "5 placares exatos no torneio",                "icon": "🎯", "points_bonus": 25},
    {"slug": "polvo",           "name": "Polvo 🐙",           "description": "Acertou todos os jogos de uma rodada",         "icon": "🐙", "points_bonus": 30},
    {"slug": "aguia",           "name": "Águia 🦅",           "description": "Previu eliminação de um dos 5 favoritos",     "icon": "🦅", "points_bonus": 20},
    {"slug": "lenda",           "name": "Lenda 👑",           "description": "Acertou placar exato de empate",              "icon": "👑", "points_bonus": 10},
    {"slug": "sortudo",         "name": "Sortudo 🎪",         "description": "Placar exato no jogo de abertura",            "icon": "🎪", "points_bonus": 15},
    {"slug": "fantasma",        "name": "Fantasma 👻",        "description": "Não apostou em 5 jogos seguidos",             "icon": "👻", "points_bonus": 0},
    {"slug": "rei",             "name": "O Rei 🏆",           "description": "Acertou o campeão da Copa",                   "icon": "🏆", "points_bonus": 50},
    {"slug": "100pts",          "name": "Centenário 💯",      "description": "Atingiu 100 pontos no bolão",                 "icon": "💯", "points_bonus": 20},
]


def run_seed(reset: bool = False):
    connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
    engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

    if reset:
        print("⚠️  RESET: Recriando todas as tabelas...")
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    db = Session()

    try:
        # 1. Times
        print(f"\n📌 Inserindo {len(TEAMS)} times...")
        team_map = {}
        for t in TEAMS:
            tid, name_pt, name_en, iso_code, group, confederation = t
            existing = db.query(Team).filter(Team.name == name_pt, Team.group_name == group).first()
            if existing:
                team_map[tid] = existing
                continue
            team = Team(
                name=name_pt,
                name_en=name_en,
                iso_code=iso_code,
                group_name=group,
                flag_url=f"https://flagcdn.com/64x48/{iso_code}.png",
                confederation=confederation,
            )
            db.add(team)
            db.flush()
            team_map[tid] = team
            print(f"  ✅ {name_pt} ({iso_code}) — Grupo {group}")

        # 2. Fase de grupos (72 jogos)
        print(f"\n⚽ Inserindo {len(GROUP_STAGE_FIXTURES)} jogos da fase de grupos...")
        for f in GROUP_STAGE_FIXTURES:
            match_number, home_id, away_id, group, venue, scheduled_at = f
            if db.query(Match).filter(Match.match_number == match_number).first():
                continue
            match = Match(
                match_number=match_number,
                home_team_id=team_map[home_id].id,
                away_team_id=team_map[away_id].id,
                stage="group",
                group_name=group,
                venue=venue,
                scheduled_at=scheduled_at.replace(tzinfo=None),
                is_locked=False,
                is_played=False,
            )
            db.add(match)

        # 3. Mata-mata
        knockout_stages = [
            (ROUND_OF_32_FIXTURES, "round32"),
            (ROUND_OF_16_FIXTURES, "round16"),
            (QUARTERFINAL_FIXTURES, "qf"),
            (SEMIFINAL_FIXTURES, "sf"),
        ]
        for fixtures, stage in knockout_stages:
            print(f"\n🏅 Inserindo {len(fixtures)} jogos — {stage}...")
            for f in fixtures:
                match_number, match_label, venue, scheduled_at = f
                if db.query(Match).filter(Match.match_number == match_number).first():
                    continue
                match = Match(
                    match_number=match_number,
                    stage=stage,
                    venue=venue,
                    scheduled_at=scheduled_at.replace(tzinfo=None),
                    match_label=match_label,
                    is_locked=True,
                    is_played=False,
                )
                db.add(match)

        # 4. Final + 3º lugar
        print(f"\n🏆 Inserindo {len(FINAL_FIXTURES)} jogos finais...")
        for f in FINAL_FIXTURES:
            match_number, match_label, venue, scheduled_at = f
            stage = "third" if "3º" in match_label else "final"
            if db.query(Match).filter(Match.match_number == match_number).first():
                continue
            match = Match(
                match_number=match_number,
                stage=stage,
                venue=venue,
                scheduled_at=scheduled_at.replace(tzinfo=None),
                match_label=match_label,
                is_locked=True,
                is_played=False,
            )
            db.add(match)

        # 5. Achievements
        print("\n🏅 Inserindo achievements...")
        for ach in ACHIEVEMENTS_DATA:
            if db.query(Achievement).filter(Achievement.slug == ach["slug"]).first():
                continue
            db.add(Achievement(**ach))
            print(f"  ✅ {ach['icon']} {ach['name']}")

        db.commit()
        total_matches = db.query(Match).count()
        total_teams = db.query(Team).count()
        total_ach = db.query(Achievement).count()
        print(f"\n✅ Seed concluído!")
        print(f"   Times: {total_teams} | Jogos: {total_matches} | Achievements: {total_ach}")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro no seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Apaga e recria tudo")
    args = parser.parse_args()
    run_seed(reset=args.reset)
