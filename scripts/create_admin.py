"""
Cria um usuário admin.
Uso: python scripts/create_admin.py --username admin --password SenhaForte123
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.user import User
from app.config import settings


def create_admin(username: str, password: str, email: str):
    connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
    engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    try:
        if db.query(User).filter(User.username == username).first():
            print(f"⚠️  Usuário '{username}' já existe.")
            return
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        admin = User(
            username=username,
            email=email,
            password_hash=password_hash,
            display_name=username.capitalize(),
            is_admin=True,
        )
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
