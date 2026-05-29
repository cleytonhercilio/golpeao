"""
GolPeão — seed_db.py
Popula o banco de dados com times e todos os 104 jogos da Copa 2026.

Uso:
    python scripts/seed_db.py
    python scripts/seed_db.py --reset   # limpa e recria tudo
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from datetime import timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importar modelos (ajustar path conforme implementação)
# from app.models import Base, Team, Match
# from app.config import settings
from data.fixtures import (
    TEAMS,
    GROUP_STAGE_FIXTURES,
    ROUND_OF_32_FIXTURES,
    ROUND_OF_16_FIXTURES,
    QUARTERFINAL_FIXTURES,
    SEMIFINAL_FIXTURES,
    FINAL_FIXTURES,
    print_summary,
)


def seed_teams(session, teams_data: list) -> dict:
    """Insere times e retorna dict {id_fixture: team_db_obj}"""
    print("\n📌 Inserindo times...")
    team_map = {}

    for team_tuple in teams_data:
        team_id, name_pt, name_en, iso_code, group, confederation = team_tuple

        # Verificar se já existe
        # existing = session.query(Team).filter_by(name=name_pt).first()
        # if existing:
        #     team_map[team_id] = existing
        #     continue

        flag_url = f"https://flagcdn.com/64x48/{iso_code}.png"

        # team = Team(
        #     name=name_pt,
        #     name_en=name_en,
        #     iso_code=iso_code,
        #     group_name=group,
        #     flag_url=flag_url,
        #     confederation=confederation,
        # )
        # session.add(team)
        # session.flush()
        # team_map[team_id] = team

        # Placeholder para quando models estiverem implementados:
        team_map[team_id] = {
            "id": team_id,
            "name": name_pt,
            "iso": iso_code,
            "flag_url": flag_url,
        }
        print(f"  ✅ {name_pt} ({iso_code}) — Grupo {group}")

    return team_map


def seed_group_stage(session, fixtures: list, team_map: dict):
    """Insere os 72 jogos da fase de grupos"""
    print(f"\n⚽ Inserindo {len(fixtures)} jogos da fase de grupos...")

    for fixture in fixtures:
        match_number, home_id, away_id, group, venue, scheduled_at = fixture

        home_team = team_map.get(home_id)
        away_team = team_map.get(away_id)

        if not home_team or not away_team:
            print(f"  ⚠️  Jogo #{match_number}: time não encontrado (home_id={home_id}, away_id={away_id})")
            continue

        # match = Match(
        #     match_number=match_number,
        #     home_team_id=home_team.id,
        #     away_team_id=away_team.id,
        #     stage="group",
        #     group_name=group,
        #     venue=venue,
        #     scheduled_at=scheduled_at,
        #     is_locked=False,
        #     is_played=False,
        # )
        # session.add(match)

        home_name = home_team['name'] if isinstance(home_team, dict) else home_team.name
        away_name = away_team['name'] if isinstance(away_team, dict) else away_team.name
        print(f"  ✅ Jogo #{match_number:3d} — {home_name} vs {away_name} | Grupo {group} | {venue}")


def seed_knockout_stage(session, fixtures: list, stage: str, label: str):
    """Insere jogos do mata-mata (sem times definidos ainda)"""
    print(f"\n🏅 Inserindo {len(fixtures)} jogos — {label}...")

    for fixture in fixtures:
        match_number, match_label, venue, scheduled_at = fixture

        # match = Match(
        #     match_number=match_number,
        #     home_team_id=None,   # preenchido pelo bracket engine
        #     away_team_id=None,
        #     stage=stage,
        #     group_name=None,
        #     venue=venue,
        #     scheduled_at=scheduled_at,
        #     match_label=match_label,
        #     is_locked=True,       # bloqueado até times definidos
        #     is_played=False,
        # )
        # session.add(match)
        print(f"  ✅ Jogo #{match_number:3d} — {match_label}")


def seed_achievements(session):
    """Insere os achievements no banco"""
    from services.achievements import ACHIEVEMENTS  # ajustar import

    print("\n🏅 Inserindo achievements...")
    for ach in ACHIEVEMENTS:
        # existing = session.query(Achievement).filter_by(slug=ach['slug']).first()
        # if not existing:
        #     achievement = Achievement(
        #         slug=ach['slug'],
        #         name=ach['name'],
        #         description=ach['description'],
        #         icon=ach['icon'],
        #         points_bonus=ach['points_bonus'],
        #     )
        #     session.add(achievement)
        print(f"  ✅ {ach['icon']} {ach['name']}")


def run_seed(reset: bool = False):
    """Executa o seed completo"""
    print("🏆 GolPeão — Iniciando seed do banco de dados")
    print_summary()

    # DATABASE_URL = settings.DATABASE_URL
    # engine = create_engine(DATABASE_URL)
    # SessionLocal = sessionmaker(bind=engine)

    # if reset:
    #     print("\n⚠️  RESET: Deletando todos os dados existentes...")
    #     Base.metadata.drop_all(engine)
    #     Base.metadata.create_all(engine)
    # else:
    #     Base.metadata.create_all(engine)

    # session = SessionLocal()
    session = None  # placeholder

    try:
        # 1. Times
        team_map = seed_teams(session, TEAMS)

        # 2. Fase de grupos (72 jogos)
        seed_group_stage(session, GROUP_STAGE_FIXTURES, team_map)

        # 3. Mata-mata (32 jogos)
        seed_knockout_stage(session, ROUND_OF_32_FIXTURES, "round32", "Round of 32")
        seed_knockout_stage(session, ROUND_OF_16_FIXTURES, "round16", "Round of 16")
        seed_knockout_stage(session, QUARTERFINAL_FIXTURES, "qf", "Quartas de Final")
        seed_knockout_stage(session, SEMIFINAL_FIXTURES, "sf", "Semifinais")
        seed_knockout_stage(session, FINAL_FIXTURES + FINAL_FIXTURES[1:], "final", "Final + 3º Lugar")

        # 4. Achievements
        # seed_achievements(session)

        # session.commit()
        print("\n✅ Seed concluído com sucesso!")
        print(f"   Times inseridos: {len(TEAMS)}")
        total_matches = (
            len(GROUP_STAGE_FIXTURES) + len(ROUND_OF_32_FIXTURES) +
            len(ROUND_OF_16_FIXTURES) + len(QUARTERFINAL_FIXTURES) +
            len(SEMIFINAL_FIXTURES) + len(FINAL_FIXTURES)
        )
        print(f"   Jogos inseridos: {total_matches}")

    except Exception as e:
        # session.rollback()
        print(f"\n❌ Erro no seed: {e}")
        raise
    # finally:
    #     session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed do banco GolPeão")
    parser.add_argument("--reset", action="store_true",
                        help="Apaga dados existentes antes de inserir")
    args = parser.parse_args()
    run_seed(reset=args.reset)
