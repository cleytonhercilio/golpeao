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
    stage: Mapped[str] = mapped_column(String(20), nullable=False)
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
