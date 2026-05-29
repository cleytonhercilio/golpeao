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


def _generate_invite_code(db: Session) -> str:
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not db.query(BolaoGroup).filter(BolaoGroup.invite_code == code).first():
            return code


def _group_to_out(group: BolaoGroup, db: Session) -> GroupOut:
    count = db.query(GroupMember).filter(GroupMember.group_id == group.id).count()
    out = GroupOut.model_validate(group)
    out.member_count = count
    return out


@router.post("/", response_model=GroupOut, status_code=201)
def create_group(
    data: GroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    group = BolaoGroup(
        name=data.name,
        invite_code=_generate_invite_code(db),
        owner_id=current_user.id,
    )
    db.add(group)
    db.flush()
    db.add(GroupMember(group_id=group.id, user_id=current_user.id))
    db.commit()
    db.refresh(group)
    return _group_to_out(group, db)


@router.post("/join", response_model=GroupOut)
def join_group(
    invite_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    group = db.query(BolaoGroup).filter(BolaoGroup.invite_code == invite_code.upper()).first()
    if not group:
        raise HTTPException(404, "Código de convite inválido")
    if db.query(GroupMember).filter(
        GroupMember.group_id == group.id,
        GroupMember.user_id == current_user.id,
    ).first():
        raise HTTPException(400, "Você já é membro deste bolão")
    db.add(GroupMember(group_id=group.id, user_id=current_user.id))
    db.commit()
    db.refresh(group)
    return _group_to_out(group, db)


@router.get("/", response_model=List[GroupOut])
def my_groups(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    memberships = db.query(GroupMember).filter(GroupMember.user_id == current_user.id).all()
    result = []
    for m in memberships:
        g = db.query(BolaoGroup).filter(BolaoGroup.id == m.group_id).first()
        if g:
            result.append(_group_to_out(g, db))
    return result


@router.get("/{group_id}", response_model=GroupDetail)
def get_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    group = (
        db.query(BolaoGroup)
        .options(joinedload(BolaoGroup.members).joinedload(GroupMember.user))
        .filter(BolaoGroup.id == group_id)
        .first()
    )
    if not group:
        raise HTTPException(404, "Bolão não encontrado")
    out = GroupDetail.model_validate(group)
    out.member_count = len(group.members)
    out.members = [
        MemberOut(
            user_id=m.user.id,
            username=m.user.username,
            display_name=m.user.display_name,
            avatar_emoji=m.user.avatar_emoji,
            tier=m.user.tier,
            total_points=m.user.total_points,
            joined_at=m.joined_at,
        )
        for m in group.members
    ]
    return out
